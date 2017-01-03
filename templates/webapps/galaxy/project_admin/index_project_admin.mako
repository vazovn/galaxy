<%inherit file="/webapps/galaxy/base_panels.mako"/>
<%namespace file="/message.mako" import="render_msg" />

## Default title
<%def name="title()">Lifeportal Administration</%def>

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
        self.has_left_panel=True
        self.has_right_panel=False
        self.active_view="admin"
    %>
</%def>

<%def name="left_panel()">
    <div class="unified-panel-header" unselectable="on">
        <div class='unified-panel-header-inner'>Project Administration</div>
    </div>
    <div class="unified-panel-body" style="padding: 10px; overflow: auto;">
        <div class="toolMenu">
            <div class="toolSectionList">
                <div class="toolSectionTitle">Users</div>
                <div class="toolSectionBody">
                    <div class="toolSectionBg">
                        <div class="toolTitle"><a href="${h.url_for( controller='project_admin', action='users' )}" target="galaxy_main">Manage users</a></div>
                    </div>
                </div>
                <div class="toolSectionPad"></div>
                <div class="toolSectionTitle">Projects</div>
                <div class="toolSectionBody">
                    <div class="toolSectionBg">
                        <div class="toolTitle"><a href="${h.url_for( controller='project_admin', action='manipulate_gold_projects' )}" target="galaxy_main">Manage projects</a></div>
                    </div>
                </div>
                <div class="toolSectionBody">
                    <div class="toolSectionBg">
                        <div class="toolTitle"><a href="${h.url_for( controller='project_admin', action='show_pending_projects' )}" target="galaxy_main">Show pending projects</a></div>
                   </div>
                </div>
                <div class="toolSectionBody">
                    <div class="toolSectionBg">
                        <div class="toolTitle"><a href="${h.url_for( controller='project_admin', action='show_rejected_projects' )}" target="galaxy_main">Show rejected projects</a></div>
                   </div>
                </div>
            </div>
        </div>    
    </div>
</%def>

<%def name="center_panel()">
    <% center_url = h.url_for( controller='project_admin', action='center_project_admin', message=message, status=status ) %>
    <iframe name="galaxy_main" id="galaxy_main" frameborder="0" style="position: absolute; width: 100%; height: 100%;" src="${center_url}"> </iframe>
</%def>
