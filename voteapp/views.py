from django.shortcuts import render, render_to_response, HttpResponse, redirect
from django.http import Http404,JsonResponse,HttpResponseBadRequest
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views import generic
from django.views.generic.list import ListView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
import requests, json, facebook, re
from .models import *
import datetime
from django.utils import timezone
from django.template import RequestContext

def home(request):
	if request.user.is_authenticated():
		return render(request, 'index.html', {'email' : request.user.email})
	else :
		return render(request, 'index.html')	
def about(request):
	if request.user.is_authenticated():
		return render(request, 'about.html', {'email' : request.user.email})
	else :
		return render(request, 'about.html')
def rightbar(request):
	if request.user.is_authenticated():
		return render(request, 'right-sidebar.html', {'email' : request.user.email})	
	else :
		return render(request, 'right-sidebar.html')
def nobar(request):
	if request.user.is_authenticated():
		return render(request, 'no-sidebar.html', {'email' : request.user.email})	
	else :	
		return render(request, 'no-sidebar.html')
def contact(request):
	if request.user.is_authenticated():
		return render(request, 'contact.html', {'email' : request.user.email})
	else :	
		return render(request, 'contact.html')
# def dashboard(request,email):
# 	return render(request, 'dashboard.html',{'email':email})			
# def registration(request):
# 	return render(request, 'registration/registration.html')	
def underconstruction(request):
	return render(request, 'under-construction.html')	
# def handler404(request):
#     response = render_to_response('404.html', {},context_instance=RequestContext(request))
#     response.status_code = 404
#     return response


# def handler500(request):
#     response = render_to_response('500.html', {},context_instance=RequestContext(request))
#     response.status_code = 500
#     return response

@login_required(login_url = "/login")
def DashboardView(request):
    if request.method =='GET':
        template_name = 'dashboard.html'
        return render(request, template_name, {'email' : request.user.email})   

def LoginView(request):
    if request.user.is_authenticated():
        return redirect('/')

    template_name = 'registration/login.html'
    if request.method == "POST":
        post = request.POST
        email = post['email']
        password = post['password']
        # username = User.objects.get(email=email)
        # print(username)
        username = email
        user = authenticate(username=username,email=email, password=password)
        if user is not None:

            if user.is_active:
                login(request,user)
                return redirect('/dashboard')
            else:
                messages.warning(request, "You cannot login", fail_silently=True)
                return redirect('/login')
        else:
            messages.error(request,'Invalid Credentials',fail_silently=True)
            return render(request,template_name,{})
    else:
        return render(request,template_name)


@login_required(login_url = "/login")
def LogoutView(request):
    logout(request)
    return redirect('/')

@login_required(login_url = "/login")
@csrf_exempt
def getCauseData(request):
    context = {}
    if request.method == 'POST':
        data = request.POST
        email = data.get("email")
        print(email)
        causeArray = []
        voteArray = []
        cause_list = Cause.objects.all()
        user = User.objects.get(email=email)
        # vote_list = Vote.objects.filter(user=user)
        context['email'] = user.email
        for cause in cause_list:
            causeObject = {}
            causeObject['name'] = cause.name
            causeObject['causeId'] = cause.causeId
            try:
                vote = Vote.objects.get(user=user,cause=cause)
                causeObject['activeStatus'] = str(vote.activeStatus).lower()
                causeObject['submitStatus'] = str(vote.submitStatus).lower()     
            except:
                causeObject['activeStatus'] = "false"
                causeObject['submitStatus'] = "false"
            # print(causeObject)
            causeArray.append(causeObject)
        # for vote in vote_list:
        #     voteObject = {}
        #     voteObject['activeStatus'] = vote.activeStatus
        #     voteObject['submitStatus'] = vote.submitStatus
        #     # causeObject['activeStatus'] = str(cause.activeStatus).lower()
        #     # causeObject['submitStatus'] = str(cause.submitStatus).lower()
        #     # print(causeObject)
        #     voteArray.append(voteObject)
        context['causeData'] = causeArray         
        # context['voteData'] = voteArray     
        return JsonResponse(context)  
    else:
        context['status'] = "CANNOT GET DATA"   
        return JsonResponse(context)   
