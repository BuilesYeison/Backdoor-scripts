#!/usr/bin/env python
#_*_ coding utf8 _*_

import os
import socket

s = socket.socket() #socket instance
host = socket.gethostname() #getting name of the operating system machine
port = 8080 
s.bind((host, port)) #assign an ip and port to the socket instance for establish connection with other machine
print("\nServer is currently running at @",host)
print("\nWaiting for connections...")
s.listen(1) #waiting for connections (from slave.py in this case)
conn, addr = s.accept() #accept the connection
print(addr, "Has connected to the server successfully")

#connection has been complete

#command handling

while True:
    command = input(str("\nCommand >>> "))
    if command == "getcwd":
        conn.send(command.encode()) #send the command to slave script for execution
        print("\nCommand sent, waiting for execution...")
        print("\nCommand has been executed succesfully")
        files = conn.recv(5000) #receive the response from the slave script
        files = files.decode() #decode the received info
        print("\nCommand output: {}".format(files)) #show received info
    elif command == "custom_dir":
        conn.send(command.encode()) #send command to slave script
        userInput = input(str(" -Set custom dir: "))
        conn.send(userInput.encode()) #send the custom dir
        print("\nCommand has been sent")        
        files = conn.recv(5000) #receive data from slave script           
        files = files.decode()
        print("Custom dir result: {}".format(files))        
    else:
        print("\nCommand not recognised")