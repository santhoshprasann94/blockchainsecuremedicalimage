# Create your views here.
from django.shortcuts import render, HttpResponse
from django.contrib import messages
from .forms import UserRegistrationForm
from .models import UserRegistrationModel, DoctorRegistrationModel, PatientModel, BlockChainTransactionModel
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import numpy as np
import random
import os
from .blkchain import Blockchain
from datetime import datetime
import json

blockchain = Blockchain()


# Create your views here.
def UserRegisterActions(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print('Data is Valid')
            form.save()
            messages.success(request, 'You have been successfully registered')
            form = UserRegistrationForm()
            return render(request, 'UserRegistrations.html', {'form': form})
        else:
            messages.success(request, 'Email or Mobile Already Existed')
            print("Invalid form")
    else:
        form = UserRegistrationForm()
    return render(request, 'UserRegistrations.html', {'form': form})


def UserLoginCheck(request):
    if request.method == "POST":
        loginid = request.POST.get('loginid')
        pswd = request.POST.get('pswd')
        print("Login ID = ", loginid, ' Password = ', pswd)
        try:
            check = UserRegistrationModel.objects.get(loginid=loginid, password=pswd)
            status = check.status
            print('Status is = ', status)
            if status == "activated":
                request.session['id'] = check.id
                request.session['loggeduser'] = check.name
                request.session['loginid'] = loginid
                request.session['email'] = check.email
                print("User id At", check.id, status)
                return render(request, 'users/UserHomePage.html', {})
            else:
                messages.success(request, 'Your Account Not at activated')
                return render(request, 'UserLogin.html')
        except Exception as e:
            print('Exception is ', str(e))
            pass
        messages.success(request, 'Invalid Login id and password')
    return render(request, 'UserLogin.html', {})


def UserHome(request):
    return render(request, 'users/UserHomePage.html', {})


def AddMedicalData(request):
    if request.method == 'POST':
        patientName = request.POST.get('patientName')
        department = request.POST.get('dpts')
        doctor = request.POST.get('doctor')
        address = request.POST.get('address')
        patientEmail = request.POST.get('patientEmail')
        mobile = request.POST.get('mobile')
        print(f"{patientName},{department},Doctor:{doctor}")
        image_file = request.FILES['file']
        fs = FileSystemStorage(location="media/files/")
        filename = fs.save(image_file.name, image_file)
        uploaded_file_url = "/media/files/" + filename  # fs.url(filename)
        print("Image path ", uploaded_file_url)
        loc = settings.MEDIA_ROOT + '\\' + 'files'
        filepath = os.path.join(loc, filename)
        loginid = request.session['loginid']

        from .utility.cloudUploads import user_input
        # user_input(filename)
        PatientModel.objects.create(loginid=loginid, patientName=patientName,
                                    department=department, doctor=doctor,
                                    address=address, patientEmail=patientEmail, mobile=mobile,
                                    fileName=filename, file=filepath)

        t1 = blockchain.new_transaction(loginid, doctor, 1)
        proofId = ''.join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])
        blockchain.new_block(int(proofId))
        print("Genesis block: ", blockchain.chain)
        print("T1 is ", t1)
        currentTrnx = blockchain.chain[-1]
        previousTranx = blockchain.chain[-2]
        ### Current Tranasction Details
        c_transactions = currentTrnx.get('transactions')
        c_tnx_Dict = c_transactions[0]
        c_index = currentTrnx.get('index')
        c_timestamp = currentTrnx.get('timestamp')
        c_timestamp = datetime.fromtimestamp(c_timestamp)
        c_sender = c_tnx_Dict.get('sender')
        c_recipient = c_tnx_Dict.get('recipient')
        c_vote = c_tnx_Dict.get('vote')
        c_proof = currentTrnx.get('proof')
        c_previous_hash = currentTrnx.get('previous_hash')
        try:
            c_dict_rslt = {'c_index': c_index, 'c_timestamp': c_timestamp, 'c_sender': c_sender,
                           'c_recipient': c_recipient, 'c_vote': c_vote, 'c_proof': c_proof,
                           'c_previous_hash': c_previous_hash}

            # previous Transaction
            p_dict_rslt = {}
            p_transactions = previousTranx.get('transactions')

            if (len(p_transactions) != 0):
                p_tnx_Dict = p_transactions[0]
                p_index = previousTranx.get('index')
                p_timestamp = previousTranx.get('timestamp')
                p_timestamp = datetime.fromtimestamp(p_timestamp)
                p_sender = p_tnx_Dict.get('sender')
                p_recipient = p_tnx_Dict.get('recipient')
                p_vote = p_tnx_Dict.get('vote')
                p_proof = previousTranx.get('proof')
                p_previous_hash = previousTranx.get('previous_hash')

                p_dict_rslt = {'p_index': p_index, 'p_timestamp': p_timestamp, 'p_sender': p_sender,
                               'p_recipient': p_recipient, 'p_vote': p_vote, 'p_proof': p_proof,
                               'p_previous_hash': p_previous_hash}
                BlockChainTransactionModel.objects.create(c_index=c_index, c_timestamp=c_timestamp,
                                                          c_sender=c_sender,
                                                          c_recipient=c_recipient, c_vote=c_vote, c_proof=c_proof,
                                                          c_previous_hash=c_previous_hash, p_index=p_index,
                                                          p_timestamp=p_timestamp, p_sender=p_sender,
                                                          p_recipient=p_recipient, p_vote=p_vote, p_proof=p_proof,
                                                          p_previous_hash=p_previous_hash)
            else:

                BlockChainTransactionModel.objects.create(c_index=c_index, c_timestamp=c_timestamp,
                                                          c_sender=c_sender,
                                                          c_recipient=c_recipient, c_vote=c_vote, c_proof=c_proof,
                                                          c_previous_hash=c_previous_hash, p_index='p_index',
                                                          p_timestamp='p_timestamp', p_sender='p_sender',
                                                          p_recipient="p_recipient", p_vote="p_vote",
                                                          p_proof="p_proof",
                                                          p_previous_hash="p_previous_hash")
        except Exception as ex:
            print(ex)
        return render(request, 'users/UploadForm.html', {'msg': 'Success'})

    else:
        return render(request, 'users/UploadForm.html', {})


def get_doctors(request):
    if request.method == 'GET':
        department = request.GET.copy().get('department')
        print(department)
        context = dict()
        if department and DoctorRegistrationModel.objects.filter(doctorQualification=department).exists:
            data = DoctorRegistrationModel.objects.filter(doctorQualification=department)

        result_list = list(data.values('doctorName'))
        # print('What is Data', data, result_list)
        return HttpResponse(json.dumps(result_list))


def UserViewPatients(request):
    loginid = request.session['loginid']
    data = PatientModel.objects.filter(loginid=loginid)
    return render(request, 'users/viewPatients.html', {'data': data})


