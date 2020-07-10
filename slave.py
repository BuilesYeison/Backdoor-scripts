#!/usr/bin/env python
#_*_ coding utf8 _*_

import os
import socket

s = socket.socket() #socket instance
port = 8080 
host = input(str("Please enter the server address: ")) #asking for the server that the user want to connect
s.connect((host, port)) #connect to the server
print("\nConnected to the server successfully")

#Connection has been completed 

#Command receiving and execution

while True:
    command = s.recv(1024) #receive the command from server script for execution
    command = command.decode() #decode command
    print("\nCommand received") 
    if command == "getcwd":
        files = os.getcwd() #get actual directory
        files = str(files) 
        s.send(files.encode()) #send the info encoded to server script
        print("\nCommand has been executed successfully...")
    elif command == "custom_dir":
        try:
            userInput = s.recv(5000)
            userInput = userInput.decode()
            files = os.listdir(userInput)
            files = str(files)
            s.send(files.encode())
            print("\nCommand has been executed succesfully...")
        except Exception as e:
            error = str("Path not found, try again")
            s.send(error.encode())
            print("\nError has been sent")
    else:
        print("\nCommand not recognised")