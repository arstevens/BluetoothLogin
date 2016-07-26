from ErmrestHandler import ErmrestHandler
import argparse

def parse_command_line():
	parser = argparse.ArgumentParser(description="Registers a phone for Blutooth Login")
	parser.add_argument("phone_name",type=str,help="The name of your phone")
	parser.add_argument("username",type=str,help="The username mapped to your phone name")
	args = parser.parse_args()
	return args

def register():
	args = parse_command_line()
	ermrest = ErmrestHandler("ec2-54-172-182-170.compute-1.amazonaws.com","root","root")
	new_user_data = {"username":args.username,"phone_name":args.phone_name}
	try:
		ermrest.put_data(8,"users",new_user_data)
		print("[*] Success: User {} has been added to the registry".format(args.username))
	except Exception as exc:
		print("[!] Error: "+str(exc))
		print("[!] Error: User {} has not been added to the registry".format(args.username))

if __name__ == "__main__":
	register()
