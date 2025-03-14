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
from django.utils import timezone
from django.db.models import Q
from django.db.models import Sum
from django.db.models.functions import TruncDate, TruncMonth
from django.contrib.auth.models import User
from django.views.decorators.csrf import ensure_csrf_cookie


# Create your views here.


# forms

@ensure_csrf_cookie
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password')
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


def index(request):
    return render(request, 'index.html')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def base(request):
    return render(request, 'base.html')


@login_required
def home(request):
    today = timezone.now().date()
    
    # Count queries
    count_sitters = Sitter_registration.objects.count()
    
    count_babies_signed_out = Baby_departure.objects.filter(
        created_at__date=today
    ).count()
    
    count_sitters_signed_in = Arrivalsitter.objects.filter(
        Arrival_Date__date=today
    ).count()
    
    count_babies_registered = Babie_registration.objects.filter(
        Arrival_Date=today
    ).count()
    
    count_babies_total = count_babies_registered - count_babies_signed_out

    # Chart data
    stock_data = {}
    items = Stock.objects.all()
    
    for item in items:
        try:
            dates = (
                Sellingdoll.objects.filter(item=item)
                .values('date')
                .annotate(quantity=Sum('sold_quantity'))
                .order_by('date')
            )
            
            formatted_dates = []
            quantities = []
            for d in dates:
                if d['date']:
                    formatted_dates.append(d['date'].strftime('%Y-%m-%d'))
                    quantities.append(d['quantity'] or 0)
            
            stock_data[item.item_name] = quantities
        except Exception as e:
            print(f"Error processing item {item.item_name}: {str(e)}")
            stock_data[item.item_name] = []

    # Chart configurations
    data_colors = {
        "tooltip": {"pointFormat": "{series.name}: <br>{point.percentage:.1f} %"},
        "plotOptions": {
            "pie": {
                "colors": ["#4764ae", "#3f528e"],
                "dataLabels": {
                    "enabled": True,
                    "format": "<b>{point.name}</b>:<br>{point.percentage:.1f} %",
                },
            }
        },
    }

    baby_colors = data_colors.copy()

    line_chart_options = {
        "title": "Stock Management Overview",
        "yAxis": {"title": {"text": "Total Stock"}},
        "xAxis": {"title": {"text": "Items"}},
        "series": [
            {"name": item_name, "data": quantities}
            for item_name, quantities in stock_data.items()
        ],
    }

    context = {
        "count_sitters": count_sitters,
        "count_babies": count_babies_total,
        "count_babies_signed_out": count_babies_signed_out,
        "count_sitters_signed_in": count_sitters_signed_in,
        "data": {
            "Registered Sitters": count_sitters,
            "Signed In Sitters": count_sitters_signed_in,
        },
        "baby": {
            "Attended Babies": count_babies_total,
            "Signed Out Babies": count_babies_signed_out,
        },
        "data_colors": data_colors,
        "baby_colors": baby_colors,
        "stock_data": stock_data,
        "line_chart_options": line_chart_options,
    }

    return render(request, "home.html", context)


# Babie views(forms)
@login_required
def Babie(request):
    if request.method == 'POST':
        getbabieform = AddBabie(request.POST)
        if getbabieform.is_valid():
            getbabieform.save()
            messages.success(request, 'Baby added successfully')
            return redirect('/babie/')
    else:
        getbabieform = AddBabie()
    return render(request, 'baby.html', {'getbabieform': getbabieform})

@login_required
def baby_departure(request):
    if request.method == 'POST':
        form = BabyDepartureForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Baby signed out successfully')
            return redirect('/baby_departure/')
        else:
            messages.error(
                request, 'Form submission failed. Please correct the errors.')
    else:
        form = BabyDepartureForm()
    return render(request, 'baby_departure.html', {'form': form})


@login_required
def signinbaby(request):
    signinbaby = Arrivalbaby.objects.all()
    return render(request, 'baby_signedin.html', {'signinbaby': signinbaby})

# sitter views (forms)
@login_required
def Sitter(request):
    if request.method == 'POST':
        getsitterform = AddSitter(request.POST)
        if getsitterform.is_valid():
            getsitterform.save()
            messages.success(request, 'Sitter added successfully')
            return redirect('/sitter/')
        else:
            messages.error(
                request, 'Form submission failed. Please correct the errors.')
    else:
        getsitterform = AddSitter()
    return render(request, 'sitter.html', {'getsitterform': getsitterform})


