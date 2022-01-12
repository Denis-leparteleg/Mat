from decouple import config
from django.http.response import JsonResponse
from django.urls import reverse
from django.contrib.auth import logout
from django.shortcuts import render
from decimal import Decimal
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from requests.api import get
from .models import User, Mat, Booking
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

def stk_push_success(request, p_number):
	phone_number = p_number
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

def payment (request):
    if request.method == 'POST':
        name=request.POST.get('fname')
        phone_number=request.POST.get('phone_number')

        ph_number = None

        if phone_number[0] == '0':
            ph_number = '254'+ phone_number[1:]
        elif phone_number[0:2] == '254':
            ph_number = phone_number
        else:
            # messages.error(request, 'Check you Phone Number format 2547xxxxxxxx')
            return redirect(request.get_full_path())


        stk_push_success(request, ph_number)

        return HttpResponse(f'Stk Push for {phone_number}')
    
    return render (request,'payments.html', {'title': 'Payment'})

@login_required(login_url='login')
def findmat(request):
    context = {}
    if request.method == 'POST':
        terminus_r = request.POST.get('terminus')
        route_r = request.POST.get('route')
        date_r = request.POST.get('date')
        mat_list = Mat.objects.filter(terminus=terminus_r, route=route_r, date=date_r)
        if mat_list:
             return render(request, 'list.html', locals())
        else:
            context["error"] = "Sorry no matatus available"
            return render(request, 'findmat.html', context)
    else:
        return render(request, 'findmat.html')


@login_required(login_url='login')
def bookings(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('mat_id')
        seats_r = int(request.POST.get('no_seats'))
        mat = Mat.objects.get(id=id_r)
        if mat:
            if mat.rem > int(seats_r):
                sacco_name_r = mat.sacco_name
                cost = int(seats_r) * mat.fare_price
                terminus_r = mat.terminus
                route_r = mat.route
                nos_r = Decimal(mat.nos)
                fare_price_r = mat.fare_price
                date_r = mat.date
                time_r = mat.time
                username_r = request.user.username
                email_r = request.user.email
                userid_r = request.user.id
                rem_r = mat.rem - seats_r
                Mat.objects.filter(id=id_r).update(rem=rem_r)
                booking = Booking.objects.create(name=username_r, email=email_r, userid=userid_r, sacco_name=sacco_name_r,
                                           terminus=terminus_r, mat_id=id_r,
                                           route=route_r, fare_price=fare_price_r, nos=seats_r, date=date_r, time=time_r,
                                           status='BOOKED')
                print('------------booking id-----------', booking.id)
                # book.save()
                return render(request, 'bookings.html', locals())
            else:
                context["error"] = "Sorry select fewer number of seats"
                return render(request, 'findmat.html', context)

    else:
        return render(request, 'findmat.html')


@login_required(login_url='login')
def cancellings(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('mat_id')
        #seats_r = int(request.POST.get('no_seats'))

        try:
            booking = Booking.objects.get(id=id_r)
            mat = Mat.objects.get(id=booking.mat_id)
            rem_r = mat.rem + booking.nos
            Mat.objects.filter(id=booking.mat_id).update(rem=rem_r)
            #nos_r = book.nos - seats_r
            Booking.objects.filter(id=id_r).update(status='CANCELLED')
            Booking.objects.filter(id=id_r).update(nos=0)
            return redirect(seebookings)
        except Booking.DoesNotExist:
            context["error"] = "Sorry You have not booked that matatu"
            return render(request, 'error.html', context)
    else:
        return render(request, 'findmat.html')


@login_required(login_url='login')
def seebookings(request,new={}):
    context = {}
    id_r = request.user.id
    booking_list = Booking.objects.filter(userid=id_r)
    if booking_list:
        return render(request, 'booklist.html', locals())
    else:
        context["error"] = "Sorry no matatus booked"
        return render(request, 'findmat.html', context)


