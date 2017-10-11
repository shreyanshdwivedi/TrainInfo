from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import User
from .forms import LoginForm, RegisterForm, trainStatus, pnrStatus, seatAvailability,trainBWstation, fareEnquiry, liveStation, Info, cancelledTrain, rescheduledTrain
import datetime
import requests
import json
from urllib.request import urlopen

def index(request):
    return render(request, 'trainapp/live_status.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            if username is None:
                error_msg = "Please enter the username"
                return render(request, 'social/register.html', {'error_msg':error_msg, 'form':form})
            elif User.objects.filter(username=username).exists():
                error_msg = "Username already exists"
                return render(request, 'social/register.html', {'error_msg': error_msg, 'form': form})
            elif User.objects.filter(email=email).exists():
                error_msg = "You are already registered user"
                return render(request, 'social/register.html', {'error_msg': error_msg, 'form': form})
            else:
                newUser = User.objects.create(username=username, email=email, password=password)
                success_msg = "Thank You for registering!!"
                return render(request, 'social/login.html', {'success_msg':success_msg})
        else:
            error_msg = "Enter all the details correctly"
            return render(request, 'social/register.html', {'error_msg': error_msg, 'form': form})
    else:
        form = RegisterForm()
        return render(request, 'social/register.html', {'form': form})

def login(request):
    if 'is_logged_in' not in request.session or request.session['is_logged_in'] == False:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                keep_logged_in = form.cleaned_data['keep_logged_in']
                if User.objects.filter(username=username).exists():
                    if User.objects.get(username=username).password == password:
                        userid = User.objects.get(username=username).id
                        request.session['user_id'] = userid
                        request.session['is_logged_in'] = True
                        if keep_logged_in == False:
                            request.session.set_expiry(0)
                        else:
                            request.session.set_expiry(130000000)
                        return render(request, 'trainapp/index.html')
                    else:
                        error_msg = "Incorrect credentials"
                        return render(request, 'social/login.html', {'error_msg': error_msg, 'form': form})
                else:
                    error_msg = "Username does not exists!"
                    return render(request, 'social/login.html', {'error_msg': error_msg, 'form': form})
            else:
                error_msg = "Error vaild form!"
                return render(request, 'social/login.html', {'error_msg':error_msg ,'form': form})
        else:
            form = LoginForm()
            return render(request, 'social/login.html', {'form': form})
    else:
        if request.session['is_logged_in']==True:
            return HttpResponseRedirect(reverse('social:index'))
        else:
            form = LoginForm()
            return render(request, 'social/login.html', {'form':form})

def logout(request):
    request.session['is_logged_in'] = False
    return HttpResponseRedirect(reverse('social:login'))

def live_status(request):
    if request.method == 'POST':
        form = trainStatus(request.POST)
        if form.is_valid():
            train_number = form.cleaned_data['train_number']
            date = form.cleaned_data['date']
            apikey = "6a721e3ch2"
            jsonList = []
            req = requests.get("http://api.railwayapi.com/v2/live/train/%s/date/%s/apikey/%s/"%(train_number, date, apikey))
            if req:
                jsonList.append(json.loads(req.content))
                traindata = {}
                trainroute ={}
                for data in jsonList:
                    traindata['train_number'] = data['train_number']
                    traindata['name'] = data['train']['name']
                    traindata['debit'] = data['debit']
                    trainroute['route'] = data['route']
                return render(request, 'trainapp/live_status.html', { 'trainData':traindata, 'trainRoute':trainroute })
            else:
                error_msg = "Train Number does not exists"
                return render(request, 'trainapp/live_status.html', {'error_msg': error_msg})
        else:
            error_msg = "Form validation error!!"
            return render(request, 'trainapp/live_status.html', {'error_msg': error_msg})
    else:
        form = trainStatus()
        return render(request, 'trainapp/live_status.html', {'form': form})

def pnr_status(request):
    if request.method == 'POST':
        form = pnrStatus(request.POST)
        if form.is_valid():
            pnr_number = form.cleaned_data['pnr_number']
            apikey = "6a721e3ch2"
            jsonList = []
            req = requests.get("http://api.railwayapi.com/v2/pnr-status/pnr/%s/apikey/%s/"%(pnr_number, apikey))
            if req:
                jsonList.append(json.loads(req.content))
                return render(request, 'trainapp/pnr_status.html', { 'pnrData':jsonList })
            else:
                error_msg = "Train Number does not exists"
                return render(request, 'trainapp/pnr_status.html', {'error_msg':error_msg})
        else:
            error_msg = "Form validation error!!"
            return render(request, 'trainapp/pnr_status.html', {'error_msg': error_msg})
    else:
        form = pnrStatus()
        return render(request, 'trainapp/pnr_status.html', {'form': form})

def train_route(request):
    if request.method == 'POST':
        form = trainStatus(request.POST)
        if form.is_valid():
            train_number = form.cleaned_data['train_number']
            d = datetime.date.today()
            date = str(d.strftime('%d-%m-%Y'))
            apikey = "6a721e3ch2"
            jsonList = []
            req = requests.get("http://api.railwayapi.com/v2/route/train/%s/apikey/%s/"%(train_number, apikey))
            if req:
                jsonList.append(json.loads(req.content))
                traindata = {}
                trainroute = {}
                for data in jsonList:
                    traindata['train'] = data['train']
                    trainroute['route'] = data['route']
                return render(request, 'trainapp/train_route.html', {'trainRoute':trainroute, 'trainData':traindata})
            else:
                error_msg = "Train Number does not exists"
                return render(request, 'trainapp/train_route.html', {'error_msg':error_msg})
        else:
            error_msg = "Form validation error!!"
            return render(request, 'trainapp/train_route.html', {'error_msg': error_msg})
    else:
        form = trainStatus()
        return render(request, 'trainapp/train_route.html', {'form': form})

def train_auto(request):
    if request.method == 'POST':
        form = Info(request.POST)
        if form.is_valid():
            info = form.cleaned_data['info']
            apikey = "6a721e3ch2"

            jsonList = []
            req = requests.get("http://api.railwayapi.com/v2/suggest-train/train/%s/apikey/%s/"%(info, apikey))
            jsonList.append(json.loads(req.content))
            return render(request, 'trainapp/train_auto.html', {'train_info':jsonList})
        else:
            error_msg = "Form validation error!!"
            return render(request, 'trainapp/train_auto.html', {'error_msg': error_msg})
    else:
        form = Info()
        return render(request, 'trainapp/train_auto.html', {'form': form})

def station_auto(request):
    if request.method == 'POST':
        form = Info(request.POST)
        if form.is_valid():
            info = form.cleaned_data['info']
            apikey = "6a721e3ch2"

            jsonList = []
            req = requests.get("http://api.railwayapi.com/v2/suggest-station/name/%s/apikey/%s/" % (info, apikey))
            jsonList.append(json.loads(req.content))
            return render(request, 'trainapp/station_auto.html', {'station_info': jsonList})
        else:
            error_msg = "Form validation error!!"
            return render(request, 'trainapp/station_auto.html', {'error_msg': error_msg})
    else:
        form = Info()
        return render(request, 'trainapp/station_auto.html', {'form': form})


def seat_availability(request):
    if request.method == 'POST':
        form = seatAvailability(request.POST)
        if form.is_valid():
            train_number = form.cleaned_data['train_number']
            source_code = form.cleaned_data['source_code']
            dest_code = form.cleaned_data['dest_code']
            class_code = form.cleaned_data['class_code']
            quota_code = form.cleaned_data['quota_code']
            date = form.cleaned_data['date']
            apikey = "6a721e3ch2"
            jsonList = []
            req = requests.get("http://api.railwayapi.com/v2/check-seat/train/%s/source/%s/dest/%s/date/%s/class/%s/quota/%s/apikey/%s/"%(train_number, source_code, dest_code, date, class_code, quota_code, apikey))
            if req:
                jsonList.append(json.loads(req.content))
                seat_availability = {}
                train_data = {}
                for data in jsonList:
                    seat_availability['availability'] = data['availability']
                    train_data = data['train']
                return render(request, 'trainapp/seat_availability.html', {'seat_availability':seat_availability, 'train_data':train_data, 'date':date, 'from_station':source_code, 'to_station':dest_code, 'quota':quota_code, 'class_code':class_code})
            else:
                error_msg = "Train Number does not exists"
                return render(request, 'trainapp/seat_availability.html', {'error_msg':error_msg})
        else:
            error_msg = "Form validation error!!"
            return render(request, 'trainapp/seat_availability.html', {'error_msg': error_msg})
    else:
        form = seatAvailability()
        return render(request, 'trainapp/seat_availability.html', {'form': form})

def train_bw_station(request):
    if request.method == 'POST':
        form = trainBWstation(request.POST)
        if form.is_valid():
            source_code = form.cleaned_data['source_code']
            dest_code = form.cleaned_data['dest_code']
            date = form.cleaned_data['date']
            apikey = "6a721e3ch2"
            jsonList = []
            req = requests.get("http://api.railwayapi.com/v2/between/source/%s/dest/%s/date/%s/apikey/%s/"%(source_code, dest_code, date, apikey))
            if req:
                jsonList.append(json.loads(req.content))
                train_data = {}
                for data in jsonList:
                    train_data['trains'] = data['trains']
                return render(request, 'trainapp/train_bw_station.html', {'train_data':train_data})
            else:
                error_msg = "Train Number does not exists"
                return render(request, 'trainapp/train_bw_station.html', {'error_msg':error_msg})
        else:
            error_msg = "Form validation error!!"
            return render(request, 'trainapp/train_bw_station.html', {'error_msg': error_msg})
    else:
        form = trainBWstation()
        return render(request, 'trainapp/train_bw_station.html', {'form': form})

def fare_enquiry(request):
    if request.method == 'POST':
        form = fareEnquiry(request.POST)
        if form.is_valid():
            train_number = form.cleaned_data['train_number']
            source_code = form.cleaned_data['source_code']
            dest_code = form.cleaned_data['dest_code']
            age = form.cleaned_data['age']
            quota_code = form.cleaned_data['quota_code']
            date = form.cleaned_data['date']
            apikey = "6a721e3ch2"
            jsonList = []
            req = requests.get("http://api.railwayapi.com/v2/fare/train/%s/source/%s/dest/%s/age/%s/quota/%s/date/%s/apikey/%s/"%(train_number, source_code, dest_code, age, quota_code, date, apikey))
            #req = requests.get("http://api.railwayapi.com/v2/fare/train/12555/source/gkp/dest/ndls/age/18/quota/PT/date/23-11-2017/apikey/6a721e3ch2/")
            if req:
                jsonList.append(json.loads(req.content))
                return render(request, 'trainapp/fare_enquiry.html', {'fare_data': jsonList})
            else:
                error_msg = "Train Number does not exists"
                return render(request, 'trainapp/fare_enquiry.html', {'error_msg':error_msg})
        else:
            error_msg = "Form validation error!!"
            return render(request, 'trainapp/fare_enquiry.html', {'error_msg': error_msg})
    else:
        form = fareEnquiry()
        return render(request, 'trainapp/fare_enquiry.html', {'form': form})

def live_station(request):
    if request.method == 'POST':
        form = liveStation(request.POST)
        if form.is_valid():
            station_code = form.cleaned_data['station_code']
            hours = form.cleaned_data['hours']
            apikey = "6a721e3ch2"
            jsonList = []
            req = requests.get("http://api.railwayapi.com/v2/arrivals/station/%s/hours/%s/apikey/%s/"%(station_code, hours, apikey))
            if req:
                jsonList.append(json.loads(req.content))
                return render(request, 'trainapp/live_station.html', {'live_station': jsonList})
            else:
                error_msg = "Train Number does not exists"
                return render(request, 'trainapp/live_station.html', {'error_msg':error_msg})
        else:
            error_msg = "Form validation error!!"
            return render(request, 'trainapp/live_station.html', {'error_msg': error_msg})
    else:
        form = liveStation()
        return render(request, 'trainapp/live_station.html', {'form': form})

def cancelled_train(request):
    if request.method == 'POST':
        form = cancelledTrain(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            apikey = "6a721e3ch2"
            jsonList = []
            req = requests.get("http://api.railwayapi.com/v2/cancelled/date/%s/apikey/%s/"%(date, apikey))
            if req:
                jsonList.append(json.loads(req.content))
                return render(request, 'trainapp/cancelled_train.html', {'cancelled_train': jsonList})
            else:
                error_msg = "Train Number does not exists"
                return render(request, 'trainapp/cancelled_train.html', {'error_msg':error_msg})
        else:
            error_msg = "Form validation error!!"
            return render(request, 'trainapp/cancelled_train.html', {'error_msg': error_msg})
    else:
        form = cancelledTrain()
        return render(request, 'trainapp/cancelled_train.html', {'form': form})

def rescheduled_train(request):
    if request.method == 'POST':
        form = rescheduledTrain(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            apikey = "6a721e3ch2"
            jsonList = []
            req = requests.get("http://api.railwayapi.com/v2/rescheduled/date/%s/apikey/%s/"%(date, apikey))
            if req:
                jsonList.append(json.loads(req.content))
                return render(request, 'trainapp/rescheduled.html', {'rescheduled': jsonList})
            else:
                error_msg = "Train Number does not exists"
                return render(request, 'trainapp/rescheduled.html', {'error_msg':error_msg})
        else:
            error_msg = "Form validation error!!"
            return render(request, 'trainapp/rescheduled.html', {'error_msg': error_msg})
    else:
        form = rescheduledTrain()
        return render(request, 'trainapp/rescheduled.html', {'form': form})