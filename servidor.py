import socket, os
import json
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
        self.dicionarios = []
    
    def run(self):
        with self.conexao:
            print(f'Conectado com >>> {self.addr}')
            self.conexao.sendall(b"Seja Bem Vindo!")

            with open('usuarios.json', encoding='utf-8') as usuarios:
                dados = json.load(usuarios)
            
            while(TRUE):
                self.conexao.send('Informe seu usuario: \n'.encode())
                USUARIO = self.conexao.recv(1024).decode('utf-8')
                self.conexao.send('Agora, informe sua senha: \n'.encode())
                SENHA = self.conexao.recv(1024).decode('utf-8')

                status = False
                for login in dados:
                    if USUARIO == login['username'] and SENHA == login['password']:
                        status = True
                        self.conexao.send('Acesso permitido!'.encode())
                        break

                if status == True:
                    break
                else:
                    self.conexao.send('Acesso negado! :() Tente novamente. \n'.encode())

            while(TRUE):
                self.conexao.send(b'##### MENU #################: \n 0 - Logout \n 1 - Todos \n')
                mensagem = self.conexao.recv(1024).decode('utf-8')
                
                if mensagem == '0':
                    print(f'Usuário {self.addr} desconectado')
                    self.conexao.send(b'0')
                    break
                elif mensagem and mensagem == '1':
                     with open('database.json', encoding='utf-8') as usuarios:
                        dados = json.load(usuarios)
                        
                        vetorMensagem = []
                        for msn in dados:
                            if msn['tipo'] == 'grupo':
                                opcao = 'Data da mensagem (' + msn['tempo'] + ') \n' + 'Mensagem >>> ' + msn['mensagem'] + ' \n'
                                vetorMensagem.append(opcao)
                                # mensagem = self.conexao.recv(1024).decode('utf-8')
                                # print(f'Mensagem recebida >>> {mensagem}')
                        self.conexao.send(opcao.encode())