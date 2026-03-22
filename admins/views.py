from django.shortcuts import render, HttpResponse
from django.contrib import messages
from users.models import UserRegistrationModel, DoctorRegistrationModel, BlockChainTransactionModel


# Create your views here.
def AdminLoginCheck(request):
    if request.method == 'POST':
        usrid = request.POST.get('loginid')
        pswd = request.POST.get('pswd')
        print("User ID is = ", usrid)
        if usrid == 'admin' and pswd == 'admin':
            return render(request, 'admins/AdminHome.html')

        else:
            messages.success(request, 'Please Check Your Login Details')
    return render(request, 'AdminLogin.html', {})


def AdminHome(request):
    return render(request, 'admins/AdminHome.html')


def RegisterUsersView(request):
    data = UserRegistrationModel.objects.all()
    return render(request, 'admins/viewregisterusers.html', {'data': data})


def ActivaUsers(request):
    if request.method == 'GET':
        id = request.GET.get('uid')
        status = 'activated'
        print("PID = ", id, status)
        UserRegistrationModel.objects.filter(id=id).update(status=status)
        data = UserRegistrationModel.objects.all()
        return render(request, 'admins/viewregisterusers.html', {'data': data})


def AddDoctorsandView(request):
    if request.method == 'POST':
        doctorName = request.POST.get('doctorName')
        doctorQualification = request.POST.get('doctorQualification')
        experience = request.POST.get('experience')
        address = request.POST.get('address')
        doctorEmail = request.POST.get('doctorEmail')
        mobile = request.POST.get('mobile')
        DoctorRegistrationModel.objects.create(doctorName=doctorName, mobile=mobile, email=doctorEmail,
                                               doctorQualification=doctorQualification, experience=experience,
                                               address=address)
        data = DoctorRegistrationModel.objects.all()
        return render(request, 'admins/addCliniciansandView.html', {'data': data})

    else:
        data = DoctorRegistrationModel.objects.all()
        return render(request, 'admins/addCliniciansandView.html', {'data': data})


def DeleteDoctor(request):
    if request.method == 'GET':
        id = request.GET.get('uid')
        DoctorRegistrationModel.objects.filter(id=id).delete()
        data = DoctorRegistrationModel.objects.all()
        return render(request, 'admins/addCliniciansandView.html', {'data': data})


def AdminBlockChain(request):
    data = BlockChainTransactionModel.objects.all()
    return render(request, 'admins/viewblockchainNode.html', {'data': data})



