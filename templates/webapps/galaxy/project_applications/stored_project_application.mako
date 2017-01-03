<%inherit file="/base.mako"/>
<%namespace file="/message.mako" import="render_msg" />

<%def name="title()">Application for a Lifeportal project is registered</%def>

<h2>Lifeportal project application confirmation</h2>

${render_msg( message, status )}