# @login_required(login_url = "/login")
@csrf_exempt
@login_required(login_url = "/login")
def submitCauseData(request):
    response_data = {}
    #if someone clicks submit then it mean activestatus=True
    if request.method == 'POST':
        data = request.POST
        email = data.get("email")
        print(email)
        causeId = data.get("causeId")
        activestatus = True
        submitStatus = data.get("submitStatus")
        if(submitStatus == "false"):
            submitStatus = False #do not support it
        else:
            submitStatus = True  #do support it 
        try:
            print("Checking if exists user and cause")
            user = User.objects.get(email=email)
            cause = Cause.objects.get(causeId=causeId)
            print('check DONE')
            try:
                print("if vote already exists")
                # vote = user.vote_set.all()
                # vote = Vote.objects.get(email=email)
                vote_add = Vote.objects.get(user=user,cause=cause)
                print(vote_add)
                print("IT DOES")
                response_data['status'] = 'USER ALREADY SUBMITTED POLL'
                return JsonResponse(response_data)
            except:    
                vote = Vote.objects.create()
                # cause = Cause.objects.get(causeId=causeId)
                # cause.activeStatus = True
                # cause.submitStatus = submitStatus
                # vote_create = Vote(causeId = causeId,user=user,activestatus=True,submitStatus=submitStatus)
                vote.cause = cause
                vote.user = user
                vote.activeStatus = True
                vote.submitStatus = submitStatus
                print("CREATING NEW VOTE")
                vote.save()
                # print('yolyo')
                response_data['status'] = 'VOTE SUCCESS'
                return JsonResponse(response_data)
        except:
            response_data['status'] = "USER_NOT_FOUND"
            return JsonResponse(response_data)    

def RegistrationView(request):
    if request.user.is_authenticated():
        return redirect('/')
    context = {}    
    template_name = 'registration/registration.html'
    if request.method == "POST":
        post = request.POST
        print(post)

        context['email'] =  post.get('email');
        context['first_name'] =  post.get('first_name');
        context['last_name'] =  post.get('last_name');

        email = post.get('email')
        email = email.lower()
        username = email
        # username = context['first_name'] + " " + context['last_name']
        print(username)
        if len(email) > 30 or len(email) <= 0:
            messages.warning(request, "Email address is too long. Register with a different email address.", fail_silently=True)
            return render(request,template_name,context)
        
        password1 = post.get('password')
        password2 = post.get('repassword')
        if password1 != password2:
            messages.warning(request, "Passwords did not match.", fail_silently=True)
            return render(request,template_name,context)
        if len(password1) < 5:
            messages.warning(request, "Enter a password having atleast 5 characters.", fail_silently=True)
            return render(request,template_name,context)
        
        try:
            already_a_user = User.objects.get(email=email)
        except:#unique user.
            already_a_user = False

        if not already_a_user:#create new User instance.
            try:
                user = User.objects.create_user(username=username,email=email)
                first_name = post.get('first_name')
                last_name = post.get('last_name')
                user.first_name = first_name
                user.last_name = last_name
                # user.is_active = False #Can login when the quiz starts
                user.set_password(password1)
                user.save()
                userprofile = UserProfile.objects.create(user=user)
 
                #Checking an empty field
                if first_name == "" or last_name=="":
                    messages.warning(request, "Form is not valid. Make sure you fill ALL the fields correctly!", fail_silently=True)
                    user.delete()
                    return render(request,template_name,context)

                userprofile.save()
                # sheetRegistration(userprofile)
                messages.success(request, 'Successfully Registered.', fail_silently=True)
                return redirect('/registration')
            except:
                messages.warning(request, "Enter a valid form!", fail_silently=True)
                user.delete()
                return render(request,template_name,context)
        else:#already a user.
            messages.warning(request, "Email already registered!", fail_silently=True)
            return render(request,template_name,context)

    else:#request.method == "GET"
        return render(request,template_name,context)

@csrf_exempt
@login_required(login_url = "/login")
def stats(request,email,causeId):
    # print(causeId)
    # print(email)
    context = {}
    try: 
        user = User.objects.get(email=email)
        cause = Cause.objects.get(causeId=causeId)
        # if request.method =='GET':
        # template_name = 'canvasjs.html'
        vote_favour = Vote.objects.filter(cause=cause,submitStatus=True)
        vote_oppose = Vote.objects.filter(cause=cause,submitStatus=False)
        context['email'] = email
        context['name'] = cause.name
        context['causeId'] = cause.causeId
        context['favour'] = len(vote_favour)
        context['oppose'] = len(vote_oppose)
        context['fav_per'] = round((len(vote_favour)/(len(vote_favour)+len(vote_oppose)))*100,3)
        context['opp_per'] = round((len(vote_oppose)/(len(vote_favour)+len(vote_oppose)))*100,3)
            # print(len(vote_favour))
    # print(len(vote_oppose))
    # for vote in vote_list:
        # print(vote)
        # return JsonResponse(context) 
        # if request.method =='GET':
        #     template_name = 'index.html'
        return render(request, 'stats.html',context)     
    except:
        return render(request,'under-construction.html')    