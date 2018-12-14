from django import forms

from user.models import User


class UserRegisterForm(forms.Form):
    user_name = forms.CharField(max_length=20, min_length=5,
                                required=True, error_messages={
                                'required':'用户名必填',
                                'max_length':'不能超过20',
                                 'min_length':'用户不能少于5'
                                 })
    pwd = forms.CharField(max_length=20, min_length=8,
                                required=True, error_messages={
                                'required':'密码必填',
                                'max_length':'不能超过20',
                                 'min_length':'密码不能少于8'
                                 })
    cpwd = forms.CharField(max_length=20, min_length=8,
                                required=True, error_messages={
                                'required':'密码必填',
                                'max_length':'不能超过20',
                                 'min_length':'密码不能少于5'
                                 })
    email = forms.CharField(required=True, error_messages={
        'required':'邮箱必填'
    })


    def clean(self):
        user = User.objects.filter(username=self.cleaned_data.get('user_name'))
        if user:
            raise forms.ValidationError({'user_name':'该用户已经被注册，请去登录'})
        pwd = self.cleaned_data.get('pwd')
        cpwd = self.cleaned_data.get('cpwd')
        if pwd != cpwd:
            raise forms.ValidationError({'pwd':'两次密码不一致'})
        return self.cleaned_data




# 登录
class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=5,
                                required=True, error_messages={
                                'required':'用户名必填',
                                'max_length':'不能超过20',
                                 'min_length':'用户不能少于5'
                                 })
    pwd = forms.CharField(max_length=20, min_length=8,
                                required=True, error_messages={
                                'required':'密码必填',
                                'max_length':'不能超过20',
                                 'min_length':'密码不能少于8'
                                 })



    def clean(self):
        user = User.objects.filter(username=self.cleaned_data.get('username'))
        if not user:
            raise forms.ValidationError({'username':'没有该用户名，请去注册'})

        return self.cleaned_data


class UserAddressForm(forms.Form):
    site_name = forms.CharField(max_length=20, min_length=2,
                                required=True, error_messages={
                                'required': '姓名必填',
                                'max_length': '不能超过20',
                                'min_length': '姓名不能少于2'
                                })
    addr_name = forms.CharField(max_length=20, min_length=2,
                                required=True, error_messages={
                                'required': '地址必填',
                                'max_length': '不能超过20',
                                'min_length': '地址不能少于2'
                                })
    email_name = forms.CharField(max_length=20, min_length=2,
                                required=True, error_messages={
                                'required': '邮箱必填',
                                'max_length': '不能超过20',
                                'min_length': '邮箱不能少于2'
                                })
    tel_name = forms.CharField(max_length=11, min_length=1,
                                required=True, error_messages={
                                'required': '手机必填',
                                'max_length': '不能超过11',
                                'min_length': '手机不能少于1'
                                })

