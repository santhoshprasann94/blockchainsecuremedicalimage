from django.shortcuts import render
from users.models import DoctorRegistrationModel,PatientModel
from django.contrib import messages
import random


# Create your views here.


def DoctorLoginCheck(request):
    if request.method == "POST":
        mobile = request.POST.get('mobile')

        try:
            check = DoctorRegistrationModel.objects.get(mobile=mobile)
            if check.id:
                request.session['id'] = check.id
                request.session['email'] = check.email
                request.session['loginid'] = check.doctorName
                request.session['email'] = check.email
                otp = ''.join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])
                print("OTP:", otp)
                request.session['originalOtp'] = otp
                return render(request, 'otpCheck.html', {})
            else:
                messages.success(request, 'Invalid Mobile Number')
                return render(request, 'DoctorLogin.html')
        except Exception as e:
            messages.success(request, 'Invalid Mobile Number')
            pass
        # messages.success(request, 'Invalid Mobile')
    return render(request, 'DoctorLogin.html', {})


def drOtpCheck(request):
    if request.method == 'POST':
        brOtp = request.POST.get('brotp')
        originalOtp = request.session['originalOtp']
        if originalOtp == brOtp:
            return render(request, 'dctrs/doctorHome.html',{})
        else:
            messages.success(request, 'Invalid OPT')
            return render(request, 'DoctorLogin.html')


def DoctorHome(request):
    return render(request, 'dctrs/doctorHome.html', {})


def ViewMedicalInfo(request):
    loginid = request.session['loginid']
    data = PatientModel.objects.filter(doctor=loginid)
    return render(request, 'dctrs/viewPatients.html', {'data': data})
