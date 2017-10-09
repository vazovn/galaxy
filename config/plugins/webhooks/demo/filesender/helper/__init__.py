import logging
import os
import errno
import Dumper

from galaxy.util import Params


log = logging.getLogger(__name__)

def main(trans, webhook, params):
    if trans.user:
        email = trans.user.email
        user_upload_dir = trans.app.config.ftp_upload_dir
        check_user_upload_dir(user_upload_dir, email)
        userStatus = 'Filesender helper : user is logged in!'
    else:
        userStatus = 'Filesender helper error : No user is logged in.'
    print userStatus

def check_user_upload_dir(path,email):
    
    ## Create an individual path for every user. This path must be a symlink
    ## and it will only be used for filesender uploads. For all other ftp uploads 
    ## a directory named after the username must be created manually. This directory
    ## will/can be used for uploads from the user's home directory on the cluster.
    
    destination = path+"/"+email
    source = os.environ['FILESENDER_STORAGE'] + "/files"
    
    try:
        os.symlink(source,destination)
    except OSError:
        if not os.path.islink(destination):
            raise
    
