from RSSI_snatcher import RSSI_snatcher
from ErmrestHandler import ErmrestHandler
import bluetooth	

def is_valid(phone_name,ermrest):
	#checks if user is valid
	user_data = ermrest.get_data(8,"users","/phone_name="+str(phone_name))

	if user_data:
		return True
	return False

def get_nearest_phone():
	snatcher = RSSI_snatcher()
	devices = bluetooth.discover_devices()	
	nearest_phone = None
	ermrest = ErmrestHandler("ec2-54-172-182-170.compute-1.amazonaws.com","root","root")	
	
	for address in devices:
		new_phone = snatcher.get_device_strength(address)
		new_phone_name = bluetooth.lookup_name(address)
		print("NewPhone: "+str(new_phone))

		if is_valid(new_phone_name,ermrest):
			print("Phone: "+new_phone[0]+" is registered")
			if nearest_phone == None:
				nearest_phone = new_phone
			elif new_phone[1] >= nearest_phone[1]:
				nearest_phone = new_phone
		else:
			print("Phone: "+new_phone[0]+" is not registered")
	if (nearest_phone != None):	
		nearest_phone = (bluetooth.lookup_name(nearest_phone[0])
				,nearest_phone[0],nearest_phone[1])
	else:
		nearest_phone = "No Devices Detected"
	print("NearestPhone: "+str(nearest_phone))
	return nearest_phone

def main():
	target_phone = get_nearest_phone()

main()
	
			
