from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render
from forms import *
from models import *

from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

# Used to create and manually log in a user
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth import login, authenticate

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# Create your views here.

# Initialized customer group and provider group
manager_users, created = Group.objects.get_or_create(name='Manager')
manager_users.save()

auditor_users, created = Group.objects.get_or_create(name='Auditor')
auditor_users.save()

admin_users, created = Group.objects.get_or_create(name='Admin')
admin_users.save()

# check whether user in customer group
def in_manager(function=None):
  actual_decorator = user_passes_test(
    lambda u: u.is_authenticated() and u.groups.filter(name='Manager').exists()
  )
  return actual_decorator(function)

# check whether user in provider group
def in_auditor(function=None):
  actual_decorator = user_passes_test(
    lambda u: u.is_authenticated() and u.groups.filter(name='Auditor').exists()
  )
  return actual_decorator(function)

def in_admin(function=None):
  actual_decorator = user_passes_test(
    lambda u: u.is_authenticated() and u.groups.filter(name='Admin').exists()
  )
  return actual_decorator(function)

def welcome(request):
    # Sets up list of just the logged-in user's (request.user's) items
    print 'WELCOME'
    return render(request, 'welcome.html', {})

@login_required
def filter(request):
    usr = User.objects.get_by_natural_key(request.user)
    try:
        customer = Manager.objects.get(user=usr)
        return redirect(reverse('home'))
    except(Manager.DoesNotExist):
        pass
    try:
        provider = Auditor.objects.get(user=usr)
        return redirect(reverse('audit'))
    except(Auditor.DoesNotExist):
        pass

    try:
        admin = Admin.objects.get(user=usr)
        return redirect(reverse('admin'))
    except(Admin.DoesNotExist):
        raise 404


def my_login(request):
    context = {}
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'login.html', context)

    form = LoginForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        print '????'
        return render(request, 'login.html', context)

    try:
        user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])
        if user == None:
            context = { 'form': form,
                'message':'The username or password is wrong. Please try again.'}
            return render(request, 'login.html', context)
        login(request, user)
        #need to be updated
    except(AttributeError):
        return redirect(reverse('login'))

    return filter(request)


@transaction.atomic
def manager_register(request):
    context = {}

    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        context['form'] = ManagerRegistrationForm()
        return render(request, 'register.html', context)

    errors = []
    context['errors'] = errors

    form = ManagerRegistrationForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'register.html', context)

    # Creates the new user from the valid form data
    new_user = User.objects.create_user(username=form.cleaned_data['username'], \
                                        password=form.cleaned_data['password1'], \
                                        first_name=form.cleaned_data['first_name'], \
                                        last_name=form.cleaned_data['last_name'], \
                                        email=form.cleaned_data['email'])
    if form.is_valid():

        new_manager, created = Manager.objects.get_or_create(user = new_user,
                                                               first_name=form.cleaned_data['first_name'],
                                                               last_name=form.cleaned_data['last_name'],)
        new_manager.save()

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1'])
    new_user.groups.add(manager_users)
    login(request, new_user)
    return redirect(reverse('home'))

@transaction.atomic
def auditor_register(request):
    context = {}

    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        context['form'] = AuditorRegistrationForm()
        return render(request, 'auditor_register.html', context)

    errors = []
    context['errors'] = errors

    form = AuditorRegistrationForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        print '????++'
        print form.errors
        print form
        return render(request, 'auditor_register.html', context)

    # Creates the new user from the valid form data
    new_user = User.objects.create_user(username=form.cleaned_data['username'], \
                                        password=form.cleaned_data['password1'], \
                                        first_name=form.cleaned_data['first_name'], \
                                        last_name=form.cleaned_data['last_name'], \
                                        email=form.cleaned_data['email'])
    if form.is_valid():
        new_auditor, created = Auditor.objects.get_or_create(user = new_user,
                                                               first_name=form.cleaned_data['first_name'],
                                                                last_name=form.cleaned_data['last_name'],)
        new_auditor.save()



    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1'])

    new_user.groups.add(auditor_users)

    login(request, new_user)
    return redirect(reverse('audit'))

