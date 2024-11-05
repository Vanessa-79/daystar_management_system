from django.forms import ModelForm
from .models import *
from django import forms


class LogoutForm(forms.Form):
    confirm_logout = forms.BooleanField(label='Are you sure you want to logout?', required=True)

    
class AddBabie(ModelForm):
    
    class Meta:
        model = Babie_registration
        fields = '__all__'
        widgets = {
            'Arrival_Time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }



class AddSitter(ModelForm):
    class Meta:
        model = Sitter_registration
        fields = '__all__'
        widgets = {
            'Date_of_birth': forms.DateInput(attrs={'type': 'date'})  # Use DateInput widget for date picker
        }
    
    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        self.fields['location'].disabled = True




class BabyDepartureForm(forms.ModelForm):
    class Meta:
        model = Baby_departure
        fields = ['baby_name', 'departure_time', 'person_taking_baby', 'comment']
        widgets = {
            'departure_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


#PAYMENTS


class BabyPaymentForm(forms.ModelForm):
    class Meta:
        model = BabyPayment
        fields = ['name', 'payment_date', 'full_day', 'half_day', 'monthly', 'total_amount_due', 'amount_paid', 'remaining_balance']


        
class AddPayment(ModelForm):
    class Meta:
        model = BabyPayment
        fields = '__all__'

class SitterArrivalForm(forms.ModelForm):
    class Meta:
        model = Arrivalsitter
        fields = ['Sitter_name', 'Arrival_Date', 'Assigned_Babies', 'Status']  # Include the 'Assigned_Babies' field in the form

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate the choices for the 'Assigned_Babies' field with the available baby names
        self.fields['Assigned_Babies'].queryset = Babie_registration.objects.all()
        
class SitterPaymentForm(ModelForm):
    class Meta:
        model = SitterPayment
        fields = '__all__'  


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['amount_paid'].disabled = True

#procurement
class AddItem(forms.ModelForm):
    class Meta:
        model = Procurement
        fields = ['item_name', 'quantity',  'Total_amount', 'Date_of_purchase']

class OutStock(forms.ModelForm):
    class Meta:
        model = Issueout
        fields = '__all__'
    

class InStock(forms.ModelForm):
    class Meta:
        model = Procurement
        fields = ['quantity_received']


    #dolls
class AddDoll(forms.ModelForm):
    class Meta:
        model = Stock
        fields = [ 'recieved_quantity']


class DollForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['item_name','total_quantity', 'unit_price', 'doll_image']



class SellDoll(forms.ModelForm):
    class Meta:
        model = Sellingdoll
        fields = ['sold_quantity','unit_price', 'issued_to', ]

