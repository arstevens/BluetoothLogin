#!/usr/bin/python
from Phone_retriever import Phone_retriever
from ErmrestHandler import ErmrestHandler
import bluetooth
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
		return True
		
	except:
		return False

def check_user_exists(ermrest):
	exists = False
	devices = bluetooth.discover_devices()
	device_names = [bluetooth.lookup_name(mac) for mac in devices]
        print(device_names)
	users = ermrest.get_data(8,"users")
	current_user = ermrest.get_data(7,"session_info")[0]['user']

	for device_name in device_names:
		for user in users:
			try:
				username = user[device_name]
			except:
				username = None
			if username == current_user:
				exists = True
				break
		if (exists):
			break
	
	return exists


def main():
	phone_retriever = Phone_retriever()
	logger = phone_retriever.logger
	ermrest = ErmrestHandler("ec2-54-172-182-170.compute-1.amazonaws.com","root","root") 
	timer = time.time()

	while True:
		if (time.time()-timer > 8):
			devices = bluetooth.discover_devices()
			users = ermrest.get_data(8,"users")[0]
			#checks if user is logged in AND if the user is still in the area.
			if (is_user(ermrest)):
				if (check_user_exists(ermrest)):
					timer = time.time()
					continue
				else:
					ermrest.delete_data(7,"session_info")

			timer = time.time()
			nearest_phone = phone_retriever.get_nearest_phone()
			if(action(nearest_phone,ermrest)):
				print("User log in at: "+time.asctime(time.localtime(time.time()))) 
				print >> logger, "User log in at: "+time.asctime(time.localtime(time.time()))
	

if __name__ == "__main__":
	main()
			
		
