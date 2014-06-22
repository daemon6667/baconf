#!/usr/bin/env python

from coreres import *

class ResourceClient(ResourceAbstract):
    def __init__(self, name):
        ResourceAbstract.__init__(self, name, RESCLASS_CLIENT)
        self.addOption('Password', OPTION_TYPE_STR, RequiredOption, SingleValue, '')
        self.addOption('Address', OPTION_TYPE_IPADDR, RequiredOption, SingleValue, '10.6.0.10')
        self.addOption('FDPort', OPTION_TYPE_INT, RequiredOption, SingleValue, 9102)
        self.addOption('File Retention', OPTION_TYPE_INT, RequiredOption, SingleValue, 60)
        self.addOption('Maximum Concurrent Jobs', OPTION_TYPE_INT, RequiredOption, SingleValue, 5)
        self.addOption('Catalog', OPTION_TYPE_RESOURCE_CATALOG, RequiredOption, SingleValue, None)

class ResourceDevice(ResourceAbstract):
    def __init__(self, name):
        ResourceAbstract.__init__(self, name, RESCLASS_DEVICE)
        self.addOption('Device Type', OPTION_TYPE_ENUM, NonRequiredOption, SingleValue, RESOURCE_DEVICE_TYPES[RESOURCE_DEVICE_TYPE_FILE])
        self.addOption('Maximum Concurrent Jobs', OPTION_TYPE_INT, NonRequiredOption, SingleValue, 5)
        self.addOption('Maximum File Size', OPTION_TYPE_SIZE, NonRequiredOption, SingleValue, 0)
        self.addOption('Archive Device', OPTION_TYPE_STR, RequiredOption, SingleValue, '')
        self.addOption('LabelMedia', OPTION_TYPE_BOOL, RequiredOption, SingleValue, True)
        self.addOption('Random Access', OPTION_TYPE_BOOL, RequiredOption, SingleValue, True)
        self.addOption('AutomaticMount', OPTION_TYPE_BOOL, RequiredOption, SingleValue, True)
        self.addOption('RemovableMedia', OPTION_TYPE_BOOL, NonRequiredOption, SingleValue, True)
        self.addOption('Media Type', OPTION_TYPE_STR, NonRequiredOption, SingleValue, 'File')
        self.addOption('AlwaysOpen', OPTION_TYPE_BOOL, NonRequiredOption, SingleValue, False)

class ResourceStorage(ResourceAbstract):
    def __init__(self, name):
        ResourceAbstract.__init__(self, name, RESCLASS_STORAGE)
        self.addOption('Address', OPTION_TYPE_IPADDR, NonRequiredOption, SingleValue, '')
        self.addOption('SDPort', OPTION_TYPE_INT, NonRequiredOption, SingleValue, 9103)
        self.addOption('Password', OPTION_TYPE_STR, NonRequiredOption, SingleValue, '')
        self.addOption('Media Type', OPTION_TYPE_STR, NonRequiredOption, SingleValue, 'File')
        self.addOption('WorkingDirectory', OPTION_TYPE_STR, NonRequiredOption, SingleValue, '/var/db/bacula')
        self.addOption('Pid Directory', OPTION_TYPE_STR, NonRequiredOption, SingleValue, '/var/run')
        self.addOption('Maximum Concurrent Jobs', OPTION_TYPE_INT, NonRequiredOption, SingleValue, 10)
        self.addOption('Device', OPTION_TYPE_RESOURCE_DEVICE, RequiredOption, SingleValue, None)

class ResourceDirector(ResourceAbstract):
    def __init__(self, name):
        ResourceAbstract.__init__(self, name, RESCLASS_DIRECTOR)
        self.addOption('Password', OPTION_TYPE_STR, NonRequiredOption, SingleValue, '')
        self.addOption('WorkingDirectory', OPTION_TYPE_STR, NonRequiredOption, SingleValue, '/var/db/bacula')
        self.addOption('DIRport', OPTION_TYPE_INT, NonRequiredOption, SingleValue, 9101)
        self.addOption('Messages', OPTION_TYPE_RESOURCE_MESSAGES, NonRequiredOption, SingleValue, None)
        self.addOption('PidDirectory', OPTION_TYPE_STR, NonRequiredOption, SingleValue, '/var/run')
        self.addOption('QueryFile', OPTION_TYPE_STR, NonRequiredOption, SingleValue, '/usr/local/share/bacula/query.sql')
        self.addOption('Maximum Concurrent Jobs', OPTION_TYPE_INT, NonRequiredOption, SingleValue, 5)

class ResourceCatalog(ResourceAbstract):
    def __init__(self, name):
        ResourceAbstract.__init__(self, name, RESCLASS_CATALOG)
        self.addOption('DBName', OPTION_TYPE_STR, RequiredOption, SingleValue, '"bacula"; dbuser = "bacula"; dbpassword = "IyDVAI8RBtKEU5Ax"')

