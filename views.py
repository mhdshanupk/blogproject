from django.shortcuts import render,redirect,HttpResponse
from . models import Blog,Comment,Profile,OTP
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from . forms import PostBlog
import random
import string
from django.core.mail import send_mail
from django.contrib import messages

def user_register(request):
    if request.method == 'POST':
        fname=request.POST.get('firstname')
        lname=request.POST.get('lastname')
        email=request.POST.get('email')
        uname=request.POST.get('username')
        pword=request.POST.get('password1')
        confirm_pword=request.POST.get('password2')
        if pword == confirm_pword:
            User.objects.create_user(
                first_name=fname,
                last_name=lname,
                email=email,
                username=uname,
                password=pword,
            )
            return redirect('login')
    return render (request,'register.html')

def user_login(request):
    if request.method == 'POST':
        uname=request.POST.get('username')
        pword=request.POST.get('password')
        user=authenticate(username=uname,password=pword)
        if user is not None:
            login(request,user)
            return redirect('home')
        return HttpResponse('Invalid Credentials')
    return render(request,'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

def home(request):
    user=request.user
    if user.is_authenticated:
        profile=Profile.objects.filter(user=user)
        if not profile:
            return redirect('profile')
        blogs=Blog.objects.all()
        if request.method == 'POST':
            temp_type=request.POST.get('type')
            temp_title=request.POST.get('title')
            if temp_type == '':
                blogs=Blog.objects.all()
            else:
                blogs=Blog.objects.filter(type=temp_type)
            if temp_title:
                blogs=Blog.objects.filter(title__icontains=temp_title)
    return render(request,'home.html',{'blogs':blogs,'profile':profile})

def profile_view(request):
    current_user=request.user
    if current_user.is_authenticated:
        profile_details=Profile.objects.filter(user=current_user)
    return render(request,'profile_view.html',{'profile':profile_details})

@login_required(login_url='login')
def add_blog(request):
    if request.method == 'POST':
        blog_title=request.POST.get('title')
        blog_content=request.POST.get('content')
        blog_image=request.FILES.get('photo')
        blog_type=request.POST.get('type')
        Blog.objects.create(
            title=blog_title,
            content=blog_content,
            image=blog_image,
            type=blog_type,
        )
        return redirect('home')
    return render(request,'add_blog.html')

def post_blog(request):
    if request.method == 'POST':
        form = PostBlog(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return HttpResponse(form.errors)
    else:
        form = PostBlog()
    return render(request,'post_blog.html', {'form':form})

@login_required(login_url='login')
def blog_view(request,id):
    blog=Blog.objects.get(id=id)
    comment=Comment.objects.filter(fk_blog=id)
    current_user=request.user
    if request.method == 'POST':
        temp_comment=request.POST.get('comment')
        Comment.objects.create(
            fk_user=current_user,
            fk_blog=blog,
            comment=temp_comment,
        )
        return redirect('blog_view',id=blog.id)
    
    return render(request,'blog_view.html',{'blog':blog , 'comment':comment})

@login_required(login_url='login')
def blog_edit(request,id):
    blog1=Blog.objects.get(id=id)
    if request.method == 'POST':
        blog_title=request.POST.get('title')
        blog_content=request.POST.get('content')
        blog_image=request.FILES.get('photo')
        blog1.title=blog_title
        blog1.content=blog_content
        blog1.image=blog_image
        blog1.save()
        return redirect('home')
    return render(request,'blog_edit.html',{'blog':blog1})

@login_required(login_url='login')
def blog_delete(request,id):
    blog=Blog.objects.get(id=id)
    blog.delete()
    return redirect('home')

@login_required(login_url='login')
def edit_comment(request,id):
    data=Comment.objects.get(id=id)
    blog=data.fk_blog
    if request.method == 'POST':
        temp_comment=request.POST.get('comment')
        data.comment=temp_comment
        data.save()
        return redirect('blog_view',id=blog.id)
    return render(request,'edit_comment.html',{'data':data})

@login_required(login_url='login')
def delete_comment(request,id):
    data=Comment.objects.get(id=id)
    blog=data.fk_blog
    data.delete()
    return redirect('blog_view',id=blog.id)

@login_required(login_url='login')
def profile_add(request):
    current_user=request.user
    if request.method == 'POST':
        temp_phone=request.POST.get('phone_number')
        temp_photo=request.FILES.get('photo')
        temp_location=request.POST.get('place')
        Profile.objects.create(
            user=current_user,
            phone=temp_phone,
            location=temp_location,
            photo=temp_photo,
        )
        return redirect('home')
    return render(request, 'profile.html')

@login_required(login_url='login')
def edit_profile(request,id):
    profile=Profile.objects.get(id=id)
    user_data=profile.user
    if request.method == 'POST':
        temp_fname=request.POST.get('fname')
        temp_lname=request.POST.get('lname')
        temp_email=request.POST.get('email')
        temp_phone=request.POST.get('phone')
        temp_location=request.POST.get('place')
        temp_photo=request.FILES.get('photo')
        profile.phone=temp_phone
        profile.location=temp_location
        profile.photo=temp_photo
        user_data.email=temp_email
        user_data.first_name=temp_fname
        user_data.last_name=temp_lname
        user_data.save()
        profile.save()
        return redirect('profile_view')
    return render(request, 'edit_profile.html' ,{'profile':profile})

def generateotp():
    num=string.digits
    temp= random.sample(num,6)
    otp=''.join(temp)
    return otp

def send_mail_to_user(email,otp,username):
    subject= 'Your account need to be verify'
    message= f'Click the link "http://127.0.0.1:8000/verify/password/{username}/" , Please enter the OTP : {otp}' 
    from_email= 'email@example.com'
    recipient_list= [email]
    return send_mail(subject,message,from_email,recipient_list)


def forgot_password(request):
    if request.method == 'POST':
        user_email=request.POST.get('email')
        user= User.objects.filter(email=user_email).first()
        if user is not None:
            data=OTP.objects.filter(fk_user=user).first()
            if data:
                data.delete()
            new_otp=generateotp()
            OTP.objects.create(
                fk_user=user,
                otp=new_otp
            )
            send_mail_to_user(user_email,new_otp,user.username)
            return HttpResponse('Mail sent successfully')
                
        else:
            return HttpResponse('Invalid email address')   
    return render(request,'forgot_password.html')

def verify_password(request,username):
    if request.method == 'POST':
        otp=request.POST.get('otp')
        data=OTP.objects.filter(fk_user__username=username).first()
        if data:
            if data.otp == otp:
                return redirect('set_password',id=data.id)
            else:
                return HttpResponse("Invalid OTP")
        else:
            return HttpResponse('unauthorized')
        
    return render(request,'verify_password.html')

def set_new_password(request,id):
    data=OTP.objects.get(id=id)
    user=data.fk_user
    if request.method == 'POST':
        temp_pwd1=request.POST.get('new_password')
        temp_pwd2=request.POST.get('confirm_password')
        if temp_pwd1==temp_pwd2:
            user.set_password(temp_pwd1)
            user.save()
            data.delete()
            return redirect('login')
        else:
            return HttpResponse('password mismatch')
    return render(request,'set_password.html')