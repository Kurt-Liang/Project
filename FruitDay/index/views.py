import json

from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import *
from .forms import *

# Create your views here.

# http://localhost:8000/login
def login_views(request):
	# 1. 判斷是get請求還是post請求
	if request.method == 'GET':
		# 獲取來訪地址，如果沒有則設置為/
		url = request.META.get('HTTP_REFERER', '/')
		# get請求 - 判斷session，判斷cookie，登錄頁
		# 先判斷session中是否有登錄信息
		if 'uid' in request.session and 'uphone' in request.session:
			# 有登錄信息保存在session
			# 從哪來回哪去
			resp = HttpResponseRedirect(url)
			return resp
		else:
			# 沒有登錄信息保存在session，繼續判斷cookies中是否有登錄信息
			if 'uid' in request.COOKIES and 'uphone' in request.COOKIES:
				# cookies中有登錄信息，曾記住過密碼
				# 將cookies中的信息保存進session，再返回到首頁
				uid = request.COOKIES['uid']
				uphone = request.COOKIES['uphone']
				request.session['uid'] = uid
				request.session['uphone'] = uphone
				# 從哪來回哪去
				resp = redirect(url)
				return resp
			else:
				# cookies中沒有登錄信息，去往登錄頁
				form = LoginForm()
				# 將來訪地址保存進cookies中
				resp = render(request, 'login.html', locals())
				resp.set_cookie('url', url)
				return resp
		pass
	else:
		# post請求 - 實現登錄操作
		# 獲取手機號和密碼
		uphone = request.POST['uphone']
		upwd = request.POST['upwd']
		# 判斷手機號和密碼是否存在(登錄是否成功)
		users = User.objects.filter(uphone=uphone, upwd=upwd)
		if users:
			# 登錄成功:先存進session
			request.session['uid'] = users[0].id
			request.session['uphone'] = uphone
			# 聲明響應對象:從哪來回哪去
			url = request.COOKIES.get('url', '/')
			print(url)
			resp = redirect(url)
			# 將url從cookies中刪除出去
			if 'url' in request.COOKIES:
				resp.delete_cookie('url')
			# 判斷是否存進coolies
			if 'isSaved' in request.POST:
				expire = 60*60*24*90
				resp.set_cookie('uid', users[0].id, expire)
				resp.set_cookie('uphone', uphone, expire)
			return resp
		else:
			# 登錄失敗
			form = LoginForm()
			return render(request, 'login.html', locals())

# http://localhost:8000/register
def register_views(request):
	# 判斷請求
	if request.method == 'GET':
		return render(request, 'register.html')
	else:
		# 先驗證手機號在數據庫中是否存在
		uphone = request.POST['uphone']
		# users = User.objects.filter(uphone=uphone)
		# if users:
		# 	# uphone 已經存在
		# 	errMsg = '手機號碼已經存在'
		# 	return render(request, 'register.html', locals())
		# 接收數據插入到數據庫中
		upwd = request.POST['upwd']
		uname = request.POST['uname']
		uemail = request.POST['uemail']
		user = User()
		user.uphone = uphone
		user.upwd = upwd
		user.uname = uname
		user.uemail = uemail
		user.save()
		# 取出user中的id和uphone的值保存進session
		request.session['uid'] = user.id
		request.session['uphone'] = user.uphone
		return HttpResponse('註冊成功')

# 檢查手機好是否已經被註冊過
def check_uphone_views(request):
	# 接收前端傳遞過來的數據 - uphone
	uphone = request.GET['uphone']
	users = User.objects.filter(uphone=uphone)
	if users:
		status = 1
		msg = "手機號碼已經存在"
	else:
		status = 0
		msg = "手機號碼可以使用"

	dic = {
		'status': status,
		'msg': msg,
	}

	return HttpResponse(json.dumps(dic))

def index_views(request):
	return render(request, 'index.html')

def check_login_views(request):
	# 檢查session中是否有登錄信息，如果有獲取對應數據的uname值
	if 'uid' in request.session and 'uphone' in request.session:
		loginStatus = 1
		# 通過uid的值獲取對應的uname
		id = request.session['uid']
		uname = User.objects.get(id=id).uname
		dic = {
			'loginStatus': loginStatus,
			'uname': uname
		}
		return HttpResponse(json.dumps(dic))
	else:
		dic = {
			'loginStatus':0
		}
		return HttpResponse(json.dumps(dic))

# 退出
def logout_views(request):
	if 'uid' in request.session and 'uphone' in request.session:
		del request.session['uid']
		del request.session['uphone']
		# 構建響應對象：哪發的退出請求，則返回到哪去
		url = request.META.get("HTTP_REFERER", '/')
		resp = HttpResponseRedirect(url)
		# 判斷cookies中是否有登錄信息，有的話則刪除
		if 'uid' in request.COOKIES and 'uphone' in request.COOKIES:
			resp.delete_cookie('uid')
			resp.delete_cookie('uphone')
		return resp
	return redirect('/')

def test_views(request):
	return render(request, 'test.html')

# 加載所有的商品類型以及對應的每個類型下的前10條數據
def type_goods_views(request):
	all_list = []
	# 加載所有的商品類型
	types = GoodsType.objects.all()
	for type in types:
		type_json = json.dumps(type.to_dict())
		# 獲取type類型下最新的10條數據
		g_list = type.goods_set.filter(isActive=True).order_by('-id')[0:10]
		# 將g_list轉換為json
		g_list_json = serializers.serialize('json', g_list)
		# 將type_json和g_list_json封裝到一個字典中
		dic = {
			"type": type_json,
			"goods": g_list_json,
		}
		# 將字典追加到all_list中
		all_list.append(dic)

	return HttpResponse(json.dumps(all_list))

# 將商品添加至購物車，或更新現有商品的數量
def add_cart_views(request):
	# 獲取商品id，獲取用戶id，購買數量默認為1
	goods_id = request.GET['gid']
	user_id = request.session['uid']
	ccount = 1
	# 查看購物車中是否有相同用戶購買的相同商品
	cart_list = CartInfo.objects.filter(user_id=user_id, goods_id=goods_id)
	if cart_list:
		# 已經有相同用戶購買過相同產品，更新商品數量
		cartinfo = cart_list[0]
		cartinfo.ccount = cartinfo.ccount + ccount
		cartinfo.save()
		dic = {
			'status': 1,
			'statusText': '更新數量成功'
		}
	else:
		# 沒有對應的用戶和對應的商品
		cartinfo = CartInfo()
		cartinfo.user_id = user_id
		cartinfo.goods_id = goods_id
		cartinfo.ccount = ccount
		cartinfo.save()
		dic = {
			'status': 1,
			'statusText': '添加購物車成功'
		}
	return HttpResponse(json.dumps(dic))





