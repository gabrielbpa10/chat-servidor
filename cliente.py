import socket

HOST = 'localhost'
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST,PORT))
    print('Conexão iniciada com o servidor')
    # sock.sendall(b"Hello World")
    # data = sock.recv(1024)
    # print(f"Começar: {data.decode('utf8')}")

    while True:
        mensagem = input('Escreva alguma mensagem: \n')
        sock.sendall(mensagem.encode('utf8'))
        
        if mensagem == 'END' or mensagem == 'end': 
            break
        