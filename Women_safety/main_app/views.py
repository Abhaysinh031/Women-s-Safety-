from django.shortcuts import render, redirect
from django.contrib.auth.forms import (
    PasswordChangeForm,
)
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib import messages
from .forms import ContactForm
from django.conf import settings
from .models import User, contact as Contact
from django.contrib.auth.models import User, auth
from .mail import send_email
from .whatsapp import send_whatsapp
from .location import lat , log
from .forms import UserCreateForm, LoginForm
from django.core.mail import EmailMessage
from django.views import View
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import account_activation_token
from django.http import JsonResponse
import json
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
import urllib
from django.shortcuts import render
import requests 
import json
from flask import Flask, render_template
from twilio.rest import Client
import logging



# Create your views here


def home(request):
    context = {}
    return render(request, "main_app/home.html", context)


def register(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")  # noqa
        password2 = request.POST.get("password2")  # noqa
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            user.is_active = False
            user.save()

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            link = reverse(
                "activate",
                kwargs={
                    "uidb64": uidb64,
                    "token": account_activation_token.make_token(user),
                },
            )

            activate_url = "http://" + domain + link

            email_subject = "Rescue - Activate you Account!"
            email_body = (
                "Hi  "
                + user.username  # noqa
                + "  ,  Please use this link to verify your account\n"  # noqa
                + activate_url  # noqa
            )
            email = EmailMessage(
                email_subject,
                email_body,
                "noreply@gmail.com",
                [email],
            )
            messages.success(request, f"New Account Created Successfully: {username}")
            messages.success(request, "Check your email to Activate your account!")
            email.send(fail_silently=False)
            return redirect('main_app:email_sent')
        elif User.objects.filter(username=username).exists():
            messages.warning(
                request,
                "The username you entered has already been taken. Please try another username",
            )
        elif User.objects.filter(email=email).exists():
            messages.warning(
                request,
                "The Email you entered has already been taken. Please try another Email",
            )
        elif user.exists():
            for msg in form.error_messages:
                messages.warning(request, f"{form.error_messages[msg]}")

    else:
        form = UserCreateForm()
    return render(request, "main_app/register.html", {"form": form})


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect(
                    "main_app:login" + "?message=" + "User already activated"
                )

            if user.is_active:
                return redirect("main_app:login")
            user.is_active = True
            user.save()

            messages.success(request, "Account activated successfully")
            return redirect("main_app:login")

        except Exception:
            pass

        return redirect("main_app:login")


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main_app:home")


def delete_account(request, username):
    try:
        user = User.objects.get(username=username)
        user.delete()
        messages.success(
            request, user.username + ", Your account is deleted successfully!"
        )

    except User.DoesNotExist:
        messages.error(request, "User doesnot exist")

    return redirect("main_app:home")

def login_request(request):
    form = LoginForm(request.POST)
    Username = request.POST.get("Username_or_Email")
    password = request.POST.get("password")
    if request.method == "POST":
        form = LoginForm(request.POST)
        username_or_email = request.POST.get("Username_or_Email")
        password = request.POST.get("password")

        if username_or_email and password:
            # Check if the input is a valid email address
            is_email = "@" in username_or_email
            if is_email:
                users = User.objects.filter(email=username_or_email)
            else:
                users = User.objects.filter(username=username_or_email)

            if users.exists():
                user = users.first()
                user = authenticate(username=user.username, password=password)

                if user:
                    if user.is_active:
                        login(request, user)
                        messages.success(
                            request, f"Welcome, {user.username}! You are now logged in."
                        )
                        return redirect("main_app:home")
                    else:
                        messages.error(request, "Account is not active. Please check your email.")
                else:
                    messages.error(request, "Invalid password")
            else:
                messages.error(request, "Invalid username or email")
        else:
            messages.error(request, "Both username/email and password are required")

    else:
        form = LoginForm()

    return render(request, "main_app/login.html", {"form": form})



def emergency_contact(request):
    users = User.objects.all()
    curr = 0
    for user in users:
        if request.user.is_authenticated:
            curr = user
            break
    if curr == 0:
        return redirect("main_app:login")
    contacts = Contact.objects.filter(user=request.user)
    total_contacts = contacts.count()
    context = {
        "contacts": contacts,
        "total_contacts": total_contacts,
        "user": request.user,
    }
    return render(request, "main_app/emergency_contact.html", context)


def create_contact(request):
    inst = Contact(user=request.user)
    form = ContactForm(instance=inst)
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
           form.save()
           contact_instance = form.save(commit=True)
           contact_instance.user = request.user
           contact_instance.save()
           
           messages.info(request, "New contact created successfully!!")
           messages.info(request, "An email has been sent to your contact!!")
           return redirect("main_app:emergency_contact") 
        else:
           print("Form errors:", form.errors)
           messages.error(request, "Invalid form submission. Please check the errors.")
    else:
        # Assuming you want to show a blank form for GET requests
        form = ContactForm()
        
    return render(request, "main_app/create_contact.html", {'form':form})



def update_contact(request, pk):
    curr_contact = Contact.objects.get(id=pk)
    name = curr_contact.name
    form = ContactForm(
        initial={
            "name": name,
            "email": curr_contact.email,
            "mobile_no": curr_contact.mobile_no,
            "relation": curr_contact.relation,
        }
    )
    if request.method == "POST":
        form = ContactForm(request.POST, instance=curr_contact)
        if form.is_valid():
            form.save()
            messages.error(request, f"{name} updated successfully!!")
            messages.info(request, "A message has been sent to your contact!!")
            return redirect("main_app:emergency_contact")
    context = {"form": form}
    return render(request, "main_app/create_contact.html", context)


def delete_contact(request, pk):
    curr_contact = Contact.objects.get(id=pk)
    name = curr_contact.name
    if request.method == "POST":
        curr_contact.delete()
        messages.error(request, f"{name} deleted successfully!!")
        return redirect("main_app:emergency_contact")
    context = {"item": curr_contact}
    return render(request, "main_app/delete_contact.html", context)

app = Flask(__name__)

THING_SPEAK_URL = "https://api.thingspeak.com/channels/2505252/feeds.json?api_key=9OOWPUGXMW56G6TB&results=1"

@app.route('/')

def index(request):
    data = fetch_data()
    return render(request, 'index.html', {'data': data})

def fetch_data():
    response = requests.get(THING_SPEAK_URL)
    if response.status_code == 200:
        data = json.loads(response.text)
        return data.get('feeds', [])[0] if 'feeds' in data else None
    return None


# def emergency(request):
#     users = User.objects.all()
#     curr = 0
#     for user in users:
#         if request.user.is_authenticated:
#             curr = user
#             break
#     if curr == 0:
#         return redirect("main_app:login")
#     contacts = contact.objects.filter(user=request.user)
#     total_contacts = contacts.count()
#     context = {
#         "contacts": contacts,
#         "total_contacts": total_contacts,
#         "user": request.user,
        

#     }
#     emails, mobile_numbers = [], []
#     for j in contacts:
#         emails.append(j._meta.get_field("email"))
#         mobile_numbers.append(str(j.mobile_no).replace(" ", ""))
#     name = request.user.username
#     link = "http://www.google.com/maps/place/" + "19.449711783793365" + "," + "73.36758829603433"
#     data= fetch_data()
#     for c in contacts:
#         send_email(name, c.email, link, data)
#         messages.success(request,f"Email deleiverd to {name} at {c.email}")
        
#     try:
#         send_whatsapp(mobile_numbers, name, data,link)
#         messages.success(request,f"Message deleivered to {name} at {mobile_numbers}")
          
#     except:  # noqa
#         messages.warning(
#             request, "your contact numbers contains number without country code."
#         )
        
#     data = fetch_data()
#     return render(request, "main_app/index.html", {'data': data},)

logger = logging.getLogger(__name__)
def emergency(request):
    if not request.user.is_authenticated:
        return redirect("main_app:login")

    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message_body = """🚨🛑 *Emergency* 🛑🚨is in emergency and need your help immediately.  Click the link below for location """
    link = "http://www.google.com/maps/place/" + lat + "," + log
    full_message = f"{message_body}: {link}"
    contacts = Contact.objects.filter(user=request.user)
    total_contacts = contacts.count()

    # Initialize lists for emails and mobile numbers
    emails, mobile_numbers = [], []

    # Iterate over contacts to send SMS and collect emails and mobile numbers
    for contact in contacts:
        mobile_no = contact.mobile_no.strip().replace(" ", "")
        if not mobile_no.startswith("+"):
            mobile_no = f"+{mobile_no}"  # Assuming a default country code prefix

        try:
            client.messages.create(
                body=full_message,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=mobile_no
            )
            messages.success(request, f"SMS sent to {mobile_no}")
        except Exception as e:
            logger.error(f"Failed to send SMS to {mobile_no}: {str(e)}")
            messages.error(request, f"Failed to send SMS to {mobile_no}: {str(e)}")
        
        
        emails.append(contact.email)
        mobile_numbers.append(mobile_no)

    # Send emails and WhatsApp messages
    name = request.user.username
    link = "http://www.google.com/maps/place/" + lat + "," + log
    data = fetch_data()

    for email in emails:
        try:
            send_email(name, email, link, data)
            messages.success(request, f"Email delivered to {name} at {email}")
        except Exception as e:
            logger.error(f"Failed to send email to {email}: {str(e)}")
            messages.error(request, f"Failed to send email to {email}: {str(e)}")


    try:
        send_whatsapp(mobile_numbers, name, data, link)
        messages.success(request, f"WhatsApp message delivered to {name} at {mobile_numbers}")
    except Exception as e:
        logger.error(f"Error in sending WhatsApp messages: {str(e)}")
        messages.warning(request, f"Error in sending WhatsApp messages: {str(e)}")

    context = {
        "contacts": contacts,
        "total_contacts": total_contacts,
        "user": request.user,
        "data": data,
    }

    return render(request, "main_app/index.html", context)


THING_SPEAK_URL = "https://api.thingspeak.com/channels/2505252/feeds.json?api_key=9OOWPUGXMW56G6TB&results=1"





def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, "Your password was successfully updated!")
            return redirect("main_app:home")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{form.error_messages[msg]}")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "main_app/change_password.html", {"form": form})


