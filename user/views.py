from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from user.forms import UserRegisterForm, UserLoginForm, UserAddressForm
from user.models import User, UserAddress


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')

    if request.method == 'POST':
        # 使用表单做验证
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # 字段验证成功，注册用户名不存在于数据库，密码和确认密码是一致的
            username = form.cleaned_data['user_name']
            password = form.cleaned_data['pwd']
            email = form.cleaned_data['email']
            # from django.contrib.auth.hashers import make_password
            new_password = make_password(password)
            User.objects.create(username=username,
                                password=new_password,
                                email=email)
            # 注意render和redirect的区别
            return HttpResponseRedirect(reverse('user:login'))
        else:
            # 字段验证不成功，将验证失败的信息返回给页面
            errors = form.errors
            return render(request, 'register.html', {'errors': errors})


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        # 使用表单验证
        form = UserLoginForm(request.POST)
        if form.is_valid():
            # 验证字段成功，验证了登录用户名已存在于数据库
            username = form.cleaned_data['username']
            pwd = form.cleaned_data['pwd']
            user = User.objects.filter(username=username).first()
            # 校验密码是否一致, 一致返回True，否则返回False
            if check_password(pwd, user.password):
                # 校验成功
                request.session['user_id'] = user.id
                return HttpResponseRedirect(reverse('goods:index'))
            else:
                # 密码错误
                err_pwd = '账号或密码错误'
                return render(request, 'login.html', {'err_pwd': err_pwd})
        else:
            errors = form.errors
            return render(request, 'login.html', {'errors': errors})



def user_center(request):
    if request.method == 'GET':
        return render(request, 'user_center_info.html')


def user_order(request):
    if request.method == 'GET':
        return render(request, 'user_center_order.html')


def user_site(request):
    if request.method == 'GET':
        return render(request, 'user_center_site.html')
    if request.method == 'POST':
        form = UserAddressForm(request.POST)
        if form.is_valid():
            user_id = request.session['user_id']
            addr = form.cleaned_data['addr_name']
            name = form.cleaned_data['site_name']
            email = form.cleaned_data['email_name']
            tel = form.cleaned_data['tel_name']
            UserAddress.objects.create(user_id= user_id,
                                           address=addr,
                                           signer_name=name,
                                           signer_postcode=email,
                                           signer_mobile=tel)
            return HttpResponseRedirect(reverse('user:user_site'))
        else:
            errors = form.errors
            return render(request, 'user_center_site.html', {'errors':errors})



