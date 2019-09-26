

from student import Student 

def input_student():
	L = []
	while True :
		name = input("請輸入姓名：")
		if not name :
			break
		age = int(input("請輸入年齡："))
		score = int(input("請輸入成績："))
		L.append(Student(name,age,score))

	return L

def output_student(L):
	mm = []
	for i in L :
		n , a , s = i.get_info()
		mm.append(len(n))
	mm = max(mm)
	print("+-"+"-"*mm+"-+" + "-"*5 + "+" + "-"*7 + "+")
	print("| "+'name'.center(mm)+" |"+'age'.center(5)+"|"+'score'.center(7)+"|")
	print("+-"+"-"*mm+"-+" + "-"*5 + "+" + "-"*7 + "+")
	for x in L :
		n , a , s = x.get_info()
		print("| "+('%s'%n).center(mm)+" |" + 
			('%2d'% a).center(5) + "|" + 
			('%3d'% s).center(7) + "|" )
	print("+-"+"-"*mm+"-+" + "-"*5 + "+" + "-"*7 + "+")

def change_score(lst):
	name = input("請輸入要修改成績的學生姓名：")
	for d in lst :
		if d.is_name :
			score = int(input("請輸入新的成績："))
			d.set_score(score)
			print("修改",name,'的成績為',score)
			return
	else:
		print("沒有找到名為",name,'的學生信息')

def delete_student(lst):
	name = input("請輸入要刪除的學生姓名：")
	for d in lst :
		if lst[d].is_name(name) :
			del lst[d]
			print("已成功刪除",name)
			return True
	else:
		print("沒有找到名為",name,'的學生信息')

def score_high(L):
	L2 = sorted(L , key = lambda L : L.get_score() , reverse = True)
	output_student(L2)

def score_low(L):
	L2 = sorted(L , key = lambda L : L.get_score() )
	output_student(L2)

def age_high(L):
	L2 = sorted(L , key = lambda L : L.get_age() , reverse = True)
	output_student(L2)

def age_low(L):
	L2 = sorted(L , key = lambda L : L.get_age() )
	output_student(L2)

def save_data(L,filename = 'si.txt'):
	try:
		f = open(filename , 'w')
		s = []
		for d in L :
			d.write_to_file(f)

		f.close()
		print("資料寫入成功")
	except OSError :
		print("資料寫入失敗")

def load_data(filename = 'si.txt'):
	L = []
	try:
		f = open('si.txt')
		while True:
			s = f.readline()
			if not s :
				break
			s = s.rstrip()
			name , age , score = s.split(',')
			L.append(Student(name,int(age),int(score)))

		f.close()
		print("資料讀取成功")

	except OSError :
		print("資料讀取失敗")
	return L











