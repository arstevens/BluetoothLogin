from ErmrestHandler import ErmrestHandler
import argparse
import sys

def parse_command_line():
	parser = argparse.ArgumentParser(description="Register a phone for Bluetooth Login")
	parser.add_argument("phone_id",type=str,help="the identification for your phone (mac address or phone name)") 
	parser.add_argument("username",type=str,help="The username mapped to your phone name")
	parser.add_argument("delete",nargs='?',default="n",type=str,help="delete the account specified, put d to delete")
	args = parser.parse_args()
	return args

def is_username_taken(ermrest,username):
	users = ermrest.get_data(8,"users") 
	usernames = [] 

	for user in users:
		usernames.append(user['username'])

	if username in usernames:
		return True
	return False

def is_phone_registered(ermrest,phone):
	users = ermrest.get_data(8,"users")
	phones = []

	for user in users:
		phones.append(user['phone_identification'])

	if phone in phones:
		return True
	return False

def delete(ermrest,username):
	success = bool()
	query = "/username="+username
	
	try:
		ermrest.delete_data(8,"users",query)
		success = True
	except:
		success = False

	return success
		

def register():
	args = parse_command_line()
	ermrest = ErmrestHandler("ec2-54-172-182-170.compute-1.amazonaws.com","root","root")

	if (args.delete == 'd'): 
		success = delete(ermrest,args.username)
		if (success):
			print("User '{}' successfully deleted".format(args.username))
			sys.exit(0)
		else:
			print("Invalid phone id. User '{}' not deleted".format(args.username))
			sys.exit(0)

	if (is_username_taken(ermrest,args.username)):
		print("Username '{}' is taken. Please choose another one".format(args.username))
		sys.exit(0)

	elif (is_phone_registered(ermrest,args.phone_id)):
		taken_username = str(ermrest.get_data(8,"users","/phone_identification="+args.phone_id)[0]['username'])
		print("Phone '{}' is already registered under the username '{}'".format(args.phone_id,taken_username))
		sys.exit(0)

	new_user_data = {"username":args.username,"phone_identification":args.phone_id}
	try:
		ermrest.put_data(8,"users",new_user_data)
		print("[*] Success: User '{}' has been added to the registry".format(args.username))
	except Exception as exc:
		print("[!] Error: "+str(exc))
		print("[!] Error: User '{}' has not been added to the registry".format(args.username))

if __name__ == "__main__":
	register()
