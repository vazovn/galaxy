<%inherit file="/base.mako"/>
<%namespace file="/message.mako" import="render_msg" />

<%def name="title()">Lifeportal Administration</%def>

<h2>Create New Local Lifeportal Project</h2>

<%
     form_action = h.url_for( controller='project_admin', action='manipulate_gold_projects')
%>


    ${render_msg( message, status )}
    <form action="${form_action}" method="post">
        <table id="create_gold_project" class="grid">
            <tr><h2 colspan=6 align="center">Local Lifeportal project</h2></tr>
           <tr><h2 colspan=6 align="center">&nbsp;</h2></tr>
            <tr>
                <th valign="top">Project owner<font color="red">*</font></br>(email of the owner : </br>must be same as in Lifeportal and GOLD</br>user DB)</th>
                <th valign="top">Project name</br>(auto-generated)</th>
                <th valign="top" align="center">Amount in CPU hours<font color="red">*</font></br>(9 digits max)</th>
                <th valign="top" valign="center">Start date<font color="red">*</font></th>
                <th valign="top" valign="center">End date<font color="red">*</font></th>
                <th valign="top">Description (30 chars : [A-Za-z0-9]) </th>
            </tr>
            <tr>
                <td><input type="email" pattern="[^ @]*@[^ @]*" name="project_owner_email"  value=""></td>
                <td><input type="text" pattern="[A-Za-z0-9]*" name="project_name" maxlength="15" size=15 value="${project_name}" readonly style="background-color:#D8D8D8"/></td>
                <td><input type="text" pattern="\d*" name="cpu_amount" maxlength="9" size=9 value="" /></td>
                <td><input type="date" pattern="\d\d\d\d-\d\d-\d\d"  name="start_date" value="YYYY-MM-DD" /></td>
                <td><input type="date" pattern="\d\d\d\d-\d\d-\d\d"  name="end_date" value="YYYY-MM-DD" /></td>
                <td><input type="text"  name="gold_project_description" maxlength="50" size=30  value="" /></td>
            </tr>
        </table>
        <div class="form-row">
                <input type="submit" name="save_new_project" value="Save"/>
                <input type="submit" name="cancel" value="Cancel"/>
         </div>
    </form>
