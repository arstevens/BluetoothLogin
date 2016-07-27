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
		self.ermrest = ErmrestHandler("ec2-54-172-182-170.compute-1.amazonaws.com","root","root")

	def is_valid(self,phone):
		#checks if user is valid
		
		valid_users = self.ermrest.get_data(8,"users")
		phone_name = str(bluetooth.lookup_name(phone[0]))
		
		for usr in valid_users:
			if (usr['phone_identification'] == phone[0] or usr['phone_identification'] == phone_name):
				return True
		return False

	def get_nearest_phone(self):
		nearest_phone = None
		while (self.completed == False):
			snatcher = RSSI_snatcher(self.logger)
			devices = bluetooth.discover_devices()	
			nearest_phone = None 
			
			for address in devices:
				new_phone = snatcher.get_device_strength(address)
				print("NewPhone: "+str(new_phone))
				print >> self.logger, "NewPhone: "+str(new_phone)

				if self.is_valid(new_phone):
					print("Phone: "+new_phone[0]+" is registered")
					print >> self.logger, "Phone: "+new_phone[0]+" is registered"
					if nearest_phone == None: 
						nearest_phone = new_phone
					elif new_phone[1] >= nearest_phone[1]:
						nearest_phone = new_phone
				else:
					print("Phone: "+new_phone[0]+" is not registered")
					print >> self.logger, "Phone: "+new_phone[0]+" is not registered"
			if nearest_phone != None: 
				nearest_phone = (bluetooth.lookup_name(nearest_phone[0])
						,nearest_phone[0],nearest_phone[1])
				self.completed = True
			else:
				self.completed = False
				nearest_phone = "No Devices Detected"
			print("NearestPhone: "+str(nearest_phone))
			print >> self.logger, "NearestPhone: "+str(nearest_phone)
		return nearest_phone

	def _init_logger(self):
#		os.chdir("/home/pi/main/BluetoothLogin/logs")
		os.chdir("logs")
		log_name = time.asctime(time.localtime(time.time())).replace(" ","_")+".log"
		logger = open(log_name,"w")
		print >> logger, "LOG AT: {}".format(time.asctime(time.localtime(time.time())).replace(" ","_"))
		print >> logger, " "
		return logger


