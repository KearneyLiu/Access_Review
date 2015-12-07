from django.contrib.auth.models import User
from django.db import models

'''
Administrator
The one that controls the whole app
'''
class Admin(models.Model):
    user = models.OneToOneField(User)
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)

'''
Manager
The one that reviews applications assigned to him
'''
class Manager(models.Model):
    user = models.OneToOneField(User)
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.first_name + " " + self.last_name

'''
Auditor
The one that audit all the applications
'''
class Auditor(models.Model):
    user = models.OneToOneField(User)
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)

'''
User
The normal user in the app
'''
class RegularUser(models.Model):
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    #user_name = models.CharField(max_length=30)

'''
Application
id is autoincremented
'''
class Application(models.Model):
    app_name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.app_name



'''
App-Manager-Relation:
Shows the app and manager relation
'''
class App_Manager_Relation(models.Model):
    application = models.ForeignKey(Application)
    manager = models.ForeignKey(Manager, null = True)

    def __unicode__(self):
        return self.application.app_name +"  "+ self.manager.first_name + " " + self.manager.last_name

class App_Auditor_Relation(models.Model):
    application = models.ForeignKey(Application)
    auditor = models.ForeignKey(Auditor, null = True)

'''
App-Permission:
The app-user and permission result
'''
class App_Permission(models.Model):
    read = "Read"
    read_write = "Read-write"
    choices = (
        (read, u'Read'),
        (read_write, u'Read and Write'),
    )

    application = models.ForeignKey(Application, related_name='application', null = True)
    regular_user = models.ForeignKey(RegularUser, related_name='regular_user', null = True)
    manager = models.ForeignKey(Manager, related_name='manager', null = True)
    status = models.CharField(max_length=30, choices=choices, default=read)
    reviewed_by = models.ForeignKey(Manager, related_name='reviewed_by', null = True)

    def __unicode__(self):
        return "status:" + self.status



class Test(models.Model):
    status = models.CharField(max_length=30)
