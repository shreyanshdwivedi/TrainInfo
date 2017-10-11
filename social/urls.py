from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^train_auto/$', views.train_auto, name='train_auto'),
    url(r'^station_auto/$', views.station_auto, name='station_auto'),
    url(r'^live_status/$', views.live_status, name='live_status'),
    url(r'^pnr_status/$', views.pnr_status, name='pnr_status'),
    url(r'^train_route/$', views.train_route, name='train_route'),
    url(r'^seat_availability/$', views.seat_availability, name='seat_availability'),
    url(r'^train_bw_station/$', views.train_bw_station, name='train_bw_station'),
    url(r'^fare_enquiry/$', views.fare_enquiry, name='fare_enquiry'),
    url(r'^live_station/$', views.live_station, name='live_station'),
    url(r'^cancelled_train/$', views.cancelled_train, name='cancelled_train'),
    url(r'^rescheduled_train/$', views.rescheduled_train, name='rescheduled_train'),
]