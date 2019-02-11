The changes in Lifeportal for galaxy release 18.09
=================================================

Remove .venv directory

1. (to be done after boot - .venv has to be created first) 

Add file usit.pth into 

.venv/lib/python2.7/site-packages

the file contains the PATHs to custom python packages


The file content is :
/home/galaxy/galaxy/lib/Teusit/python
/home/galaxy/galaxy/lib/

2. (to be done after boot - .venv has to be created first)

Edit the file 

.venv/lib/python2.7/site-packages/sqalchemy_utils/functions/database.py

It contains a DB check which blocks the read of Galaxy DB on a different host

l.463
if url.drivername.startswith('postgres'):
        # Nikolay USIT
        #url.database = 'postgres'
        url.database = database

3. 

Edit the config files 

galaxy.yml
==
mind the syntax, no '=' sign any more
tricky issues : paths, dbs, secret must be taken from the ssl.conf file of Apache 
OIDCClientID "xxx000xx0-00xx00000x-000"
==


local_env.sh
==
set all dbs to require=ssl
==

job_conf_xml.lifeportal
==
remove <handler> block
==


4.

The following packages may be needed in .venv

cp wkhtmltox dir (wkhtmltox-0.12.4_linux-generic-amd64.tar.gz) to .venv/bin 
create a link : wkhtmltopdf -> /home/galaxy/galaxy/.venv/bin/wkhtmltox/bin/wkhtmltopdf
   
pip install pdfkit (if necessary)


5. 

ssl.conf file shall be modified as follows :

RewriteEngine on
RewriteRule ^/callback - [END]
RewriteRule ^/logout https://auth.dataporten.no/logout [R,END]
RewriteRule ^/static/style/(.*) /home/galaxy/galaxy/static/style/blue/$1 [L]
RewriteRule ^/static/(.*) /home/galaxy/galaxy/static/$1 [L]
RewriteRule ^/favicon.ico /home/galaxy/galaxy/static/favicon.ico [L]
RewriteRule ^/robots.txt /home/galaxy/galaxy/static/robots.txt [L]
RewriteRule ^(.*) http://127.0.0.1:8080$1 [P]


6. Check static/welcome.html


== To build

as user galaxy
source .venv/bin/activate
make client-production-maps
deactivate (if needed)




================ FROM GALAXY TEAM ==========

.. figure:: https://galaxyproject.org/images/galaxy-logos/galaxy_project_logo.jpg
   :alt: Galaxy Logo

The latest information about Galaxy is available via `https://galaxyproject.org/ <https://galaxyproject.org/>`__

.. image:: https://img.shields.io/badge/questions-galaxy%20biostar-blue.svg
    :target: https://biostar.usegalaxy.org
    :alt: Ask a question

.. image:: https://img.shields.io/badge/chat-irc.freenode.net%23galaxyproject-blue.svg
    :target: https://webchat.freenode.net/?channels=galaxyproject
    :alt: Chat on irc

.. image:: https://img.shields.io/badge/chat-gitter-blue.svg
    :target: https://gitter.im/galaxyproject/Lobby
    :alt: Chat on gitter

.. image:: https://img.shields.io/badge/release-documentation-blue.svg
    :target: https://docs.galaxyproject.org/en/master/
    :alt: Release Documentation

.. image:: https://travis-ci.org/galaxyproject/galaxy.svg?branch=dev
    :target: https://travis-ci.org/galaxyproject/galaxy
    :alt: Inspect the test results

Galaxy Quickstart
=================

Galaxy requires Python 2.7 To check your python version, run:

.. code:: console

    $ python -V
    Python 2.7.3

Start Galaxy:

.. code:: console

    $ sh run.sh

Once Galaxy completes startup, you should be able to view Galaxy in your
browser at:

http://localhost:8080

Configuration & Tools
=====================

You may wish to make changes from the default configuration. This can be
done in the ``config/galaxy.ini`` file.

Tools can be either installed from the Tool Shed or added manually.
 For details please see the `tutorial <https://galaxyproject.org/admin/tools/add-tool-from-toolshed-tutorial/>`__.
Note that not all dependencies for the tools provided in the
``tool_conf.xml.sample`` are included. To install them please visit
"Manage dependencies" in the admin interface.

Issues and Galaxy Development
=============================

Please see `CONTRIBUTING.md <CONTRIBUTING.md>`_ .

Roadmap
=============================

Interested in the next steps for Galaxy? Take a look at the `roadmap <https://github.com/galaxyproject/galaxy/projects/8>`__.
