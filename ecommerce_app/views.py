from django.shortcuts import render,redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import Contect,Product, Order, OrderUpdate
from math import ceil
from . import keys
from django.conf import settings
MERCHANT_KEY = keys.MK
from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum
# import pdb

# pdb.set_trace()

# Create your views here.
def index(request):
    all_prods = []
    catprods = Product.objects.values('category','id')
    # print(catprods)
    cats ={item['category'] for item in catprods}
    # print(cats)
    for cat in cats:
        # print(cat)
        prod = Product.objects.filter(category=cat)
        # print(prod)/
        n=len(prod)
        # print(n)
        nslidce = n//4 + ceil(n/4 - n//4)
        # print(nslidce)
        all_prods.append([prod,range(1,nslidce),nslidce])
    params ={'allprods':all_prods}
    return render(request , 'main/index.html',params)
        
@csrf_exempt
def contect(request):
    if request.method == "POST":
        name= request.POST.get('name')
        email= request.POST.get('email')
        phone= request.POST.get('number')
        desc= request.POST.get('desc')
        user = Contect(name=name, email=email , phone_number=phone , desc=desc)
        user.save()
        messages.info(request,'This is contects are save.')
        return render(request,'main/index.html')
    return render(request, 'main/contect.html')

def about(request):
    return render(request, 'main/about.html')

def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please Login & Try Again')
        return redirect('/auth/login/')
    
    if request.method == "POST":
        items_json = request.POST.get('itemsJson','')
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        address1 = request.POST.get('address','')
        address2 = request.POST.get('address2','')
        city = request.POST.get('city','')
        state = request.POST.get('state','')
        zip_code = request.POST.get('zip_code','')
        phone = request.POST.get('phone','')
        print(request.POST )
        amount = request.POST.get('amt')
        print("amount:", amount) 
        # breakpoint()
        order = Order(items_json=items_json, name=name, email=email, address1=address1, address2=address2, city=city, state=state, zip_code=zip_code, phone=phone, amount= amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed" , delivered=True)
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'main/checkout.html', {'thank':thank, 'id':id})
        # PAYMENT INTEGRATION STARTS HERE
        # param_dict = {
        #     'MID': 'Keys.YourMerchantID',
        #     'ORDER_ID': str(order.order_id),
        #     'TXN_AMOUNT': str(amount),
        #     'CUST_ID': email,
        #     'INDUSTRY_TYPE_ID': 'Retail',
        #     'WEBSITE': 'WEBSTAGING',
        #     'CHANNEL_ID': 'WEB',
        #     'CALLBACK_URL': 'http://localhost:8000/handlerequest/'
        # }
        # param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        # return render(request, 'main/paytm.html', {'param_dict': param_dict})
        # return render(request, 'main/checkout.html', {'thank':thank, 'id':id})
    return render(request, 'main/checkout.html')

# @csrf_exempt
# def handlerequest(request):
#     # paytm will send you post request here
#     form = request.POST
#     response_dict = {}
#     for i in form.keys():
#         response_dict[i] = form[i]
#         if i == 'CHECKSUMHASH':
#             checksum = form[i]

#     verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
#     if verify:
#         if response_dict['RESPCODE'] == '01':
#             print('order successful')
#             a=response_dict['ORDERID']
#             b=response_dict['TXNAMOUNT']
#             rid=a.replace("Order","")
#             filter2=Order.objects.filter(order_id=rid)
#             for item in filter2:
#                 item.amount=b
#                 item.save()
#         else:
#             print('order was not successful because' + response_dict['RESPMSG'])
#     return render(request, 'main/paymentstatus.html', {'response': response_dict})

def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please Login & Try Again')
        return redirect('/auth/login/')
    current_user = request.user.username
    print("current_user:", current_user)
    items = Order.objects.filter(email=current_user)
    rid = 0
    for item in items:
        myid = item.order_id
        print("myid:", myid)
        rid = myid
    print("rid:", rid)
    status = OrderUpdate.objects.filter(order_id=rid, delivered=True)
    print(status)
    context = {'items': items, 'status': status}
    return render(request, 'main/profile.html', context)
    
def blog(request):
    return render(request, 'main/blog.html')
