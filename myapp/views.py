from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages 
from django.contrib.auth.models import User 
from django.contrib.auth  import authenticate,  login, logout

from myapp.models import Chat

# gemini ai
import google.generativeai as genai
import os


API_KEY = "AIzaSyAT2p4A0DNhQfwHGMc4jRsGDtAK36GKRVw"
genai.configure(api_key= API_KEY)
generation_config ={
    "temperature": 0.9,
    "top_p": 1,
    "max_output_tokens":2048
}
model = genai.GenerativeModel("gemini-pro",generation_config=generation_config)



def home(request): 
    user_id = request.user.id
    unique_user_ids = User.objects.values_list('id', flat=True).distinct()
    if user_id in unique_user_ids:
        return redirect('chat')
    return render(request, "home.html")


def chat(request):
    username=request.user                                 # userid
    user_id = request.user.id
    
    if request.method=="POST":
        userInput=request.POST['userInput']                 #chatperson
        if userInput!='':
            obj = Chat(user=username,chat_person="user",chat=userInput)
            obj.save()
            try:
                aiInput = model.generate_content(userInput) #chatperson
                aiInput = aiInput.text
                aiInput = aiInput.replace('*', '')
                obj = Chat(user=username,chat_person="ai",chat=aiInput)
                obj.save()
            except:
                obj = Chat(user=username,chat_person="ai",chat="oops somthing went wrong!!!")
                obj.save()

    unique_user_ids = User.objects.values_list('id', flat=True).distinct()
    if user_id not in unique_user_ids:
        return redirect('home')
    chats=Chat.objects.all().filter(user_id=username)

    return render(request, "chat.html",{'chats':chats})


def handleSignUp(request):
    if request.method=="POST":
        # Get the post parameters
        username=request.POST['username']
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        # check for errorneous input
        if len(username)<5:
            messages.error(request, " Your user name must be under 10 characters")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('home')
        if (pass1!= pass2):
            messages.error(request, " Passwords do not match")
            return redirect('home')
        try:
            myuser = User.objects.create_user(username, email, pass1)
            myuser.first_name= fname
            myuser.last_name= lname
            myuser.save()
            messages.success(request, " Your iCoder has been successfully created")
            return redirect('home')
        except:
            messages.error(request, " try another user name")
            return redirect('home')

    else:
        return HttpResponse("404 - Not found")
    return HttpResponse("login")


def handeLogin(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("chat")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("home")

    return HttpResponse("404- Not found")

def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')

def deleteChat(request,id):
    try:
        delete = Chat.objects.get(id=id)
        delete.delete()
    except:
        return redirect('chat')
    return redirect('chat')

def deleteAll(request,id):
    delete=Chat.objects.all().filter(user=id)
    delete.delete()
    print(delete)
    return redirect('chat')
