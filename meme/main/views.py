from django.shortcuts import render,redirect
from django.http import HttpResponse
from .utilis import registerUser,userLogin
from django.contrib.sessions.backends.db import SessionStore
import requests
import bcrypt
# Session handling
s=  SessionStore()
# Create your views here.
import psycopg2
try:
    connection =psycopg2.connect(
        host="127.0.0.1",
        port="5432",
        database="memestore",
        user="postgres",
        password="123"
    )
    print("database connected")
except Exception as e:
    print(e)
    print("databse not connected")
connection.autocommit=True
cursor=connection.cursor()

# Middle 

def chcekSesson():
    
    try:
        email=s['email']
        return True
    except Exception as e:
        print("error",e)
        return False
    



def home(request):
    return HttpResponse("<h2>Welcome,this a python framework<h2/>")

def register(request):
    SessionExist=chcekSesson()
    if SessionExist==False:
        if request.method=="POST":
            name=request.POST['username']
            email=request.POST['email']
            cont=request.POST['contact']
            password=request.POST['password']
            
            
            password=password.encode()
            
            hashed=bcrypt.hashpw(password,bcrypt.gensalt())
            
            hashed=hashed.decode('utf-8')
            userdata={
                "name":name,
                "email":email,
                "contact":cont,
                "password":hashed
            }
            
            response=registerUser(userdata,cursor)
        
           
            if response['status']==200:
              
                return redirect('/main/login/')
            else:
                s['email']=userdata['email']
                s['password']=userdata['password']
            
                return redirect('/main/meme/')
                
                    
        elif request.method=="GET":
            return render(request,'register.html')
        else:
            return HttpResponse("invalid")
    else:
        return redirect("/main/meme/")
def login(request):
    SessionExist=chcekSesson()
    if SessionExist==False:
        if request.method=='POST':
            email=request.POST['email']
            password=request.POST['password']
            userdata={
                "email":email,
                "password":password
            }
            response=userLogin(userdata,cursor)
            if response['status']==200:
                s['email']=userdata['email']
                s['password']=userdata['password']
                return  redirect("/main/meme/")
            elif response['status']==503 and response['message']=="password error":
                return render(request,'login.html',{"message":response['message']})
            else: 
                return render(request,'login.html',{"message":response['message']})
        elif request.method=="GET":
            return render(request,"login.html")
    else:
        return redirect("/main/meme/")
    
def getMeme(request):
    
    SessionExist=chcekSesson()
    if SessionExist==False:
        return redirect("/main/login/")
    else:
        r=requests.get("https://api.imgflip.com/get_memes")
        meme_data=r.json()
        return render(request,"meme.html",{"content":meme_data['data']['memes']})
        
        
        
def logout(request):
    s.clear()
    return redirect("/main/login")  

def meme_details(request):
    SessionExist=chcekSesson()
    if SessionExist==True:
        meme_id=request.GET['id']
        return render(request,'memeDetails.html',{"meme_id":meme_id})
    
    else:
        return redirect('/main/login/')

def edit(request):
    SessionExist=chcekSesson()
    if SessionExist==True:
        if request.method=='POST':
            id=request.POST['id']
            text_1=request.POST['text_1']
            text_2=request.POST['text_2']
            print(id,text_1,text_2)
            payload={
                "template_id": id,
                 "username":"PriyamGupta",
                 "password":"8004416988",
                 "text0":text_1,
                 "text1":text_2
                   
            }
            response=requests.request("POST","https://api.imgflip.com/caption_image",params=payload).json()
            print(response)
            meme_data=f'''
                    <img src="{response["data"]["url"]}"/>
                    <button><a href="{response['data']['url']}"> View Image</a></button>
                           
            '''
            return HttpResponse(meme_data)
 
    else:
        return redirect('/main/login/')