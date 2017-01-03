#!/bin/env python

import os, sys, string
import re
from pprint import *
import subprocess


def get_project_managers () :
   """
   Gets all the project managers (PIs who manage projects), but not Administrators approving the applications
   """
   
   project_managers = []
   f=open('/home/galaxy/galaxy/lib/usit/external_dbs'+'/project_managers.txt', 'r')
   for line in f :
        line = line.rstrip()
        line = line.lstrip()
        project_managers.append(line)
        
   f.close()
   
   return project_managers


def search_project_manager ( email ) :
   """
   Checks if smb IS a manager
   """
   
   sed_search_command = "sed -n '/^%s$/p' /home/galaxy/galaxy/lib/usit/external_dbs/project_managers.txt" % email
   p = subprocess.Popen(sed_search_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
   p.wait()
   
   if p.stdout.readlines() :
        return email
        

def delete_project_manager (email ) :
   """
   Deletes a project manager (shall be executed if the manager has 0 projects to manage)
   """
   
   sed_delete_command = "sed -i '/^%s$/d' /home/galaxy/galaxy/lib/usit/external_dbs/project_managers.txt" % email
   p = subprocess.Popen(sed_delete_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
   p.wait()

   found_email = search_project_manager( email )
   if not found_email :
        return "Deleted"
   

def add_project_manager (email ) :
   """
   Adds a project manager (run during the project approval procedure, check if manager exists allready)
   """
   found_email = search_project_manager( email )
   if not found_email :
        add_command = "echo '%s' >> /home/galaxy/galaxy/lib/usit/external_dbs/project_managers.txt " % email
        p = subprocess.Popen(add_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()
        found_email2 = search_project_manager( email )
        if found_email2 :
              return "Project manager added"
        else :
              return "Error adding Project manager into project_managers.txt"
   else :
        return "Project manager already exists"

