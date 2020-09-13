import socket
import select
import sys
import threading
from collections import Counter

HOST = '127.0.0.1'
PORT = 65432        

def inicia_servidor():
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.bind((HOST,PORT))
  sock.listen(5)
  return sock

def aceita_conexao(sock):
  conn, endr = sock.accept()
  return conn, endr

def atende_requisicoes(conn, endr):
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

  

def lista_palavras(text):
  return text[0].split()

def conta_palavras(array):
  print('Contando palavras')
  return Counter(array).most_common(10)

def main():
  sock = inicia_servidor()
  print("Pronto para receber conexões...")
  entradas = [sock] #select da API do Windows só recebe socket, stdin é um file descriptor

  while True:
    r, w, e = select.select(entradas, [], [])
    if sys.stdin.isatty():
      for line in sys.stdin:
        print(line)

    for pronto in r:
      if pronto == sock:
        conn, endr = aceita_conexao(sock)
        print("Conectado com : ", endr)
        thread_atendente = threading.Thread(target=atende_requisicoes, args=(conn, endr))
        thread_atendente.start()


main()