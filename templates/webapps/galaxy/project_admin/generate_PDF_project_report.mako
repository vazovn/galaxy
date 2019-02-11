<%inherit file="/base.mako"/>
<%namespace file="/message.mako" import="render_msg" />

<%def name="title()">Generate report for a Lifeportal project</%def>

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


${render_msg( message, status)}

<h2>Lifeportal report generated on ${project_data['date']} for ${project_data['author']}</h2>

<form action="${form_action}" method="post">

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
             <td>${project_data['name']}</td>
        </tr>
        <tr>
             <td>Job title/position :</td>
             <td>&nbsp;</td>
             <td>${project_data['job_title']}</td>
        </tr>
        <tr>
             <td>E-mail address:</td>
             <td>&nbsp;</td>
             <td>${project_data['email']}</td>
        </tr>
      
        <tr>
             <td>Institution (Faculty, Department) :</td>
             <td>&nbsp;</td>
             <td>${project_data['institution']}</td>
        </tr>
        
        <tr>
              <td>Country :</td>
              <td>&nbsp;</td>
              <td>${project_data['country']}</td>
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
              <td>${project_data['project_name']}</td>
        </tr>

        <tr>
              <td>CPU hours allocated:</td>
              <td>&nbsp;</td>
              <td>${project_data['cpu_hours_required']}</td>
        </tr>

     <tr>
              <td>CPU hours used:</td>
              <td>&nbsp;</td>
              <td>${project_data['cpu_hours_used']}</td>
        </tr>

     <tr>
              <td>CPU hours remaining:</td>
              <td>&nbsp;</td>
              <td>${project_data['cpu_hours_remaining']}</td>
        </tr>


         <tr>
              <td>Start date :</td>
              <td>&nbsp;</td>
              <td>${project_data['start_date']}</td>
        </tr>

        <tr>
              <td>End date :</td>
              <td>&nbsp;</td>
              <td>${project_data['end_date']}</td>
        </tr>
        
        <tr>
             <th colspan='3'>&nbsp;</th>
        </tr>
        
        <tr>
              <td>Extension is applied for the project until (optional):</td>
              <td>&nbsp;</td>
              <td>${project_data['extension_date']}</td>
        </tr>
        
        <tr>
              <td>Additional CPU hours needed (optional) :</td>
              <td>&nbsp;</td>
              <td>${project_data['additional_cpu_hours']}</td>
        </tr>
        
        <tr>
             <th colspan='3'>&nbsp;</th>
        </tr>
        
        <tr>
              <td>Project report :</td>
              <td>&nbsp;</td>
              <td>${project_data['project_report']}</textarea> 
              </td>
        </tr>
        
        <tr>
             <th colspan='3'>&nbsp;</th>
        </tr>
       
       </table>
        </p>

        <h2>Publications</h2>
     
                       <TABLE id="dataTable" width="100%" border="1"  cellpadding="10">
                            <tr>
                                      <TH align="center">TITLE</TH>
                                      <TH align="center" >Journal</TH>
                                      <TH align="center">YEAR</TH>
                                      <TH align="center">DOI</TH>
                             </tr>
                             <TR>
                                      <TD valign="center">${project_data['title']}</TD>
                                      <TD valign="center">${project_data['journal']}</TD>
                                      <TD valign="center">${project_data['year']}</TD>
                                      <TD valign="center">${project_data['DOI']}</TD>
                              </TR>
                              
                              %if 'publications' in project_data and project_data['publications'] and len(project_data['publications'] ) > 0 :
                                  %for row in project_data['publications'] :

                                      <TR>
                                                 <TD valign="center">${row[0]}</TD>
                                                 <TD valign="center">${row[1]}</TD>
                                                 <TD valign="center">${row[2]}</TD>
                                                 <TD valign="center">${row[3]}</TD>
                                      </TR>
                                  %endfor
                              %endif
                              
                      </TABLE>
 
    </form>
  
