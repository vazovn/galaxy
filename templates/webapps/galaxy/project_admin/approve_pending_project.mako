<%inherit file="/base.mako"/>
<%namespace file="/message.mako" import="render_msg" />

<%def name="title()">Lifeportal Administration</%def>

<h2>Lifeportal Project Administration</h2>

<%
   ## 'error' means the application has been rejected
   if status != 'error' :
       import Accounting_project_management
       form_action = h.url_for( controller='project_admin', action='approve_pending_project')
       pending_project = Accounting_project_management.check_pending_projects(project_id = project_id)
       labels = [
             'Project requestor',
             'Requestors email',
             'Requestors Institution',
             'Requestors country',
             'Project name',
             'Requested CPU hours',
             'Project description',
             'Selected applications',
             'Start date',
             'End date',
             'Application date'
       ]
       names = ['requestor','email','institution','country','project_name','cpu_hours','description','selected_apps','start_date','end_date','application_date']
       
       for  p in pending_project:
           print "PPP >>>>", p
%>

    ${render_msg( message, status )}
    
    %if status != 'error' :
       <form action="${form_action}" method="post">
                      <table id="approve_pending_project">
                                <tr><h2 colspan=3 align="center">Project approval</h2></tr>
                                <tr><h5 colspan=3 align="center">The data in the red-border fields can be modified before approval</h5></tr>
                                <tr><h2 colspan=3 align="center">&nbsp;</h2></tr>
                                   %for  p in pending_project:
                                    <tr>
                                           <td><input type="hidden" name="project_id" value="${p[0]}"></td>
                                    </tr>
                                           %for  label,item, data in zip(labels,names, p[1:]):
                                               <tr>
                                                       %if item == 'cpu_hours' :
                                                             <th>${label} : </th>
                                                             <td>&nbsp;</td>
                                                             <td><input style="border:1px solid #ff0000"  pattern="\d*" name="${item}" value="${data}"></td>
                                                       %elif item == 'start_date'  or item == 'end_date' :
                                                             <th>${label} : </th>
                                                             <td>&nbsp;</td>
                                                             <td><input style="border:1px solid #ff0000"  type="date" name="${item}" value="${data}"></td>
                                                       %elif item == 'reason_for_rejection' :
                                                             <th>${label} : </th>
                                                             <td>&nbsp;</td>
                                                             <td><input style="border:1px solid #ff0000"  type="text" name="${item}" value="" size="100"></td>
                                                       %elif item == 'description' :
                                                             <th>${label} : </th>
                                                             <td>&nbsp;</td>
                                                             <td><textarea rows="4" cols="50" name="${item}" value="${data}" readonly>${data}</textarea></td>
                                                       %else :
                                                             <th>${label} : </th>
                                                             <td>&nbsp;</td>
                                                             <td><input name="${item}" value="${data}" readonly></td>
                                                       %endif
                                                </tr>
                                           %endfor
                                    </tr>
                                   %endfor
                      </table>
                      </p>

                      <div class="form-row">
                           <span style='color:red;font-weight:bold'>The requestor has declared that the project will not contain any sensitive data</span> 
                      </div>


                      <div class="form-row">
                               <input type="submit" name="approve_pending_project" value="Approve pending project"/>
                      </div>
                      <div class="form-row">
                             Please, be patient! The procedure takes some time ...
                      </div>
                      
                      <table id="reject_pending_project">
                                <tr><h2 colspan=3 align="center">Project rejection</h2></tr>
                                <tr><h2 colspan=3 align="center">&nbsp;</h2></tr>
                                <tr>
                                            <th>Reason for rejection : </th>
                                            <td>&nbsp;</td>
                                            <td><textarea rows="2" cols="50" name="reason_for_rejection" value="" ></textarea></td>
                                </tr>
                     </table>
                      </p>
                      <div class="form-row">
                               <input type="submit" name="reject_pending_project" value="Reject pending project"/>
                      </div>
      </form>
    %endif 
    
    
 
