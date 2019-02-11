<%inherit file="/base.mako"/>
<%namespace file="/message.mako" import="render_msg" />

<%def name="title()">Lifeportal Administration</%def>

<h2>Lifeportal Project Administration</h2>

<%
     form_action = h.url_for( controller='project_admin', action='pre_approve_rejected_project')
    ## check if user is a project administrator or just project manager
     readonly = 'True'
     project_admin_users = trans.app.config.get( "project_admin_users", "" ).split( "," )
     if trans.user.email in project_admin_users :
         readonly = 'False'
%>

    ${render_msg( message, status )}
    <form action="${form_action}" method="post">
                      <table id="approve_rejected_project" class="grid">
                                <tr><h2 colspan=13 align="center">Lifeportal rejected local projects</h2></tr>
                                <tr><h2 colspan=13 align="center">&nbsp;</h2></tr>
                                <tr>
                                               <th>&nbsp;</th>
                                               <th>Project requestor</th>
                                               <th>Requestor's email</th>
                                               <th>Requestor's Institution</th>
                                               <th>Requestor's country</th>
                                               <th>Project name</th>
                                               <th>Requested CPU hours</th>
                                               <th>Project description</th>
                                               <th>Selected applications</th>
                                               <th>Start date</th>
                                               <th>End date</th>
                                               <th>Application date</th>
                                               <th>Reason for rejection</th>
                                   </tr>
                                   %for  p in rejected_projects:
                                    <tr>
                                           %if readonly == 'False' :
                                                 <td><input type="radio" name="project_id" value="${p[0]}"></td>
                                           %else :
                                                 <td>&nbsp;</td>
                                           %endif
                                           %for  item in p[1:]:
                                                    <td readonly>${item}</td>
                                           %endfor
                                    </tr>
                                   %endfor
                      </table>
                      %if readonly == 'False' :
                         <div class="form-row">
                               <input type="submit" name="approve_pending_project" value="Approve rejected project"/>
                         </div>
                      %endif
    </form>