@transaction.atomic
def admin_register(request):
    context = {}

    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        context['form'] = AdminRegistrationForm()
        return render(request, 'admin_register.html', context)

    errors = []
    context['errors'] = errors

    form = AdminRegistrationForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'admin_register.html', context)

    # Creates the new user from the valid form data
    new_user = User.objects.create_user(username=form.cleaned_data['username'], \
                                        password=form.cleaned_data['password1'], \
                                        first_name=form.cleaned_data['first_name'], \
                                        last_name=form.cleaned_data['last_name'], \
                                        email=form.cleaned_data['email'])
    if form.is_valid():

        new_admin, created = Admin.objects.get_or_create(user = new_user,
                                                               first_name=form.cleaned_data['first_name'],
                                                               last_name=form.cleaned_data['last_name'],)
        new_admin.save()

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1'])
    new_user.groups.add(admin_users)
    login(request, new_user)
    return redirect(reverse('admin'))

@in_manager
def home(request):
    context = {}
    print("manager")
    manager = get_object_or_404(Manager, user = request.user)
    relations = App_Manager_Relation.objects.filter(manager=manager)
    applications = []
    for relation in relations:
        applications.append(relation.application)

    if applications == []:
        context={'messages': "No Application Assigned to You."}
        return render(request, "error_page.html", context)

    permissions = App_Permission.objects.filter(application = applications[0])

    context = {'permissions':permissions, 'applications': applications, 'app':applications[0]}
    return render(request, 'homepage.html', context)

@in_manager
def view_permission(request, id):
    application = get_object_or_404(Application, id=id)
    permissions = App_Permission.objects.filter(application = application)

    manager = get_object_or_404(Manager, user = request.user)
    relations = App_Manager_Relation.objects.filter(manager=manager)
    applications = []
    for relation in relations:
        applications.append(relation.application)


    context = {'permissions':permissions, 'applications': applications,  'app':application}
    return render(request, "view_permission.html", context)



@transaction.atomic
def addData(request):
    print("add data")
    manager = get_object_or_404(Manager, user = request.user)
    application = Application.objects.create(app_name = "AWS")
    print application
    application2 = Application.objects.create(app_name = "Google")
    application.save()
    application2.save()


    app_manager_relation = App_Manager_Relation.objects.create(application = application, manager = manager)
    app_manager_relation.save()
    app_manager_relation2 = App_Manager_Relation.objects.create(application = application2, manager = manager)
    app_manager_relation2.save()
    #print application
    #print app_manager_relation

    ruser1 = RegularUser.objects.create(last_name="Josh", first_name='Smith')
    ruser2 = RegularUser.objects.create(last_name="Kobe", first_name='Paul')
    ruser3 = RegularUser.objects.create(last_name="Taylor", first_name='Fisher')

    ruser1.save()
    ruser2.save()
    ruser3.save()

    permission1, created = App_Permission.objects.get_or_create(application = application, regular_user=ruser1, manager=manager,
                                                       status="Read", reviewed_by=manager)
    permission2, created = App_Permission.objects.get_or_create(application = application, regular_user=ruser2, manager=manager,
                                                       status="Read-Write", reviewed_by=manager)
    permission3, created = App_Permission.objects.get_or_create(application = application, regular_user=ruser3, manager=manager,
                                                       status="Read-Write", reviewed_by=manager)
    permission4, created = App_Permission.objects.get_or_create(application = application2, regular_user=ruser1, manager=manager,
                                                       status="Read", reviewed_by=manager)
    permission5, created = App_Permission.objects.get_or_create(application = application2, regular_user=ruser2, manager=manager,
                                                       status="Read-Write", reviewed_by=manager)
    permission6, created = App_Permission.objects.get_or_create(application = application2, regular_user=ruser3, manager=manager,
                                                       status="Read-Write", reviewed_by=manager)

    permission1.save()
    permission2.save()
    permission3.save()
    permission4.save()
    permission5.save()
    permission6.save()

    return HttpResponse("all done")


