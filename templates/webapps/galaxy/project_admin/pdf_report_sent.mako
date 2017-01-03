<%inherit file="/base.mako"/>
<%namespace file="/message.mako" import="render_msg" />

<%def name="title()">Lifeportal Administration</%def>

<h2>An email with attached PDF file containing the report has been sent to your email address</h2>

<%
     form_action = h.url_for( controller='project_admin', action='manipulate_gold_projects')
%>

    <form action="${form_action}" method="post">
        ${render_msg( message, status )}
        <div class="form-row">
                <input type="submit" name="cancel" value="Back to &quot;Manage projects&quot;"/>
         </div>
    </form>
