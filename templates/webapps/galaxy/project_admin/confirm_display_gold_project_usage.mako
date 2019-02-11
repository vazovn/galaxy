<%inherit file="/base.mako"/>
<%namespace file="/message.mako" import="render_msg" />

<%def name="title()">Lifeportal Administration</%def>

<h2>Display usage features</h2>

<%
     form_action = h.url_for( controller='project_admin', action='manipulate_gold_projects')
%>

    ${render_msg( message, status )}
    <form action="${form_action}" method="post">
        <table id="modify_gold_project" class="grid">
            <tr><h2 colspan=3 align="center">Setting the project period for usage report</h2> 
           </tr>
           <tr><h2 colspan=3 align="center">&nbsp;</h2></tr>
            <tr>
                <th>Project name</th>
                <th valign="top" valign="center">Start date</th>
                <th valign="top" valign="center">End date</th>
            </tr>
            <tr>
                     <td><input type="text" name="project_name" id="project_name" value="${project_name}" readonly style="background-color:#E6E6E6"></td>
                     <td><input type="date" style="border:1px solid #ff0000"  pattern="\d\d\d\d-\d\d-\d\d"  name="start_date" value="${start_date}" /></td>
                     <td><input type="date" style="border:1px solid #ff0000"  pattern="\d\d\d\d-\d\d-\d\d"  name="end_date" value="${end_date}" /></td>
            </tr>
        </table>
        <div class="form-row">
                <input type="submit" name="project_usage" value="Display usage"/>
                <input type="submit" name="cancel" value="Cancel"/>
         </div>
    </form>
