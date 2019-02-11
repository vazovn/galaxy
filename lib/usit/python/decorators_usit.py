import inspect
from traceback import format_exc
from functools import wraps

import paste.httpexceptions

from galaxy.web.framework import url_for
from galaxy import util
from galaxy.exceptions import error_codes
from galaxy.exceptions import MessageException
from galaxy.util.json import safe_dumps as dumps

import logging
log = logging.getLogger( __name__ )

def error( message ):
    raise MessageException( message, type='error' )


# Galaxy - GOLD - Nikolay - USIT
def require_project_admin( func ):
    @wraps(func)
    def decorator( self, trans, *args, **kwargs ):
        if not trans.user_is_project_admin():
            msg = "You must be a project administrator to access this feature."
            user = trans.get_user()
            if not trans.app.config.project_admin_users_list:
                msg = "You must be logged in as a project administrator to access this feature, but no such administrators are set in the Galaxy configuration."
            elif not user:
                msg = "You must be logged in as a project administrator to access this feature."
            trans.response.status = 403
            if trans.response.get_content_type() == 'application/json':
                return msg
            else:
                return trans.show_error_message( msg )
        return func( self, trans, *args, **kwargs )
    return decorator

