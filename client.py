import socket
import sys

HOST = '127.0.0.1'
PORT = 65432 

arquivos = sys.argv[1:]
arquivos = str(arquivos)
arquivos = arquivos.encode()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.connect((HOST, PORT))
  s.send(arquivos)
  data = s.recv(4096)

server_response = eval(data.decode('utf-8'))

for arquivo in server_response:
  print("Arquivo: " + arquivo)
  for tupla in server_response[arquivo]:
    print("A palavra " + tupla[0] + " apareceu " + str(tupla[1]) + " vezes.")
  print("")