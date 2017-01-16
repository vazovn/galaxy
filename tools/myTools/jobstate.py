#!/usr/bin/env python

import sys
import os
import subprocess
import ntpath
from sqlalchemy import *

postgresdb=os.environ['GALAXYDB']                         
datadir=os.environ['DATADIR']                                                                                              

jobsdir=datadir+'/job_working_directory'
datasetdir=datadir+'/files'



def RegisteredDatasets(jobid):
   return ExQuery("select history_dataset_association.dataset_id, history_dataset_association.name from history_dataset_association,job_to_output_dataset where job_to_output_dataset.dataset_id=history_dataset_association.id and job_to_output_dataset.job_id='%s'"%jobid)
   

def ExQuery(query):
   return connection.execute(query)


def walktree(top = ".", depthfirst = False):
    """Walk the directory tree, starting from top. Credit to Noah Spurrier and Doug Fort."""
    import os, stat, types
    names = os.listdir(top)
    if not depthfirst:
        yield top, names
    for name in names:
        try:
            st = os.lstat(os.path.join(top, name))
        except os.error:
            continue
        if stat.S_ISDIR(st.st_mode):
            for (newtop, children) in walktree (os.path.join(top, name), depthfirst):
                yield newtop, children
    if depthfirst:
        yield top, names

def makeHTMLtable(top, depthfirst=False):
    from xml.sax.saxutils import escape # To quote out things like &amp;
    import os
    import re
    import ntpath

    ret = ['<table class="fileList">\n']
    ## add registered output datasets
    datasets = RegisteredDatasets('%s'%ntpath.basename(top))
    ret.append('   <b>Registered output</b>\n')
    for row in datasets:
       namedat = 'dataset_'+str(row[0])+'.dat'
       chunkd = str(int(row[0]/1000)).zfill(3)
       pathdat=datasetdir+'/'+chunkd+'/'+namedat
       llcmd = 'cd %s;ln -s %s %s.txt'%(exfiles,pathdat,namedat)
       p = subprocess.Popen(args=llcmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
       ret.append('   <tr><td class="file"><a href="%s.txt">%s</a></td></tr>\n'%(escape(namedat),escape(row[1])))

    for top, names in walktree(top):
        ## remove the jobdir string from top
        shtop = top.replace(jobsdir+"/"+str(int(jobid/1000)).zfill(3) +"/","")
        ret.append('   <tr><td class="directory"><b>Directory: %s</b></td></tr>\n'%escape(shtop))
        for name in names:
            if not os.path.isdir('%s/%s'%(top,name)):
               if not (re.search('galaxy',name) or re.search('metadata',name) or re.search('~',name)):
                  lcmd='cd %s;ln -s %s/%s %s.txt'%(exfiles,top,name,name)
                  p = subprocess.Popen(args=lcmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) 
                  ret.append('   <tr><td class="file"><a href="%s.txt">%s</a></td></tr>\n'%(escape(name),escape(name)))
    ret.append('</table>')
    return ''.join(ret) # Much faster than += method




def makeHTMLpage(top, depthfirst=False):
    return '\n'.join(['<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"',
                      '"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">',
                      '<html>'
                      '<head>',
                      '   <title></title>',
                      '   <style type="text/css">',
                      '      table.fileList { text-align: left; }',
                      '      td.directory { font-weight: bold; font-size: 20px;}',
                      '      td.file { padding-left: 4em; }',
                      '   </style>',
                      '</head>',
                      '<body>',
                      '<h1>Job files</h1>',
                      makeHTMLtable(top, depthfirst),
                      '</body>',
                      '</html>'])

def DieinHTML(message):
   return '\n'.join(['<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"',
                      '"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">',
                      '<html>'
                      '<head>',
                      '   <title></title>',
                      '   <style type="text/css">',
                      '      table.fileList { text-align: left; }',
                      '      td.directory { font-weight: bold; }',
                      '      td.file { padding-left: 4em; }',
                      '   </style>',
                      '</head>',
                      '<body>',
                      '<h3>Error</h3>',
                       message,
                      '</body>',
                      '</html>'])
                  

def OwnsJob(cjogid, jobid):

   cuser = ExQuery("select user_id from job where id='%s'"%cjobid)
   user = ExQuery("select user_id from job where id='%s'"%jobid) 
   for row in cuser:
      cuserid=row[0]
   for row in user:
      userid=row[0]
   if cuserid==userid:
      return True
   else:
      return False


if __name__ == '__main__':

    application_db_engine = create_engine('%s'%postgresdb, encoding='utf-8')
    connection = application_db_engine.connect()


    if len(sys.argv) == 3:
        jobid=int(sys.argv[1])
        exfiles=sys.argv[2]
        dircmd='mkdir -p %s'%exfiles
        p = subprocess.Popen(args=dircmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        chunkdir = str(int(jobid/1000)).zfill(3)
        top = '%s/%s/%s'%(jobsdir,chunkdir,jobid)
        if os.path.exists(top):
           cjobid=ntpath.basename(os.getcwd())
           if OwnsJob(cjobid, jobid):
               print makeHTMLpage(top)
           else:
              print DieinHTML("The requested job doesn't belong to you.")
        else: 
           print DieinHTML("Job id was not found.")
    else:
      print DieinHTML("Error executing the tool.")
