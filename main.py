#!/usr/bin/python
from Phone_retriever import Phone_retriever
from ErmrestHandler import ErmrestHandler
import bluetooth
import time

def is_user(ermrest):
	try:
        	data = ermrest.get_data(7,"session_info")[0]
	except:
		data = {"user":None,"jarvis_response":None,"current_experiment_id":None}

        if (data['user'] != None):
                return True
        return False

def action(phone,ermrest):
        try:
                users = ermrest.get_data(8,"users")
		user_info = None
		for user in users:
			if user['phone_identification'] in phone:
				user_info = user

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
	devices = bluetooth.discover_devices()
	device_names = []
	for device in devices:
		device_names.append(bluetooth.lookup_name(device))

	current_user = ermrest.get_data(7,"session_info")[0]['user']	
	try:
		user_info = ermrest.get_data(8,"users","/username="+current_user)[0]
	except:
		user_info = {'phone_identification':"Empty_id_slot"} #A string because lookup_name can return None
	phone = user_info['phone_identification']

	if phone in devices or phone in device_names:
		return True
	return False
 


def main():
	empty_table = {"user":None,"jarvis_response":None,"current_experiment_id":None}
	phone_retriever = Phone_retriever()
	logger = phone_retriever.logger
	ermrest = ErmrestHandler("ec2-54-172-182-170.compute-1.amazonaws.com","root","root") 
	fail_counter = 0
	timer = time.time()
	reset_timer = time.time()
	bootup_run = True
	logged_in = False 
	user = ""
	run_interval = 8

	while True: #main loop
		if (time.time()-timer > run_interval): #checks when to run so it isn't constantly running
			devices = bluetooth.discover_devices()
			users = ermrest.get_data(8,"users")[0]
			#checks if user is logged in AND if the user is still in the area.
			if (is_user(ermrest)):
				user = ermrest.get_data(7,"session_info")[0]['user']
				if (logged_in == False):
					print("User {} log in at: ".format(user)+time.asctime(time.localtime(time.time()))) 
					print >> logger, "User {} log in at: ".format(user)+time.asctime(time.localtime(time.time()))
					logged_in = True
				
				if (check_user_exists(ermrest)):
					timer = time.time()
					fail_counter = 0
					continue
				else: #leeway for some signal drops
					if (fail_counter >= 2):
						ermrest.delete_data(7,"session_info")
						ermrest.put_data(7,"session_info",empty_table)
						print("User {} log out at: ".format(user)+time.asctime(time.localtime(time.time())))
						print >> logger,"User {} log out at: ".format(user)+time.asctime(time.localtime(time.time()))
						logged_in = False
						continue
					else:
						fail_counter += 1
						continue
					timer = time.time()
			elif (logged_in):
				print("User {} log out at: ".format(user)+time.asctime(time.localtime(time.time())))
				print >> logger,"User {} log out at: ".format(user)+time.asctime(time.localtime(time.time()))
				logged_in = False
						

			timer = time.time()
			nearest_phone = phone_retriever.get_nearest_phone()

			if(action(nearest_phone,ermrest)):
				print("User log in at: "+time.asctime(time.localtime(time.time()))) 
				print >> logger, "User log in at: "+time.asctime(time.localtime(time.time()))
				logged_in = True
				try:
					ermrest.delete_data(7,"step_completed")
				except:
					pass
				ermrest.put_data(7,"step_completed",{"completed_step":None})
			if (bootup_run):
				run_interval = 5
				bootup_run = False

		if (time.time()-reset_timer > 600): # reset some cookies so connection doesn't become invalid
			phone_retriever.reset()
			ermrest = ErmrestHandler("ec2-54-172-182-170.compute-1.amazonaws.com","root","root")
			reset_timer = time.time()
			


if __name__ == "__main__":
	main() 
                        
                
