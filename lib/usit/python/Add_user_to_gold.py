#!/usr/bin/env python

import argparse
import ConfigParser
import json
import subprocess

import datetime
import re
import psutil
import urlparse
import os
import io
import sys
import time

from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Read (or create) config file
config = ConfigParser.ConfigParser()
if os.path.isfile('/etc/galaxy_email.cfg'):
    config.read('/etc/galaxy_email.cfg')
if config.has_option('crediting', 'default_hours'):
    HOURS = config.get('crediting', 'default_hours')
else:
    HOURS = '200'
if config.has_option('log', 'file'):
    LOGFILENAME = config.get('log', 'file')
else:
    LOGFILENAME = '200'

# Database connection
engine = create_engine(config.get('db_gold', 'uri'))
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

class Mas_projects(Base):
    __tablename__ = config.get('db_gold', 'mas_table_name')
    id = Column(Integer, primary_key=True)
    uname = Column(String(20), index=True, unique=True)
    status = Column(String(20))
    projects = Column(String(200))
    mas_email = Column(String(100))
    uio_email = Column(String(50))

    def __init__(self, uname, uio_email, status=None, projects=None, mas_email=None):
        self.uname = uname
        self.status = ""
        self.projects = ""
        self.mas_email = ""
        self.uio_email = uio_email

def popen_communicate(command):
    """

    :param command: gold command
    :type command: list
    :return: dictionary: {stdout, stderr, rc} (returncode)
    """
    with open(os.devnull, 'w') as devnull:
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        sdata = p.communicate()
    return {'stdout': sdata[0],
            'stderr': sdata[1],
            'rc': p.returncode}


def add_remote_user_to_gold(email, provider=None):
    """
    At registration all users are added to GOLD: User is inserted to
    GOLD user DB and to gx_default (Galaxy default) project in GOLD.
    This is a new function for the common code only!!

    @:param email email address
    @:param provider idp provider type (feide, social) retrieved from dataporten
    """
    message = u""
    username = email.lower()
    user_info = []

    if provider[0] == "feide":
        description = 'Default FEIDE-Galaxy user'
    else:
        description = ":".join(provider)

    useradd_command = ['sudo', '-u', 'gold', '/opt/gold/bin/gmkuser', username, '-d', description]
    useradd = popen_communicate(useradd_command)

    ## If the user is already created:
    if useradd['rc'] == 74:
        return

    ## If goldd is not running:
    if useradd['rc'] == 22:
        log_message("Gold is not running. {} not added.".format(email))

    ## If the user is sucessfully created
    if useradd['rc'] == 0:
            ## Add user to default galaxy project gx_default, create account and credit the account with default CPU hours
            add_to_gx_default_command = ['sudo', '-u', 'gold', '/opt/gold/bin/gchproject', '--addUsers', username, 'gx_default']
            tmp = popen_communicate(add_to_gx_default_command)
            if tmp['rc'] != 0:
                log_message(tmp['stderr'])
                raise Exception()

            ## Add user to account 'username_gx_default' in project gx_default
            create_account_command = ['sudo', '-u', 'gold', '/opt/gold/bin/gmkaccount', '-p', 'gx_default', '-u', username, '-n', "{}_gx_default".format(username)]
            tmp = popen_communicate(create_account_command)
            if tmp['rc'] != 0:
                log_message(tmp['stderr'])
                raise Exception()

            ## Credit the account - CPU hours from config

            ## Get the account id
            get_account_id_command = ['sudo', '-u', 'gold', '/opt/gold/bin/glsaccount', "--show", "Id", "-n", "{}_gx_default".format(username)]
            tmp = popen_communicate(get_account_id_command)
            if tmp['rc'] != 0:
                log_message(tmp['stderr'])
                raise Exception()

            #for line in tmp['stdout'].readlines():
            account_info = tmp['stdout'].splitlines()[-1].split()
            account_id = account_info[0]
            # TODO remove

            ## Credit the account (in hours)
            credit_account_command = ['sudo', '-u', 'gold', "/opt/gold/bin/gdeposit", "-h", "-a", account_id, "-z", HOURS]
            tmp = popen_communicate(credit_account_command)
            if tmp['rc'] != 0:
                log_message(tmp['stderr'])
                raise Exception()
            log_message("Added {} to gx_default and credited {} hours to account id {}".format(username, HOURS, account_id))


