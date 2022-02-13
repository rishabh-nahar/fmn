from unicodedata import category
from django.db import IntegrityError
from django.shortcuts import redirect, render
from  django.contrib import messages
from backend.models import extra_details, register_user, file_upload
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
import random
from django.core.files.storage import FileSystemStorage


def home(request):
    if request.method == "POST":
        search = request.POST['searchnote']
        return redirect(searched_page,search)
    return render(request,"home.html",{
        'username':request.session.get("username"),
        'user_unique_id':request.session.get('user_unique_id'),
        })

def profile(request):
    profile_user_details = register_user.objects.get(username = request.session.get("username"))
    # profile_extra_details = extra_details.objects.get(user_id = request.session.get("user_unique_id"))
    return render(request,'profile.html',{
        'user_details': profile_user_details,
        'username':request.session.get("username"),
        'user_unique_id':request.session.get('user_unique_id')
        # 'extra_details':profile_extra_details,
        })
def feed(request):
    profile_user_details = register_user.objects.get(username = request.session.get("username"))
    uploaded_images = file_upload.objects.filter(user_id = request.session.get("user_unique_id"),file_type = "image")
    uploaded_pdfs = file_upload.objects.filter(user_id = request.session.get("user_unique_id"),file_type = "pdf")
    uploaded_videos = file_upload.objects.filter(user_id = request.session.get("user_unique_id"),file_type = "video")

    return render(request,'feed.html',{
        'user_details': profile_user_details,
        'username':request.session.get("username"),
        'user_unique_id':request.session.get('user_unique_id'),
        'uploaded_images':uploaded_images,
        'uploaded_pdfs':uploaded_pdfs,
        'uploaded_videos':uploaded_videos,
        })

def registration(request):

    if request.method == "POST":
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        gender = request.POST['gender'] 
        mail = request.POST['mail'] 
        phone = request.POST['phone'] 
        username = request.POST['username'] 
        password = request.POST['password'] 
        print(username)
        exists_username = register_user.objects.filter(username = username).count()
        exists_email = register_user.objects.filter(mail = mail).count()
        if exists_username > 0:
            print("username error")
            messages.error(request,"Username Exist")
        elif exists_email > 0:
            print("email error")
            messages.error(request,"Email Exist")
        else:
            users = register_user.objects.create(
                first_name=first_name,
                last_name=last_name,
                gender = gender,
                mail = mail,
                phone = phone,
                username = username,
                password = password,
                )
            users.save()
            # We will load the html content first
            random_num = random.randint(1000,9999)

            html_content = render_to_string("mail_template.html", {'name': first_name ,'otp':random_num })

            # html content jo load karenge usme se HTML tags nikal denge
            text_content = strip_tags(html_content)
            mail = EmailMultiAlternatives(  # Initialize a single email message (which can be sent to multiple recipients).
                # subject
                "Please Verify Your Account",
                # content
                text_content,
                # from email
                'findmynotes2002@gmail.com',
                # receipient list
                [mail]
            )

            # attach the html content
            mail.attach_alternative(html_content, "text/html")
            mail.send()
            request.session["new_user"] = username
            request.session["new_user_id"] = users.unique_id
            request.session["new_otp"] = random_num

            extra_details.objects.create(
                user_id = register_user.objects.get(username = username)
            )
            return redirect(otp_page)
    return render(request,"registration.html")

def otp_page(request):
    if request.method == "POST":
        input_otp = request.POST['opt_input']
        if input_otp == str(request.session.get('new_otp')):
            set_active = register_user.objects.get(username = request.session.get("new_user"))
            set_active.is_active = True
            set_active.save()
            messages.success(request,"valid OTP")
            request.session['username'] = request.session.get("new_user")
            request.session['user_unique_id'] = request.session.get("new_user_id")
            return redirect(home)
        else:
            messages.error(request,"Invalid OTP")
    return render(request,"otp_page.html")

def search_page(request):
    if request.method == "POST":
        search = request.POST['searchnote']
        return redirect(searched_page,search)

    return render(request,'search.html',{
        'username':request.session.get("username"),
        'user_unique_id':request.session.get('user_unique_id'),
        })

