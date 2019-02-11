#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import time
import logging
import os
from datetime import datetime, timedelta
from string import punctuation as PUNCTUATION

from sqlalchemy import and_, false, func, or_

import galaxy.queue_worker
from galaxy import util, web
from galaxy.util import inflector
from galaxy.web.form_builder import CheckboxField
from tool_shed.util import shed_util_common as suc
from tool_shed.util.web_util import escape

log = logging.getLogger( __name__ )


## Nikolay's
import Accounting_project_management
import re
from galaxy import config
import datetime
import pytz
import subprocess
import os
import pdfkit

## Nikolay's attachment send as email
import smtplib
from galaxy.web.base.controller import BaseUIController


log = logging.getLogger( __name__ )

class ProjectAdmin( BaseUIController ):
    
    @web.expose
    @web.require_project_admin
    def index( self, trans, **kwd ):
        """
        Displays the main project_admin panel : left and center
        """
        message = kwd.get( 'message', ''  )
        status = kwd.get( 'status', 'done' )
        return trans.fill_template( '/webapps/galaxy/project_admin/index_project_admin.mako',
                                        message=message,
                                        status=status )

    @web.expose
    @web.require_project_admin
    def center_project_admin( self, trans, **kwd ):
        """
        Displays the center project_admin panel
        """
        message = kwd.get( 'message', ''  )
        status = kwd.get( 'status', 'done' )
        return trans.fill_template( '/webapps/galaxy/project_admin/center_project_admin.mako',
                                        message=message,
                                        status=status )
 

    ### USERS ###

    @web.expose
    @web.require_project_admin
    def users ( self, trans, email=None, **kwd ):
        """
        Function called from index_project_admin.mako. Populates the list of Galaxy users (after clicking on "Manage users" link)
        """
        message = ''
        status = 'done'
        emails = None
        if email is not None:
            user = trans.sa_session.query( trans.app.model.User ).filter_by( email=email ).first()
            if user:
                trans.handle_user_logout()
                trans.handle_user_login(user)
                message = 'You are now logged in as %s, <a target="_top" href="%s">return to the home page</a>' % ( email, url_for( controller='root' ) )
                emails = []
            else:
                message = 'Invalid user selected'
                status = 'error'
        if emails is None:
            emails = [ u.email for u in trans.sa_session.query( trans.app.model.User ).enable_eagerloads( False ).all() ]
        return trans.fill_template( 'webapps/galaxy/project_admin/manage_users.mako', emails=emails, message=message, status=status )


    @web.expose
    @web.require_project_admin
    def create_new_user( self, trans, **kwd ):
        """
        Creates a GOLD user and sends an email to the user to register in Galaxy
        """
        return trans.response.send_redirect( web.url_for( controller='user',
                                                          action='create_non_feide_user_in_GOLD',
                                                          cntrller='project_admin' ) )

    @web.expose
    @web.require_project_admin
    def associate_to_project ( self, trans, **kwd ) :

        message = ''
        status = ''
        
        ## check if users and project are selected

        if not 'gold_user' in kwd.keys() or kwd['gold_user'] == None:
            message = "Please, select a user!"
            status = 'error'
        elif not 'gold_project' in kwd.keys() or kwd['gold_project'] == '0':
            message = "Please, select a project!"
            status = 'error'
            
        if status == 'error' :
            return trans.fill_template( '/webapps/galaxy/project_admin/center_project_admin.mako',
                                        message=message,
                                        status=status )

        ## All data are available - associate has a "go"!
        else :

            project = kwd['gold_project']
            emails = kwd['gold_user']

            ## associate the users to projects
            (message,status) = Accounting_project_management.associate_users_to_projects ( emails, project )
            print ">>>> Associate users :  %s to project %s " % (emails,project)
            return trans.fill_template( '/webapps/galaxy/project_admin/center_project_admin.mako',
                                        message=message,
                                        status=status )

    ### PROJECTS ###

    @web.expose
    @web.require_project_admin
    def manipulate_gold_projects ( self, trans, **kwd ):

        print "KWD manipulate_gold_projects >>> ", kwd
        
        project_name = ''
        cpu_hours = ''
        description = ''
        project_info = []
        start_date = ''
        end_date = ''
        project_admin = "False"

        ## check if user is a project administrator or just project manager
        project_admin_users = trans.app.config.get( "project_admin_users", "" ).split( "," )
        if trans.user.email in project_admin_users :
             project_admin = True

        if project_admin == True:
             ## Default message
             message= 'Lifeportal projects list sorted by project name'
        else :
             ## Default message
             message= 'You own the following projects in the Lifeportal'

        ## Default status
        status='done'
 

        if 'save_new_project' in kwd:
                    if 'project_owner_email' in kwd :
                            email = kwd['project_owner_email'] 
                            error_message = ''
                            if len( email ) == 0 or "@" not in email or "." not in email:
                                     error_message = "Enter a real email address"
                            elif len( email ) > 255:
                                     error_message = "Email address exceeds maximum allowable length"
                            if len(error_message) > 0:
                                     return trans.fill_template( '/webapps/galaxy/project_admin/create_new_gold_project.mako',
                                        message = error_message,
                                        status= 'error' )
                    if 'project_name' in kwd :
                              if kwd['project_name'] != '' and re.match(r'^[A-Za-z0-9_]*$', kwd['project_name']) :
                                  project_name = util.sanitize_text( kwd['project_name'] )
                              else :
                                  return trans.fill_template( '/webapps/galaxy/project_admin/create_new_gold_project.mako',
                                        message = 'Missing or unauthorised project name (please check the project name format)',
                                        status= 'error' )
                    if 'cpu_amount' in kwd :
                              if kwd['cpu_amount'] != '' and re.match(r'^[0-9]*$', kwd['cpu_amount']) :
                                  cpu_amount = util.sanitize_text( kwd['cpu_amount'] )
                              else :
                                  return trans.fill_template( '/webapps/galaxy/project_admin/create_new_gold_project.mako',
                                        message = 'Missing or unauthorised amount (please check the amount format)',
                                        status= 'error' )
                    if 'gold_project_description' in kwd :
                              if kwd['gold_project_description'] != '' :
                                  gold_project_description = util.sanitize_text( kwd['gold_project_description'] )
                    if 'start_date' in kwd :
                              if kwd['start_date'] != '' :
                                  start_date = util.sanitize_text( kwd['start_date'] )
                                  if not re.match(r'^\d\d\d\d-\d\d-\d\d$',start_date) :
                                        return trans.fill_template( '/webapps/galaxy/project_admin/create_new_gold_project.mako',
                                              message = 'Wrong start date format',
                                              status= 'error' )
                              else :
                                  return trans.fill_template( '/webapps/galaxy/project_admin/create_new_gold_project.mako',
                                        message = 'Missing start date',
                                        status= 'error' )
                    if 'end_date' in kwd :
                              if kwd['end_date'] != '' :
                                  end_date = util.sanitize_text( kwd['end_date'] )
                                  if not re.match(r'^\d\d\d\d-\d\d-\d\d$',end_date) :
                                        return trans.fill_template( '/webapps/galaxy/project_admin/create_new_gold_project.mako',
                                              message = 'Wrong end date format',
                                              status= 'error' )
                              else :
                                  return trans.fill_template( '/webapps/galaxy/project_admin/create_new_gold_project.mako',
                                        message = 'Missing end date',
                                        status= 'error' )

                    ## Finally add the project to GOLD !!
                    message = Accounting_project_management.add_project_to_GOLD( email, project_name, cpu_amount, gold_project_description, start_date, end_date)

        elif 'save_modified_project' in kwd :

                    project_name = kwd['project_name']
                    cp_amount = ''
                    old_start_date = kwd['old_start_date'] 
                    old_end_date = kwd['old_end_date'] 
                    old_cpu_amount = kwd['old_cpu_amount']
                    start_date = ''
                    end_date = ''
                    
                    if 'cpu_amount' in kwd :
                              if kwd['cpu_amount'] != '' and re.match(r'^-*[0-9]*$', kwd['cpu_amount']) :
                                  cpu_amount = util.sanitize_text( kwd['cpu_amount'] )
                              else :
                                  return trans.fill_template( '/webapps/galaxy/project_admin/modify_gold_project.mako',
                                        project_name = project_name,
                                        message = 'Missing or unauthorised amount (please check the amount format)',
                                        status= 'error' )
                                        
                    if 'start_date' in kwd :
                              if kwd['start_date'] != '' :
                                  start_date = util.sanitize_text( kwd['start_date'] )
                                  if not re.match(r'^\d\d\d\d-\d\d-\d\d$',start_date) :
                                        return trans.fill_template( '/webapps/galaxy/project_admin/modify_gold_project.mako',
                                              project_name = project_name,
                                              message = 'Wrong start date format',
                                              status= 'error' )
                              else :
                                  return trans.fill_template( '/webapps/galaxy/project_admin/modify_gold_project.mako',
                                        project_name = project_name,
                                        message = 'Missing start date',
                                        status= 'error' )
                    
                    if 'end_date' in kwd :
                              if kwd['end_date'] != '' :
                                  end_date = util.sanitize_text( kwd['end_date'] )
                                  if not re.match(r'^\d\d\d\d-\d\d-\d\d$',end_date) :
                                        return trans.fill_template( '/webapps/galaxy/project_admin/modify_gold_project.mako',
                                              project_name = project_name,
                                              message = 'Wrong end date format',
                                              status= 'error' )
                                  elif end_date <= start_date :
                                        return trans.fill_template( '/webapps/galaxy/project_admin/modify_gold_project.mako',
                                              project_name = project_name,
                                              message = 'End date was set before or equal to Start date!!',
                                              status= 'error' )
                              else :
                                  return trans.fill_template( '/webapps/galaxy/project_admin/modify_gold_project.mako',
                                        project_name = project_name,
                                        message = 'Missing end date',
                                        status= 'error' )
                    
                    ## Modify the project
                    if old_cpu_amount != cp_amount  or old_start_date != start_date or old_end_date != end_date  :
                               (message,status) = Accounting_project_management.modify_project( project_name, cpu_amount, start_date, end_date)
   

        elif 'cancel' in kwd:
                    return trans.fill_template( '/webapps/galaxy/project_admin/manipulate_gold_projects.mako',
                                        message = message,
                                        status =  status)

        elif 'modify_project' in kwd:
                    if 'gold_projects' in kwd :
                              project_name = kwd['gold_projects']
                              return trans.fill_template( '/webapps/galaxy/project_admin/modify_gold_project.mako',
                                        project_name = project_name,
                                        message = "Modify existing project",
                                        status =  status)

        elif 'create_project' in kwd:
                    project_name = Accounting_project_management._generate_project_name()
                    return trans.fill_template( '/webapps/galaxy/project_admin/create_new_gold_project.mako',
                                        project_name = project_name,
                                        message = "Lifeportal local project creation page",
                                        status = status)

        elif 'deactivate_project' in kwd :
                    if 'gold_projects' in kwd :
                              project_name = kwd['gold_projects']
                              (message,status) = Accounting_project_management.deactivate_project(project_name)
                              
                              return trans.fill_template( '/webapps/galaxy/project_admin/manipulate_gold_projects.mako',
                                        project_name = project_name,
                                        project_info = project_info,
                                        message = message,
                                        status= status)
                              

        elif 'activate_project' in kwd :
                    if 'gold_projects' in kwd :
                              project_name = kwd['gold_projects']
                    
                              ## Get project information
                              (message,status) = Accounting_project_management.activate_project( project_name )
                                                  
                              return trans.fill_template( '/webapps/galaxy/project_admin/manipulate_gold_projects.mako',
                                        project_name = project_name,
                                        project_info = project_info,
                                        message = message,
                                        status= status)
                              
                         
        elif 'pre_project_usage' in kwd:
                   if 'gold_projects' in kwd :
                              project_name = kwd['gold_projects']
                              ## set dates for the report
                              projects = Accounting_project_management.list_all_GOLD_projects ( filter_by_project_name = project_name)
                              project_name = projects[0][1]
                              start_date = projects[0][6]
                              end_date = projects[0][7]
                              return trans.fill_template( '/webapps/galaxy/project_admin/confirm_display_gold_project_usage.mako',
                                        project_name = project_name,
                                        start_date = start_date,
                                        end_date = end_date,
                                        message = "Set the dates for the report - the dates below display the entire project period",
                                        status= status)
                                        
        elif 'generate_report_page' in kwd:
                   if 'gold_projects' in kwd :
                              project_name = kwd['gold_projects']
                              
                              ## get date / hour of the report
                              date = datetime.datetime.now(pytz.timezone('Europe/Oslo'))
     
                              project_data = Accounting_project_management.collect_project_info_for_report ( project_name )

                              ## get extension right : add 6 months
                              expire_date = project_data[8]
                              extended_until = (expire_date + datetime.timedelta(6*365/12)).isoformat()
                              print "EXTENDED UNTIL", extended_until


                              return trans.fill_template( '/webapps/galaxy/project_admin/generate_project_report.mako',
                                        project_data = project_data,
                                        extension_date = extended_until,
                                        message = "Report information collected on "+str(date),
                                        status= status)                                                            
                                        
        elif 'generate_pdf' in kwd:
                   
                   pdf_reports_directory = os.environ['PDF_REPORTS_DIRECTORY']
                   
                   if 'project_code' in kwd :
                              project_name = kwd['project_code']
                              generate_pdf = True

                              ## get date / hour of the report
                              date = datetime.datetime.now(pytz.timezone('Europe/Oslo'))
                              printable_date = date
                              date = str(date).split(".")[0].replace(" ","_").replace(":","_")

                              ## organize project data
                              project_data = {}
                              
                              project_data['author'] = trans.user.email
                              project_data['date'] = printable_date
                              
                              project_data['name'] = kwd['name']
                              project_data['job_title'] = kwd['job_title']
                              project_data['email'] = kwd['email']
                              project_data['institution'] = kwd['institution']
                              project_data['country'] = kwd['country']
                              
                              project_data['project_name'] = kwd['project_name']
                              project_data['project_code'] = kwd['project_code']
                              
                              project_data['cpu_hours_required'] = kwd['cpu_hours_required']
                              project_data['cpu_hours_used'] = kwd['cpu_hours_used']
                              project_data['cpu_hours_remaining'] = kwd['cpu_hours_remaining']
                              
                              project_data['start_date'] = kwd['start_date']
                              project_data['end_date'] = kwd['end_date']
                              
                              if 'extension_date' in kwd and kwd['extension_date'] :
                                    project_data['extension_date'] = kwd['extension_date']
                              else :
                                    project_data['extension_date'] = "NA"
                              
                              if 'additional_cpu_hours' in kwd and kwd['additional_cpu_hours'] :
                                    project_data['additional_cpu_hours'] = kwd['additional_cpu_hours']
                              else :
                                    project_data['additional_cpu_hours'] = 'NA'
                                    
                              project_data['project_report'] = kwd['project_report']
                              
                              project_data['title'] = kwd['title'] if kwd['title'] != '' else "&nbsp;"
                              project_data['journal'] = kwd['journal'] if kwd['journal'] != '' else "&nbsp;"
                              project_data['year'] = kwd['year'] if kwd['year'] != '' else "&nbsp;" 
                              project_data['DOI'] = kwd['DOI'] if kwd['DOI'] != '' else "&nbsp;"
                              
                              ## process additional rows for publications
                              if 'txtbox[]' in kwd :
                                        
                                        rows = []
                                      
                                        if isinstance(kwd['txtbox[]'], unicode) : 

                                            # n publications = 2 (the first one takes the default title, journal, year, DOI kwd names)
                                            title2 = kwd['txtbox[]'] 
                                            journal2 = kwd['txtbox1[]']
                                            year2 = kwd['txtbox2[]']
                                            DOI2 =  kwd['txtbox3[]'] 
                                            rows.append([title2, journal2, year2, DOI2])
                                        
                                        elif isinstance(kwd['txtbox[]'], list) : 
                                        
                                            # n publications > 2
                                            titles = kwd['txtbox[]']
                                            journals = kwd['txtbox1[]']
                                            years = kwd['txtbox2[]']
                                            DOI = kwd['txtbox3[]']

                                            for t, j, y, d in zip(titles,journals,years,DOI):  
                                                   rows.append([t,j,y,d]) 

                                        project_data['publications'] = rows
                              
                              #print "PROJECT DATA BEFORE PDF", project_data
                              
                              html_page = trans.fill_template( '/webapps/galaxy/project_admin/generate_PDF_project_report.mako',
                                        project_data = project_data,
                                        generate_pdf = generate_pdf,
                                        message = "Project report for %s " % project_data['project_code'],
                                        status = status) 
                                        
                              #print "HTML_PAGE RAW CONTENT ", html_page
                              
                              html_filename = project_name+"_"+date+".html"
                              pdf_filename = project_name+"_"+date+".pdf"
                              
                              ## create html file
                              f = open( pdf_reports_directory+html_filename, 'w' )
                              f.write(html_page)
                              f.close()
                              
                              ## convert html to pdf
                              options = {'quiet':''}
                              try:
                                  pdfkit.from_file(pdf_reports_directory+html_filename, pdf_reports_directory+pdf_filename, options=options)
                              except:
								  pass

                              ################  EMAIL send pdf as attachment ########################
                          
                              receiver = trans.user.email
                              email_command = "mail -s \"Lifeportal PDF generated report for %s\" -a %s %s < %sPDFmessage.txt" % (kwd['project_code'], pdf_reports_directory+pdf_filename, receiver, pdf_reports_directory)
                              p = subprocess.Popen(email_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                              p.wait()
                          
                              message = "Successfully sent PDF report email for %s on %s" % (kwd['project_code'], printable_date)
                              print "Successfully sent PDF report email for %s on %s" % (kwd['project_code'], printable_date)
                          
                              ## delete html file
                              os.unlink(pdf_reports_directory+html_filename)
                              
                              return trans.fill_template( '/webapps/galaxy/project_admin/pdf_report_sent.mako',
                                        message = message,
                                        status =  'done')
 

                          
        elif 'project_usage' in kwd:
                   if 'project_name' in kwd :
                              project_name = kwd['project_name']
                              start_date = kwd['start_date']
                              end_date = kwd['end_date']
                              ## Get usage
                              message = Accounting_project_management.get_GOLD_project_usage( project_name,start_date,end_date )                                           
                              return trans.fill_template( '/webapps/galaxy/project_admin/display_gold_project_usage.mako',
                                        message = message,
                                        status= status)
                                   
                                                                      
        return trans.fill_template( '/webapps/galaxy/project_admin/manipulate_gold_projects.mako',
                                        message = message,
                                        status =  status)


    @web.expose
    @web.require_project_admin
    def show_pending_projects ( self, trans, **kwd ):
              
               ## check if admin or manager
               project_admin_users = trans.app.config.get( "project_admin_users", "" ).split( "," )
               if trans.user.email in project_admin_users :
                      ## can see all pending projects
                      pending_projects = Accounting_project_management.check_pending_projects()
               else :
                      ## can see only their own applications
                      pending_projects = Accounting_project_management.check_pending_projects( email = trans.user.email )
               return trans.fill_template( '/webapps/galaxy/project_admin/show_pending_projects.mako',
                                        pending_projects = pending_projects,
                                        message = "List of pending projects for approval",
                                        status= 'done')
                                        
    @web.expose
    @web.require_project_admin
    def pre_approve_pending_project( self, trans, **kwd ):
            if 'project_id' in kwd :
                      project_id = kwd['project_id']
                      return trans.fill_template( '/webapps/galaxy/project_admin/approve_pending_project.mako',
                                        project_id = project_id,
                                        message = "Approve the pending project",
                                        status =  'done')
                                        
    @web.expose
    @web.require_project_admin
    def approve_pending_project( self, trans, **kwd ):
            
            print "KWD approve pending project >>> ", kwd
  
            start_date = ''
            end_date = ''
            kwd['last_modified_by'] = trans.user.email
            
            if 'reason_for_rejection' and 'reject_pending_project' in kwd :
                    reason = kwd['reason_for_rejection']
                    project_id = kwd['project_id']
                    project_name = kwd['project_name']
                    message = "Project " + project_name + " has been rejected for the following reason : "
                    message += reason

                    Accounting_project_management.approve_pending_project( kwd)
                    
                    return trans.fill_template( '/webapps/galaxy/project_admin/approve_pending_project.mako',
                                        project_id = project_id,
                                        message = message,
                                        status= 'error')
            
            
            elif 'project_id' in kwd :
                    project_id = kwd['project_id']

                    if 'cpu_hours' in kwd :
                              if kwd['cpu_hours'] != '' and re.match(r'^-*[0-9]*$', kwd['cpu_hours']) :
                                  cpu_amount = util.sanitize_text( kwd['cpu_hours'] )
                              else :
                                  return trans.fill_template( '/webapps/galaxy/project_admin/approve_pending_project.mako',
                                        project_id = project_id,
                                        message = 'Missing or unauthorised amount (please check the cpu amount format)',
                                        status= 'error' )
                                        
                    if 'start_date' in kwd :
                              if kwd['start_date'] != '' :
                                  start_date = util.sanitize_text( kwd['start_date'] )
                                  if not re.match(r'^\d\d\d\d-\d\d-\d\d$',start_date) :
                                        return trans.fill_template( '/webapps/galaxy/project_admin/approve_pending_project.mako',
                                              project_id = project_id,
                                              message = 'Wrong start date format',
                                              status= 'error' )
                              else :
                                  return trans.fill_template( '/webapps/galaxy/project_admin/approve_pending_project.mako',
                                        message = 'Missing start date',
                                        status= 'error' )
                    
                    if 'end_date' in kwd :
                              if kwd['end_date'] != '' :
                                  end_date = util.sanitize_text( kwd['end_date'] )
                                  if not re.match(r'^\d\d\d\d-\d\d-\d\d$',end_date) :
                                        return trans.fill_template( '/webapps/galaxy/project_admin/approve_pending_project.mako',
                                              project_id = project_id,
                                              message = 'Wrong end date format',
                                              status= 'error' )
                                  elif end_date <= start_date :
                                        return trans.fill_template( '/webapps/galaxy/project_admin/approve_pending_project.mako',
                                              project_id = project_id,
                                              message = 'End date was set before or equal to Start date!!',
                                              status= 'error' )
                              else :
                                  return trans.fill_template( '/webapps/galaxy/project_admin/approve_pending_project.mako',
                                        project_id = project_id,
                                        message = 'Missing end date',
                                        status= 'error' )

                    ##start the approval
                    message = Accounting_project_management.approve_pending_project( kwd)

                    ## display the list of active projects in GOLD
                    return trans.fill_template( '/webapps/galaxy/project_admin/project_approved.mako',
                                        message = message,
                                        status =  'done')
                                        

    @web.expose
    @web.require_project_admin
    def show_rejected_projects ( self, trans, **kwd ):
              
               ## check if admin or manager
               project_admin_users = trans.app.config.get( "project_admin_users", "" ).split( "," )
               if trans.user.email in project_admin_users :
                      ## can see all pending projects
                      rejected_projects = Accounting_project_management.check_rejected_projects()
               else :
                      ## can see only their own applications
                      rejected_projects = Accounting_project_management.check_rejected_projects( email = trans.user.email )
                      
               ## the status 'error' below to force the red banner on the galaxy page during display
               return trans.fill_template( '/webapps/galaxy/project_admin/show_rejected_projects.mako',
                                        rejected_projects = rejected_projects,
                                        message = "List of rejected projects for approval",
                                        status= 'error')
                                        

    @web.expose
    @web.require_project_admin
    def pre_approve_rejected_project( self, trans, **kwd ):
            if 'project_id' in kwd :
                      project_id = kwd['project_id']
                      return trans.fill_template( '/webapps/galaxy/project_admin/approve_rejected_project.mako',
                                        project_id = project_id,
                                        message = "Approve the rejected project",
                                        status =  'done')


## ---- Utility methods -------------------------------------------------------

def get_user( trans, user_id ):
    """Get a User from the database by id."""
    user = trans.sa_session.query( trans.model.User ).get( trans.security.decode_id( user_id ) )
    if not user:
        return trans.show_error_message( "User not found for id (%s)" % str( user_id ) )
    return user

