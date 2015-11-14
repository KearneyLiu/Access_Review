from django.db import models

'''
Administrator
The one that controls the whole app
'''
class Admin(models.Model):
    admin_id = models.EmailField(max_length=60,primary_key=True)
    admin_name = models.CharField(max_length=30)

'''
Manager
The one that reviews applications assigned to him
'''
class Manager(models.Model):
    manager_id = models.EmailField(max_length=50,primary_key=True)
    manager_name = models.CharField(max_length=60)

'''
Auditor
The one that audit all the applications
'''
class Auditor(models.Model):
    auditor_id = models.EmailField(max_length=60,primary_key=True)
    auditor_name = models.CharField(max_length=30)

'''
User
The normal user in the app
'''
class user(models.Model):
    user_id = models.EmailField(max_length=60)
    user_name = models.CharField(max_length=30)

'''
Application
id is autoincremented
'''
class Application(models.Model):
    app_name = models.CharField(max_length=30)


'''
App-Manager-Relation:
Shows the app and manager relation
'''
class App_Manager_Relation(models.Model):
    app_id = models.ForeignKey(Application)
    manager_id = models.ForeignKey(Manager)

'''
App-Permission:
The app-user and permission result
'''
class App_Permission(models.Model):
    app_id = models.ForeignKey(Application)
    user_id = models.EmailField(max_length=60)
    permission = models.CharField(max_length=30)
    reviewed_by = models.CharField(max_length=30)





