from django.db import models
from django.utils import timezone
from django.db.models import Count
from django.contrib.auth.models import User
import datetime
import re
from django.core.exceptions import ValidationError

# Create your models here.

def validate_letters(value):
    if not re.match("^([a-zA-Z]+\s)*[a-zA-Z]+$", value):
        raise ValidationError("Only letters are allowed.")
def validate_numbers(value):
    if not re.match("^[0-9]*$", value):
        raise ValidationError("Only numbers are allowed.")

def validate_contacts(value):
    if len(value) != 10:
        raise ValidationError("Contact field must contain exactly 10 digits.")

def validate_NIN(value):
    if len(value) != 14:
        raise ValidationError("NIN field must contain exactly 14 digits.")


class Categorystay(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return self.name


class PaymentRate(models.Model):
    name = models.CharField(max_length=50, null=False,blank=True)
    def __str__(self):
        return self.name

class Babie_registration(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    #linking the categorystay to babe(making a foreign key)
    Baby_Name = models.CharField(max_length=200, validators=[validate_letters])
    Baby_No = models.CharField( max_length=200,unique=True, null=True, blank=False)
    Period_of_stay = models.ForeignKey(Categorystay, on_delete=models.CASCADE)
    Age = models.IntegerField(default=0)
    Gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    Location = models.CharField(max_length=80)
    Parent_name = models.CharField(max_length=100, validators=[validate_letters])   
    Brought_by = models.CharField(max_length=200, validators=[validate_letters])
    Arrival_Date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def has_sitter_assigned(self):
        return self.arrivalsitter_set.exists()
    def __str__(self):
        return self.Baby_Name


class Sitter_registration(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    Name = models.CharField(max_length=200, validators=[validate_letters])
    Sitter_No = models.CharField(max_length=500, unique=True, null=True, blank=False)
    Sitter_Contact = models.CharField(max_length=10, validators=[validate_contacts])
    Location = models.CharField(max_length=10, default= 'Kabalagala')
    Date_of_birth = models.DateField()
    Gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    Next_of_kin = models.CharField(max_length=100, validators=[validate_letters])
    NIN = models.CharField(max_length=14, validators=[validate_NIN])
    Recommenders_name = models.CharField(max_length=200, validators=[validate_letters])
    Recommenders_contact = models.CharField(max_length=10, validators=[validate_contacts])
    Religion = models.CharField(max_length=20, null=True, blank=True,  verbose_name="Religion (Optional)")
    Level_of_education = models.CharField(max_length=100, choices=( 
        ('Certificate', 'Certificate'),
        ('Diploma', 'Diploma'),
        ('Degree', 'Degree'),
        ('Other', 'Other')))
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.Name



class Arrivalsitter(models.Model):
    Sitter_name = models.ForeignKey(Sitter_registration, on_delete=models.CASCADE, null=True, blank=True)
    Sitter_Number = models.CharField(max_length=200, default=0)
    Arrival_Date = models.DateTimeField(default=timezone.now)
    Arrival_Time = models.TimeField(null=True, blank=True)
    Assigned_Babies = models.ManyToManyField(Babie_registration, blank=True)  # Changed to ManyToManyField
    Status = models.CharField(max_length=10)

    def calculate_total_babies(self):
        return self.Assigned_Babies.count() 
    
    def __str__(self):
        return str(self.Sitter_name)

class SitterPayment(models.Model):
    sitter = models.ForeignKey(Arrivalsitter, on_delete=models.CASCADE)
    payment_date = models.DateField(default=timezone.now)
    babies_attended = models.PositiveIntegerField(default=0)  # Field to store the total number of babies attended
    amount_paid = models.IntegerField(default=3000)


    def __str__(self):
        return str(self.sitter)


    def total_amount(self):
        amount = self.babies_attended * self.amount_paid
        return int(amount)
   

#babiePayments
class Baby_departure(models.Model):
    baby_name = models.ForeignKey(Babie_registration, on_delete=models.CASCADE, null=True, blank=True)
    departure_time = models.DateTimeField()
    person_taking_baby = models.CharField(max_length=100, validators=[validate_letters])
    comment = models.TextField(blank=True, verbose_name= "Comment (Optional)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.baby_name)


class BabyPayment(models.Model):
    name = models.CharField(max_length=100)
    payment_date = models.DateField()
    full_day = models.BooleanField(default=False, blank=True)
    half_day = models.BooleanField(default=False,blank=True)
    monthly = models.BooleanField(default=False, blank=True)
    total_amount_due = models.DecimalField(max_digits=10, decimal_places=2,blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_balance = models.DecimalField(max_digits=10, decimal_places=2,default=False,blank=True)
    is_complete = models.BooleanField(default=False) 
    def is_complete(self):
        return self.amount_paid == self.total_amount_due

    def __str__(self):
        return self.name


class Procurement(models.Model):
    item_name = models.CharField(max_length=100, choices=( 
        ('Fruits', 'Fruits'),
        ('Diapers', 'Diapers'),
        ('Milk', 'Milk'),
        ('Toys', 'Toys')))
    quantity = models.IntegerField(default=0, null=True, blank=True)
    quantity_received = models.IntegerField(default=0, null=True, blank=True)
    Total_amount = models.IntegerField(default=0, null=True, blank=True)
    Date_of_purchase = models.DateField(default=timezone.now())
    quantity_issued_out = models.IntegerField(default=0, null=True, blank=True)
    stock_at_hand = models.IntegerField(default=0, null=True, blank=True)
    
def total_quantity(self):
    total = self.quantity + self.quantity_received
    return total


    def __str__(self):
        return self.item_name

    
class Issueout(models.Model):
    quantity_issued_out = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return int(self.quantity_issued_out)





       
#Dolls  
class Stock(models.Model):
    item_name = models.CharField(max_length=100, null=True, blank=True)
    total_quantity = models.IntegerField(default=0, null=True, blank=True)
    recieved_quantity = models.IntegerField(default=0, null=True, blank=True)
    unit_price = models.IntegerField(default=0, null=True, blank=True)
    doll_image = models.ImageField(null=True, blank=True, upload_to='images/')

    def __str__(self):
        return self.item_name

class Sellingdoll(models.Model):
    item = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date = models.DateField(default=timezone.now())
    unit_price = models.IntegerField(default=0, null=True, blank=True)
    issued_to = models.ForeignKey(Babie_registration, on_delete=models.CASCADE, null=True, blank=True)
    sold_quantity = models.IntegerField(default=0, null=True, blank=True)
    # unit_price = models.IntegerField(default=0, null=True, blank=True)

    def gettotal_amount(self):
        total= self.quantity * self.item.unit_price
        return int(total)

    def balance(self):
        balance = self.gettotal_amount() - self.amount_received
        return abs(int(balance))

    def __str__(self):
        return self.item.item_name



    







