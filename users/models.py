from django.db import models


# Create your models here.
class UserRegistrationModel(models.Model):
    name = models.CharField(max_length=100)
    loginid = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=100)
    mobile = models.CharField(unique=True, max_length=100)
    email = models.CharField(unique=True, max_length=100)
    locality = models.CharField(max_length=100)
    address = models.CharField(max_length=1000)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.loginid

    class Meta:
        db_table = 'UserRegistrations'


class DoctorRegistrationModel(models.Model):
    doctorName = models.CharField(max_length=100)
    mobile = models.CharField(unique=True, max_length=100)
    email = models.CharField(unique=True, max_length=100)
    doctorQualification = models.CharField(max_length=100)
    experience = models.CharField(max_length=1000)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.doctorName

    class Meta:
        db_table = 'DoctorTable'


class PatientModel(models.Model):
    loginid = models.CharField(max_length=100)
    patientName = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    doctor = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    patientEmail = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    fileName = models.CharField(max_length=100)
    file = models.FileField(upload_to='files/')
    cdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.patientName

    class Meta:
        db_table = 'PatientTable'


class BlockChainTransactionModel(models.Model):
    c_index = models.CharField(max_length=100)
    c_timestamp = models.CharField(max_length=100)
    c_sender = models.CharField(max_length=100)
    c_recipient = models.CharField(max_length=100)
    c_vote = models.CharField(max_length=100)
    c_proof = models.CharField(max_length=100)
    c_previous_hash = models.CharField(max_length=100)
    p_index = models.CharField(max_length=100)
    p_timestamp = models.CharField(max_length=100)
    p_sender = models.CharField(max_length=100)
    p_recipient = models.CharField(max_length=100)
    p_vote = models.CharField(max_length=100)
    p_proof = models.CharField(max_length=100)
    p_previous_hash = models.CharField(max_length=100)

    def __str__(self):
        return self.id

    class Meta:
        db_table = "BlockChainTransactiontable"
