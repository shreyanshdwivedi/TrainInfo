from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(label='username', max_length=200)
    email = forms.CharField(max_length=200)
    password = forms.CharField(label='password', max_length=200)

class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=200)
    password = forms.CharField(label='password', max_length=200)
    keep_logged_in = forms.CharField(label='keep_logged_in')

class trainStatus(forms.Form):
    train_number = forms.CharField(max_length=10)
    date = forms.CharField(max_length=10)

class pnrStatus(forms.Form):
    pnr_number = forms.CharField(max_length=20)

class seatAvailability(forms.Form):
    train_number = forms.CharField(max_length=10)
    source_code = forms.CharField(max_length=10)
    dest_code = forms.CharField(max_length=10)
    class_code = forms.CharField(max_length=10)
    quota_code = forms.CharField(max_length=10)
    date = forms.CharField(max_length=10)

class trainBWstation(forms.Form):
    source_code = forms.CharField(max_length=10)
    dest_code = forms.CharField(max_length=10)
    date = forms.CharField(max_length=10)

class fareEnquiry(forms.Form):
    train_number = forms.CharField(max_length=10)
    source_code = forms.CharField(max_length=10)
    dest_code = forms.CharField(max_length=10)
    quota_code = forms.CharField(max_length=10)
    age = forms.CharField(max_length=3)
    date = forms.CharField(max_length=10)

class liveStation(forms.Form):
    station_code = forms.CharField(max_length=10)
    hours = forms.CharField(max_length=1)

class cancelledTrain(forms.Form):
    date = forms.CharField(max_length=10)

class rescheduledTrain(forms.Form):
    date = forms.CharField(max_length=10)

class Info(forms.Form):
    info = forms.CharField(max_length=10)