class ResourceMessages(ResourceAbstract):
    def __init__(self, name):
        ResourceAbstract.__init__(self, name, RESCLASS_MESSAGE)
        self.addOption('MailCommand', OPTION_TYPE_STR, NonRequiredOption, SingleValue, '/usr/local/sbin/bsmtp -f \"\(Bacula\) \<%r\>\" -s \"Bacula daemon message\" %r')
        self.addOption('Mail', OPTION_TYPE_STR, NonRequiredOption, SingleValue, 'backup = all, skipped')
        self.addOption('Console', OPTION_TYPE_RESOURCE_CONSOLE, NonRequiredOption, SingleValue, None)
        self.addOption('Append', OPTION_TYPE_STR, NonRequiredOption, SingleValue, '"/var/log/bacula/bacula.log" = all, !skipped')
        self.addOption('OperatorCommand', OPTION_TYPE_STR, NonRequiredOption, SingleValue, '/usr/local/sbin/bsmtp -f \\"(Bacula) <%r>\\" -s \\"Bacula: Intervention needed for %j\\" %r')
        self.addOption('Operator', OPTION_TYPE_STR, NonRequiredOption, SingleValue, 'backup = mount')
        self.addOption('Catalog', OPTION_TYPE_RESOURCE_CATALOG, NonRequiredOption, SingleValue, 'all')

class ResourcePool(ResourceAbstract):
    def __init__(self, name):
        ResourceAbstract.__init__(self, name, RESCLASS_POOL)
        self.addOption('Pool Type', OPTION_TYPE_ENUM, RequiredOption, SingleValue, RESOURCE_POOL_TYPES[RESOURCE_POOL_TYPE_BACKUP])
        self.addOption('Label Format', OPTION_TYPE_STR, NonRequiredOption, SingleValue, "Vol_")
        self.addOption('Maximum Volume Jobs', OPTION_TYPE_INT, NonRequiredOption, SingleValue, 5)
        self.addOption('Maximum Volume Bytes', OPTION_TYPE_SIZE, RequiredOption, SingleValue, '100M')
        self.addOption('Maximum Volumes', OPTION_TYPE_INT, NonRequiredOption, SingleValue, 5)
        self.addOption('Storage', OPTION_TYPE_RESOURCE_STORAGE, RequiredOption, SingleValue, ResourceStorage)
        self.addOption('Recycle', OPTION_TYPE_BOOL, NonRequiredOption, SingleValue, True)
        self.addOption('Purge Oldest Volume', OPTION_TYPE_BOOL, NonRequiredOption, SingleValue, True)
        self.addOption('AutoPrune', OPTION_TYPE_BOOL, NonRequiredOption, SingleValue, True)

class ResourceFileSet(ResourceAbstract):
    def __init__(self, name):
         ResourceAbstract.__init__(self, name, RESCLASS_FILESET)

class ResourceConsole(ResourceAbstract):
    def __init__(self, name):
        ResourceAbstract.__init__(self, name, RESCLASS_CONSOLE)
        self.addOption('Password', OPTION_TYPE_STR, RequiredOption, SingleValue, '')
        self.addOption('CommandACL', OPTION_TYPE_STR, RequiredOption, SingleValue, 'status, .status')

class ResourceSchedule(ResourceAbstract):
    def __init__(self, name):
        ResourceAbstract.__init__(self, name, RESCLASS_SCHEDULE)
        self.addOption('Run', OPTION_TYPE_SCHEDULE, RequiredOption, MultipleValue, None)

class ResourceJob(ResourceAbstract):
    def __init__(self, name):
        ResourceAbstract.__init__(self, name, RESCLASS_JOB)
        self.addOption('JobDefs', OPTION_TYPE_STR, NonRequiredOption, SingleValue, '')
        self.addOption('Client', OPTION_TYPE_RESOURCE_CLIENT, RequiredOption, SingleValue, None)
        self.addOption('Pool', OPTION_TYPE_RESOURCE_POOL, RequiredOption, SingleValue, None)
        self.addOption('Storage', OPTION_TYPE_RESOURCE_STORAGE, RequiredOption, SingleValue, None)
        self.addOption('FileSet', OPTION_TYPE_RESOURCE_FILESET, RequiredOption, SingleValue, None)
        self.addOption('Schedule', OPTION_TYPE_RESOURCE_SCHEDULE, RequiredOption, SingleValue, None)

if __name__ == "__main__":
    client = ResourceDevice('airlan.cubie')
    print(client.m_class)
    print(client.listOptions())
    print(client.option('Name').value())
    print(client.print_conf())

