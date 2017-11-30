<%inherit file="/base.mako"/>
<%namespace file="/message.mako" import="render_msg" />

<%def name="title()">Lifeportal Administration</%def>

<h2>Lifeportal Project Administration</h2>

<%
     form_action = h.url_for( controller='project_admin', action='manipulate_gold_projects')
%>


<% 
    import re
    import Accounting_project_management
    project_admin = "False"
    date_index = 1
    ## check if user is a project administrator or just project manager
    project_admin_users = trans.app.config.get( "project_admin_users", "" ).split( "," )
    if trans.user.email in project_admin_users :
        projects = Accounting_project_management.list_all_GOLD_projects()
        for p in projects :
            if p[3] == "True" :
               p[3] = "<font color=\"green\">True</font>"
            else :
               p[3] = "<font color=\"red\">False</font>"
        project_admin = "True"
    else :
        projects = Accounting_project_management.list_owned_GOLD_projects ( trans.user.email)
        for p in projects :
            if p[2] == "True" :
               p[2] = "<font color=\"green\">True</font>"
            else :
               p[2] = "<font color=\"red\">False</font>"
%>

    ${render_msg( message, status )}
    <form action="${form_action}" method="post">
        %if project_admin == 'True':
                      <div class="form-row">
                               <input type="submit" name="modify_project" value="Modify project"/>
                               <input type="submit" name="pre_project_usage" value="Display project usage"/>
                               <input type="submit" name="activate_project" value="Activate project"/>
                               <input type="submit" name="deactivate_project" value="Deactivate project"/>
                               <input type="submit" name="generate_report_page" value="Generate report page"/>
                      </div>
                      <table id="create_gold_project" class="grid">
                                <tr><h2 colspan=8 align="center">Full Lifeportal local projects list</h2></tr>
                                <tr><h6 colspan=8 align="center"><font color="red">Attention! The Amount of CPU hours below will only be displayed from <em>Start date</em>.</p>
                                     The value will be 0.00 before <em>Start</em> and after <em>End</em></h6></tr>
                                <tr><h2 colspan=8 align="center">&nbsp;</h2></tr>
                                <tr>
                                               <th>&nbsp;</th>
                                               <th>Project owner</th>
                                               <th>Project name</th>
                                               <th>Users</th>
                                               <th>Active</th>
                                               <th>Amount</th>
                                               <th>Description</th>
                                               <th>Start</th>
                                               <th>End</th>
                                   </tr>
                                   %for p in projects :
                                    <tr>
                                           <td><input type="radio" name="gold_projects" value="${p[1]}"></td>
                                           %for i in range(len(p)):
                                               %if i == len(p)-2:
                                                      <td><input type="date" name="start_date" value="${p[i]}" readonly></td>
                                               %elif i == len(p)-1:
                                                       <td><input type="date" name="end_date" value="${p[i]}" readonly></td>
                                               %else :
                                                       <td>${p[i]}</td>
                                               %endif
                                           %endfor
                                    </tr>
                                   %endfor
                      </table>
                      <div class="form-row">
                               <input type="submit" name="modify_project" value="Modify project"/>
                               <input type="submit" name="pre_project_usage" value="Display project usage"/>
                               <input type="submit" name="activate_project" value="Activate project"/>
                               <input type="submit" name="deactivate_project" value="Deactivate project"/>
                               <input type="submit" name="generate_report_page" value="Generate report page"/>
                      </div>
        %else :
                      <table id="create_gold_project" class="grid">
                              <tr><h2 colspan=7 align="center">Your Lifeportal projects list</h2></tr>
                              <tr><h2 colspan=7 align="center">&nbsp;</h2></tr>
                              <tr>
                                         <th>&nbsp;</th>
                                         <th>Project name</th>
                                         <th>Users</th>
                                         <th>Active</th>
                                         <th>Amount</th>
                                         <th>Description</th>
                                         <th>Start</th>
                                         <th>End</th>
                             </tr>
                             %for p in projects :
                                 <tr>
                                       <td><input type="radio" name="gold_projects" value="${p[0]}"></td>
                                        %for i in range(len(p)):
                                               %if i == len(p)-2:
                                                      <td name="start_date" value="${p[i]}">${p[i]}</td>
                                               %elif i == len(p)-1:
                                                       <td name="end_date" value="${p[i]}">${p[i]}</td>
                                               %else :
                                                       <td>${p[i]}</td>
                                               %endif
                                        %endfor
                                 </tr>
                             %endfor
                        </table>
                        <div class="form-row">
                                        <input type="submit" name="pre_project_usage" value="Display project usage"/>
                                        <input type="submit" name="generate_report_page" value="Generate report page"/>
                       </div>
        %endif
    </form>
