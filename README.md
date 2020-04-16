# Sockets-API
the python version is 3.7
## How to use:
### 1. Run the server:
   #### ./Server.py (0 for hostname, 1 for ip address) (hostname or ip address) (port)
   for example:
   #### ./Server.py 0 localhost 12235 or ./Client.py 1 127.0.0.1 12235
   #### Notice that our server keeps opening to accept the request from the client, to exit, please use ctrl+C

### 2. Run the client:
   #### ./Client.py (0 for hostname, 1 for ip address) (hostname or ip address) (port)  
   for example:
   #### ./Client.py 0 attu2.cs.washington.edu 12235 or ./Client.py 1 128.208.1.138 12235

### The following test passed in our local machine
#### ./Client.py 0 attu2.cs.washington.edu 12235 (Our client successfully connect with atuu server)
#### ./Server.py 0 localhost 12235 AND ./Client.py 0 localhost 12235 (Our client successfully connect with our server
