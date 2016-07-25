from ErmrestHandler import ErmrestHandler
from RSSI_snatcher import RSSI_snatcher
import bluetooth	
import time
import os

#globalVariable
class Phone_retriever:

	def __init__(self):
		self.completed = False
		self.logger = self._init_logger()
		self.ermrest = ErmrestHandler("ec2-54-172-182-170.compute-1.amazonaws.com","root","root")	


	def is_valid(self,phone_name):
		#checks if user is valid
		user_data = self.ermrest.get_data(8,"users","/phone_name="+str(phone_name))

		if user_data:
			return True
		return False

	def get_nearest_phone(self):
		nearest_phone = None
		while (self.completed == False or nearest_phone == None):
			snatcher = RSSI_snatcher(self.logger)
			devices = bluetooth.discover_devices()	
			nearest_phone = None
			
			for address in devices:
				new_phone = snatcher.get_device_strength(address)
				new_phone_name = bluetooth.lookup_name(address)
				print("NewPhone: "+str(new_phone))
				print >> self.logger, "NewPhone: "+str(new_phone)

				if self.is_valid(new_phone_name):
					print("Phone: "+new_phone[0]+" is registered")
					print >> self.logger, "Phone: "+new_phone[0]+" is registered"
					if nearest_phone == None:
						nearest_phone = new_phone
					elif new_phone[1] >= nearest_phone[1]:
						nearest_phone = new_phone
				else:
					print("Phone: "+new_phone[0]+" is not registered")
					print >> self.logger, "Phone: "+new_phone[0]+" is not registered"
			if (nearest_phone != None and nearest_phone[1] != -9999):	
				nearest_phone = (bluetooth.lookup_name(nearest_phone[0])
						,nearest_phone[0],nearest_phone[1])
				self.completed = True
			else:
				nearest_phone = "No Devices Detected"
			print("NearestPhone: "+str(nearest_phone))
			print >> self.logger, "NearestPhone: "+str(nearest_phone)
		print("np: ",nearest_phone)
		return nearest_phone

	def _init_logger(self):
		os.chdir("/home/pi/main/BluetoothLogin/logs")
		log_name = time.asctime(time.localtime(time.time())).replace(" ","_")+".log"
		logger = open(log_name,"w")
		print >> logger, "LOG AT: {}".format(time.asctime(time.localtime(time.time())).replace(" ","_"))
		print >> logger, " "
		return logger