def helpline_numbers(request):
    return render(
        request, "main_app/helpline_numbers.html", {"title": "helpline_numbers"}
    )


def ngo_details(request):
    return render(request, "main_app/ngo_details.html", {"title": "ngo_details"})


def gallery(request):
    return render(request, "main_app/gallery.html", {"title": "Gallery"})


def FAQ(request):
    return render(request, "main_app/FAQ.html", {"title": "FAQ"})


def women_laws(request):
    return render(request, "main_app/women_laws.html", {"title": "women_laws"})



def women_rights(request):
    return render(request, "main_app/women_rights.html", {"title": "women_rights"})


def page_not_found(request, exception):
    return render(request, "main_app/404.html")


def check_username(request):
    username = request.GET.get("name")
    if User.objects.filter(username=username).exists():
        return JsonResponse({"exists": "yes"})
    return JsonResponse({"exists": "no"})


def check_email(request):
    email = request.GET.get("email")
    if User.objects.filter(email=email).exists():
        return JsonResponse({"exists": "yes"})
    return JsonResponse({"exists": "no"})


def contact_user(request):
    if request.method == "POST":
        message_name = request.POST["message-name"]
        message_email = request.POST["message-email"]
        message = request.POST["message"]

        # send an email
        send_email(  # noqa
            message_name,  # subject
            message,  # message
            message_email,  # from email
            ["rescue@gmail.com"],  # To Email
        )

        return render(
            request, "main_app/contact_user.html", {"message_name": message_name}
        )

    else:
        return render(request, "main_app/contact_user.html", {})
