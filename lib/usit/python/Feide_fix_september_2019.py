#!/usr/bin/env python

import argparse
import ConfigParser
import json

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
if config.has_option('log', 'file'):
    LOGFILENAME = config.get('log', 'file')
else:
    LOGFILENAME = '200'

# Database connection
engine = create_engine(config.get('db_gold', 'uri'))
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

class Feide_fix(Base):
    __tablename__ = config.get('db_gold', 'feide_fix_table')
    id = Column(Integer, primary_key=True)
    eppn = Column(String(30), index=True, unique=True)
    email = Column(String(50))

    def __init__(self, eppn, email):
        self.eppn = uname
        self.email = email

def get_user_email_and_uname(eppn):
    user = Feide_fix.query.filter_by(eppn=eppn).first()
    return user