@transaction.atomic
def addData_2(request):
    print("add data")
    manager = get_object_or_404(Manager, user = request.user)
    application = Application.objects.get(app_name = "AWS")
    print application
    application2 = Application.objects.get(app_name = "Google")
    print application2

    #app_manager_relation = App_Manager_Relation.objects.create(application = application, manager = manager)
    #app_manager_relation.save()
    #app_manager_relation2 = App_Manager_Relation.objects.create(application = application2, manager = manager)
    #app_manager_relation2.save()
    #print application
    #print app_manager_relation

    ruser1 = RegularUser.objects.get(last_name="Josh", first_name='Smith')
    ruser2 = RegularUser.objects.get(last_name="Kobe", first_name='Paul')
    ruser3 = RegularUser.objects.get(last_name="Taylor", first_name='Fisher')


    permission3, created = App_Permission.objects.get_or_create(application = application, regular_user=ruser3, manager=manager,
                                                       status="Read-Write", reviewed_by=manager)
    permission4, created = App_Permission.objects.get_or_create(application = application2, regular_user=ruser1, manager=manager,
                                                       status="Read", reviewed_by=manager)
    permission5, created = App_Permission.objects.get_or_create(application = application2, regular_user=ruser2, manager=manager,
                                                       status="Read-Write", reviewed_by=manager)
    permission6, created = App_Permission.objects.get_or_create(application = application2, regular_user=ruser3, manager=manager,
                                                       status="Read-Write", reviewed_by=manager)


    permission3.save()
    permission4.save()
    permission5.save()
    permission6.save()

    return HttpResponse("all done")


@transaction.atomic
def addData_3(request):
    auditor =  get_object_or_404(Auditor, user = request.user)
    application = Application.objects.get(app_name = "AWS")
    print application
    application2 = Application.objects.get(app_name = "Google")
    print application2

    app_auditor_relation = App_Auditor_Relation.objects.create(application = application, auditor = auditor)
    app_auditor_relation.save()

    app_auditor_relation2 = App_Auditor_Relation.objects.create(application = application2, auditor = auditor)
    app_auditor_relation2.save()

    return HttpResponse("ALL DONE")

@transaction.atomic
@in_manager
def edit_permission(request, id):
    permission = get_object_or_404(App_Permission, id=id)
    print permission
    if request.method == 'GET':
        form = PermissionForm(instance=permission)
        context = { 'permission':permission, 'form': form }
        return render(request, 'edit_permission.html', context)

    form = PermissionForm(request.POST, instance=permission)

    if not form.is_valid():
        context = { 'message':'status wrong', 'permission': permission, 'form': form  }

        return render(request, 'edit_permission.html', context)

    form.save()
    permission.reviewed_by = get_object_or_404(Manager, user = request.user)
    permission.save()


    application = permission.application
    return redirect(reverse('view_permission', args=(application.id,)))



@in_auditor
def audit(request):
    print("audit")

    auditor = get_object_or_404(Auditor, user = request.user)
    relations = App_Auditor_Relation.objects.filter(auditor=auditor)
    applications = []
    for relation in relations:
        applications.append(relation.application)

    if applications == []:
        context={'messages': "No Application Assigned to You."}
        return render(request, "error_page.html", context)

    permissions = App_Permission.objects.filter(application = applications[0])

    context = {'permissions':permissions, 'applications': applications}

    return render(request, 'audit_home.html', context)

@in_auditor
def audit_permission(request, id):
    print("audit")

    application = get_object_or_404(Application, id=id)
    auditor = get_object_or_404(Auditor, user = request.user)
    relations = App_Auditor_Relation.objects.filter(auditor=auditor)
    applications = []
    for relation in relations:
        applications.append(relation.application)

    permissions = App_Permission.objects.filter(application = application)

    context = {'permissions':permissions, 'applications': applications}

    return render(request, 'audit_home.html', context)