# tables(sitters)
@login_required
def sitters_list(request):
    search_query = request.GET.get('search_query')
    gender_filter = request.GET.get('gender')

    sitters_list = Sitter_registration.objects.all()

    if search_query:
        sitters_list = sitters_list.filter(
            Q(Name__icontains=search_query) |
            Q(Sitter_No__icontains=search_query) |
            Q(Sitter_Contact__icontains=search_query) |
            Q(Religion__icontains=search_query) |
            Q(Location__icontains=search_query)
        )

    if gender_filter:
        # Use iexact for case-insensitive exact match
        sitters_list = sitters_list.filter(Gender__iexact=gender_filter)

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
def sitter_arrival_delete(request, sitter_id):
    sitter_arrival = get_object_or_404(Arrivalsitter, pk=sitter_id)
    if request.method == 'POST':
        sitter_arrival.delete()
        messages.success(
            request, 'Sitter deleted successfully from arrival list.')
        return redirect('/sitter_arrival_list/')
    return render(request, 'sitter_arrival_delete.html', {'sitter': sitter_arrival})


@login_required

def sitter_arrival(request):
    if request.method == 'POST':
        form = SitterArrivalForm(request.POST)
        if form.is_valid():
            sitter_arrival = form.save(commit=False)
            sitter_arrival.save()
            form.save_m2m()

            # Set the is_assigned attribute for each baby instance
            assigned_babies = form.cleaned_data['Assigned_Babies']
            for baby in assigned_babies:
                baby.is_assigned = True
                baby.save()

            messages.success(request, 'Attendance successful')
            return redirect('/sitter_arrival_list/')
    else:
        form = SitterArrivalForm()
    return render(request, 'sitterarrival.html', {'form': form})

@login_required
def sitter_arrival_list(request):
    search_query = request.GET.get('search_query')

    sitter_arrival_list = Arrivalsitter.objects.all()

    if search_query:
        sitter_arrival_list = sitter_arrival_list.filter(
            Q(Sitter_name__Name__icontains=search_query) |
            Q(Sitter_Number__icontains=search_query) |
            Q(Arrival_Date__icontains=search_query) |
            Q(Assigned_Babies__Baby_Name__icontains=search_query)

        )

    return render(request, 'sitter_arrival_list.html', {'sitter_arrival_list': sitter_arrival_list})


# tables(babies)
@login_required
def baby_list(request):
    search_query = request.GET.get('search_query')
    gender_filter = request.GET.get('gender')

    baby_list = Babie_registration.objects.all()

    if search_query:
        baby_list = baby_list.filter(
            Q(Baby_Name__icontains=search_query) |
            Q(Baby_No__icontains=search_query) |
            Q(Age__icontains=search_query) |
            Q(Gender__icontains=search_query) |
            Q(Period_of_stay__name__icontains=search_query)
        )

    if gender_filter:
        # Use iexact for case-insensitive exact match
        baby_list = baby_list.filter(Gender__iexact=gender_filter)

    return render(request, 'baby_list.html', {'baby_list': baby_list})


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
    return render(request, 'edit_baby.html', {'form': form})


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


