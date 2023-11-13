import socket

def send_request(request):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5000))

    client_socket.sendall(request.encode())

    response = client_socket.recv(1024)

    print(response.decode())

if __name__ == '__main__':
    request = 'GET /blog HTTP/1.1\r\nHost: localhost:5000\r\n\r\n'
    send_request(request)