#!/bin/env python

import os, sys, logging, threading, time, string
from sqlalchemy import *
import subprocess
import re
from pprint import *

application_db_engine = create_engine(os.environ['FILESENDERDB'], encoding='utf-8')
metadata = MetaData(application_db_engine)
connection = application_db_engine.connect()

def get_user_files( email ):
    """
    Retrieves the real file name for the Upload table
    """

    filenames = {}
    s = text("select \
                    f.uid as file_uid, f.name as file_name \
              from \
                    files as f, transfers as t \
              where \
                    LOWER(t.user_email) = :email \
                and \
                    t.id = f.transfer_id \
                and \
                    t.status = 'available'")
                    
    result = connection.execute(s,email=email)
    for row in result:
        filenames[row.file_uid] = row.file_name
        
    #print "Filesender.py : FILENAMES FILTERED", filenames
    return filenames
    
    
def get_real_file_name( hash_filesender_name ):
    """
    Retrieves the real file name for History display
    """
    real_name = []
    
    s = text("select name from  files  where  uid = :hash_filesender_name ")

    result = connection.execute(s,hash_filesender_name=hash_filesender_name)
    for row in result:
        real_name.append(row.name)
        
    #print "Filesender.py : REAL NAME", real_name
    return real_name
