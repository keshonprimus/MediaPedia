from django.forms import ModelForm, TextInput, EmailInput,NumberInput, PasswordInput, Select
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms 
from .models import Employee, Products


ROLES = [
('M', 'MANAGER'),
('S', 'SUPERVISOR'),
('C', 'CLERK'),
('R', 'RETAIL'),
]

CATEGORIES = [
    ('C', 'CD'),
    ('D', 'DVD'),
    ('R', 'RECORD'),
    ('B', 'BOOK'),
]

MOVIE_GENRES = []
CD_RECORD_GENRES = []
BOOK_GENRES = []

class RegistrationForm(forms.ModelForm):
    employeeid = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Employee ID', 'style': 'width: 320px;', 'class': 'form-control'}),label= '', required= True)
    firstName = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name', 'style': 'width: 320px;', 'class': 'form-control'}),label= '', max_length= 20, required= True)
    lastName = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'style': 'width: 320px;', 'class': 'form-control'}),label= '', max_length= 20, required= True)
    phoneNumber = forms.IntegerField(label= '', required= True, widget = forms.TextInput(attrs={'placeholder': 'Phone Number', 'style': 'width: 320px;', 'class': 'form-control'}))
    email = forms.EmailField(label= '', required= True, widget=forms.EmailInput(attrs={'placeholder': 'Email','style':'width:320px;','class':'form-control'}))
    password = forms.CharField(label='', max_length=20, required= True, widget=forms.PasswordInput(attrs={'placeholder':'Password', 'style':'width:320px;', 'class':'form-control'}))
    whatRoleAreYou = forms.CharField(label= '', widget= forms.Select(choices= ROLES, attrs={'placeholder':'Role', 'style':'width:320px;', 'class': 'form-control'}))
    
    class Meta:
        model = Employee
        fields = ['employeeid','firstName','lastName','phoneNumber','email','password','whatRoleAreYou']

#not used       
class ProductForm(ModelForm):
    class Meta:
        model = Products
        fields = '__all__'
      
        

class LogInForm(forms.Form):
    employeeid = forms.IntegerField(label= '', required= True, widget=forms.TextInput(attrs={'placeholder': 'Employee ID', 'style': 'width: 320px;', 'class': 'form-control'}))
    password = forms.CharField(label='', max_length=20, required=True, widget=forms.PasswordInput(attrs={'placeholder':'Password', 'style':'width:320px;', 'class':'form-control'}))


class UpdateEmployee(ModelForm):
    #firstName = forms.CharField(label= 'newfirstName', max_length= 20)
    #lastName = forms.CharField(label= 'newlastName', max_length= 20)
    #phoneNumber = forms.IntegerField(label= 'newphoneNumber')
    #email = forms.EmailField(label= 'newemail')
    #whatRoleAreYou = forms.CharField(label= 'newrole', widget= forms.Select(choices= ROLES))
    class Meta:
        model = Employee
        #fields = '__all__'
        fields = ['employeeEmail','employeePhone','employeeFirstName','employeeLastName','employeePassword']
        widgets= {
            'employeeEmail' : forms.EmailInput(attrs={'placeholder': 'Email', 'style': 'width: 320px;', 'class': 'form-control'}),
            'employeePhone' : forms.TextInput(attrs={'placeholder': 'PhoNe Number', 'style': 'width: 320px;', 'class': 'form-control'}),
            'employeeFirstName': forms.TextInput(attrs={'placeholder': 'First Name', 'style': 'width:320px;', 'class':'form-control'}),
            'employeeLastName': forms.TextInput(attrs={'placeholder': 'Last Name', 'style': 'width:320px;', 'class':'form-control'}),
            'employeePassword' : forms.PasswordInput(attrs= {'placeholder':'Password','style':'width:320px;', 'class': 'form-control'})
        }
        labels = {
            'employeeEmail' : ('Email'),
            'employeePhone' : ('Phone Number'),
            'employeeFirstName': ('First Name'),
            'employeeLastName': ('Last Name'),
            'employeePassword': ('Password'),
        }
    