@in_admin
def admin(request):
    print("admin")

    admin = get_object_or_404(Admin, user = request.user)
    managers = Manager.objects.all()
    auditors = Auditor.objects.all()
    applications = Application.objects.all()
    if not applications :
        context = {'messages' : "Please add application first." }
        context['form'] = CreateAppForm()
        return render(request, 'admin_home.html', context)
    else:
        application = applications[0]
        manager_relations = App_Manager_Relation.objects.filter(application=application)
        auditor_relations = App_Auditor_Relation.objects.filter(application=application)

        approved_managers = []
        approved_auditors = []

        for m_relation in manager_relations:
            approved_managers.append(m_relation.manager)
        for a_relation in auditor_relations:
            approved_auditors.append(a_relation.auditor)


        wait_managers = [ x for x in managers if x not in approved_managers]
        print wait_managers
        wait_auditors = [ x for x in auditors if x not in approved_auditors]

        context = {'applications': applications, 'approved_managers':approved_managers, 'approved_auditors':approved_auditors,
                   'wait_managers':wait_managers, 'wait_auditors':wait_auditors, 'application':application}
        context['form'] = CreateAppForm()

        return render(request, 'admin_home.html', context)



@in_admin
def view_assignment(request, id):

    admin = get_object_or_404(Admin, user = request.user)
    managers = Manager.objects.all()
    auditors = Auditor.objects.all()

    application = get_object_or_404(Application, id=id)
    applications = Application.objects.all()

    manager_relations = App_Manager_Relation.objects.filter(application=application)
    auditor_relations = App_Auditor_Relation.objects.filter(application=application)

    approved_managers = []
    approved_auditors = []

    for m_relation in manager_relations:
        approved_managers.append(m_relation.manager)
    for a_relation in auditor_relations:
        approved_auditors.append(a_relation.auditor)

    wait_managers = [ x for x in managers if x not in approved_managers]
    print wait_managers
    wait_auditors = [ x for x in auditors if x not in approved_auditors]

    context = {'applications': applications, 'approved_managers':approved_managers, 'approved_auditors':approved_auditors,
               'wait_managers':wait_managers, 'wait_auditors':wait_auditors, 'application':application}

    return render(request, 'admin_home.html', context)

@transaction.atomic
@in_admin
def assign_manager(request, id1, id2):
    manager = get_object_or_404(Manager, id=id2)
    application = get_object_or_404(Application, id=id1)
    app_manager_relation = App_Manager_Relation.objects.create(application = application, manager = manager)
    app_manager_relation.save()

    return redirect(reverse('view_assignment', args=(application.id,)))

@transaction.atomic
@in_admin
def remove_manager(request, id1, id2):
    manager = get_object_or_404(Manager, id=id2)
    application = get_object_or_404(Application, id=id1)

    app_manager_relation = App_Manager_Relation.objects.get(application = application, manager = manager)
    app_manager_relation.delete()

    return redirect(reverse('view_assignment', args=(application.id,)))

@transaction.atomic
@in_admin
def assign_auditor(request, id1, id2):
    auditor = get_object_or_404(Auditor, id=id2)
    application = get_object_or_404(Application, id=id1)
    app_auditor_relation = App_Auditor_Relation.objects.create(application = application, auditor = auditor)
    app_auditor_relation.save()

    return redirect(reverse('view_assignment', args=(application.id,)))

@transaction.atomic
@in_admin
def remove_auditor(request, id1, id2):
    auditor = get_object_or_404(Auditor, id=id2)
    application = get_object_or_404(Application, id=id1)
    app_auditor_relation = App_Auditor_Relation.objects.get(application = application, auditor = auditor)
    app_auditor_relation.delete()

    return redirect(reverse('view_assignment', args=(application.id,)))


