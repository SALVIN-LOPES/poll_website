
from operator import index
from urllib import response
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.db.models import Q




def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        phone = request.POST.get('username')
        password  = request.POST.get('password')
        # print(phone)
        try:
            user = User.objects.get(phone = phone)

        except:
            messages.error(request, 'user does not exist...')
        user =  authenticate(request,username=phone,password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('home')

    context = {'page':'before_login'}
    return render(request,'base/loginPage.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')

# @login_required(login_url='login')

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # user.username = user.username.lower()
            # user.save()
            login(request,user)
            print(user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration..')

    context = {'form' : form,'page':'before_login'}
    return render(request,'base/registerPage.html',context)

@login_required(login_url='login')
def home(request):
    # search functionality
    # q = request.GET.get('q') if request.GET.get('q') != None else ''
    # search_polls = Poll.objects.filter(
    #     ~Q(question__icontains = q) |
    #     ~Q(created_by__icontains = q)
    # )
    # print(search_polls)
    # total_polls = search_polls.count()



    user = request.user
    poll_ids = ResponseModel.objects.filter(response_by=user).values_list('poll', flat=True) #doubt
    print(list(poll_ids))
    polls = Poll.objects.filter(~Q(id__in=poll_ids))
    polls_array=[]
    index=0
    for poll in polls:
        index+=1
        poll_json={
            "index":index,
            "id":poll.id,
            "question":poll.question,
            "name":poll.created_by.name,
        }
        polls_array.append(poll_json)
    length_polls = len(polls_array)
    print(polls_array)
    context = {'page':'after_login',
    "polls":polls_array,
    'length_polls':length_polls,
    # 'search_polls' :search_polls,
    # 'total_polls' :total_polls,
    
    }
    return render(request, 'base/home.html',context)

@login_required(login_url='login')
def profilePage(request):
    # check whether the user is authenticated
    user = request.user
    if request.user.is_authenticated:
        polls = Poll.objects.filter(created_by=user)
        polls_array=[]
        index=0
        for poll in polls:
            index+=1
            responses = ResponseModel.objects.filter(poll=poll)
            total_responses = len(responses)
            # print(responses)
            total_option1=0
            total_option2=0
            total_option3=0
            total_option4=0
            for r in responses:
                if r.choose==1:
                    total_option1+=1
                elif r.choose==2:
                    total_option2+=1
                elif r.choose==3:
                    total_option3+=1
                elif r.choose==4:
                    total_option4+=1
            poll_json = {
                "question":poll.question,
                "option1":poll.option1,
                "option2":poll.option2,
                "option3":poll.option3,
                "option4":poll.option4,
                "total_option1":total_option1,
                "total_option2":total_option2,
                "total_option3":total_option3,
                "total_option4":total_option4,
                "total_responses":total_responses,
                "index":index,
            }
            polls_array.append(poll_json)
            print(poll_json)
        context = {'user':user,'page':'after_login',"polls":polls_array}
        return render(request, 'base/profilePage.html',context)
    else:
        return redirect('login')

@login_required(login_url='login')
def createPoll(request):
    user = request.user
    polls = Poll.objects.filter(created_by=user)
    total_polls = len(polls)
    if request.method == 'POST':
        question = request.POST.get('question')
        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')
        option3 = request.POST.get('option3')
        option4 = request.POST.get('option4')
        # print(question,option1,option2,option3,option4)
        poll = Poll(question=question,option1=option1,option2=option2,option3=option3,option4=option4,created_by=user)
        poll.save()
        return redirect('profile')
    context = {'page':'after_login',"total_polls":total_polls}
    return render(request, 'base/createPoll.html', context)

@login_required(login_url='login')

def getPoll(request,id):
    user = request.user
    poll = Poll.objects.filter(id=id).first()
    if poll==None:
        return redirect('home')
    poll_response = ResponseModel.objects.filter(response_by=user,poll=poll).first()
    if poll_response:
        return redirect('home')
    if request.method == 'POST':
        option = request.POST.get('poll')
        poll_response = ResponseModel(response_by=user,poll=poll,choose=option)
        poll_response.save()
        return redirect('result')
    context = {'page':'after_login',"poll":poll}
    return render(request, 'base/poll.html', context)

@login_required(login_url='login')
def getResult(request):

    user = request.user
    poll_responses = ResponseModel.objects.filter(response_by=user)

    responses_array=[]
    print("POLL_RESPONSES = ",poll_responses)
    index=0
    for r in poll_responses:
        single_poll = r.poll.question
        # print("single_poll = ", single_poll)
        index+=1
        poll_response_json={
            "index":index,
            "question":r.poll.question,
            "option1":r.poll.option1,
            "option2":r.poll.option2,
            "option3":r.poll.option3,
            "option4":r.poll.option4,
            "name":r.poll.created_by.name,
            "choose":r.choose,
            # "option1_count":  ,          
            # "option2_count":  ,         
            # "option3_count":  ,        
            # "option4_count":  ,       
        }
        responses_array.append(poll_response_json)
    # single_pole = Poll.objects.filter(id = pk)

    context = {'page':'after_login',"poll_responses":responses_array}
    return render(request, 'base/result.html', context)

# def getSinglePole(request,pk):
#     user = request.user
#     single_poll = Poll.objects.find(id = pk)
#     print(single_poll)