class NewProduct(forms.Form):
    productID = forms.CharField(label= '', max_length= 5, required=True, widget=forms.TextInput(attrs={'placeholder':'Product ID', 'style':'width:320px;', 'class':'form-control'}))
    productMediaType = forms.CharField(label= '', widget= forms.Select(choices=CATEGORIES, attrs={'placeholder': 'Media Type', 'style':'width:320px;', 'class':'form-control'}), required=True)
    productPrice = forms.IntegerField(label= '', required=True, widget=forms.NumberInput(attrs={'placeholder':'Product Price', 'style':'width:320px;', 'class':'form-control'}))
    productGenre = forms.CharField(label= '', max_length= 255, widget=forms.TextInput(attrs={'placeholder':'Genre', 'style':'width:320px;', 'class':'form-control'}))
    productQuantity = forms.IntegerField(label= '', required=True, widget=forms.NumberInput(attrs={'placeholder':'Quantity', 'style':'width:320px;', 'class':'form-control'}))
    productTitle = forms.CharField(label= '', max_length= 255, required=True, widget=forms.TextInput(attrs={'placeholder':'Title', 'style':'width:320px;', 'class':'form-control'}))
    productRating = forms.IntegerField(label= '', widget=forms.NumberInput(attrs={'placeholder':'Rating', 'style':'width:320px;', 'class':'form-control'}))
    productauthoractorartist = forms.CharField(label='',max_length= 500, widget=forms.TextInput(attrs={'placeholder':'Author/Artist/Actor','style':'width:320px;', 'class':'form-control'}))

class DeleteProduct(forms.Form):
    productID = forms.CharField(label= 'Product ID', max_length=5)


class DeleteEmployee(forms.Form):
    employeeID = forms.CharField(max_length= 5, label= 'Employee ID')

#can possibly be deleted if the updateProduct view does not require it
class UpdateProduct(ModelForm):
    #productMediaType = forms.CharField(label= 'Media Type', widget= forms.Select(choices=CATEGORIES))
    #productPrice = forms.IntegerField(label= 'Product Price')
    #productGenre = forms.CharField(label= 'Genre', max_length= 255)
    #productTitle = forms.CharField(label= 'Title', max_length= 255)
    #productRating = forms.IntegerField(label= 'Rating')

    class Meta:
        model = Products
        fields = '__all__'
    #    fields = ['pmediatype', 'pprice', 'pquantity','pamountsold']
        widgets= {
            'pid' : forms.TextInput(attrs={'placeholder': 'Product ID', 'style': 'width: 320px;', 'class': 'form-control'}),
            'pmediatype' : forms.TextInput(attrs={'placeholder': 'Media Type', 'style': 'width: 320px;', 'class': 'form-control'}),
            'pprice': forms.TextInput(attrs={'placeholder': 'Price', 'style': 'width:320px;', 'class':'form-control'}),
            'pquantity': forms.TextInput(attrs={'placeholder': 'Quantity', 'style': 'width:320px;', 'class':'form-control'}),
            'pamountsold' : forms.TextInput(attrs= {'placeholder':'Amount Sold','style':'width:320px;', 'class': 'form-control'})
        }
        labels = {
            'pid' : ('Product ID'),
            'pmediatype' : ('Media Type'),
            'pprice': ('Price'),
            'pquantity': ('Quantity'),
            'pamountsold': ('Amount Sold'),
        }

 #new       

#not used
class SearchForm(forms.Form):
    querystring = forms.CharField(label= 'Search', max_length= 50)
    category = forms.MultipleChoiceField(widget= forms.CheckboxSelectMultiple, choices=CATEGORIES)


#class LoginForm(forms.Form):
#    employeeid = forms.IntegerField(label= 'employeeID', required= True)
#    password = forms.CharField(widget=forms.PasswordInput)