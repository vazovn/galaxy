
from galaxy.web.base.controller import *
from datetime import datetime, timedelta
from sqlalchemy import and_, false, func, or_
from galaxy.util import inflector
from galaxy.web.form_builder import CheckboxField
from string import punctuation as PUNCTUATION


from galaxy import model
from galaxy import util
from galaxy import web


## Nikolay's
import Accounting_project_management
import re
from galaxy import config


class ProjectApplication ( BaseUIController ):

    @web.expose
    def index( self, trans, **kwd ):
     
        print "KWD ", kwd
     
        message = kwd.get( 'message', ''  )
        status = kwd.get( 'status', 'done' )
        return trans.fill_template( '/webapps/galaxy/project_applications/index_project_application.mako',
                                        message=message,
                                        status=status )

 
    @web.expose
    def center_project_application ( self, trans, **kwd ):
        message = kwd.get( 'message', ''  )
        status = kwd.get( 'status', 'done' )
        return trans.fill_template( '/webapps/galaxy/project_applications/center_project_application.mako',
                                        message="Please fill in the required information",
                                        status=status )


    @web.expose
    def send_application_form ( self, trans, **kwd ):

        print "KWD ", kwd
        
        kwd['last_modified_by'] = trans.user.email

        (message ,status) = Accounting_project_management.register_project_application(kwd)
        if status == 'done' :
              return trans.fill_template( '/webapps/galaxy/project_applications/stored_project_application.mako',
                                        message=message,
                                        status=status)
        else :
              return trans.fill_template( '/webapps/galaxy/project_applications/center_project_application.mako',
                                        message=message,
                                        status=status)


