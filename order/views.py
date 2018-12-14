from django.http import JsonResponse
from django.shortcuts import render

from carts.models import ShoppingCart
from order.models import OrderInfo, OrderGoods
from utils.functions import get_order_sn


def place_order(request):
    if request.method =='GET':
        user_id = request.session.get('user_id')
        shop_carts = ShoppingCart.objects.filter(user_id=user_id, is_select=1)

        all_total = 0
        for carts in shop_carts:
            price = carts.nums * carts.goods.shop_price
            carts.total = price
            all_total += price
        carts_count = len(shop_carts)

        return render(request, 'place_order.html',
                      {'shop_carts': shop_carts,
                       'all_total': all_total,
                       'carts_count': carts_count
                       })


def make_order(request):
    if request.method == 'POST':
        # 创建订单
        # 创建订单详情
        # 购物车删除已经下单的商品
        user_id = request.session['user_id']

        shop_carts = ShoppingCart.objects.filter(user_id=user_id,
                                                 is_select=1)
        order_mount = 0
        for carts in  shop_carts:
            order_mount += carts.nums * carts.goods.shop_price

        order_sn = get_order_sn()
        order = OrderInfo.objects.create(user_id=user_id,
                                 order_sn=order_sn,
                                 order_mount=order_mount)

        for carts in shop_carts:
            OrderGoods.objects.create(order=order,
                                      goods=carts.goods,
                                      goods_nums=carts.nums)
        shop_carts.delete()
        request.session.pop('goods')

        return JsonResponse({'code':200, 'msg':'请求成功'})


def user_order(request):

    if request.method == 'GET':
        user_id = request.session['user_id']
        page = request.GET.get('page', 1)
        order











