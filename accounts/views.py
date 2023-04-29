import csv
from csv import DictReader
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from .forms import *
from .models import *
from django.template import loader
from enum import Enum
from django.contrib.auth import authenticate, login, logout
from itertools import chain
import hashlib
import bcrypt
import uuid
from .filters import *

class ROLES(Enum):
    M = 'L3'
    S = 'L2'
    C = 'L1'
    R = 'L1'
   
class CATEGORIES(Enum):
    B = 'Books'
    C = 'CDs'
    D = 'DVDs'
    R = 'Records'
    

# Create your views here.
def home(request):
    return render(request, 'accounts/index.html')

def mojos(request):
    return render(request, 'accounts\mjlanding.html')

def clone(request):
    return render(request, 'accounts/clone.html')

def getstarted (request):
    return render(request, 'accounts/get_started.html')

#This was tested and it works - checked
def index(request):
    
    for role in ROLES:
        newRole = Roles(role= role.name, privilege=role.value)
        newRole.save()
        print('{}: {}'.format(role.name, role.value)) #for debugging
    
    input_file = csv.DictReader(open('mediapedia_dataset (1).csv', encoding="UTF-8"))
    # with open('mediapedia_dataset (1).csv') as f:
    #     print(f)
    # return
    for row in input_file:
        category = row['PID']
        newProduct = Products(pid = row['PID'], pprice = float(row['Price']), 
            pquantity = int(row['Quantity']), pamountsold = int(row['Amt_Sold']), 
            pmediatype = category[0])
        newProduct.save()
        
        if category[0] == 'C':
            newCD = CDs(cid = newProduct, ctitle = row['Title'], 
                cartist = row['Artist/Author'], cgenre = row['Genre'], 
                cstarrating = row['Star_rating'], cinstock = 'In Stock' if (int(newProduct.pquantity) > 0) else 'Out of Stock')
            newCD.save()
        elif category[0] == 'D':
            newDVD = DVDs(did = newProduct, dtitle = row['Title'], 
                dactor = row['Artist/Author'], dgenre = row['Genre'], 
                dstarrating = row['Star_rating'], dinstock = 'In Stock' if (int(newProduct.pquantity) > 0) else 'Out of Stock')
            newDVD.save()
        elif category[0] == 'R':
            newRecord = Records(rid = newProduct, rtitle = row['Title'], 
                rartist = row['Artist/Author'], rgenre = row['Genre'], 
                rstarrating = row['Star_rating'], rinstock = 'In Stock' if (int(newProduct.pquantity) > 0) else 'Out of Stock')
            newRecord.save()
        else:
            newBook = Books(bid = newProduct, btitle = row['Title'], 
                bauthor = row['Artist/Author'], bgenre = row['Genre'], 
                bstarrating = row['Star_rating'], binstock = 'In Stock' if (int(newProduct.pquantity) > 0) else 'Out of Stock')
            newBook.save()
            
    template = loader.get_template('accounts/loaddb.html')

    form = RegistrationForm()
    context = {}
    context['form'] = RegistrationForm()
    #return render(request, 'create_user', context)
    return HttpResponse(template.render(context, request))

#This was tested and it works. Routing and template needed <-merged w emprppofilw 
def displayAllEmployees(request):
    arr = []
    for item in Employee.objects.raw('SELECT * FROM accounts_employee JOIN accounts_roles ON "employeeRole_id" = "role"'):
        arr.append([item.employeeRole, item.employeeFirstName])
    #print(arr)
    context = {'arr':arr}
    return render (request, 'accounts/dashboard.html',context)

def searchprod(request):
    if request.method =="POST":
        searched = request.POST.get("searched")
        books = Books.objects.filter(btitle__icontains= searched)
        books2 = Books.objects.filter(bauthor__icontains= searched)
        records = Records.objects.filter(rtitle__icontains= searched)
        records2 = Records.objects.filter(rartist__icontains= searched)
        cds = CDs.objects.filter(ctitle__icontains= searched)
        cds2 = CDs.objects.filter(cartist__icontains= searched)
        dvds = DVDs.objects.filter(dtitle__icontains= searched)
        dvds2 = DVDs.objects.filter(dactor__icontains= searched)
        products = Products.objects.filter(pid__icontains = searched)
        query = list(chain(books, records, records2, cds, dvds, dvds2, books2, cds2, products))
        return render(request, 'accounts/search.html', {'result': searched, 'query': query})
    else:
        return render(request, 'accounts/search.html')

