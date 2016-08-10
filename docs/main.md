# main.py file
The file that runs on startup. Runs a loop and handles user login

## is_user(ermrest) function
 - Takes an instance of ErmrestHandler class
 - checks if their is a user logged in the session_info table

## get_username(ermrest,phone_id) function
 - Takes an instance of ErmrestHandler class
 - Takes phone identification. This can be the Bluetooth Mac or phone name
 - Gets the name of the user attached to the mac address

## action(phone,ermrest) function
 - takes a tuple conataining info on the phone. (phone_name,mac address, RSSI)
 - takes an instance of ErmrestHandler class
 - Attempts to log user in. Returns True if successfull and False if not

## check_user_exists(ermrest,devices) function
 - takes an instance of ErmrestHandler
 - takes the mac addresses of devices in the area
 - checks if the logged in users phone is still in the area

## check_for_voice_login(ermrest,logged_in,logger) function
 - takes an instance of ErmrestHandler class
 - takes a boolean variable 'logged_in'. Says if a user is logged in at the moment
 - takes logger which is a file object to write to. All logs are written here
 - checks if a user logged in with their voice instead of bluetooth. Used to stop overwritting other users

## main() function
 - Polls every five seconds. If no user is logged in it will search for a local device using Phone_retriever instance
 - Never ending loop.
