<%inherit file="/base.mako"/>
<%namespace file="/message.mako" import="render_msg" />

%if message:
    ${render_msg( message, status )}
%endif

<%
   import Accounting_project_management
   
   ## Get all the projects owned by the project administrator
   gold_project_list = Accounting_project_management.list_owned_GOLD_projects_names_only ( trans.user.email )

   # Add projects like CLOTU and BIT
   other_managed_projects = [] 
   if trans.user and app.config.is_project_admin_user( trans.user ) :
         other_managed_projects = Accounting_project_management.list_owned_GOLD_projects_names_only ( trans.user.email ) 
         print "PROJECT BASE PANELS MAKO OTHER MANAGED PROJECTS ", other_managed_projects

         for other_project in other_managed_projects :
                gold_project_list.append(other_project)
                
   ## Get all the users 
   gold_user_list = Accounting_project_management.get_all_users()
%>


    <div class="toolForm">
        <div class="toolFormTitle">Associate users to projects</div>
        <div class="toolFormBody">
        <form name="add_users_to_project" id="add_users_to_project" action="${h.url_for( controller='project_admin', action='associate_to_project' )}" method="post" >
            <div class="form-row">
                <label>
                    Select the users in the dropdown below who will be associated to a project (press Ctrl for multiple users):
                </label>
                <select multiple name="gold_user" size="15">
                       %for user in gold_user_list :  
                             <option value="${user}" >${user}</option>
                       %endfor
                </select>
            </div>
            <div class="form-row">
                <label>
                    Select a project:
                </label>
                <select name="gold_project">
                       <option value="0" selected>Select a project</option>
                       %for project in  gold_project_list :  
                             <option value="${project}" >${project}</option>
                       %endfor
                </select>
                
            </div>
            <div class="form-row">
                <input type="submit" name="add_users_to_project" value="Associate the user to the selected project"/>
            </div>
        </form>
        </div>
    </div>


