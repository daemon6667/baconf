The sources in the master branch are not work yet. The project is under development!

baconf
======

Web interface to create configs for Bacula backup tool. It's a simple framework to convinient editing configuration files of Bacula backup tool. 
All developments are on Python language. There are also used external open source software.

Capabilities
============
- loads existed backend.config file specified in the backend root directory as Bacula config
- responsible for some api queries

To be done:
- web interface for manage configurations

How to run
==========

Launch python2 backend.py to start running web server

Web API
=======
The below listed functions return json-formatted responses. Top level variables are 'data' and 'success'. If success has true value, then the backend has been processed with no errors. It doesn't garantuee that the response contain some useful data, it also can contain no data. Data variable conains data were requiested.

- /def/resource              returns a list of template resources (file: resources.def)
- /def/resource/<resource>   returns a list of the all attributes could be used for the resource

Working directory structure
===========================
Directory 
- html	  - static files for building web interface
- current - directory should contain either started bacula config files, or be empty to start with no bacula configs


