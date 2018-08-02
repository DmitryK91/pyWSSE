# pyWSSE

REST client with WSSE header.

# Requirements:

Python 3.6

pip install pycurl  
pip install hashlib

# Use:

python REST.py  
    -r - GET/PUT.  
    -u - username.  
    -p - password hash.  
    -a - URI.  
    -d - file Json format. Only for PUT.  
    -r - results file. Optional, default: <USERPROFILE>/Documents/Result.txt