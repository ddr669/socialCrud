from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import Group, User
from django.contrib.auth import login, logout
from socialCrud.quickstart.models import PostIT
from socialCrud.quickstart.serializers import UserSerializer
from django.http import HttpRequest
from django.http import HttpResponseRedirect
from rest_framework.authentication import authenticate


def LoginUser(request: HttpRequest = {}, pk = None):
    load = loader.get_template('login.html')
    context = {}
    
    if request.method == "POST":
        try:
            _ = request.POST.dict()
            context = {'username':_['username'], 'password':_['password'],}
            try:
                queryset = User.objects.get(username=context['username'])

            except User.DoesNotExist:
                return HttpResponseRedirect('/register/')
            
            userquery = authenticate(request=request, username=context['username'], password=context['password'])
            if userquery:
                login(request=request, user=queryset)
                return HttpResponseRedirect('/homepage/')
            else:
                context['incorrect_password'] = "Incorrect password."
                return HttpResponse(load.render(context=context, request=request))

        except KeyError:
            return HttpResponseRedirect('/login/')

    else:
        return HttpResponse(load.render(context=context, request=request))

def UserRegister(request: HttpRequest = {}, pk=None):
    load = loader.get_template('register.html')
    context = {}
    if request.method == 'POST':
        _ = request.POST.dict()
        try:
            context = {'username':_['username'], 'password':_['password'], 'password2':_['password2'], 'email': _['email'],}
            if context['password'] == context['password2']:
                queryset = User.objects.get_or_create(username=context['username'],
                                                password=context['password'],
                                                email=context['email'])
        
                return HttpResponseRedirect('/login/')
            else:
                context['password_failure'] = 'Incorrect Password Verification, Try again.'
                return HttpResponse(load.render(context=context, request=request))
            
        except KeyError:
            context['email_failure'] = 'No email field, Try again.'
            return HttpResponse(load.render(context=context, request=request))

    else:
        return HttpResponse(load.render(context=context, request=request))

def logOut(request: HttpRequest, pk=None):
    if request.user.is_authenticated:
        logout(request=request)
        return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/login/')
    
def HomePageMain(request: HttpRequest, pk=None):
    if request.method == "POST":
        _ = request.POST.dict()
        try:
            _username = request.user
            _content = _['content']
            _title = _['title']
            new = PostIT.objects.get_or_create(username=_username, title=_title, content=_content, creator=_username)

        except KeyError as err:
            print(err)
        
    posts = PostIT.objects.all().order_by('-created_datetime')
    context = {'posts': posts,}
    load = loader.get_template('default_home.html')
    if request.user.is_authenticated:
        context['authenticate'] = True
        context['view_username'] = request.user
    
    return HttpResponse(load.render(context=context, request=request))   