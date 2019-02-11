<%inherit file="/base.mako"/>
<%namespace file="/message.mako" import="render_msg" />

<%def name="title()">Apply for a Lifeportal project</%def>

<h2>Lifeportal project application form</h2>

<%
     form_action = h.url_for( controller='project_application', action='send_application_form')
     ## add apps manually
     ## INITIAL
     #apps = ("MyBayes","BEAST","Structure","RAxML","CLOTU","PAUP","R","PhyML","Blast","Migrate","MrModeltest","Gaussian","PAML","Phylobayes","Garli","AIR-Identifier","Treefinder","Lamarc","AIR-Remover","Mafft","Newbler","Best","Autodock4","ClustEx","Unphased","Air-Appender","McMcPhase")
     ## PRESENT LIST
     apps = ("MyBayes","BEAST","Structure","RAxML","PAUP","R","PhyML","Blast","Migrate","MrModeltest","Gaussian","PAML","Phylobayes")

     logged_user = trans.user.email
     email_of_the_logged_user = logged_user.strip()
%>

${render_msg( message, status )}
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
             <td>Project responsible, e.g. John Doe. (permitted chars: capital/small letters and blanks)<span style='color:red;font-weight:bold'>*</span>:</td>
             <td>&nbsp;</td>
             <td><input type='text' pattern="[A-Za-z ]*" name='name' value='' maxlength="20" /></td>
        </tr>
        <tr>
             <td>Job title/position (permitted chars: capital/small letters, digits and blanks):</td>
             <td>&nbsp;</td>
             <td><input type='text' pattern="[A-Za-z0-9 ]*" name='job_title' value='' maxlength="20" /></td>
        </tr>
        <tr>
             <td>E-mail address:</td>
             <td>&nbsp;</td>
             <td><input type='email'  name='email' value='${email_of_the_logged_user}' readonly /></td>
        </tr>
        <tr>
             <td>Phone no (please, use digits only, e.g. 0047XXX for Norway):</td>
             <td>&nbsp;</td>
             <td><input type='text' pattern="[0-9 ]*" maxlength="18" name='phone' value='' /></td>
        </tr>
        <tr>
             <td>Cell-phone number (please, use digits only, e.g. 0047XXX for Norway)<span style='color:red;font-weight:bold'>*</span>:</td>
             <td>&nbsp;</td>
             <td><input type='text' pattern="[0-9 ]*"  maxlength="18" name='cellphone' value='' /></td>
        </tr>

        <tr>
             <td>Institution (Faculty, Department) (permitted chars: capital/small letters and blanks)<span style='color:red;font-weight:bold'>*</span>:</td>
             <td>&nbsp;</td>
             <td><input type='text' pattern="[A-Za-z ]*" name='institution' value='' maxlength="50" /></td>
        </tr>
        
        <tr>
              <td>Country (permitted chars: capital/small letters and blanks)<span style='color:red;font-weight:bold'>*</span>:</td>
              <td>&nbsp;</td>
              <td><input type='text' pattern="[A-Za-z ]*" name='country' value='' maxlength="20"  /></td>
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
              <td>Project name (permitted chars: capital/small letters and digits)<span style='color:red;font-weight:bold'>*</span>:</td>
              <td>&nbsp;</td>
              <td><input type='text' pattern="[A-Za-z0-9]*" name='project_name' value='' maxlength="30" /></td>
        </tr>

        <tr>
              <td>CPU hours (specify how many CPU hours you need for the project)(permitted chars: digits)<span style='color:red;font-weight:bold'>*</span>:</td>
              <td>&nbsp;</td>
              <td><input type='text' pattern="[0-9]*" maxlength="9" name='cpu_hours' value='' /></td>
        </tr>

        <tr>
              <td>Preferred applications<span style='color:red;font-weight:bold'>*</span> (Click on the box to display the apps) :</td>
              <td>&nbsp;</td>
              <td>
                   <select name='applications' class='applications' multiple>
                               %for app in sorted(apps) :
                                   <option value="${app}">${app}</option>
                               %endfor
                   </select>
              </td>
        </tr>

        <tr>
              <td>Project description (permitted chars: all)<span style='color:red;font-weight:bold'>*</span>:</td>
              <td>&nbsp;</td>
              <td><textarea rows="4" cols="50" name='project_description' value=''></textarea> 
              </td>
        </tr>
        
         <tr>
              <td>Start date<span style='color:red;font-weight:bold'>*</span>:</td>
              <td>&nbsp;</td>
              <td><input type='date' name='start_date' pattern="\d\d\d\d-\d\d-\d\d" value='YYYY-MM-DD' /></td>
        </tr>

        <tr>
              <td>End date :</td>
              <td>&nbsp;</td>
              <td><input type='date'  name='end_date' pattern="\d\d\d\d-\d\d-\d\d" value='2018-12-31' readonly /></td>
        </tr>


        
        <tr>
             <th colspan='3'>&nbsp;</th>
        </tr>
        

        <tr>
              <td>I declare that the project <span style='color:red;font-weight:bold'>does not</span> contain sensitive data<span style='color:red;font-weight:bold'>*</span>:</td>
              <td>&nbsp;</td>
              <td><input type='checkbox' name='tsd_checkbox' /></td>
        </tr>
               <tr>
             <th colspan='3'>&nbsp;</th>
        </tr>

        
        <tr>
              <td>I have read the <a href='http://www.uio.no/english/services/it/research/hpc/lifeportal/start-using/index.html' target='_blank'>Lifeportal requirements</a> and accepted them<span style='color:red;font-weight:bold'>*</span>:</td>
              <td>&nbsp;</td>
              <td><input type='checkbox' name='agree_checkbox' /></td>
        </tr>

        </table>
        
        </p>
        
         <div class="form-row">
              <font color="red">Note: </font>Fields marked <span style='color:red;font-weight:bold'>*</span> must be filled out.
         </div>
         
         <div class="form-row">
                                        <input type="submit" name="send_application_form" value="Send application form"/>
                                       <input type="submit" name="cancel" value="Cancel"/>
                       </div>
    </form>
  
