from decouple import config
from django.http.response import JsonResponse
from django.urls import reverse
from django.contrib.auth import logout
from django.shortcuts import render
from decimal import Decimal
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from requests.api import get
from .models import User, Bus, Book
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django_daraja.mpesa.core import MpesaClient
import requests
from requests.auth import HTTPBasicAuth
import json
import re

# Create your views here.

# def index(request):
#      return render(request, 'index.html')
cl = MpesaClient()
stk_push_callback_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
b2c_callback_url = 'https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest'

def getAccessToken(request):
    consumer_key = 'sFpwIfYu5YBZFZe48JaftAYbWaBGW5xe'
    consumer_secret = '3cKGFxJ57yJJg4Gq'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    return HttpResponse(validated_mpesa_access_token)

def oauth_success(request):
	r = cl.access_token()
	return JsonResponse(r, safe=False)

def stk_push_success(request):
	phone_number = config('LNM_PHONE_NUMBER')
	amount = 1
	account_reference = 'Mat Pooler'
	transaction_desc = 'STK Push Description'
	callback_url = stk_push_callback_url
	r = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
	return JsonResponse(r.response_description, safe=False)

def business_payment_success(request):
	phone_number = config('B2C_PHONE_NUMBER')
	amount = 1
	transaction_desc = 'Business Payment Description'
	occassion = 'Test business payment occassion'
	callback_url = b2c_callback_url
	r = cl.business_payment(phone_number, amount, transaction_desc, callback_url, occassion)
	return JsonResponse(r.response_description, safe=False)

def salary_payment_success(request):
	phone_number = config('B2C_PHONE_NUMBER')
	amount = 1
	transaction_desc = 'Salary Payment Description'
	occassion = 'Test salary payment occassion'
	callback_url = b2c_callback_url
	r = cl.salary_payment(phone_number, amount, transaction_desc, callback_url, occassion)
	return JsonResponse(r.response_description, safe=False)

def promotion_payment_success(request):
	phone_number = config('B2C_PHONE_NUMBER')
	amount = 1
	transaction_desc = 'Promotion Payment Description'
	occassion = 'Test promotion payment occassion'
	callback_url = b2c_callback_url
	r = cl.promotion_payment(phone_number, amount, transaction_desc, callback_url, occassion)
	return JsonResponse(r.response_description, safe=False)
 
def logout_view(request):
    logout(request)
    # Redirect to a success page.
    
def home(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return render(request, 'index.html')

def about(request):
    return render(request, 'about.html', {'title': 'About'})


@login_required(login_url='login')
def findbus(request):
    context = {}
    if request.method == 'POST':
        source_r = request.POST.get('source')
        dest_r = request.POST.get('destination')
        date_r = request.POST.get('date')
        bus_list = Bus.objects.filter(source=source_r, dest=dest_r, date=date_r)
        if bus_list:
             return render(request, 'list.html', locals())
        else:
            context["error"] = "Sorry no buses available"
            return render(request, 'findbus.html', context)
    else:
        return render(request, 'findbus.html')


@login_required(login_url='login')
def bookings(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('bus_id')
        seats_r = int(request.POST.get('no_seats'))
        bus = Bus.objects.get(id=id_r)
        if bus:
            if bus.rem > int(seats_r):
                name_r = bus.bus_name
                cost = int(seats_r) * bus.price
                source_r = bus.source
                dest_r = bus.dest
                nos_r = Decimal(bus.nos)
                price_r = bus.price
                date_r = bus.date
                time_r = bus.time
                username_r = request.user.username
                email_r = request.user.email
                userid_r = request.user.id
                rem_r = bus.rem - seats_r
                Bus.objects.filter(id=id_r).update(rem=rem_r)
                book = Book.objects.create(name=username_r, email=email_r, userid=userid_r, bus_name=name_r,
                                           source=source_r, busid=id_r,
                                           dest=dest_r, price=price_r, nos=seats_r, date=date_r, time=time_r,
                                           status='BOOKED')
                print('------------book id-----------', book.id)
                # book.save()
                return render(request, 'bookings.html', locals())
            else:
                context["error"] = "Sorry select fewer number of seats"
                return render(request, 'findbus.html', context)

    else:
        return render(request, 'findbus.html')


@login_required(login_url='login')
def cancellings(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('bus_id')
        #seats_r = int(request.POST.get('no_seats'))

        try:
            book = Book.objects.get(id=id_r)
            bus = Bus.objects.get(id=book.busid)
            rem_r = bus.rem + book.nos
            Bus.objects.filter(id=book.busid).update(rem=rem_r)
            #nos_r = book.nos - seats_r
            Book.objects.filter(id=id_r).update(status='CANCELLED')
            Book.objects.filter(id=id_r).update(nos=0)
            return redirect(seebookings)
        except Book.DoesNotExist:
            context["error"] = "Sorry You have not booked that bus"
            return render(request, 'error.html', context)
    else:
        return render(request, 'findbus.html')


@login_required(login_url='login')
def seebookings(request,new={}):
    context = {}
    id_r = request.user.id
    book_list = Book.objects.filter(userid=id_r)
    if book_list:
        return render(request, 'booklist.html', locals())
    else:
        context["error"] = "Sorry no buses booked"
        return render(request, 'findbus.html', context)


