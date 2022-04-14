import socket, os
from tkinter import TRUE
from threading import Thread

class WebServer:

    def __init__(self, address='localhost', port=5000):
        self.port = port
        self.address = address
    
    def start(self):
        print('Iniciado conexão do servidor.')

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as comunicacao:
            comunicacao.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            comunicacao.bind((self.address, self.port))
            comunicacao.listen(10)

            while True:
                print('Aguardando conexão cliente...')
                conexao, addr = comunicacao.accept()
                req = HttpRequest(conexao, addr)
                req.start()
            
class HttpRequest(Thread):

    def __init__(self, conexao, addr):
        super(HttpRequest, self).__init__()
        self.conexao = conexao
        self.addr = addr
        self.CRLF = '\r\n'
        self.buffer_size = 4096
    
    def run(self):
        with self.conexao:
            print(f'Conectado com >>> {self.addr}')
            while(TRUE):
                mensagem = self.conexao.recv(1024).decode('utf-8')
                if mensagem == 'end':
                    print(f'Usuário {self.addr} desconectado')
                elif mensagem and mensagem != 'end':
                    print(f'Mensagem recebida >>> {mensagem}')

            # conexao.sendall(b"Mensagem recebida do cliente")