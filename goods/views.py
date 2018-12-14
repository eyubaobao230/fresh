from django.shortcuts import render

from goods.models import GoodsCategory, Goods

def index(request):
    if request.method == 'GET':
        data = {}
        # 循环商品分类
        for cate in GoodsCategory.CATEGORY_TYPE:
            # 获取当前分类下的钱四个商品信息
            goods = Goods.objects.filter(category_id=cate[0])[0:4]
            # 组装成键值对， key为商品分类的名称，value为当分类的商品信息
            data[cate[1]] = goods
        return render(request, 'index.html',{'goods_category':data})

def detail(request,id):
    if request.method == 'GET':
        goods = Goods.objects.filter(pk=id).first()
        return render(request, 'detail.html',{'goods':goods})