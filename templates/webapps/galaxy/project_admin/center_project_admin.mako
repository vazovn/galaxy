<%inherit file="/base.mako"/>
<%namespace file="/message.mako" import="render_msg" />

<%def name="title()">Lifeportal Administration</%def>

<h2>Project/User Administration</h2>

%if message:
    ${render_msg( message, status )}
%else:
    <p>General information</p>
    <ul>
        <li><strong>User administration</strong>. There exist the following users in the Lifeportal:
            <p/>
            <ul>
                <li>
                  <strong>FEIDE users</strong> : users who have a FEIDE affiliation (a Norwegian Higher Education Institution). These users register (at first login) and log in into the Lifeportal with their FEIDE credentials. If a FEIDE user is a member of some Notur projects, after the login s/he will be authorized to run jobs only in these projects. Otherwise, s/he receives a 200 CPU hours test quota to run jobs in the Lifeportal. FEIDE users can be associated to local Lifeportal projects by the project managers (PIs) of these projects, once the FEIDE users have registered in the Lifeportal.
                </li></p>
                <li>
                <strong>Notur users</strong> : users who <strong>do not</strong> have FEIDE affiliation but are members of Notur project(s). These users register (at first login) and log in into the Lifeportal with their Notur credentials. After the login, Notur users are authorized to run jobs only in the Notur projects they are members of. They can be associated to local Lifeportal projects by the project managers (PIs) of these projects, once the Notur users have registered in the Lifeportal.
                </li></p>
                <li>
                <strong>Local Lifeportal users</strong> : users who <strong>do not</strong> have FEIDE or Notur affiliation. They are added to Lifeportal local projects by the respective project managers (PIs) and the users receive an email that they must register into the Lifeportal as Lifeportal users. Only then can they run jobs in the local Lifeportal project they have been associated to by the project manager!
                </li>
            </ul>
        </li>
        <p/>
        <li><strong>Project administration</strong>. The Lifeportal allows the users to run jobs in the following projects:
            <p/>
            <ul>
                <li>
                  Default Lifeportal project (200 CPU hrs) - granted to FEIDE users (see here above). This project is managed by the Lifeportal administration.
                </li></p>
                <li>
                  Notur projects - registered Lifeportal users have access to their Notur projects. These projects are managed by Notur.
                </li></p>
                <li>
                  Local Lifeportal projects - project managers apply for these projects, and administer them by adding/removing Lifeportal users, deactivating the projects when necessary. These projects are managed partly by the Project managers and partly by the Lifeportal Resource Allocation Committee.
                </li>
            </ul>
        </li>
      </ul>
    <br/>
%endif
