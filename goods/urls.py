
from django.conf.urls import url
from goods import views

urlpatterns = [
    # 首页
    url(r'^index', views.index, name='index'),
    # 商品的详情信息
    url(r'^detail/(\d+)/', views.detail, name='detail'),

]
