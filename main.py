import socket
from views import *
'''
Создается словарь URLS, в котором каждому пути соответствует определенная функция. 
Например, '/' соответствует функции index, а '/blog' - функции blog.
'''
URLS = {
    '/': index,
    '/blog': blog,
}

'''
Определяется функция generate_headers, которая принимает метод запроса и URL в 
качестве аргументов. Возвращает кортеж с заголовками ответа (строка) и кодом состояния
(число). Если метод запроса не является GET, возвращается заголовок "HTTP/1.1 405 Method
not allowed" и код 405. Если URL отсутствует в словаре URLS, возвращается заголовок
"HTTP/1.1 404 Not found" и код 404. В остальных случаях возвращается заголовок
"HTTP/1.1 200 OK" и код 200.
'''


def generate_headers(method, url):
    if not method == 'GET':
        return ('HTTP/1.1 405 Method not allowed\n\n', 405)

    if not url in URLS:
        return ('HTTP/1.1 404 Not found\n\n', 404)

    return ('HTTP/1.1 200 OK\n\n', 200)


'''
Определяется функция generate_content, которая принимает код состояния и URL в качестве аргументов.
Если код состояния равен 404, возвращается строка с HTML-разметкой для страницы "Not found".
Если код состояния равен 405, возвращается строка с HTML-разметкой для страницы "Method not allowed".
В остальных случаях вызывается функция, соответствующая URL из словаря URLS.
'''


def generate_content(code, url):
    if code == 404:
        return '<h1>  404  </h1><p>  Not found  </p>'
    if code == 405:
        return '<h1>  405  </h1><p>  Method not allowed  </p>'
    return URLS[url]()


'''
Определяется функция parse_request, которая принимает запрос в виде строки и разбивает его на
метод и URL, используя разделитель пробела. Возвращает кортеж из метода и URL.
'''


def parse_request(request):
    parsed = request.split(' ')
    method = parsed[0]
    url = parsed[1]
    return method, url


'''
Определяется функция generate_response, которая принимает запрос в виде строки.
С помощью функций parse_request, generate_headers и generate_content получает заголовки,
код состояния и тело ответа. Возвращает закодированный ответ в виде строки.
'''


def generate_response(request):
    method, url = parse_request(request)
    headers, code = generate_headers(method, url)
    body = generate_content(code, url)

    return (headers + body).encode()


'''
Определяется функция run, которая выполняет следующие действия:

1)Создает серверный сокет, привязывает его к локальному хосту на порту 5000 и запускает
прослушивание подключений.
2)В бесконечном цикле принимает клиентский сокет и запрос.
3)Выводит на экран декодированную строку запроса (удобная форма отображения при помощи UTF-8), а также адрес и сокет клиента.
4)Генерирует ответ с помощью функции generate_response.
5)Отправляет ответ клиенту и закрывает соединение.
'''


def run():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5000))
    server_socket.listen()

    while True:
        client_socket, addr = server_socket.accept()
        request = client_socket.recv(1024)
        # print(request.decode('utf-8')) удобная форма отображения при помощи utf-8
        print(request.decode)
        print()
        print(addr)
        print(client_socket)

        response = generate_response(request.decode('utf-8'))

        client_socket.sendall(response)
        client_socket.close()


'''
Вызывает функцию run, только если модуль запущен непосредственно, а не импортирован как модуль.
'''
if __name__ == '__main__':
    run()
