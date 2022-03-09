import socket
import sys
import json
import datetime
import random
HOST = '0.0.0.0'
PORT = 11112
print('Initialiting server at port the default UDP PORT: ',PORT)
print('IP ADDRESS: ',socket.gethostbyname(socket.gethostname()))


requestNumber=random.randint(0,40000)
# check if client_list exists, if not create one with empty dictionary inside
try:
    with open('client_list.json', 'r+') as reader:
        rereader = json.load(reader)
        print(rereader)
    reader.close()
except:
    currentTime = datetime.datetime.now()
    with open('log.txt', 'a+') as logfile:   
        logfile.write(str(currentTime)+' : Creating an empty clientlist')
        logfile.write('\n')
    logfile.close()
    f6 = {}
    with open('client_list.json', 'w+') as writer:
            writer.write(json.dumps(f6))
    writer.close()

# Initialize socket
try:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print('Socket created')
    currentTime = datetime.datetime.now()
    with open('log.txt', 'a+') as logfile:   
        logfile.write(str(currentTime)+' : Sucessfully created socket')
        logfile.write('\n')
    logfile.close() 
except socket.error as msg:
    print('Failed to created socket. Error code :' + str(msg[0]) + ' Message ' + msg[1])
    currentTime = datetime.datetime.now()
    with open('log.txt', 'a+') as logfile:   
        logfile.write(str(currentTime)+' : Failed to initialize socket')
        logfile.write('\n')
    logfile.close()    
    sys.exit()

# Initialize bind
try:
    serverSocket.bind((HOST, PORT))
    currentTime = datetime.datetime.now()
    with open('log.txt', 'a+') as logfile:   
        logfile.write(str(currentTime)+' : Scoket bind complete')
        logfile.write('\n')
    logfile.close()    
    print ('Socket bind complete')
except socket.error as msg:
    print ('Bind Failed. Error code: ' + str(msg[0]) + ' Message ' + msg[1])
    currentTime = datetime.datetime.now()
    with open('log.txt', 'a+') as logfile:   
        logfile.write(str(currentTime)+' : Socket bind error')
        logfile.write('\n')
    logfile.close()
    sys.exit()


