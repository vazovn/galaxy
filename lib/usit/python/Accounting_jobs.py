#!/bin/env python

import os, sys, logging, threading, time, string, datetime
from sqlalchemy import *
import subprocess
import re
from pprint import *
import smtplib
from smtplib import SMTPException
import Project_managers, Accounting_project_management

## needed to sort complex data structures
from operator import itemgetter, attrgetter


## ==== ACTIVATE THE DB ENGINE variable GOLDDB defined in startup_settings.sh at deploy time  =====

if os.environ['GOLDDB'] :
    GOLDDB = os.environ['GOLDDB']
    print "Accounting jobs : GOLDDB INSTANTIATED!!"
else:
    print "GOLDDB not accessible or not set!"
    sys.exit()


application_db_engine = create_engine(GOLDDB, encoding='utf-8')
metadata = MetaData(application_db_engine)


def gold_engine_dispose():
    application_db_engine.dispose()

def _slurmtimesecs (elapsed_time) :
    """
    Converts time into seconds
    """
    
    multipliers4 = [86400,3600,60,1]
    multipliers3 = [3600,60,1]
    seconds = None
    d_h_m_s = re.findall('\d+', elapsed_time)
    if len(d_h_m_s) == 4 :
        seconds = sum([a*b for a,b in zip(multipliers4, map(int,d_h_m_s))])
    elif len(d_h_m_s) == 3 :
        seconds = sum([a*b for a,b in zip(multipliers3, map(int,d_h_m_s))])
    return seconds
               

def job_check_project_balance (project, username, requested_time) :
   """
   Check jobs balance prior to reservation / check multiple reservations
   """
   if re.search("gx_default", project ):
         balance_command = "sudo -u gold /opt/gold/bin/gbalance --show Available -p gx_default -u %s" % ( username )
   else :
         balance_command = "sudo -u gold /opt/gold/bin/gbalance --show Available -p %s " % (project)
         
   p = subprocess.Popen(balance_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
   p.wait()

   available = 0
   for line in p.stdout.readlines():
        if re.search("\d+",line) :
                available = int(line.strip())

   if available < int(requested_time) :
         return ("low_balance", available)
   else :

         ## block multiple reservations for the same amount of cpu hours (balance)
         (status_reservation, reservation) = job_reservations_check (int(requested_time), int(available), project, username)

         #print "Accounting.py TOTAL AVAILABLE CPU HOURS", available
         #print "Accounting.py REQUESTED CPU HOURS ", requested_time
         #print "Accounting.py STATUS RESERVATION ", status_reservation, " RESERVED : ", reservation

         if re.search("reservation_over_balance_limit",status_reservation) :
             return ("reservation_over_balance_limit", reservation)
         else :
             return ("ok", reservation )
         
def job_reservations_check (requested_time, available, project, username) :
   """
   Reserve time used to place a hold on the user account before a job starts to ensure that the
   credits will be there when it completes.
   e.g. greserve -J lp7 -p <project_name> -u <username> -m Abel-Galaxy -P 2 -t 3600
   """

   reserve_command = "sudo -u gold /opt/gold/bin/glsres --show Amount -p %s -u %s" % (project,username)
   p = subprocess.Popen(reserve_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
   p.wait()

   ## get the existing reservations amount
   reserved = 0
   for line in p.stdout.readlines():
          if re.search("^\d+$",line) :
                    reserved = int(line)
                    if isinstance( reserved, int) :
                          reserved += reserved
   
   print "Pending reservations ", reserved
   remaining = available - reserved
   print "Remaining hours ", remaining
   
   if requested_time > remaining:
       over_limit = requested_time-remaining
       return ("reservation_over_balance_limit", over_limit)
   else :
       return ("ok", requested_time)
       
 
         
def job_reserve(jobname,project, username, time, pe) :
   """
   Reserve time used to place a hold on the user account before a job starts to ensure that the
   credits will be there when it completes.
   e.g. greserve -J lp7 -p <project_name> -u <username> -m Abel-Galaxy -P 2 -t 3600
   """

   machine = "Abel-Galaxy"
   reserve_command = "sudo -u gold /opt/gold/bin/greserve -J %s -p %s -u %s -m %s -P %s -t %s" % (jobname,project,username,machine,pe,time)
   p = subprocess.Popen(reserve_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
   p.wait()

   for line in p.stdout.readlines():
          if re.search("Successfully ",line) :
                    return line
          else :
                    print line


def job_charge( slurm_job_id, galaxy_job_id ):
    """
    Called from ../runners/drmaa.py (finction 'finish_job'). It charges the project by the elapsed time
    """
   
    command = "sacct -j "+slurm_job_id+" -p -o jobid,jobname,alloccpus,elapsed,nodelist,account -X"
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p.wait()
    
    job_data ={}

    for line in p.stdout.readlines():
        print "SACCT LINE ", line
        job_info=line.split('|')
    
    ## Check if the project is Lifeportal project and only then charge! :: concatenates the username
    if re.search('::',job_info[1]) :
         if job_info[0] == slurm_job_id :
                job_data['slurm_job_id'] = job_info[0]
            
                ##Split username and lifeportal name if relevant
                (user,lifeportal_project_name) = job_info[1].split('::')
                job_data['user'] = user
                job_data['lifeportal_project'] = lifeportal_project_name

                job_data['processes'] = job_info[2]
            
                ## process slurm elapsed time
                slurm_time_secs = "source /home/galaxy/galaxy/lib/usit/scripts/slurm_utils.sh ; slurm_time_secs %s " % job_info[3]
                p = subprocess.Popen(slurm_time_secs, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                p.wait()
                for line in p.stdout.readlines():
                     print "LINE ",line
                     if re.match('^\d+$',line) :
                          job_data['charge_duration'] = line.strip()
            
            
                job_data['machine'] = job_info[4]
                job_data['galaxy_job_id'] = galaxy_job_id
                job_data['slurm_account'] = job_info[5]

                pprint(job_data)

                # charge the job
                machine = "Abel-Galaxy"
                job_charge_command = "sudo -u gold /opt/gold/bin/gcharge -J %s -p %s -u %s -m %s -P %s -t %s" % ( job_data['galaxy_job_id'],
                                                                                                                                                             job_data['lifeportal_project'],
                                                                                                                                                             job_data['user'],
                                                                                                                                                             machine,
                                                                                                                                                             job_data['processes'],
                                                                                                                                                             job_data['charge_duration'])
                p = subprocess.Popen(job_charge_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                p.wait()

                for line in p.stdout.readlines():
                     if re.search("does not exist", line) :
						 line = "The project you had selected was not a Lifeportal project. No charges apply!"
                     print line
                     return line
   
    else :
         return "Not a Lifeportal job, no charges registered!"


