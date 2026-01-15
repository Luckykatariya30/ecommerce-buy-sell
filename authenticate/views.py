from django.shortcuts import render,redirect
from django.http import HttpResponse    
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_str as force_text
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from .utils import TokenGenerator,generate_token
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.utils.encoding import DjangoUnicodeDecodeError
# import pdb
# pdb.set_trace()


# Create your views here.
# user signin view logic ....
@csrf_exempt
def user_sign_in(request):
    if request.method =="POST":
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['pass2']
        # Check the password creacte and not creacte..
        if password != confirm_password:
            messages.warning(request, 'This is not matching password !')
            return redirect('/auth/signup/')
        # breakpoint()
        # check the user exist and not exist...
        try:
            if User.objects.get(username=email):
                messages.info(request, 'This is already exist...!')
                return render(request, 'authentication/login.html')
                # return HttpResponse('This is already exist...!')
        except Exception as e:
            pass
        # if user is not exist than save the database..
        user = User.objects.create_user(email, email, password)
        user.is_active = False
        user.save()
        
        email_subject='Activate Your Account'
        message = render_to_string('activate.html',{
            'user':user,
            'domain':'127.0.0.1:8000',
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user)
        })
        # breakpoint()
        email_message = EmailMessage(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [email]
        )
        email_message.send()
        messages.success(request , "Activate Your Account by clicking the link in your gmail.")
        return HttpResponse('This is created !')
    # breakpoint()
    return render(request, 'authentication/signup.html')
class ActivateAccountView(View):
    def get(self, request,uidb64,token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.info(request, 'Account Activated Successfully')
            return redirect('/auth/login/')
        return render(request, 'authentication/activatefail.html')
    
@csrf_exempt
def user_log_in(request):
    if request.method=="POST":
        username = request.POST['email']
        userpass = request.POST['password']
        user = authenticate(username=username, password =userpass)
        if user is not None:
            login(request,user)
            messages.success(request,"Login Successfuly..")
            return redirect('/')
        else:
            messages.error(request, "Security Credential...")
            return redirect('/auth/login/')
    return render(request, 'authentication/login.html')

def user_logout_in(request):
    logout(request)
    messages.info(request,'Logout Success!')
    return redirect('/auth/login/') 


class RequestResetEmailView(View):
    def get(self, request):
        return render(request, 'authentication/reset_request.html')
    
    def post(self, request):
        email = request.POST['email']
        user = User.objects.filter(email=email)
        if user.exists():
            # cuuent_site = get_current_site(request)
            email_subject='[Reset Your Password]'
            message = render_to_string('authentication/reset_user_password.html',{
                'user':user[0],
                'domain':'127.0.0.1:8000',
                'uid':urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token':generate_token.make_token(user[0])
            })
            email_message = EmailMessage(
                email_subject,
                message,
                settings.EMAIL_HOST_USER,
                [email]
            )
            email_message.send()
            messages.success(request , "We have sent you an email to reset your password.")
            return render(request, 'authentication/reset_request.html')
        else:   
            messages.error(request, "No user is associated with this email address")
            return render(request, 'authentication/reset_request.html') 
class SetNewPasswordView(View):
    def get(self, request,uidb64,token):
        context={}
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            context['uidb64']=uidb64
            context['token']=token
            if user is not None and generate_token.check_token(user,token):
                return render(request, 'authentication/set-new-password.html',context)
            else:
                messages.info(request, 'Password link is invalid, please request a new one.')
                return render(request, 'authentication/reset_request.html')
        except Exception as identifier:
            pass
        
    def post(self, request,uidb64,token):
        context={}
        password = request.POST['password']
        confirm_password = request.POST['pass2']
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            context['uidb64']=uidb64
            context['token']=token
        except Exception as identifier:
            pass
        
        if password != confirm_password:
            messages.warning(request, 'Password Not Matched !')
            return render(request, 'authentication/set-new-password.html',context)
        try:
            if user is not None and generate_token.check_token(user,token):
                user.set_password(password)
                user.save()
                messages.success(request, 'Password reset successful. You can now log in with the new password.')
                return redirect('/auth/login/')
            else:
                messages.info(request, 'Password link is invalid, please request a new one.')
                return render(request, 'authentication/reset_request.html')
        except DjangoUnicodeDecodeError as identifier:
            messages.error(request, 'Something went wrong, please try again.')
            return render(request, 'authentication/set-new-password.html',context)
        return render(request, 'authentication/set-new-password.html',context)
       
       

    