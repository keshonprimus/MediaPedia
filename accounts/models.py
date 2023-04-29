from django.db import models
from django import forms
from django.forms import TextInput, EmailInput,NumberInput, PasswordInput, Widget

ROLES = (
('MANAGER', 'M'),
('SUPERVISOR', 'S'),
('CLERK', 'C'),
('RETAIL', 'R'),
)



# Create your models here.
class Roles(models.Model):
    role = models.CharField(primary_key=True, max_length= 1)
    privilege = models.CharField(max_length= 2) 

class Employee(models.Model):
    employeeID = models.IntegerField(primary_key=True)
    employeeEmail = models.EmailField(null= False)
    employeePhone = models.CharField(max_length= 15, null=True)
    employeeFirstName = models.CharField(max_length= 20)
    employeeLastName = models.CharField(max_length= 20)
    employeePassword = models.CharField(max_length= 500)
    employeeRole_id = models.ForeignKey(Roles, on_delete=models.RESTRICT, db_column= 'employeeRole_id')
    sessionID = models.CharField(max_length=128, null=True, unique=True)

    def __str__(self):
        return self.employeeFirstName


    
class Products(models.Model):
    pid = models.CharField(primary_key=True, max_length=5)
    pmediatype = models.CharField(max_length=1, null= False)
    pprice = models.DecimalField(max_digits=5, decimal_places=2)
    pquantity = models.IntegerField(default=0)
    pamountsold = models.IntegerField(default=0)

    def __str__(self):
        return self.pid #change

    
class Books(models.Model):
    bid = models.ForeignKey(Products, on_delete=models.CASCADE, primary_key= True, db_column= 'bid')
    btitle = models.CharField(max_length= 500)
    bauthor = models.CharField(max_length= 500)
    bgenre = models.CharField(max_length=500, null= False)
    bstarrating = models.FloatField(default = 0.00)
    binstock = models.CharField(max_length= 15)
    
class DVDs(models.Model):
    did = models.ForeignKey(Products, on_delete=models.CASCADE, primary_key=True, db_column= 'did')
    dtitle = models.CharField(max_length= 500)
    dactor = models.CharField(max_length=500)
    dgenre = models.CharField(max_length=500, null= False)
    dstarrating = models.FloatField(default = 0.00)
    dinstock = models.CharField(max_length= 15)
    
class CDs(models.Model):
    cid = models.ForeignKey(Products, on_delete=models.CASCADE, primary_key=True, db_column= 'cid')
    ctitle = models.CharField(max_length= 500)
    cartist = models.CharField(max_length=500)
    cgenre = models.CharField(max_length=500, null= False)
    cstarrating = models.FloatField(default = 0.00)
    cinstock = models.CharField(max_length= 15)

class Records(models.Model):
    rid = models.ForeignKey(Products, on_delete=models.CASCADE, primary_key=True, db_column= 'rid')
    rtitle = models.CharField(max_length= 500)
    rartist = models.CharField(max_length= 500)
    rgenre = models.CharField(max_length= 500, null= False)
    rstarrating = models.FloatField(default = 0.00)
    rinstock = models.CharField(max_length= 15)