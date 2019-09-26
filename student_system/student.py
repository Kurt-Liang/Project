



class Student :
	count = 0 		# 此類變量用來記錄學生的個數

	def __init__(self,name,age,score=0):
		self.__name = name
		self.__age = age
		self.__score = score
		Student.count += 1
	@classmethod
	def getTotalcount(cls):
		'''此方法用來得到學生對象的個數'''
		return cls.count

	def __del__(self):
		Student.count -= 1

	def get_info(self):
		return (self.__name , self.__age , self.__score )

	def is_name(self,name):
		return self.__name == name

	def set_score(self,score):
		'''此方法用於制定設置成績時的規則'''
		if 0 <= score <= 100:
			self.__score = score
			return
		raise ValueError('不合法的成績信息'+ str(score))
	def get_score(self):
		return self.__score

	def get_age(self):
		return self.__age

	def write_to_file(self,file):
		file.write(self.__name)
		file.write(',')
		file.write(str(self.__age))
		file.write(',')
		file.write(str(self.__score))
		file.write('\n')








