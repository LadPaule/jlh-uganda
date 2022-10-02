import random
import requests
import math

from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from .forms import DonateForm
from django.shortcuts import render, redirect




def donate_form(request):
    if request.method=='POST':
        form = DonateForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            amount = form.cleaned_data['amount']

            return redirect(str(process_payment(name, email, phone, amount)))
        
        else:
            form = DonateForm()
        ctx ={'form': form}

        return render(request, 'home/donate.html', ctx)

def process_payment(name,email,amount,phone):
    auth_token= 'FLWSECK-7dbf1cde8f4237b01ebd47213d563304-X'
    hed = {'Authorization': 'Bearer ' + auth_token}
    data = {
                "tx_ref":''+str(math.floor(1000000 + random.random()*9000000)),
                "amount":amount,
                "currency":"USD",
                "redirect_url":"http://localhost:8000/callback",
                "payment_options":"card, USSD",
                "meta":{
                    "consumer_id":23,
                    "consumer_mac":"92a3-912ba-1192a"
                },
                "customer":{
                    "email":email,
                    "phonenumber":phone,
                    "name":name
                },
                "customizations":{
                    "title":"JLH-Uganda Donations",
                    "description":"Donate to support JLH-Uganda",
                    "logo":"https://getbootstrap.com/docs/4.0/assets/brand/bootstrap-solid.svg"
                }
                }
    url = ' https://api.flutterwave.com/v3/payments'
    response = requests.post(url, json=data, headers=hed)
    response=response.json()
    link=response['data']['link']
    return link


@require_http_methods(['GET', 'POST'])
def payment_response(request):
    status = request.GET.get('status', None)
    tx_ref = request.GET.get('tx_ref', None)
    print('status is: '+ status)
    print('status is: '+ tx_ref)

    return HttpResponse('Finished')

