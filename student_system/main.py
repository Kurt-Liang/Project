

import menu , student_info

def main():
	docs = []
	while True:
		menu.show_menu()
		i = input("請輸入指令：")
		if i == '1':
			docs += student_info.input_student()
		elif i == '2':
			student_info.output_student(docs)
		elif i == '3':
			student_info.change_score(docs)
		elif i == '4':
			student_info.delete_student(docs)
		elif i == '5':
			student_info.score_high(docs)	
		elif i == '6':
			student_info.score_low(docs)
		elif i == '7':
			student_info.age_high(docs)
		elif i == '8':
			student_info.age_low(docs)	
		elif i == '9':
			student_info.save_data(docs)
		elif i == '10':
			docs = student_info.load_data(docs)	
		elif i == 'q':
			exit()
		else:
			print('請輸入正確操作')
main()