<%inherit file="/base.mako"/>
<%namespace file="/message.mako" import="render_msg" />

<%def name="title()">Generate report for a Lifeportal project</%def>

<h2>Lifeportal report generation form</h2>

<%
     
     form_action = h.url_for( controller='project_admin', action='manipulate_gold_projects')
     
%>

<SCRIPT language="javascript">
        function addRow(tableID) {
 
            var table = document.getElementById(tableID);
 
            var rowCount = table.rows.length;
            var row = table.insertRow(rowCount);
 
            var cell1 = row.insertCell(0);
            var element1 = document.createElement("input");
            element1.type = "checkbox";
            element1.name="chkbox[]";
            cell1.appendChild(element1);
 
            var cell2 = row.insertCell(1);
            cell2.innerHTML = rowCount + 1;
 
            var cell3 = row.insertCell(2);
            var element2 = document.createElement("input");
            element2.type = "text";
            element2.name = "txtbox[]";
            cell3.appendChild(element2);
            
            var cell4 = row.insertCell(3);
            var element3 = document.createElement("input");
            element3.type = "text";
            element3.name = "txtbox1[]";
            cell4.appendChild(element3);
 
            var cell5 = row.insertCell(4);
            var element4 = document.createElement("input");
            element4.type = "text";
            element4.name = "txtbox2[]";
            cell5.appendChild(element4);
            
            var cell6 = row.insertCell(5);
            var element5 = document.createElement("input");
            element5.type = "text";
            element5.name = "txtbox3[]";
            cell6.appendChild(element5);
 
        }
 
        function deleteRow(tableID) {
            try {
            var table = document.getElementById(tableID);
            var rowCount = table.rows.length;
 
            for(var i=0; i<rowCount; i++) {
                var row = table.rows[i];
                var chkbox = row.cells[0].childNodes[0];
                if(null != chkbox && true == chkbox.checked) {
                    table.deleteRow(i);
                    rowCount--;
                    i--;
                }
 
 
            }
            }catch(e) {
                alert(e);
            }
        }
 
</SCRIPT>


${render_msg( message, status )}