def search (request):
    if request.method =="POST":
        searched = request.POST.get("searched")
        books = Books.objects.filter(btitle__icontains= searched)
        books2 = Books.objects.filter(bauthor__icontains= searched)
        records = Records.objects.filter(rtitle__icontains= searched)
        records2 = Records.objects.filter(rartist__icontains= searched)
        cds = CDs.objects.filter(ctitle__icontains= searched)
        cds2 = CDs.objects.filter(cartist__icontains= searched)
        dvds = DVDs.objects.filter(dtitle__icontains= searched)
        dvds2 = DVDs.objects.filter(dactor__icontains= searched)
        products = Products.objects.filter(pid__icontains = searched)
        

        query = list(chain(books, records, records2, cds, dvds, dvds2, books2, cds2, products))
        return render(request, 'accounts/results.html', {'result': searched, 'query': query})
    else:
        return render(request, 'accounts/results.html')
    
#not used ^modified above
def searchBar(request):
    context = {}

    if request.method == 'POST':
        if request.POST.get('mybtn'):
            form = SearchForm(request.POST)
            context['form'] = form
            if form.is_valid():
                querystring = form.cleaned_data['querystring']
                categories = form.cleaned_data['category']

                for i in categories:
                    if i == 'B':
                        books1 = Books.objects.filter(btitle__contains= querystring)
                        books2 = Books.objects.filter(bauthor__contains= querystring)
                        books = list(chain(books1, books2))
                        for i in books:
                            print("Title: {}, Author: {}, Price: ${}".format(i.btitle, i.bauthor, i.bid.pprice))
                        
                            
                    elif i == 'C':
                        cds1 = CDs.objects.filter(ctitle__contains= querystring)
                        cds2 = CDs.objects.filter(cartist__contains= querystring)
                        cds = list(chain(cds1, cds2))
                        for i in cds:
                            print("Title: {}, Artist: {}, Price: ${}".format(i.ctitle, i.cartist, i.cid.pprice))
                        

                    elif i == 'D':
                        dvds1 = DVDs.objects.filter(dtitle__contains= querystring)
                        dvds2 = DVDs.objects.filter(dactor__contains= querystring)
                        dvds = list(chain(dvds1, dvds2))
                        for i in dvds:
                            print("Title: {}, Actor: {}, Price: ${}".format(i.dtitle, i.dactor, i.did.pprice))
                        

                    elif i == 'R':
                        records1 = Records.objects.filter(rtitle__contains= querystring)
                        records2 = Records.objects.filter(rartist__contains= querystring)
                        records = list(chain(records1, records2))            
                        for i in records:
                            print("Title: {}, Artist: {}, Price: ${}".format(i.rtitle, i.rartist, i.rid.pprice))
                        

                context = {'bookresults': books, 'cdresults': cds, 'dvdresults': dvds, 'recordsresults': records, 'form':form}
                return render(request, 'accounts/search.html', context)
                #return (context)
            
    else:
        template = loader.get_template('accounts/search.html')
        context = {}
        context['form'] = SearchForm()
        return HttpResponse(template.render(context, request))
    

