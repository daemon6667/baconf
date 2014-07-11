[Director]
  Name 			= type=string,required=true
  DirPort 		= type=integer,required=false,default=9101
  QueryFile 		= type=string,required=true,default=/usr/local/share/bacula/query.sql
  WorkingDirectory 	= type=string,default=/var/db/bacula
  PidDirectory 		= type=string,default=/var/run
  Maximum Concurrent Jobs = type=integer,default=5
  Password 		= type=password,required=true
  Messages 		= type=resource,resource=Messages,required=true
  Monitor 		= type=bool,default=false
