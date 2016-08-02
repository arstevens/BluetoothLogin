#!/usr/bin/python
from Phone_retriever import Phone_retriever
from ErmrestHandler import ErmrestHandler
import bluetooth
import time

def is_user(ermrest):
	#checks if a user is logged in at the moment
	returnVal = False 

	try:
        	data = ermrest.get_data(7,"session_info")[0]
	except:
		data = {"user":None,"jarvis_response":None,"current_experiment_id":None}

        if (data['user'] != None):
                returnVal = True

	return returnVal

def action(phone,ermrest):
	#attempts to log user in and start a Jarvis session
	returnVal = False

        try:
                users = ermrest.get_data(8,"users")
		for user in users:
			if user['phone_identification'] in phone:
				username = user['username']
				break

                new_data = {"user":username,"jarvis_response":None,"current_experiment_id":None}

                try:
			#erase old users data
                        ermrest.delete_data(7,"session_info")
			ermrest.delete_data(7,"step_completed")
                except:
                        print("No data in session info")

                ermrest.put_data(7,"session_info",new_data)
                returnVal = True
                
        except:
                returnVal = False

	return returnVal

def check_user_exists(ermrest,devices):
	#checks if the user is still in the area
	returnVal = False 
	device_names = []

	for device in devices:
		device_names.append(bluetooth.lookup_name(device))

	current_user = ermrest.get_data(7,"session_info")[0]['user']	
	try:
		phone = ermrest.get_data(8,"users","/username="+current_user)[0]['phone_identification']
	except:
		phone = 'NULL' #A string because lookup_name can return None

	if phone in devices or phone in device_names: #checks both because mac/name are boot valid forms of identification
		returnVal = True

	return returnVal
 
def main():
	empty_table = {"user":None,"jarvis_response":None,"current_experiment_id":None}
	phone_retriever = Phone_retriever()
	logger = phone_retriever.logger
	ermrest = ErmrestHandler("ec2-54-172-182-170.compute-1.amazonaws.com","root","root") 
	users = ermrest.get_data(8,"users")[0]
	fail_counter = 0
	timer = time.time()
	reset_timer = time.time()
	bootup_run = True
	logged_in = False 
	voice_login = False
	user = "NULL"
	run_interval = 8 #run_interval changes because it takes about 8 seconds after rc.local is run to complete bootup sequence of raspberry pi

	while True: #main loop
		if (time.time()-timer > run_interval): #checks when to run so it isn't constantly running
			devices = bluetooth.discover_devices()
			#checks if user is logged in 
			if (is_user(ermrest)):
				user = ermrest.get_data(7,"session_info")[0]['user']
				if (logged_in == False): #logs log in even if user logged in through voice command not bluetooth
					print("User {} voice log in at: ".format(user)+time.asctime(time.localtime(time.time()))) 
					print >> logger, "User {} voice log in at: ".format(user)+time.asctime(time.localtime(time.time()))
					logged_in = True
					voice_login = True
					continue
				#Checks if user is in the area	
				if (check_user_exists(ermrest,devices) and voice_login != True): 
					#must make sure that user didn't log in with voice
					#so that the user isn't logged out because they didn't use bluetooth 
					timer = time.time()
					fail_counter = 0
					continue

				elif (voice_login != True): #leeway for some signal drops
					timer = time.time()
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

			elif (logged_in): #if no user is in session_info and logged_in is still true log out user
				print("User {} log out at: ".format(user)+time.asctime(time.localtime(time.time())))
				print >> logger,"User {} log out at: ".format(user)+time.asctime(time.localtime(time.time()))
				logged_in = False
				voice_login = False

			timer = time.time() #always reset timer

			if (voice_login == False):
				nearest_phone = phone_retriever.get_nearest_phone()
				if(action(nearest_phone,ermrest)): #if user is successfully logged in
					print("User {} log in at: ".format(user)+time.asctime(time.localtime(time.time()))) 
					print >> logger, "User {} log in at: ".format(user)+time.asctime(time.localtime(time.time()))
					logged_in = True
			if (bootup_run):
				#change the run_interval after bootup_completes
				run_interval = 5 
				bootup_run = False

		if (time.time()-reset_timer > 600): #reset some cookies so connection doesn't become invalid
			phone_retriever.reset()
			ermrest = ErmrestHandler("ec2-54-172-182-170.compute-1.amazonaws.com","root","root")
			reset_timer = time.time()
			


if __name__ == "__main__":
	while(True):
		try:
			main() 
		except:
			print("[!] Signal Dropped: resetting...")
			continue
                        
