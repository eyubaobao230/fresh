import re

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from carts.models import ShoppingCart
from user.models import User


class LoginStatusMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 登录状态验证
        # 首页、登录、注册不用验证(不用跳转到登录、注册页面)
        user_id = request.session.get('user_id')
        if user_id:
            user = User.objects.filter(pk=user_id).first()
            request.user = user
        #     过滤不需要验证的URL，比如首页，登录，注册

        not_need_check = ['/goods/index/',
                          '/user/register/',
                          '/user/login/',
                          '/carts/cart/',
                          '/media/.*',
                          '/goods/detail/.*',
                          '/carts/add_cart/',
                          '/carts/count_cart/',
                          '/carts/change_cart/',
                          '/carts/del_cart/.*',
                          ]
        path = request.path
        for not_check in not_need_check:
            if re.match(not_check, path):
                # 不需要做登录验证
                return None
        # 登录校验
        user_id = request.session.get('user_id')
        if not user_id:
            # 如果session中没有user_id字段，则跳转到登录
            return HttpResponseRedirect(reverse('user:login'))
        user = User.objects.filter(pk=user_id).first()
        if not user:
            # 如果 获取的user不存在，则跳转到登录
            return HttpResponseRedirect(reverse('user:login'))
        # 获取到user，则设置全局变量
        request.user = user
        return None


# 同步session数据到数据库
class SessionSyncMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        user_id = request.session.get('user_id')
        if user_id:
            # 登录情况
            session_goods = request.session.get('goods')
            if session_goods:
                # 1.判断session存在则更新，否则创建
                shop_carts = ShoppingCart.objects.filter(user_id=user_id)

                # flag = False
                # 更新购物车商品的数量
                data = []
                for goods in shop_carts:
                    for se_goods in session_goods:
                        if se_goods[0] == goods.goods_id:
                            goods.nums = se_goods[1]
                            goods.save()
                            # 向data中添加编辑的商品的ID值
                            data.append(se_goods[0])

            #                 添加
                session_goods_ids = [i[0] for i in session_goods]
                add_goods_ids = list(set(session_goods_ids) - set(data))
                for add_goods_id in add_goods_ids:
                    for session_good in session_goods:
                        if add_goods_id == session_good[0]:
                            ShoppingCart.objects.create(user_id=user_id,
                                                        goods_id=add_goods_id,
                                                        nums=session_good[1])


            new_shop_carts = ShoppingCart.objects.filter(user_id=user_id)
            session_new_goods = [[i.goods_id, i.nums, i.is_select] for i in new_shop_carts]
            request.session['goods'] = session_new_goods


        return response






