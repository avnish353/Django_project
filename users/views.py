import random
from django.shortcuts import render,redirect
from users.forms import CustRegistrationForm
from django.contrib import messages
from django.contrib.auth.models import User
from users.models import Profile
from django.core.mail import send_mail
from django.contrib import messages
from django.utils.timezone import now
from datetime import timedelta
from users.models import PasswordResetOTP
from users.forms import EmailForm, OTPPasswordResetForm

def register(request):
    if request.method == "POST":
        register_form = CustRegistrationForm(request.POST)
        if register_form.is_valid():
            user=register_form.save()
            country_code = register_form.cleaned_data.get('country_code')
            mobile = register_form.cleaned_data.get('mobile')
            full_mobile = f"{country_code}{mobile}"
            Profile.objects.create(user=user, mobile=mobile)
            messages.success(request, "Account created successfully!")
            return redirect("menu")
    else:
        register_form = CustRegistrationForm()
    return render(request, 'register.html', {'register_form':register_form})

def send_otp(request):
    form = EmailForm()
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            try:
                user = User.objects.get(email=email)
                otp = str(random.randint(100000, 999999))

                PasswordResetOTP.objects.create(user=user, otp=otp)

                send_mail(
                    "SmartCanteen Password Reset OTP",
                    f"Your OTP is {otp}. It is valid for 5 minutes.",
                    "noreply@smartcanteen.com",
                    [email],
                )

                request.session["reset_user"] = user.id
                return redirect("verify_otp")

            except User.DoesNotExist:
                messages.error(request, "Email not registered")

    return render(request, "password_reset_email.html", {"form": form})

def verify_otp(request):
    user_id = request.session.get("reset_user")
    if not user_id:
        return redirect("send_otp")

    form = OTPPasswordResetForm()
    if request.method == "POST":
        form = OTPPasswordResetForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data["otp"]
            new_password = form.cleaned_data["new_password"]

            otp_obj = PasswordResetOTP.objects.filter(
                user_id=user_id,
                otp=otp,
                created_at__gte=now() - timedelta(minutes=5)
            ).first()

            if otp_obj:
                user = otp_obj.user
                user.set_password(new_password)
                user.save()

                PasswordResetOTP.objects.filter(user=user).delete()
                del request.session["reset_user"]

                messages.success(request, "Password reset successful")
                return redirect("login")
            else:
                messages.error(request, "Invalid or expired OTP")

    return render(request, "password_reset_otp.html", {"form": form})


