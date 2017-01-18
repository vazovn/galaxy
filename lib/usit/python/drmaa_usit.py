"""
Job control via the DRMAA API.
This file is a customized version for LAP of the usit common-code version. 
The customizations affect the MAS related issues : the check for INVALID PROJECTS in MAS is skipped
"""
import json
import logging
import os
import string
import subprocess
import sys
import time
import traceback

#from galaxy import eggs
from galaxy import model
from galaxy.jobs import JobDestination
from galaxy.jobs.handler import DEFAULT_JOB_PUT_FAILURE_MESSAGE
from galaxy.jobs.runners import AsynchronousJobState, AsynchronousJobRunner

## Nikolay USIT start
import Dumper
import re
import Accounting_project_management, Accounting_jobs

## Errors in the check parameters block
CPU_MEMORY_ERROR_MESSAGE = "error:The total memory per node (processes * memory per CPU) value can not exceed 900 GB!"
TOO_MANY_HUGEMEM_JOBS_ERROR_MESSAGE = "error:The limit of jobs running on a hugemem (a node with more than 64 GB of memory) is set to 5!"
WRONG_PROJECT_ERROR_MESSAGE = "error:You are not member of the selected project (%s)!"
LOW_BALANCE_ERROR = "error:The remaining CPU hours in your project (%s) are insufficient to execute the job! You requested %s hours."
DENIED_RESERVATION_ERROR = "error:You have too many reserved jobs and the remaining resources  (%s hrs)  are insufficient to run the job requiring %s hrs!"
RESERVATION_FAILED_ERROR = "error:Ressources are available, but the reservation failed! Please, contact the portal admins."


#eggs.require( "drmaa" )
#drmaa = None

def create_job_safe(jt,job_wrapper,job_destination,log,ds):
    try :
        result = create_job(jt,job_wrapper,job_destination,log)  
        if result.startswith("error:") : 
            fail_job_procedure(job_wrapper,ds,jt,result[6:])
            return None
        return result
    except :
        print "Exception in USIT code:"
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60              
        fail_job_procedure(job_wrapper,ds,jt,"Galaxy failed to execute the task on Abel because of an internal system error. Please inform the administrators.");
    return None

def fail_job_procedure(job_wrapper,ds,jt,message) :
    job_wrapper.fail( message )
    
    ## Removed since implemented in new drmaa version from python (JobTemplate is automatically deleted)
    ## .venv/lib64/python27/.../pulsar.managers.util.drmaa
    #ds.deleteJobTemplate( jt )

def create_job(jt,job_wrapper,job_destination,log):

    ## ==== Nikolay USIT DRMAA IMPORTANT BLOCK NATIVE SPECS OVERRIDE START  ====

    print '-'*120

    galaxy_job_id =  job_wrapper.get_id_tag()

    orig = job_destination.params.get('nativeSpecification', None)
    print 'Original Native Specifications: '+orig
    
    native_spec_dict = {}
    if job_wrapper.get_param_dict().has_key('__job_resource') :
        native_spec_dict = job_wrapper.get_param_dict()['__job_resource']
    print "Get Dynamic Native Specifications (overriding Original Native Specifications) : ", native_spec_dict
    
    o_split = orig.split(' ')
    o_split = [ x for x in o_split if x is not '']

    nodes_value = 1
    ntasks_per_node_value = 1
    time_value = ''
    mem_per_cpu_value = ''
    project_value =  'gx_default'

    # Set the Original Native Specifications
    for option in o_split :
        key=option.split('=')[0]
        value=option.split('=')[1]
        if key == '--account' or key == '-account' :
            account_value = value
        elif key == '--nodes' or key == '-nodes' :
            nodes_value = value
        elif key == '--ntasks-per-node' or key == '-ntasks-per-node' :
            ntasks_per_node_value = value
        elif  key == '--time' or key == '-time' :
            time_value = value
        elif key == '--mem-per-cpu' or key == '-mem-per-cpu' :
            mem_per_cpu_value = value
    
    # Update the Original Native Specifications by Dynamic Native Specifications
    for key, value in native_spec_dict.iteritems() :
        if key == 'project' :
            project_value = value
        if key.startswith("ntasks-per-node") :
            ntasks_per_node_value = value
        if key.startswith("nodes") :
            nodes_value = value
        if key.startswith("memory") :
            mem_per_cpu_value = int(value) * 1024
        if key.startswith("time") :
            time_value = '%s:00:00' % value

    ## Setting the parameters using the values
    
    # 'account' is always instantiated by the Original Native Specifications
    # it is manually set in the file job_conf.xml
    account = '--account=%s' % account_value
    
    time = ' --time=%s' % time_value
    nodes = ' --nodes=%s' % nodes_value
    ntasks_per_node = ' --ntasks-per-node=%s' % ntasks_per_node_value
    mem_per_cpu = ' --mem-per-cpu=%s' % mem_per_cpu_value


    ## Setting the partition parameter
    if int(mem_per_cpu_value)*int(nodes_value)*int(ntasks_per_node_value) > 61*1024:
        partition = ' --partition=hugemem'
    else :
        partition = ' --partition=normal'
    
    ## Setting the Job Name
    jt['jobName'] = '%s::%s' % (job_wrapper.user,project_value)

    ## Native specs ready!
    native_spec = account + time + nodes +  ntasks_per_node + mem_per_cpu + partition
    
    
    ## TOTAL MEMORY AND NTASKS CHECK
    
    if (int(mem_per_cpu_value) * int(ntasks_per_node_value)) > 900*1024:
        log.error( "(%s) The total memory per node (processes * memory per CPU) value can not exceed 900 GB " % galaxy_job_id )
        return CPU_MEMORY_ERROR_MESSAGE
        
    if (int(ntasks_per_node_value) > 5 and partition == ' --partition=hugemem'):
        log.error( "(%s) The limit of jobs running on a hugemem (a node with more than 64 GB of memory) is set to 5! " % galaxy_job_id )
        return TOO_MANY_HUGEMEM_JOBS_ERROR_MESSAGE

    ## GOLD RELATED CHECKS
    if "GOLDDB" in os.environ.keys() :
        result = verify_gold_access(job_wrapper,time_value,nodes_value,ntasks_per_node_value,project_value, log)
        if result.startswith("error:") :
            return result
    else :
        print "=== WARNING! GOLD package is not installed or $GOLDDB env variable is not instantiated in startup_settings.sh !! ==="

    return native_spec
    
