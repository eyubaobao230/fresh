from order import views
from django.conf.urls import url

urlpatterns = [
    url(r'^place_order/',views.place_order,name='place_order'),
    url(r'^make_order/',views.make_order,name='make_order'),



]