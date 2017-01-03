<%inherit file="/webapps/galaxy/base_panels.mako"/>
<%namespace file="/message.mako" import="render_msg" />

## Default title
<%def name="title()">Application form for a Lifeportal project</%def>

<%def name="stylesheets()">
    ${parent.stylesheets()}    
    ## Include "base.css" for styling tool menu and forms (details)
    ${h.css( "base", "autocomplete_tagging", "tool_menu" )}

    ## But make sure styles for the layout take precedence
    ${parent.stylesheets()}

    <style type="text/css">
        body { margin: 0; padding: 0; overflow: hidden; }
        #left {
            background: #C1C9E5 url(${h.url_for('/static/style/menu_bg.png')}) top repeat-x;
        }
    </style>
</%def>

<%def name="javascripts()">
    ${parent.javascripts()}
</%def>

<%def name="init()">
    <%
        self.has_left_panel=False
        self.has_right_panel=False
    %>
</%def>

<%def name="center_panel()">
    <% center_url = h.url_for( controller='project_application', action='center_project_application', message=message, status=status ) %>
    <iframe name="galaxy_main" id="galaxy_main" frameborder="0" style="position: absolute; width: 100%; height: 100%;" src="${center_url}"> </iframe>
</%def>
