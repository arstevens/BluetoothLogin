from Phone_retriever import Phone_retriever
from ErmrestHandler import ErmrestHandler
import pyvona
import time


def is_user(ermrest):
	data = ermrest.get_data(7,"session_info")

	if (data):
		return True
	return False

def action(phone,ermrest):
	try:
		user_info = ermrest.get_data(8,"users","/phone_name="+str(phone[0]))[0]
		data = {"user":user_info['username'],"jarvis_response":None,"current_experiment_id":None}
		try:
			ermrest.delete_data(7,"session_info")
		except:
			print("No data in session info")
		ermrest.put_data(7,"session_info",data)
	except Exception as exc:
		print("[*] Error: "+str(exc))
		

def main():
	phone_retriever = Phone_retriever()
	ermrest = ErmrestHandler("ec2-54-172-182-170.compute-1.amazonaws.com","root","root") 
	timer = time.time()

	while True:
		if (time.time()-timer > 10):
			if (is_user(ermrest)):
				timer = time.time()
				continue
			else:
				timer = time.time()
				nearest_phone = phone_retriever.get_nearest_phone()
				action(nearest_phone,ermrest)

if __name__ == "__main__":
	main()
			
		
