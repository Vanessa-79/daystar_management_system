from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
from .models import *
from django.template import loader
from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from datetime import *



# Create your views here.


#forms

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.GET.get('next', 'dashboard'))  # Redirect to the next parameter if available, else to dashboard
        else:
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})
    else:
        return render(request, 'login.html')


def logout_view(request):
    if request.method == 'POST':
        form = LogoutForm(request.POST)
        if form.is_valid() and form.cleaned_data['confirm_logout']:
            logout(request)
            return redirect('index')
    else:
        form = LogoutForm()
    
    return render(request, 'logout.html', {'form': form})

def Index(request):
    return render(request, 'index.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

def base(request):
    return render(request, 'base.html')


@login_required
def home(request):
    count_sitters = Sitter_registration.objects.count()
    count_babies = Babie_registration.objects.count()
    count_departure = Baby_departure.objects.count()
    count_arrival = Arrivalsitter.objects.filter(Arrival_Date=date.today()).count()
    context = {
        "count_sitters": count_sitters,
        "count_babies": count_babies,
        "count_departure": count_departure,
        "count_arrival": count_arrival,
        "data" : {'attended sitters': count_arrival , 'not attended sitters': count_sitters - count_arrival},
    }
    template = loader.get_template("home.html")
    return HttpResponse(template.render(context))


#Babie views(forms)
@login_required
def Babie(request):
    if request.method == 'POST':
        getbabieform  = AddBabie(request.POST)
        if getbabieform.is_valid():
            getbabieform.save()
            messages.success(request, 'Baby added successfully')
            return redirect('/baby_list')
    else:
        getbabieform = AddBabie()
    return render(request, 'babie.html', {'getbabieform': getbabieform})


@login_required
def baby_departure(request):
    if request.method == 'POST':
        form = BabyDepartureForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Baby signed out successfully')
            return redirect('baby_departure') 
        else:
            messages.error(request, 'Form submission failed. Please correct the errors.')
    else:
        form = BabyDepartureForm()
    return render(request, 'baby_departure.html', {'form': form})
@login_required
def signinbaby(request):
    signinbaby = Arrivalbaby.objects.all()
    return render(request, 'baby_signedin.html', {'signinbaby': signinbaby})

 #sitter views (forms)  
@login_required
def Sitter(request):
    if request.method == 'POST':
        getsitterform  = AddSitter(request.POST)
        if getsitterform.is_valid():
            getsitterform.save()
            messages.success(request, 'Baby added successfully')
            return redirect('/sitter')
    else:
        getsitterform = AddSitter()
    return render(request, 'sitter.html', {'getsitterform': getsitterform})
    




#tables(sitters)
@login_required
def sitters_list(request):
    sitters_list = Sitter_registration.objects.all()
    return render(request, 'sitters_list.html', {'sitters_list': sitters_list})


@login_required
def sitter_view(request, id):
    sitter_view = Sitter_registration.objects.get(pk=id)
    return render(request, 'sitter_view.html', {'sitter_view': sitter_view})

@login_required
def sitter_edit(request, id):
    if request.method == 'POST':
        sitter_edit = Sitter_registration.objects.get(pk=id)
        form = AddSitter(request.POST, instance=sitter_edit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sitter updated successfully.')
            return redirect('sitters_list')
    else:
        sitter_edit = Sitter_registration.objects.get(pk=id)
        form = AddSitter(instance=sitter_edit)
    return render(request, 'sitter_edit.html', {'form': form})

@login_required
def sitter_delete(request, id):
    sitter = get_object_or_404(Sitter_registration, pk=id)
    if request.method == 'POST':
        sitter.delete()
        messages.success(request, 'Sitter deleted successfully.')
        return redirect('sitters_list')
    return render(request, 'sitter_delete.html', {'sitter': sitter})

@login_required
def sitter_arrival(request):
    if request.method == 'POST':
        form = SitterArrivalForm(request.POST)
        if form.is_valid():
            sitter_arrival = form.save(commit=False)
            sitter_arrival.save()
            form.save_m2m()
            sitter_arrival.calculate_total_babies()

            messages.success(request, 'Attendance successful')
            return redirect('/sitterarrival')
    else:
        form = SitterArrivalForm()
    return render(request, 'sitterarrival.html', {'form': form})

@login_required
def sitter_arrival_list(request):
    sitter_arrival_list = Arrivalsitter.objects.prefetch_related('Assigned_Babies').all()
    print(sitter_arrival_list)  # Add this line for debugging
    return render(request, 'sitter_arrival_list.html', {'sitter_arrival_list': sitter_arrival_list})
   
#tables(babies)
@login_required
def baby_list(request):
    babies = Babie_registration.objects.all()
    if 'filter' in request.GET:
        filter_value = request.GET['filter']
        babies = babies.filter( )
    return render(request, 'baby_list.html', {'baby_list': babies})

@login_required
def add_baby(request):
    if request.method == 'POST':
        form = AddBabie(request.POST)
        if form.is_valid():
            form.save()
            return redirect('baby_list')
    else:
        form = AddBabie()
    return render(request, 'add_baby.html', {'form': form})

@login_required
def edit_baby(request, baby_id):
    if request.method == 'POST':
        edit_baby = Babie_registration.objects.get(pk=baby_id)
        form = AddBabie(request.POST, instance=edit_baby)
        if form.is_valid():
            form.save()
            messages.success(request, 'Baby updated successfully.')
            return redirect('baby_list')
    else:
        edit_baby = Babie_registration.objects.get(pk=baby_id)
        form = AddBabie(instance=edit_baby)
    return render(request, 'edit_baby.html', {'form': form })

@login_required
def view_baby(request):
    view_baby = Babie_registration.objects.all()
    return render(request, 'view_baby.html', {'view_baby': view_baby})

@login_required
def babyupdate(request):
    babyupdate = Babie_registration.objects.all()
    return render(request, 'babyupdate.html', {'babyupdate': babyupdate})

@login_required
def baby_signedoutlist(request):
    baby_signedoutlist = Baby_departure.objects.all()
    return render(request, 'baby_signedoutlist.html', {'baby_signedoutlist': baby_signedoutlist})

@login_required
def delete_baby(request, baby_id):
    baby = get_object_or_404(Babie_registration, id=baby_id)
    if request.method == 'POST':
        baby.delete()
        return redirect('baby_list')
    return render(request, 'confirmation_delete.html', {'baby': baby})



#payments

# @login_required
# def payment_baby(request):
#     if request.method == 'POST':
#         form = AddPayment(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('payment_list')  
#         else:
#             print(form.errors)
#     else:
#         form = AddPayment()
#     return render(request, 'payment_baby.html', {'form': form})



@login_required
def payment_baby(request):
    if request.method == 'POST':
        # Extract data from the POST request
        name = request.POST.get('name')
        payment_date = request.POST.get('date')
        full_day = request.POST.get('full_day') == 'on'  # Convert checkbox value to boolean
        half_day = request.POST.get('half_day') == 'on'  # Convert checkbox value to boolean
        monthly = request.POST.get('monthly') == 'on'  # Convert checkbox value to boolean
        total_amount_due = request.POST.get('total_amount')
        amount_paid = request.POST.get('amount_paid')
        remaining_balance = request.POST.get('remaining_balance')

        # Create a new BabyPayment instance
        payment = BabyPayment(
            name=name,
            payment_date=payment_date,
            full_day=full_day,
            half_day=half_day,
            monthly=monthly,
            total_amount_due=total_amount_due,
            amount_paid=amount_paid,
            remaining_balance=remaining_balance
        )
        
        # Save the instance to the database
        payment.save()

        # Redirect to a new page to prevent form resubmission
        return redirect('payment_list')
    else:
        return render(request, 'payment_baby.html')
@login_required
def payment_list(request):
    payment_list = BabyPayment.objects.all()
    return render(request, 'paymentbaby_list.html', {'payment_list': payment_list})


@login_required
def payment_edit(request, id):
    if request.method == 'POST':
        payment = get_object_or_404(BabyPayment, pk=id)
        form = AddPayment(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Payment updated successfully.')
            return redirect('payment_list')
    else:
        payment = get_object_or_404(BabyPayment, pk=id)
        form = AddPayment(instance=payment)
    return render(request, 'payment_edit.html', {'form': form })


#sitterpayement

def paymentsitter(request):
    if request.method == 'POST':
        form = SitterPaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('paymentsitter_list')  # Redirect to the payment list view
        else:
            print(form.errors)
    else:
        form = SitterPaymentForm()
    return render(request, 'paymentsitter.html', {'form': form})

def paymentsitter_list(request):
    payment_list = SitterPayment.objects.all()
    return render(request, 'paymentsitterlist.html', {'payment_list': payment_list})



    
#procurement
@login_required
def issue_item(request):
    if request.method == 'POST':
        form  = SellDoll(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stock added successfully')
            return redirect('issue_item')
    else:
        form = SellDoll()
    return render(request, 'issue_item.html', {'form': form})


@login_required
def procurement(request):
    if request.method == 'POST':
        form = AddItem(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item added successfully')
            return redirect('item_list')
    else:
        form = AddItem()
    return render(request, 'procurement.html', {'form': form})


@login_required
def item_list(request):
    item_list = Procurement.objects.all()
    return render(request, 'item_list.html', {'item_list': item_list})

@login_required
def issued_out(request, pk):
    issued_item = get_object_or_404(Procurement, pk=pk)
    form = OutStock(request.POST)
        
    if request.method == 'POST':
        
        if form.is_valid():
            new_issue = form.save(commit=False)
            new_issue.item_name = issued_item
            new_issue.save()
            issued_quantity = int(request.POST.get('quantity_issued_out'))  # Corrected access of POST data
            issued_item.quantity -= issued_quantity
            issued_item.save()
            print(request.POST.get('quantity_issued_out'))  # Corrected access of POST data
            print(issued_item.quantity)
            messages.success(request, 'Stock issued out successfully')
            return redirect('item_list') 
    else:
        form = OutStock()
    return render(request, 'issue_out.html', {'form': form, 'issued_item': issued_item})

@login_required
def issued_in(request, pk):
    issued_procurement = Procurement.objects.get(id=pk)
    
    if request.method == 'POST':
        form = InStock(request.POST)
        if form.is_valid():
            received_quantity = form.cleaned_data.get('quantity_received')
            added_quantity = int(received_quantity) 
            issued_procurement.quantity += added_quantity

            issued_procurement.save()
            return redirect('item_list')  
    else:
        form = InStock()
    return render(request, 'issue_item.html', {'form': form})


#dolls
@login_required
def doll_stock(request):
    products = Stock.objects.all().order_by('-id')
    return render(request, 'doll_stock.html')


@login_required
def add_doll(request):
    issued_item = Stock.objects.get()
    form = AddDoll(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            added_quantity = form.cleaned_data['recieved_quantity']
            issued_item.total_quantity += added_quantity
            issued_item.save()
            form.save()
            messages.success(request, 'Stock added successfully')
            return redirect('doll_stock')
    return render(request, 'dolladd.html', {'form': form})

def dollsale(request, pk):
    product = get_object_or_404(Stock, pk=pk)
    if request.method == 'POST':
        form = SellDoll(request.POST)
        if form.is_valid():
            sold_quantity = form.cleaned_data['sold_quantity']
            if sold_quantity is None:
                # Handle the case where sold_quantity is None (e.g., not filled out in the form)
                messages.error(request, 'Please provide a valid quantity.')
            elif sold_quantity > product.total_quantity:
                messages.error(request, 'Insufficient quantity available.')
            else:
                # Ensure sold_quantity is converted to an integer
                sold_quantity = int(sold_quantity)
                product.total_quantity -= sold_quantity
                product.save()
                # Logic for selling dolls goes here
                messages.success(request, 'Stock sold successfully')
                return redirect('doll_stock')
    else:
        form = SellDoll()
    return render(request, 'dollsale.html', {'form': form, 'product': product})