def verify_gold_access(job_wrapper,time_value,nodes_value,ntasks_per_node_value,project_value, log):

    print "=== Running Gold Verification ==="
    
    galaxy_job_id =  job_wrapper.get_id_tag()
    
    print "The user requested to run using the project: "+project_value
    LP_user_projects = Accounting_project_management.get_member_of_GOLD_projects ( job_wrapper.user )
    if project_value not in (LP_user_projects)  :
        log.error( "(%s) You are not member of the selected project! " % project_value )
        return WRONG_PROJECT_ERROR_MESSAGE % project_value
            
    ## requested walltime per CPU
    timestring_raw = '00-'+time_value
    timestring_secs = Accounting_jobs._slurmtimesecs(timestring_raw)
    ## total walltime
    total_walltime = int(timestring_secs) * int(nodes_value) * int(ntasks_per_node_value)
    (result, available) = Accounting_jobs.job_check_project_balance( project_value, job_wrapper.user,  total_walltime)
    if result == 'low_balance':
        available = float(available)/3600
        log.error( "(%s) You have requested %s hours but the remaining CPU hours in your project are " % ( galaxy_job_id,  time_value) + "%.2f" % round(available,2))
        return LOW_BALANCE_ERROR % ( available, time_value )
    elif result == 'reservation_over_balance_limit':
        available = float(available)/3600
        log.error( "(%s) You are trying to reserve %s hours. The remaining CPU hours in your project are" % ( galaxy_job_id, time_value ) + "%.2f" % round( available, 2))
        return DENIED_RESERVATION_ERROR % ( available, time_value)
    elif result != 'ok' :
        log.error( "(%s) Job reservation failed! See the log messages above." % galaxy_job_id )
        return RESERVATION_FAILED_ERROR
        
    pe = int(nodes_value) * int(ntasks_per_node_value)
    message = Accounting_jobs.job_reserve( galaxy_job_id, project_value, job_wrapper.user, str(timestring_secs), pe)
    action = "go"
    if message is not None and re.search("Successfully reserved 0 credits",message) :
        print "Job reservation failed : ", message
        print "Job reservation failed - user %s has used up their CPU hour limit for project %s , reservation value = 0 " % (job_wrapper.user, project_value)
        action = "stop"
    elif message is not None and re.search("Successfully",message) :
        print "Job reservation successful : ", message
    elif message is not None :
        print "Job reservation failed : ", message
        print "Job reservation failed - user %s has used up their CPU hour limit for project %s " % (job_wrapper.user, project_value)
        action = "stop"
    else :
        print "Message from drmaa.py - Job reserve returned empty message for project %s : user : %s" % (project_value, job_wrapper.user)
        action ="stop"
                 
    if action == "stop" :
        log.error( "(%s) Job reservation failed! See the log messages above." % galaxy_job_id )
        return RESERVATION_FAILED_ERROR;

    return "ok"

def charge_job(ajs,log) :
    if "GOLDDB" in os.environ.keys() :
        external_job_id = ajs.job_id
        galaxy_job_id = ajs.job_wrapper.get_id_tag()
        print "============ CHARGE JOB HERE ============"
        #print "SLURM JOB ID ", external_job_id
        #print "GALAXY JOB ID ",  galaxy_job_id
        #print ""
        message = Accounting_jobs.job_charge(external_job_id ,galaxy_job_id)
        log.debug(message)
        print "========================================="
