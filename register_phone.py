from ErmrestHandler import ErmrestHandler
import argparse
import sys

def parse_command_line():
	parser = argparse.ArgumentParser(description="Registers a phone for Blutooth Login")
	parser.add_argument("mac",type=str,help="the mac address of your phone")
	parser.add_argument("username",type=str,help="The username mapped to your phone name")
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
		phones.append(user['mac'])

	if phone in phones:
		return True
	return False

def register():
	args = parse_command_line()
	ermrest = ErmrestHandler("ec2-54-172-182-170.compute-1.amazonaws.com","root","root")
	if (is_username_taken(ermrest,args.username)):
		print("Username '{}' is taken. Please choose another one".format(args.username))
		sys.exit(0)
	elif (is_phone_registered(ermrest,args.mac)):
		taken_username = str(ermrest.get_data(8,"users","/mac="+args.mac)[0]['username'])
		print("Phone '{}' is already registered under the username '{}'".format(args.mac,taken_username))
		sys.exit(0)
	new_user_data = {"username":args.username,"mac":args.mac}
	try:
		ermrest.put_data(8,"users",new_user_data)
		print("[*] Success: User '{}' has been added to the registry".format(args.username))
	except Exception as exc:
		print("[!] Error: "+str(exc))
		print("[!] Error: User '{}' has not been added to the registry".format(args.username))

if __name__ == "__main__":
	register()