def add_remote_user_to_mas(email, idp_provider_type, request):
    """
    Inserts the users into the gold_db which contains their MAS projects.
    If users are not feide but social, their mas data will be populated directly by the cron script
    # (for uio users the uio_email will be updated at first login)

    :param email: email address from dataporten,
    :param idp_provider_type: tuple with idp provider type (first element: string with feide or social)
    :param request:
    """
    
    ## If logging in from Dataporten for the first time, 'userids' is missing in the request
    request_dict = json.loads(urlparse.parse_qs(request)['acresponse'][0])
    if 'userids' not in request_dict:
        return "none"
    
    if len(idp_provider_type) > 1 and idp_provider_type[0] == "feide" and idp_provider_type[1] == "uio.no":

        uname = uname_from_request(request)
        user = Mas_projects.query.filter_by(uname=uname).first()

        if user:
            if user.uio_email != email and user.mas_email[-12:] == "ulrik.uio.no":
                user.uio_email = email
                db_session.add(user)
                db_session.commit()

        # insert a new user with the two values below
        # status, projects and mas_email come via cron script in the night
        else:
            user = Mas_projects(uname, email)
            db_session.add(user)
            db_session.commit()
            
        log_message("Added {} to mas tables".format(uname))


def log_message(message):
    """
    Log timestamp and message to logfile.

    :param message: Message to be logged.
    """
    # If different location is needed, different SELinux context must be set.
    location = "/home/galaxy/galaxy/"
    with io.open("{}/{}".format(location, LOGFILENAME), 'a') as logfile:
        message = u"" + datetime.datetime.now().isoformat() + ' ' + message + '\n'
        logfile.write(message)


def uname_from_request(request):
    """
    :param request: From httpd server on the form email;dpid;http-request
    :type request: String
    :return: uname
    """
    if not request :
        return "none"

    try:
        uname =  json.loads(urlparse.parse_qs(request)['acresponse'][0])['userids'][0].split(":")[1].split("@")[0]
    except (ValueError, TypeError, AttributeError) as e:
        log_message(e)
        log_message(request)
        uname = "unknown",

    return uname


def idp_provider_type_from_request(request):
    """
    Extracts IDP provider and type from request

    :param request: From httpd: on the form email;dpid;http-request
    :type request: String
    :return: tuple with idp provider type (first element: string with feide or social)
    """
    if not request:
        return "none"
    else:
        
        try:
            request_dict = json.loads(urlparse.parse_qs(request)['acresponse'][0])
            
            #This check is needed if logging for the first time from Dataporten
            if 'def' in request_dict:
                idp_provider_type_id = request_dict['def'][0][0]
                idp_provider_type_sub_id = request_dict['def'][0][1] if len(request_dict['def'][0]) == 2 else request_dict['def'][0][2] 
                idp_provider_type = [idp_provider_type_id, idp_provider_type_sub_id]
            else :
                if 'id' in request_dict and 'subid' in request_dict and request_dict['id'].startswith("https://idp.feide"):
                    idp_provider_type = ['feide', request_dict['subid']]
                elif 'type' in request_dict:
                    idp_provider_type = [request_dict['type']]
                    
            print "IDP PROVIDER TYPE ", idp_provider_type
            
        except (ValueError, TypeError, AttributeError) as e:
            log_message(e)
            log_message(request)
            idp_provider_type = "unknown",
            
    return idp_provider_type
