# Phone_retriever class
Searches the area for nearby phones using an instance of the RSSI_snatcher class and returns the phone
with the strongest Bluetooth signal.

## reset() method
creates a new ErmrestHandler instance so the cookie doesn't run out

## is_valid(phone) method
Checks if the phone is registered or not. Checks the "users" table for registered users.

## get_nearest_phone() method
Scans for nearby Bluetooth Connections using RSSI snatcher and then returns a tuple with information about
the nearest connection that is registered. 

## _init_logger() method
Initiates log file to write to.
