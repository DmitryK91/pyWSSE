# pyWSSE

REST.py - REST client with WSSE header.  
WSSEGen.py - WSSE header generate.  
main.py - Show GUI.  

## Requirements:

Python 3.6

pip install pycurl  
pip install hashlib

## Use:

python main.py

python REST.py  
-t - GET/PUT.  
-u - username.  
-p - password hash.  
-a - URI.  
-d - file Json format. Only for PUT.  
-r - results file. Optional, default: <USERPROFILE>/Documents/Result.txt

python WSSEGen.py  
-u <USER>  
-p <PASSWORD>  