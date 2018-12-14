from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from carts.models import ShoppingCart
from goods.models import Goods


def cart(request):
    if request.method == 'GET':
        # 返回购物车中的数据，不用区分登录和没登录的情况
        # 因为所有的数据只需从session中获取
        session_goods = request.session.get('goods')
        data = []
        total_num = 0
        m_price = 0
        if session_goods:
            for se_goods in session_goods:
                goods = Goods.objects.filter(pk=se_goods[0]).first()
                nums = se_goods[1]
                total_num += nums
                price = goods.shop_price * se_goods[1]
                m_price += price
                data.append([goods, nums, price])

        # 返回给页面，需要将结构[[商品对象，商品数量，商品价格], [商品对象，商品数量，商品价格],...]
        return render(request, 'cart.html', {'goods_all':data, 'total_num':total_num, 'm_price':m_price})

def add_cart(requset):
    if requset.method == 'POST':
        # 保存到session
        # 1.获取前段ajax提交的商品goods_id，商品数量nums
        # 2.组装储存到session的数据结构中
        # 3.加入到session就更新nums

        goods_id = int(requset.POST.get('goods_id'))
        nums = int(requset.POST.get('nums'))
        # 组装储存的结构
        goods_list = [goods_id, nums, 1]

        session_goods = requset.session.get('goods')
        if session_goods:
            # 修改
            flag = False
            # 添加或者修改
            for goods in session_goods:
                if goods[0] == goods_id:
                    goods[1] += nums
                    flag = True
        #             添加
            if not flag:
                session_goods.append(goods_list)
            requset.session['goods'] = session_goods
            # 保存的商品数量
            goods_count = len(session_goods)

        else:
            # 第一次添加到session，保存键值对
            requset.session['goods'] = [goods_list]
            goods_count = 1

        return JsonResponse({'code': 200, 'msg': '请求成功',
                             'goods_count':goods_count})


def count_cart(request):
    if request.method == 'GET':
        session_goods = request.session.get('goods')
        count = len(session_goods) if session_goods else 0
        return JsonResponse({'code':200, 'msg':'请求成功', 'count':count})


def change_cart(request):
    if request.method == 'POST':
        # 获取ajax传递的
        goods_id = int(request.POST.get('goods_id'))
        is_select = request.POST.get('is_select')
        nums = request.POST.get('nums')
        # 获取session的商品信息
        session_goods = request.session.get('goods')
        for goods in session_goods:
            if goods_id == goods[0]:
                #更新
                goods[1] = int(nums) if nums else goods[1]
                goods[2] = int(is_select) if is_select else goods[2]
        request.session['goods'] = session_goods
        return JsonResponse({'code': 200, 'msg': '请求成功'})


# 删除
def del_cart(request, id):
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        if user_id:
            ShoppingCart.objects.filter(user_id=user_id,
                                        goods_id =id).delete()

        #删除session的数据
        session_goods = request.session.get('goods')
        for goods in session_goods:
            if goods[0] == int(id):
                session_goods.remove(goods)
            request.session['goods'] = session_goods
        return HttpResponseRedirect(reverse('carts:cart'))






