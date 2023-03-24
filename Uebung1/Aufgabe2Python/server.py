import sys
import socket
import threading

class Person:
  def __init__(self, name, ip, port):
    self.name = name
    self.ip = ip
    self.port = port
       

server_address = "127.0.0.1"
server_port = 5000

newest_message = ""

list_of_people = []

# create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((server_address, server_port))


while True:

    print("waiting for messages\n")
    data, addr = server_socket.recvfrom(1024)
    message = str(data, 'utf-8')
    print("received message: " + message)

    words = message.split()
    if words[0] == "l":
        new_person = Person(words[1], words[2], words[3])
        list_of_people.append(new_person)
    
    elif words[0] == "n":
       for person in list_of_people:
          if person.name == words[1]:
            response = "" + person.ip + " " + person.port 
            server_socket.sendto(bytes(response, 'utf-8'), addr)
    


