import socket
import threading
import os
import random


# Максимальный размер UDP пакета
UDP_MAX_SIZE = 65535


COMMANDS = (
    '/connect',
    '/exit',
)

"""
/connect <client> - connect to member
/exit - disconnect from client
"""


# Запускаем UDP-сервер
def listen(s: socket.socket, host: str, port: int):
    print("Server listen port", port)
    while True:
        print("lll")
        msg, addr = s.recvfrom(UDP_MAX_SIZE)
        msg_port = addr[-1]
        msg = msg.decode('ascii')
        allowed_ports = threading.current_thread().allowed_ports
        if msg_port not in allowed_ports:
            continue

        if not msg:
            continue

        if '__' in msg:
            command, content = msg.split('__')
        else:
            peer_name = f'client{msg_port}'
            print('\r\r' + f'{peer_name}: '+ msg + '\n' + f'you: ', end='')
            
            
# Слушаем сервер в отдельном потоке
def start_listen(target, socket, host, port):
    th = threading.Thread(target=target, args=(socket, host, port), daemon=True)
    th.start()

    
    return th



            

def connect(host: str = 'localhost', port: int = 3000):
    # Собственный порт
    own_port = random.randint(8000, 9000)   
    # Открываем UDP-сокет
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, own_port))
    
    listen_thread = start_listen(listen, s, host, port)
    allowed_ports = [port]
    listen_thread.allowed_ports = allowed_ports
    

    sendto = (host, port)
    print(own_port)
    
    
    while True:
        msg = input(f'you: ')
        sleep(2)
        command = msg.split(' ')[0]
        if command in COMMANDS:
            if msg == '/exit':
                peer_port = sendto[-1]
                allowed_ports.remove(peer_port)
                sendto = (host, port)
                print(f'Disconnect from client{peer_port}')

            if msg.startswith('/connect'):
                peer_port = int(msg.split(' ')[-1])
                allowed_ports.append(peer_port)
                sendto = (host, peer_port)
                print(f'Connect to client{peer_port}')
        else:
            s.sendto(msg.encode('ascii'), sendto)
    

    













if __name__ == '__main__':
    os.system('clear')
    print('Welcome to chat!')
    connect()