@login_required
def payment_baby(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        payment_date = request.POST.get('date')
        full_day = request.POST.get('full_day')
        half_day = request.POST.get('half_day')
        monthly = request.POST.get('monthly')
        total_amount_due = request.POST.get('total_amount')
        amount_paid = request.POST.get('amount_paid')
        remaining_balance = request.POST.get('remaining_balance')

        # Convert checkboxes to boolean values
        full_day = True if full_day else False
        half_day = True if half_day else False
        monthly = True if monthly else False

        pay = BabyPayment(
            name=name,
            payment_date=payment_date,
            full_day=full_day,
            half_day=half_day,
            monthly=monthly,
            total_amount_due=total_amount_due,
            amount_paid=amount_paid,
            remaining_balance=remaining_balance
        )
        pay.save()
        return redirect('/payment_list/')
    else:
        return render(request, 'payment_baby.html')

@login_required
def payment_list(request):
    search_query = request.GET.get('search_query')

    payment_list = BabyPayment.objects.all()

    if search_query:
        if search_query.lower() in ['full day', 'half day', 'monthly', 'complete', 'pending']:
            if search_query.lower() == 'full day':
                payment_list = payment_list.filter(full_day=True)
            elif search_query.lower() == 'half day':
                payment_list = payment_list.filter(half_day=True)
            elif search_query.lower() == 'monthly':
                payment_list = payment_list.filter(monthly=True)
            elif search_query.lower() == 'complete':
                payment_list = payment_list.filter(status='complete')
            elif search_query.lower() == 'pending':
                payment_list = payment_list.filter(status='pending')
        else:
            payment_list = payment_list.filter(
                Q(name__icontains=search_query) |
                Q(payment_date__icontains=search_query) |
                Q(total_amount_due__icontains=search_query) |
                Q(amount_paid__icontains=search_query) |
                Q(remaining_balance__icontains=search_query)
            )

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
    return render(request, 'payment_edit.html', {'form': form})


def delete_payment(request, payment_id):
    if request.method == 'POST':
        payment_id = request.POST.get('payment_id')
        try:
            payment = BabyPayment.objects.get(pk=payment_id)
            payment.delete()
            messages.success(request, 'Payment deleted successfully.')
        except BabyPayment.DoesNotExist:
            messages.error(request, 'Payment not found.')
    return redirect('paymentbaby_list')

# sitterpayement


def paymentsitter(request):
    if request.method == 'POST':
        form = SitterPaymentForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to the payment list view
            return redirect('paymentsitter_list')
        else:
            print(form.errors)
    else:
        form = SitterPaymentForm()
    return render(request, 'paymentsitter.html', {'form': form})


def paymentsitter_list(request):
    payment_list = SitterPayment.objects.all()
    return render(request, 'paymentsitterlist.html', {'payment_list': payment_list})


# procurement
@login_required
def issue_item(request):
    if request.method == 'POST':
        form = SellDoll(request.POST)
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
            issued_quantity = int(request.POST.get('quantity_issued_out'))
            issued_item.quantity -= issued_quantity
            issued_item.save()
            print(request.POST.get('quantity_issued_out'))
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


# dolls
@login_required
def doll_stock(request):
    products = Stock.objects.all().order_by('-id')
    return render(request, 'doll_stock.html', {'products': products})

def add_doll(request):
    product_id = request.GET.get('product_id')
    if request.method == 'POST':
        form = AddDoll(request.POST)
        if form.is_valid():
            added_quantity = form.cleaned_data['recieved_quantity']
            if product_id:
                product = get_object_or_404(Stock, id=product_id)
                product.total_quantity += added_quantity
                product.save()
                messages.success(request, 'Stock added successfully')
                return redirect('doll_stock')
            else:
                messages.error(request, 'No product ID provided.')
        else:
            messages.error(request, 'Form is not valid')
    else:
        form = AddDoll()
    return render(request, 'dolladd.html', {'form': form, 'product_id': product_id})

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

                # Create a Sellingdoll instance to record the sale
                Sellingdoll.objects.create(item=product, quantity=sold_quantity, unit_price=form.cleaned_data[
                                           'unit_price'], issued_to=form.cleaned_data['issued_to'], sold_quantity=sold_quantity)

                # Logic for selling dolls
                messages.success(request, 'Stock sold successfully')
                return redirect('doll_sell_list')
    else:
        form = SellDoll()
    return render(request, 'dollsale.html', {'form': form, 'product': product})


def doll_delete(request, pk):
    stock_item = get_object_or_404(Stock, pk=pk)
    if request.method == 'POST':
        stock_item.delete()
        return redirect('doll_stock')
    return render(request, 'doll_delete.html', {'stock_item': stock_item})


def add_newdoll(request, pk):
    if request.method == 'POST':
        form = DollForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('doll_stock')
    else:
        form = DollForm()
    return render(request, 'dollnew.html', {'form': form})


@login_required
def update_doll(request, pk):
    # Retrieve the doll object
    item = get_object_or_404(Stock, pk=pk)
    if request.method == 'POST':
        form = DollForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('doll_stock')
    else:
        form = DollForm(instance=item)
    return render(request, 'doll_update.html', {'form': form})


def doll_sell_list(request):
    doll_sales = Sellingdoll.objects.all()
    for sale in doll_sales:
        sale.total_amount = sale.quantity * sale.item.unit_price

    return render(request, 'doll_sell_list.html', {'doll_sales': doll_sales})


def receipt(request, pk):
    sale = get_object_or_404(Sellingdoll, pk=pk)
    return render(request, 'dollreciept.html', {'sale': sale})

def create_admin(request):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        return HttpResponse("Admin user created successfully!")
    return HttpResponse("Admin user already exists!")
