from ErmrestHandler import ErmrestHandler
from RSSI_snatcher import RSSI_snatcher
import bluetooth	
import time
import os

class Phone_retriever:

	def __init__(self):
		self.completed = False
		self.logger = self._init_logger()
		self.ermrest = ErmrestHandler("ec2-54-172-182-170.compute-1.amazonaws.com","root","root")	

	def reset(self):
		#resets ermrest so that the cookie is still valid
		self.ermrest = ErmrestHandler("ec2-54-172-182-170.compute-1.amazonaws.com","root","root")

	def is_valid(self,phone):
		#checks if user is in the list of registered users
		returnVal = False
		valid_users = self.ermrest.get_data(8,"users")
		phone_name = str(bluetooth.lookup_name(phone[0]))
		
		for usr in valid_users:
			if (usr['phone_identification'] == phone[0] or usr['phone_identification'] == phone_name): #checks for mac address or phone name. 
															#Both are valid forms of identification
				returnVal = True
		return returnVal		

	def get_nearest_phone(self):
		#finds the phone with the best rssi value. returns a tuple with phone_name,mac_address,rssi_value
		nearest_phone = None
		self.completed = False
		while (self.completed == False):
			snatcher = RSSI_snatcher(self.logger) #class that gets the signal strength of a phone
			devices = bluetooth.discover_devices()	
			nearest_phone = None 
			
			for address in devices:
				new_phone = snatcher.get_device_strength(address)
				print("NewPhone: "+str(new_phone))
				print >> self.logger, "NewPhone: "+str(new_phone)

				if self.is_valid(new_phone): #executes if phone is registered
					print("Phone: "+new_phone[0]+" is registered")
					print >> self.logger, "Phone: "+new_phone[0]+" is registered"
					if nearest_phone == None: 
						nearest_phone = new_phone
					elif new_phone[1] >= nearest_phone[1]: #checks RSSI value is stronger and sets the strongest as nearest phone
						nearest_phone = new_phone
				else:
					print("Phone: "+new_phone[0]+" is not registered")
					print >> self.logger, "Phone: "+new_phone[0]+" is not registered"

			if nearest_phone != None: #creates final return value 
				nearest_phone = (bluetooth.lookup_name(nearest_phone[0])
						,nearest_phone[0],nearest_phone[1])
				self.completed = True

			else: #get out of loop to check for voice log in's
				self.completed = True 
				nearest_phone = "No Devices Detected"
			print("NearestPhone: "+str(nearest_phone))
			print >> self.logger, "NearestPhone: "+str(nearest_phone)

		return nearest_phone

	def _init_logger(self):
		#initiates the log file to write to.
		#os.chdir("/home/pi/main/BluetoothLogin/logs")
		os.chdir("logs")
		log_name = time.asctime(time.localtime(time.time())).replace(" ","_")+".log"
		logger = open(log_name,"w")
		print >> logger, "LOG AT: {}".format(time.asctime(time.localtime(time.time())).replace(" ","_"))
		print >> logger, " "
		return logger


