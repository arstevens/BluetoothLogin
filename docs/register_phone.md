# register_phone.py file
registers phone for Bluetooth Login.

## parse_command_line() function
Gets the phone_id and username from the user. Also checks if the user wants to delete their account.
returns arguments.

## is_username_taken(ermrest,username) function 
checks if the username provided is in use by another user

## is_phone_registered(ermrest,phone) function
checks if the phone identification the user provided is in use
already.

## delete(ermrest,username) function
deletes a user from the registry.
returns success status

## register() function
attempts to register the phone.