#tested
#This was tested and works. template and routing needed for the page display of it
def topProducts(request):
    #search = {}
    #search = searchBar(request)
    books = []
    cds = []
    dvds = []
    records = []
    highpriority = []
    mediumpriority = []
    
    for item in Books.objects.raw('''SELECT * FROM accounts_books JOIN accounts_products ON bid = pid 
        ORDER BY bstarrating DESC, pquantity ASC LIMIT 5'''):
        books.append([item.btitle, item.bauthor, item.bstarrating])
    
    for item in CDs.objects.raw('''SELECT * FROM accounts_cds JOIN accounts_products ON cid = pid
        ORDER BY cstarrating DESC, pquantity ASC LIMIT 5'''):
        cds.append([item.ctitle, item.cartist, item.cstarrating])
        
    for item in DVDs.objects.raw('''SELECT * FROM accounts_dvds JOIN accounts_products ON did = pid
        ORDER BY dstarrating DESC, pquantity ASC LIMIT 5;'''):
        dvds.append([item.dtitle, item.dactor, item.dstarrating])
        
    for item in Records.objects.raw('''SELECT * FROM accounts_records JOIN accounts_products ON rid = pid
        ORDER BY rstarrating DESC, pquantity ASC LIMIT 5;'''):
        records.append([item.rtitle, item.rartist, item.rstarrating])
    
    
    products = Products.objects.all()
    
    booktotal = products.filter(pmediatype='B').count()
    recordtot = products.filter(pmediatype='R').count()
    CDtot = products.filter(pmediatype='C').count()
    DVDtot = products.filter(pmediatype='D').count()
    
    for item in Products.objects.raw('SELECT * FROM accounts_products JOIN accounts_books ON pid = bid'):
        if  item.pquantity == 0:
            highpriority.append([item.pid, item.pmediatype, "${:.2f}".format(item.pprice), item.btitle, item.pquantity])
        elif item.pquantity < 5:
            mediumpriority.append([item.pid, item.pmediatype, "${:.2f}".format(item.pprice), item.btitle, item.pquantity])
    
    for item in Products.objects.raw('SELECT * FROM accounts_products JOIN accounts_records ON pid = rid'):
        if  item.pquantity == 0:
            highpriority.append([item.pid, item.pmediatype, "${:.2f}".format(item.pprice), item.rtitle, item.pquantity])
        elif item.pquantity < 5:
            mediumpriority.append([item.pid, item.pmediatype, "${:.2f}".format(item.pprice), item.rtitle, item.pquantity])
            
    for item in Products.objects.raw('SELECT * FROM accounts_products JOIN accounts_dvds ON pid = did'):
        if  item.pquantity == 0:
            highpriority.append([item.pid, item.pmediatype, "${:.2f}".format(item.pprice), item.dtitle, item.pquantity])
        elif item.pquantity < 5:
            mediumpriority.append([item.pid, item.pmediatype, "${:.2f}".format(item.pprice), item.dtitle, item.pquantity])
    
    for item in Products.objects.raw('SELECT * FROM accounts_products JOIN accounts_cds ON pid = cid'):
        if  item.pquantity == 0:
            highpriority.append([item.pid, item.pmediatype, "${:.2f}".format(item.pprice), item.ctitle, item.pquantity])
        elif item.pquantity < 5:
            mediumpriority.append([item.pid, item.pmediatype, "${:.2f}".format(item.pprice), item.ctitle, item.pquantity])
    
    #myfilter = SearchFilter()

    context = {'books':books, 'cds':cds, 'dvds':dvds, 'records':records,'booktotal':booktotal, 'recordtot':recordtot, 'CDtot':CDtot, 'DVDtot':DVDtot,'products':products, 'highpriority':highpriority, 'mediumpriority':mediumpriority}
    #context.update(search)
    return render(request,'accounts/products.html', context)
    #return books, cds, dvds, records
    
#change this to fit the current models in this file and add the required templates for testing. 


def deleteProduct(request,pk): #mine
     product = Products.objects.get(pid=pk)
     if request.method =='POST':
        product.delete()
        return redirect('products')
 
     context = {'item':product}
     return render(request, 'accounts/deleteprod.html', context)

#tested
def updateUser(request,pk):
    user = Employee.objects.get(employeeID=pk)
    form = UpdateEmployee(instance=user)
    context ={'form':form}

    if request.method =='POST':
         form = UpdateEmployee(request.POST,instance=user)
         if form.is_valid():
              form.save() 
              return redirect('dash')
         
    return render(request, 'accounts/register.html', context)



