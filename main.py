from RSSI_snatcher import RSSI_snatcher
from ErmrestHandler import ErmrestHandler
import bluetooth	

def is_user_valid(user_data,phone_name):
	#checks if user is valid
	for user in user_data:
		if user['phone_name'] == phone_name:
			return True
	return False
		
def get_nearest_phone():
	snatcher = RSSI_snatcher()
	devices = bluetooth.discover_devices()	
	nearest_phone = None
	
	for address in devices:
		new_phone = snatcher.get_device_strength(address)
		print("NewPhone: "+str(new_phone))

		if nearest_phone == None:
			nearest_phone = new_phone
		elif new_phone[1] >= nearest_phone[1]:
			nearest_phone = new_phone
	
	nearest_phone = (bluetooth.lookup_name(nearest_phone[0]),
			nearest_phone[0],nearest_phone[1])
	print("NearestPhone: "+str(nearest_phone))
	return nearest_phone

def main():
	target_phone = get_nearest_phone()

main()
	
			
