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
                self.dicionarios = []
                for login in dados:
                    if USUARIO == login['username'] and SENHA == login['password']:
                        with open('logs.json', encoding='utf-8') as usuarios:
                            dados = json.load(usuarios)
                            print(dados)
                        if len(dados) > 0:
                            dicionarios = dados
                        
                        dicionario = {
                            'username': USUARIO,
                            'ip': self.addr[0],
                            'port':self.addr[1]
                        }
                        self.dicionarios.append(dicionario)

                        json_object = json.dumps(self.dicionarios, indent=1)
                        with open('logs.json','w') as escrever:
                            escrever.write(json_object)
                        
                        self.conexao.send('Acesso permitido!'.encode())
                        status = True
                        break
                    else:
                        self.conexao.send('Acesso negado! :() Tente novamente. \n'.encode())

                if status == True:
                    break

            while(TRUE):
                self.conexao.send(b'Informe com quem voce deseja se comunicar: \n 0 - Logout \n 1 - Todos \n')
                mensagem = self.conexao.recv(1024).decode('utf-8')
                
                if mensagem == '0':
                    print(f'Usuário {self.addr} desconectado')
                    break
                elif mensagem and mensagem == '1':
                    self.conexao.send('Envie uma mensagem: \n'.encode())
                    mensagem = self.conexao.recv(1024).decode('utf-8')
                    print(f'Mensagem recebida >>> {mensagem}')
                    for d in self.dicionarios:
                        print(d)
                        cliente = '(' + str(d['ip']) + ',' + str(d['port']) + ')'
                        print(cliente)
                        #TypeError: sendto(): AF_INET address must be tuple, not str
                        self.conexao.sendto(mensagem.encode(),0,cliente)
                    print(f'Mensagem enviada >>> {mensagem}')

            # self.conexao.sendall(b"Mensagem recebida do cliente")