# Keep receiving data
while 1:

    data_Received = serverSocket.recvfrom(1024)
    data = data_Received[0]
    client_Address = data_Received[1]

    # pass everything and wait for new data received in line 45
    if not data:
        pass
    
    isClient=False    
    temp = data.decode()
    with open('client_list.json', 'r+') as reader:
                    clientlistChcker = json.load(reader)
    reader.close()
    
 
    if clientlistChcker: # if it has stuff inside
        for key, values in clientlistChcker.items():

                if str(client_Address[0])==values[0]:
                    isClient=True
                    break
            
                        
    reader.close()    
    if temp =='registration':
        message = 'please enter your username'
        
        serverSocket.sendto(message.encode(),client_Address)
        flag = 0
        while flag<1:
                data_Received = serverSocket.recvfrom(1024)
                data = data_Received[0]
                client_Address = data_Received[1]
                name = data.decode()
                with open('client_list.json', 'r+') as reader:
                    clientlistObject = json.load(reader)
                yida=clientlistObject
                reader.close()
                if name in clientlistObject:    
                    message = 'REGISTER-DENIED RQ : '+str(requestNumber)+' Reason : '+name+' already exist'
                    reply = message.encode()
                    serverSocket.sendto(reply,client_Address)
                    currentTime = datetime.datetime.now()
                    with open('log.txt', 'a+') as logfile:   
                        logfile.write(str(currentTime)+' : REGISTER-DENIED RQ : '+str(requestNumber)+' Reason : '+name+' already exist')
                        logfile.write('\n')
                    logfile.close()   
                    requestNumber=requestNumber+1 
                else:
                    yida.setdefault(name, [client_Address[0],str(client_Address[1])])
                
                    message = 'REGISTERED '+str(requestNumber)
                    reply = message.encode()
                    serverSocket.sendto(reply,client_Address)
                    flag2=0
                    while flag2<1:
                        data_Received = serverSocket.recvfrom(1024)
                        data = data_Received[0]
                        
                        tcpport = data.decode()
                        yida[name].append(tcpport)
                        yida[name].append([])                        
                        with open('client_list.json', 'w+') as writer:
                            writer.write(json.dumps(yida))
                        writer.close()    
                        currentTime = datetime.datetime.now()
                        with open('log.txt', 'a+') as logfile:   
                            logfile.write(str(currentTime)+' : '+name+' REGISTERED RQ: '+str(requestNumber))
                            logfile.write('\n')
                        logfile.close()
                        requestNumber=requestNumber+1                      
                        flag2=flag2+1          
                flag=flag+1 # finish loop
    elif temp == 'print' and isClient ==True:
        with open('client_list.json', 'r+') as reader:
            clientlistObject = json.load(reader)
        
        reader.close()
        reply = json.dumps(clientlistObject).encode()
        serverSocket.sendto(reply,client_Address)
    
    elif temp == 'RETRIEVE-ALL' and isClient ==True:
        with open('client_list.json', 'r+') as reader:
            clientlistObject = json.load(reader)
        
        reader.close()
        currentTime = datetime.datetime.now()
        with open('log.txt', 'a+') as logfile:   
                            logfile.write(str(currentTime)+': RETRIEVE-ALL RQ: '+str(requestNumber))
                            logfile.write('\n')
        logfile.close()
              

        everyOneInfo = json.dumps(clientlistObject)
        reply='RETRIEVE RQ: '+str(requestNumber)+' '+everyOneInfo
        requestNumber=requestNumber+1
        serverSocket.sendto(reply.encode(),client_Address)

    elif temp == 'RETRIEVE-INFOT' and isClient ==True:
        with open('client_list.json', 'r+') as reader:
            clientlistObject = json.load(reader)
        message = 'enter the name of person you would like info on'
        reader.close()        
        reply = message.encode()
        serverSocket.sendto(reply,client_Address)
        data_Received = serverSocket.recvfrom(1024)
        currentTime = datetime.datetime.now()
        with open('log.txt', 'a+') as logfile:   
                            logfile.write(str(currentTime)+': RETRIEVE-INFOT RQ: '+str(requestNumber)+' on '+message)
                            logfile.write('\n')
        logfile.close()

        data = data_Received[0]        
        nameChecker=False        
        for key, values in clientlistObject.items():
            if key==data.decode():
                message='RETRIEVE-INFOT RQ: '+str(requestNumber)+'name:'+key+', ip:'+values[0]+', udp port:'+values[1]+', tcp port: '+values[2]+', list of files available : '
                for i in values[3]:
                    message+= i
                    message+= ' '
                reply=message.encode()
                requestNumber=requestNumber+1
                serverSocket.sendto(reply,client_Address)
                nameChecker=True
                break
        if nameChecker==False:
                message='RETRIEVE-ERROR RQ: '+str(requestNumber)+' Reason : person dont exist'
                reply=message.encode()
                serverSocket.sendto(reply,client_Address)           
                requestNumber=requestNumber+1


    elif temp == 'Publish' and isClient ==True:
        with open('client_list.json', 'r+') as reader:
            clientlistObject = json.load(reader)        
        reader.close()

        PublishChecker=False

        for key, values in clientlistObject.items():

            if str(client_Address[0])==values[0]:
                message = 'enter the name of the file'
                reply = message.encode()
                serverSocket.sendto(reply,client_Address)
                data_Received = serverSocket.recvfrom(1024)
                data = data_Received[0]
                          
                values[3].append(data.decode())
                currentTime = datetime.datetime.now()
                with open('log.txt', 'a+') as logfile:   
                        logfile.write(str(currentTime)+' : PUBLISH RQ : '+str(requestNumber)+' Name : '+name+' file : '+data.decode())
                        logfile.write('\n')
                logfile.close()                                   
                message = ' PUBLISH RQ : '+str(requestNumber)
                reply = message.encode()
                serverSocket.sendto(reply,client_Address)
                requestNumber=requestNumber+1 
                PublishChecker=True
                break
        if PublishChecker==False:
                message = ' PUBLISH-DENIED RQ : '+str(requestNumber)
                reply = message.encode()
                serverSocket.sendto(reply,client_Address)
                requestNumber=requestNumber+1   
        with open('client_list.json', 'w+') as writer:
            writer.write(json.dumps(clientlistObject))
        writer.close() 


    elif temp == 'Remove' and isClient ==True:
        with open('client_list.json', 'r+') as reader:
            clientlistObject = json.load(reader)        
        reader.close()

        RemoveChecker=False

        for key, values in clientlistObject.items():

            if str(client_Address[0])==values[0]:
                message = 'enter the name of the file to remove'
                reply = message.encode()
                serverSocket.sendto(reply,client_Address)
                data_Received = serverSocket.recvfrom(1024)
                data = data_Received[0]
                
                for i in values[3]:

                        if i == data.decode():
                            values[3].remove(i)
                            currentTime = datetime.datetime.now()
                            with open('log.txt', 'a+') as logfile:   
                                    logfile.write(str(currentTime)+' : REMOVE RQ : '+str(requestNumber)+' Name : '+name+' file to removed : '+data.decode())
                                    logfile.write('\n')
                            logfile.close()                                              
                
                            message = 'REMOVE RQ : '+str(requestNumber)
                            reply = message.encode()
                            requestNumber=requestNumber+1 
                            serverSocket.sendto(reply,client_Address)
                            RemoveChecker=True
                            break               
        if RemoveChecker==False:
                message = 'REMOVE-DENIED RQ : '+str(requestNumber)+' REASON : File dont exist'
                reply = message.encode()
                requestNumber=requestNumber+1 
                serverSocket.sendto(reply,client_Address)  
        with open('client_list.json', 'w+') as writer:
            writer.write(json.dumps(clientlistObject))
        writer.close()    

    elif temp == 'SEARCH-FILE' and isClient ==True:
        with open('client_list.json', 'r+') as reader:
            clientlistObject = json.load(reader)        
        reader.close()

        FileChecker=False
        fileInfo=''
        message = 'enter the name of the file to search for'
        reply = message.encode()
        currentTime = datetime.datetime.now()
     

        serverSocket.sendto(reply,client_Address)
        data_Received = serverSocket.recvfrom(1024)
        data = data_Received[0]
        with open('log.txt', 'a+') as logfile:   
                                    logfile.write(str(currentTime)+' : SEARCH-FILE RQ : '+str(requestNumber)+' File-name : '+data.decode())
                                    logfile.write('\n')
        logfile.close()

        for key, values in clientlistObject.items():

                for i in values[3]:

                        if i == data.decode():
                            
                            fileInfo+='name:'+key+', ip: '+values[0]+', tcp port: '+values[2]+'    '              
                

                            FileChecker=True
                            


        if FileChecker==False:
                message = ' SEARCH-ERROR RQ : '+str(requestNumber)+' Reason : file does not exist'
                reply = message.encode()
                requestNumber=requestNumber+1
                serverSocket.sendto(reply,client_Address)

        else:
            reply = 'SEARCH-FILE RQ '+str(requestNumber)+' '+fileInfo
            serverSocket.sendto(reply.encode(),client_Address)
            requestNumber=requestNumber+1

    elif temp == 'DE-REGISTER' and isClient ==True:
        with open('client_list.json', 'r+') as reader:
            clientlistObject = json.load(reader)        
        reader.close()
        
        for key, values in clientlistObject.items():

            if str(client_Address[0])==values[0]:
                clientlistObject.pop(key)
                currentTime = datetime.datetime.now()
                with open('log.txt', 'a+') as logfile:   
                    logfile.write(str(currentTime)+' : DE-REGISTER RQ: '+str(requestNumber)+' Name: '+key)
                    logfile.write('\n')
                logfile.close()
                requestNumber=requestNumber+1
                message = 'DE-REGISTER RQ: '+str(requestNumber)+' Name: '+key
    
                reply = message.encode()
                serverSocket.sendto(reply,client_Address)        
                break

        with open('client_list.json', 'w+') as writer:
            writer.write(json.dumps(clientlistObject))
        writer.close()          


    elif temp == 'UPDATE' and isClient ==True:
        with open('client_list.json', 'r+') as reader:
            clientlistObject = json.load(reader)        
        reader.close()
        updateChecker=False
        for key, values in clientlistObject.items():

            if str(client_Address[0])==values[0]:
                currentTime = datetime.datetime.now()
                with open('log.txt', 'a+') as logfile:   
                    logfile.write(str(currentTime)+' : UPDATE-CONTACT RQ: '+str(requestNumber)+' Name: '+key+ ' IP: '+values[0]+' UDP: '+values[1]+' TCP:'+values[2])
                    logfile.write('\n')
                logfile.close()
                username=key    #temp value stored to be used in line 420
                newIP=values[0] 
                newTCP=values[2]
                newUDP=values[1]
                message = 'enter the new ip address, or enter to skip/REFUSE'
                reply = message.encode()
                serverSocket.sendto(reply,client_Address)
                data_Received = serverSocket.recvfrom(1024)
                data = data_Received[0]
                if data.decode()=='':
                    
                    message = 'THE ip didnt change enter the new tcp address, or enter to skip/REFUSE'
                    reply = message.encode()
                    serverSocket.sendto(reply,client_Address)
                    
                else:
                    values[0]=data.decode()                  
                    updateChecker=True
                    message = 'THE ip did changed to'+values[0]+' enter the new tcp address, or enter to skip/REFUSE'
                    reply = message.encode()
                    serverSocket.sendto(reply,client_Address)                    
                    newIP=values[0] #temp value stored to be used

                data_Received = serverSocket.recvfrom(1024)
                data = data_Received[0]
                if data.decode()=='':
                    message = 'THE tcp didnt change, enter the new udp address, or enter to skip/REFUSE'
                    reply = message.encode()
                    serverSocket.sendto(reply,client_Address)
                else:
                    updateChecker=True
                    values[2]=data.decode() 
                    message = 'THE tcp did changed to'+values[2]+', enter the new udp address, or enter to skip/REFUSE'
                    reply = message.encode()
                    serverSocket.sendto(reply,client_Address)
                    newTCP=values[2] #temp value stored to be used 


                data_Received = serverSocket.recvfrom(1024)
                data = data_Received[0]
                if data.decode()=='':
                    pass
                    
                else:
                    updateChecker=True
                    values[1]=data.decode()
                    newUDP=values[1] #temp value stored to be used                
                    

                  

        with open('client_list.json', 'w+') as writer:
            writer.write(json.dumps(clientlistObject))
        writer.close()    

        if updateChecker==False:      
            message = 'UPDATE DENIED RQ: '+str(requestNumber)+' Name: '+username
            requestNumber=requestNumber+1  
            reply = message.encode()
            serverSocket.sendto(reply,client_Address)
        else:
            message = 'UPDATE CONFIRMED RQ: '+str(requestNumber)+' Name: '+username+ ' IP: '+newIP+' UDP: '+newUDP+' TCP:'+newTCP
            currentTime = datetime.datetime.now()
            with open('log.txt', 'a+') as logfile:   
                    logfile.write(str(currentTime)+' : UPDATE CONFIRMED RQ: '+str(requestNumber)+' Name: '+username+ ' IP: '+newIP+' UDP: '+newUDP+' TCP:'+newTCP)
                    logfile.write('\n')
            logfile.close()
            requestNumber=requestNumber+1            
            reply = message.encode()
            serverSocket.sendto(reply,client_Address)              

    elif isClient ==False:
        message = 'ur not a client'
        reply = message.encode()
        serverSocket.sendto(reply,client_Address)
    else:
        message = 'useless request, send something else'
        reply = message.encode()
        serverSocket.sendto(reply,client_Address)
    #print('Message[' + client_Address[0] + ':' + str(client_Address[1]) + '] - ' + str(data.strip()))
    
serverSocket.close()
