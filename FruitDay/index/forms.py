from django import forms
from .models import *

class LoginForm(forms.ModelForm):
	class Meta:
		# 指定關聯的Model
		model = User
		# 指定要顯示的控件
		fields = ["uphone", 'upwd']
		# 指定每個控件對應的label
		labels = {
			"uphone": '手機號',
			"upwd": '密碼',
		}
		# 指定每個控件對應的小部件，並給出其他屬性
		widgets = {
			'uphone': forms.TextInput(attrs={
				'class': 'form-control',
			}),
			'upwd': forms.PasswordInput(attrs={
				'placeholder': '請輸入密碼',
				'class': 'form-control',
			}),
		}