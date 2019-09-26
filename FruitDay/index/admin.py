from django.contrib import admin
from .models import *

# Register your models here.

class GoodsAdmin(admin.ModelAdmin):
	# 指定列表頁中顯示的字段們
	list_display = ('title', 'goodsType', 'price', 'spec')
	# 指定右側顯示的過濾器
	list_filter = ('goodsType',)
	# 指定在上方顯示的搜索字段們
	search_fields = ('title',)

admin.site.register(GoodsType)
admin.site.register(Goods, GoodsAdmin)