@in_admin
def upload(request, id):
    application = get_object_or_404(Application, id=id)
    applications = Application.objects.all()
    context = {'applications': applications,  'application':application}
    context['form'] = CreateAppForm()
    return render(request, 'admin_upload.html', context)

@transaction.atomic
@in_admin
def upload_file(request, id):
    form = UploadFileForm(request.POST, request.FILES)
    print form
    success = 0
    if form.is_valid():
        f = request.FILES['file']
        for line in f:
            if len(line)>0:
                line = line[:-1]
            try:
                print line
                s = line.split(",")
                email = s[0]
                name = s[1]
                permission = s[2]
                print permission
                names = s[1].split(" ")
                firstname = names[0]
                lastname = names[1]
                user,created = RegularUser.objects.get_or_create(last_name=lastname,first_name=firstname)
                user.save()
                app= Application.objects.get(id=id)
                app_permission,created = App_Permission.objects.get_or_create(application=app,regular_user = user,status = permission)
                app_permission.save()
            except Exception as e:
                break
        success = 1

    application = get_object_or_404(Application, id=id)
    applications = Application.objects.all()
    if success==0:
        context = {'applications': applications,  'application':application,'messages':"File is not in valid format. Try again"}
    else:
        context = {'applications': applications,  'application':application,'messages':"Success!"}
    return render(request, 'admin_upload.html', context)


def report_pdf(request,id):
    application = get_object_or_404(Application, id=id)
    permissions = App_Permission.objects.filter(application = application)


    doc = SimpleDocTemplate("report.pdf", pagesize=A4, rightMargin=30,leftMargin=30, topMargin=30,bottomMargin=18)
    doc.pagesize = landscape(A4)
    elements = []


    data = []
    data.append(["User ID","First Name","Last Name","Permission","Reviewed By"])
    for permission in permissions:
        user = permission.regular_user
        id = user.id
        firstname = user.first_name
        lastname = user.last_name
        status = permission.status
        if permission.reviewed_by:
            reviewer = permission.reviewed_by.first_name+" "+permission.reviewed_by.last_name
        else:
            reviewer = "None"
        data.append([str(id),firstname,lastname,status,reviewer])


    style = TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
                           ('TEXTCOLOR',(1,1),(-2,-2),colors.red),
                           ('VALIGN',(0,0),(0,-1),'TOP'),
                           ('TEXTCOLOR',(0,0),(0,-1),colors.blue),
                           ('ALIGN',(0,-1),(-1,-1),'CENTER'),
                           ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                           ('TEXTCOLOR',(0,-1),(-1,-1),colors.green),
                           ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                           ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                           ])

    #Configure style and word wrap
    stylesheet = getSampleStyleSheet()
    s = stylesheet["BodyText"]
    s.wordWrap = 'CJK'
    data2 = [[Paragraph(cell, s) for cell in row] for row in data]
    t=Table(data2)
    t.setStyle(style)

    title = "Access Review Report for "
    title += application.app_name
    elements.append(Paragraph(title,stylesheet['Title']))
    elements.append(t)
    doc.build(elements)

    with open('report.pdf', 'r') as pdf:
        response = HttpResponse(pdf.read(),content_type='application/pdf')
        response['Content-Disposition'] = 'filename=report.pdf'
        return response
    pdf.closed

@transaction.atomic
@in_admin
def create_app(request):
    context={}
    #application = get_object_or_404(Application, id=id)

    #if request.method == 'GET':
        #applications = Application.objects.all()
        #context['form'] = CreateAppForm()
        #application = get_object_or_404(Application, id=id)
        #context = {'applications': applications,  'application':application,}
        #return render(request, 'admin_upload.html', context)

    form = CreateAppForm(request.POST)

    if form.is_valid():
        new_app = Application.objects.create(app_name=form.cleaned_data['app_name'])
    new_app.save()
    #applications = Application.objects.all()
    #application = get_object_or_404(Application, id=id)
    #context = {'applications': applications,  'application':application,}
    #context['form'] = CreateAppForm()

    return redirect(reverse('admin'))