def searched_page(self,search_obj=None):

    if self.method == "POST":
        search = self.POST['searchnote']
        return redirect(searched_page,search)
    
    searched_result_pdf = file_upload.objects.filter(category = search_obj , file_type = 'pdf')
    searched_result_image = file_upload.objects.filter(category = search_obj , file_type = 'image')
    searched_result_video = file_upload.objects.filter(category = search_obj , file_type = 'video')
    return render(self,'search.html',{
        'username':self.session.get("username"),
        'user_unique_id':self.session.get('user_unique_id'),
        'search_obj_pdf':searched_result_pdf,
        'search_obj_image':searched_result_image,
        'search_obj_video':searched_result_video,
        })

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        try:
            user_obj =  register_user.objects.get(username = username)
            if user_obj.is_active == True:
                if user_obj.password == str(password):
                    messages.error(request,"Valid Password")
                    request.session['username'] = username
                    request.session['user_unique_id'] = user_obj.unique_id
                    return redirect(home)
                else:
                    messages.error(request,"Invalid Password")
            elif user_obj.is_active == False and user_obj.password == str(password):
                try:
                    random_num = random.randint(1000,9999)
                    mail = user_obj.mail
                    html_content = render_to_string("mail_template.html", {'otp':random_num })
                    text_content = strip_tags(html_content)
                    mail = EmailMultiAlternatives(  # Initialize a single email message (which can be sent to multiple recipients).
                        # subject
                        "Please Verify Your Account first",
                        # content
                        text_content,
                        # from email
                        'findmynotes2002@gmail.com',
                        # receipient list
                        [mail]
                    )
                    # attach the html content
                    mail.attach_alternative(html_content, "text/html")
                    mail.send()
                    request.session["new_user"] = username
                    request.session["new_user_id"] = user_obj.unique_id
                    request.session["new_otp"] = random_num
                    return redirect(otp_page)
                except:
                    messages.error(request,"Error: please try again")
            else:
                messages.error(request,"Error: try again")
        
        except:
            messages.error(request,"Bad credentials")
            user_obj = None

    return render(request,"login.html")

def upload(request):
    profile_user_details = register_user.objects.get(username = request.session.get("username"))

    if request.method == "POST":
        file = request.FILES['file_data']
        file_type = request.POST['file_type']
        fs = FileSystemStorage(location= 'files/'+str(request.session['user_unique_id'])+"/"+file_type+"/")
        file_details = file_upload.objects.create(
            file_type = file_type , 
            file_name = file.name,
            category = request.POST['category'],
            file_url = str(request.session['user_unique_id'])+"/"+file_type+"/"+file.name,
            user_id = register_user.objects.get(username = request.session.get("username"))
            )
        file_details.save()
        fs.save(file.name,file)

    return render(request,"upload.html",{
        'username':request.session.get("username"),
        'user_unique_id':request.session.get('user_unique_id')
        }) 


def approve_file(request):
    profile_user_details = register_user.objects.get(username = request.session.get("username"))
    uploaded_images = file_upload.objects.filter(file_type = "image" , is_appropriate = False)
    uploaded_pdfs = file_upload.objects.filter(file_type = "pdf" , is_appropriate = False)
    uploaded_videos = file_upload.objects.filter(file_type = "video" , is_appropriate = False)

    if request.method == "POST":
        user_id = request.POST['unique_id']
        file_url = request.POST['file_url']
        is_appropriate = request.POST['is_appropriate']
        selected_file = file_upload.objects.get(user_id = user_id, file_url = file_url)
        selected_file.is_appropriate = is_appropriate
        print(is_appropriate + user_id)
        selected_file.save()
    
    return render(request,'approve_file.html',{
        'user_details': profile_user_details,
        'username':request.session.get("username"),

        'user_unique_id':request.session.get('user_unique_id'),
        'uploaded_images':uploaded_images,
        'uploaded_pdfs':uploaded_pdfs,
        'uploaded_videos':uploaded_videos,
        })


def logout(request):
    request.session.delete()
    return redirect('/')