<%inherit file="/base.mako"/>
<%namespace file="/message.mako" import="render_msg" />

<%def name="title()">Lifeportal Administration</%def>

<h2>Lifeportal Local Project Approved</h2>

<%
     form_action = h.url_for( controller='project_admin', action='show_pending_projects')
%>

    <form action="${form_action}" method="post">
        ${render_msg( message, status )}
        <div class="form-row">
                <input type="submit" name="cancel" value="Back"/>
         </div>
    </form>
