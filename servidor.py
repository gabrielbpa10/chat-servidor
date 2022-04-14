import socket

HOST = ""
PORT = 5000

print('Iniciado conexão do servidor.')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as comunicacao:
    comunicacao.bind((HOST, PORT))
    comunicacao.listen(2)

    print('Aguardando conexão cliente...')
    conexao, addr = comunicacao.accept()

    with conexao:
        print(f'Conectado com >>> {addr}')
        mensagem = conexao.recv(1024).decode('utf-8')

        print(f'Mensagem recebida >>> {mensagem}')

        conexao.sendall(b"Mensagem recebida do cliente")