<form action="${form_action}" method="post">

         <input type="hidden" name="project_code"  value="${project_data[11]}" />

         <table id='big_table' >
         <tr><td>
         <table id='personal data'>
         
        <tr>
             <th colspan='3' valign='top'>Personal information about the project leader</th>
        </tr>
        <tr>
             <th colspan='3'>&nbsp;</th>
        </tr>
        <tr>
             <td>Project responsible:</td>
             <td>&nbsp;</td>
             <td><input type='text' name='name' value='${project_data[0]}' maxlength="20" readonly /></td>
        </tr>
        <tr>
             <td>Job title/position :</td>
             <td>&nbsp;</td>
             <td><input type='text'  name='job_title' value='${project_data[1]}' maxlength="20" readonly /></td>
        </tr>
        <tr>
             <td>E-mail address:</td>
             <td>&nbsp;</td>
             <td><input type='email'  name='email' value='${project_data[2]}' readonly /></td>
        </tr>
      
        <tr>
             <td>Institution (Faculty, Department) :</td>
             <td>&nbsp;</td>
             <td><input type='text'   name='institution' value='${project_data[3]}' maxlength="50"  readonly /></td>
        </tr>
        
        <tr>
              <td>Country :</td>
              <td>&nbsp;</td>
              <td><input type='text'  name='country' value='${project_data[4]}' maxlength="20" readonly /></td>
        </tr>
 
        <tr>
             <th colspan='3'>&nbsp;</th>
        </tr>
        <tr>
             <th colspan='3'>&nbsp;</th>
        </tr>
        
        <tr>
             <th colspan='3'>Project information</th>
        </tr>

        <tr>
             <th colspan='3'>&nbsp;</th>
        </tr>

        <tr>
              <td>Project name  :</td>
              <td>&nbsp;</td>
              <td><input type='text'  name='project_name' value='${project_data[5]}' maxlength="30"  readonly /></td>
        </tr>

        <tr>
              <td>CPU hours allocated:</td>
              <td>&nbsp;</td>
              <td><input type='text'  maxlength="9" name='cpu_hours_required' value='${project_data[6]}' readonly /></td>
        </tr>

     <tr>
              <td>CPU hours used:</td>
              <td>&nbsp;</td>
              <td><input type='text'  maxlength="9" name='cpu_hours_used' value='${project_data[9]}' readonly /></td>
        </tr>

     <tr>
              <td>CPU hours remaining:</td>
              <td>&nbsp;</td>
              <td><input type='text'  maxlength="9" name='cpu_hours_remaining' value='${project_data[10]}' readonly /></td>
        </tr>


         <tr>
              <td>Start date :</td>
              <td>&nbsp;</td>
              <td><input type='date' name='start_date'  value='${project_data[7]}' readonly /></td>
        </tr>

        <tr>
              <td>End date :</td>
              <td>&nbsp;</td>
              <td><input type='date'  name='end_date'  value='${project_data[8]}' readonly /></td>
        </tr>
        
        <tr>
             <th colspan='3'>&nbsp;</th>
        </tr>
        
        <tr>
             <th colspan='3'>&nbsp;</th>
        </tr>
        
        <tr>
              <td>Project report :</br><font size="-2">Please specify if there are large discrepancies between</br>the CPU hours initially required in the application and </br>actually used CPU hours</font></td>
              <td>&nbsp;</td>
              <td><textarea rows="4" cols="50" name='project_report' value=''></textarea> 
              </td>
        </tr>
        
        <tr>
             <th colspan='3'>&nbsp;</th>
        </tr>
        
        <tr>
              <td>Publications :</td>
              <td>&nbsp;</td>
              <td>
                      
                       <TABLE id="dataTable" width="350px" border="1">
                            <tr>
                                      <td align="center">&nbsp;</td>
                                      <td align="center">1</td>
                                      <TH align="center">TITLE</TH>
                                      <TH align="center" >Journal</TH>
                                      <TH align="center">YEAR</TH>
                                      <TH align="center">DOI</TH>
                             </tr>
                             <TR>
                                      <TD valign="center"><INPUT type="checkbox" name="chk"/></TD>
                                      <TD valign="center"> 2 </TD>
                                      <TD valign="center"> <INPUT type="text" name="title"  /> </TD>
                                      <TD valign="center"> <INPUT type="text" name="journal" />  </TD>
                                      <TD valign="center"> <INPUT type="text" name="year"/>  </TD>
                                      <TD valign="center"> <INPUT type="text" name="DOI" />  </TD>
                              </TR>
                      </TABLE>
                      <p></p>
                      <INPUT type="button" value="Add Row" onclick="addRow('dataTable')" />
                      <INPUT type="button" value="Delete Row" onclick="deleteRow('dataTable')" />
              </td>
        </tr>
        
               
        <tr>
             <th colspan='3'>&nbsp;</th>
        </tr>
        <tr>
             <th colspan='3'>Required project modification (optional)</th>
        </tr>
        <tr>
             <th colspan='3'>&nbsp;</th>
        </tr>
        
        <tr>
              <td>Apply for extension until ${extension_date} ? (optional):</td>
              <td>&nbsp;</td>
              <td><input type='checkbox' name='extension_date'  value='${extension_date}' /></td>
        </tr>
        
        <tr>
              <td>I would also apply for additional CPU hours (optional) :</td>
              <td>&nbsp;</td>
              <td><input type='text' name='additional_cpu_hours' pattern="\d+" maxlength="5" maxsize="5"  value='' /></td>
        </tr>
        
       </table>
        </p>
        
             <div class="form-row">
                    <input type="submit" name="generate_pdf" value="Generate PDF file"/>
             </div>
 
    </form>
  