#tested
def deleteUser(request,pk):
    user = Employee.objects.get(employeeID=pk)
    if request.method =='POST':
        user.delete()
        return redirect('dash')
    context = {'item':user}
    return render(request, 'accounts/deleteuser.html', context)



#changed to dynamic method - tested 
def updateProd(request,pk):
    user = Products.objects.get(pid=pk)
    form = UpdateProduct(instance=user)
    context ={'form':form}

    if request.method =='POST':
         form = UpdateProduct(request.POST,instance=user)
         if form.is_valid():
              form.save() 
              return redirect('products')
         
    return render(request, 'accounts/updateprod.html', context)


#tested
#This works as intended.
def signUp(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegistrationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            email = form.cleaned_data['email']
            firstname = form.cleaned_data['firstName']
            lastname = form.cleaned_data['lastName']
            phonenumber = form.cleaned_data['phoneNumber']
            password = form.cleaned_data['password']
            employeeid = form.cleaned_data['employeeid']
            #password = prepassword
            temprole = form.cleaned_data['whatRoleAreYou']
            
            for item in Roles.objects.raw('SELECT role FROM accounts_roles WHERE role = %s', temprole):
                finalrole = item
            
            newEmployee = Employee(employeeID = employeeid, employeeFirstName = firstname,
                employeeLastName = lastname, employeeEmail = email, employeePhone = phonenumber,
                employeePassword = password, employeeRole_id = finalrole)
            newEmployee.save()

            #newLoginCredential = LoginCredentials(Username = username, Password = password, WorkerID = employeeid)
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return redirect('login')

    # if a GET (or any other method) we'll create a blank form
    else:
        template = loader.get_template('accounts/register.html')
        context = {}
        context['form'] = RegistrationForm()
        return HttpResponse(template.render(context, request))
#tested
#This works as intended now. Officially fixed and fully functional
def logIn(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            pword = form.cleaned_data['password'] #input
        # fname = form.cleaned_data ['firstname']
            id = form.cleaned_data['employeeid']
            
            query = Employee.objects.get(employeeID=id)

            if (query.employeePassword == pword):
                # instantiate new session to begin
                csrftoken = query.employeeFirstName[:-2]
                csrftoken += query.employeeEmail[:2]
                csrftoken += query.employeePassword[2:4]
                
                my_hash = hashlib.sha256(csrftoken.encode('utf-8')).hexdigest()
                
                session_data = my_hash
                query.sessionID = session_data
                query.save()
                return redirect('dash')
            else:
                return redirect('create_user')
                #return redirect('accounts/register.html')
        # if a GET (or any other method) we'll create a blank form
    else:
        template = loader.get_template('accounts/login.html')
        context = {}
        context['form'] = LogInForm()
        return HttpResponse(template.render(context, request))

#tested
def employeeprofile(request,pk): 
    employee = Employee.objects.get(employeeID=pk)
    details = employee
    #rolespelling = ROLES(employee.employeeRole_id)
    context = {'employee':employee,'details':details} #, 'rolespelling':rolespelling}
    return render(request,'accounts/profile.html',context)

def item(request,pk):
    item = Products.objects.get(pid=pk)
    if item.pmediatype =='B':
        book = Books.objects.get(bid=item.pid)
        final = book
    elif item.pmediatype =='C':
        cd = CDs.objects.get(cid=item.pid)
        final = cd
    elif item.pmediatype =='D':
        dvd = DVDs.objects.get(did=item.pid)
        final = dvd
    elif item.pmediatype =='R':
        record = Records.objects.get(rid=item.pid)
        final = record

   
    #rolespelling = ROLES(employee.employeeRole_id)
    context = {'final':final} #, 'rolespelling':rolespelling}
    return render(request,'accounts/item.html',context)



#tested
def dash(request): 
    
    role1 = Roles.objects.get(role='M')
    role2 = Roles.objects.get(role='S')
    role3 = Roles.objects.get(role='R')
    role4 = Roles.objects.get(role='R')
    
    employees1 = role1.employee_set.all()
    employees2 = role2.employee_set.all()
    employees3 = role3.employee_set.all()
    employees4 = role4.employee_set.all()
    
    employeeroles = list(chain(employees1, employees2, employees3, employees4))
    for i in employeeroles:
        print(i.employeeRole_id.role, i.employeeID)

    total_employees = len(employeeroles)

    context = {'total_employees':total_employees, 'employee_roles' : employeeroles}

    return render(request,'accounts/dashboard.html',context)

#Tested
def addProduct(request):
    if request.method == 'POST':
        print('got to here')
        form = NewProduct(request.POST)
        if form.is_valid():
            productid = form.cleaned_data['productID']
            producttitle = form.cleaned_data['productTitle']
            productprice = form.cleaned_data['productPrice']
            productquantity = form.cleaned_data['productQuantity']
            productmediatype = form.cleaned_data['productMediaType']
            productgenre =  form.cleaned_data['productGenre']
            productauthoractorartist = form.cleaned_data['productauthoractorartist']
            productrating = form.cleaned_data['productRating']
                
            newProduct = Products(pid = productid, pmediatype = productmediatype,
                pprice = productprice, pquantity = productquantity, pamountsold = 0)
            newProduct.save()
            
            if productmediatype == 'C':
                newCD = CDs(cid = newProduct, ctitle = producttitle, cinstock = 'In Stock', 
                    cartist = productauthoractorartist, cgenre = productgenre, 
                    cstarrating = productrating)
                newCD.save()
            elif productmediatype == 'D':
                newDVD = DVDs(did = newProduct, dtitle = producttitle, dinstock = 'In Stock', 
                    dactor = productauthoractorartist, dgenre = productgenre, 
                    dstarrating = productrating)
                newDVD.save()
            elif productmediatype == 'R':
                newRecord = Records(rid = newProduct, rtitle = producttitle, rinstok = 'In Stock', 
                    rartist = productauthoractorartist, rgenre = productgenre, 
                    rstarrating = productrating)
                newRecord.save()
            else:
                newBook = Books(bid = newProduct, btitle = producttitle, binstok = 'In Stock', 
                    bauthor = productauthoractorartist, bgenre = productgenre, 
                    bstarrating = productrating)
                newBook.save()
            return redirect ('products')
        # presetcategories = ['B', 'C', 'D', 'R']
        # form = SearchForm(request.POST)
        # if form.is_valid():
        #     querystring = form.cleaned_data['querystring']
        #     categories = form.cleaned_data['category']

        #     for i in categories:
        #         if i == 'B':
        #             books1 = Books.objects.filter(btitle__contains= querystring)
        #             books2 = Books.objects.filter(bauthor__contains= querystring)
        #             books = list(chain(books1, books2))
        #             for i in books:
        #                 print("Title: {}, Author: {}, Price: ${}".format(i.btitle, i.bauthor, i.bid.pprice))
                        
        #         elif i == 'C':
        #             cds1 = CDs.objects.filter(ctitle__contains= querystring)
        #             cds2 = CDs.objects.filter(cartist__contains= querystring)
        #             cds = list(chain(cds1, cds2))
        #             for i in cds:
        #                 print("Title: {}, Artist: {}, Price: ${}".format(i.ctitle, i.cartist, i.cid.pprice))
                
        #         elif i == 'D':
        #             dvds1 = DVDs.objects.filter(dtitle__contains= querystring)
        #             dvds2 = DVDs.objects.filter(dactor__contains= querystring)
        #             dvds = list(chain(dvds1, dvds2))
        #             for i in dvds:
        #                 print("Title: {}, Actor: {}, Price: ${}".format(i.dtitle, i.dactor, i.did.pprice))
                
        #         elif i == 'R':
        #             records1 = Records.objects.filter(rtitle__contains= querystring)
        #             records2 = Records.objects.filter(rartist__contains= querystring)
        #             records = list(chain(records1, records2))            
        #             for i in records:
        #                 print("Title: {}, Artist: {}, Price: ${}".format(i.rtitle, i.rartist, i.rid.pprice))
            
    else:
        template = loader.get_template('accounts/addprod.html')
        context = {}
        context['form'] = NewProduct()
        return HttpResponse(template.render(context, request))

