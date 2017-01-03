<%inherit file="/base.mako"/>
<%namespace file="/message.mako" import="render_msg" />

<%def name="title()">Lifeportal Administration</%def>

<h2>Modify Local Lifeportal Project</h2>

<%
     form_action = h.url_for( controller='project_admin', action='manipulate_gold_projects')
%>


<% 
    import Accounting_project_management
    projects = Accounting_project_management.list_all_GOLD_projects ( filter_by_project_name = project_name)
    for p in projects :
         if p[3] == "True" :
               p[3] = "<font color=\"green\">True</font>"
         else :
               p[3] = "<font color=\"red\">False</font>"
%>

    ${render_msg( message, status )}
    <form action="${form_action}" method="post">
        <table id="modify_gold_project" class="grid">
            <tr><h2 colspan=6 align="center">Modifying project <em>${project_name}</em></h2>
           </tr>
           <tr><h2 colspan=6 align="center">&nbsp;</h2></tr>
            <tr>
                <th>Project owner</th>
                <th>Project name</th>
                <th>Status</th>
                <th>Amount in CPU hours (6 digits)</th>
                <th>Description</th>
                <th valign="top" valign="center">Start date</th>
                <th valign="top" valign="center">End date</th>
            </tr>
            %for p in projects :
                 <tr>
                    <input type="hidden" name="project_name" id="project_name" value="${p[1]}" />
                    <input type="hidden" name="old_cpu_amount" id="old_cpu_amount" value="${p[4]}" />
                    <input type="hidden" name="old_start_date" id="old_start_date" value="${p[6]}" />
                    <input type="hidden" name="old_end_date" id="old_end_date" value="${p[7]}" />
                    <td>${p[0]}</td>
                    <td>${p[1]}</td>
                    <td>${p[3]}</td>
                    <td>
                        <label>Add/Withdraw amount:</br>The exisitng one is <strong>${p[4]}</strong> CPU hrs</label></br>
                        <input type="text" maxlength="6" size=6 style="border:1px solid #ff0000" pattern="-*\d*" name="cpu_amount" maxlength="9" size=9 value="0" />
                   </td>
                   <td>${p[5]}</td>
                   <td><input type="date" style="border:1px solid #ff0000"  pattern="\d\d\d\d-\d\d-\d\d"  name="start_date" value="${p[6]}" /></td>
                   <td><input type="date" style="border:1px solid #ff0000"  pattern="\d\d\d\d-\d\d-\d\d"  name="end_date" value="${p[7]}" /></td>
                 </tr>
             %endfor
        </table>
        <div class="form-row">
                <input type="submit" name="save_modified_project" value="Save"/>
                <input type="submit" name="cancel" value="Cancel"/>
         </div>
         <div class="form-row">
              <font color="red">Note:</font>The amount can be positive or negative. The negative amount will be withdrawn from the total of CPU hours.</br>
              The negative amount is given like this : e.g. -100
         </div>
    </form>
