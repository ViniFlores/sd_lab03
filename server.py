import socket
from collections import Counter

def lista_palavras(text):
  return text[0].split()

def conta_palavras(array):
  print('Contando palavras')
  return Counter(array).most_common(10)

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.bind((HOST, PORT))
  s.listen()
  while True:
    print('Esperando conexão...')
    conn, addr = s.accept()
    with conn:
        print('Recebendo conexão')
        while True:
            data = conn.recv(4096)
            if not data:
                break

            lista_de_arquivos = eval(data.decode('utf-8'))

            resultado = {}

            for arquivo in lista_de_arquivos:
              file = open("arquivos/" + arquivo, "r")
              print('Abrindo arquivo ' + arquivo + '')
              resultado[arquivo] = conta_palavras(lista_palavras(file.readlines()))

            conn.sendall((str(resultado)).encode())

