import socket

HOST = 'localhost'
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST,PORT))
    print('Conexão iniciada com o servidor')
    data = sock.recv(1024)
    print(data.decode('utf-8'))

    while True:
        data = sock.recv(1024)
        if data.decode('utf-8') == 'Acesso permitido!':
            break
        else:
            mensagem = input(data.decode('utf-8'))
            sock.sendall(mensagem.encode())

    print('Conectado ;)')
    while True:
        response = sock.recv(1024)
        mensagem = input(response.decode('utf-8'))
        sock.sendall(mensagem.encode())
        
        if mensagem == '0': 
            break
        else:
            response = sock.recv(1024)
            print(response.decode('utf-8'))