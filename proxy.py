import select
import socket
import socketserver
import http.server
from time import sleep
from threading import Thread


def proxy_factory():
    class Proxy(http.server.SimpleHTTPRequestHandler):
        def get_client_conn(self):
            client_conn = socket.socket()
            host_port_split = self.path.split(':')
            host_port = host_port_split[0], int(host_port_split[-1])
            try:
                print('Connection {}: Started'.format(client_conn.fileno()))
                client_conn.connect(host_port)
            except socket.error as arg:
                print('Connection {}: Connection failed'.format(client_conn.fileno()))
                self.send_error(404, str(arg))
            return client_conn

        def send_data_to_hosts(self, client_conn):
            wait_items = [self.connection, client_conn]
            socket_idle = 0
            while True:
                input_ready, output_ready, exception_ready = select.select(wait_items, [], wait_items, .1)
                if exception_ready:
                    print('Connection {}: Error'.format(client_conn.fileno()))
                    return
                if input_ready:
                    for item in input_ready:
                        data = item.recv(8192)
                        if data:
                            if item is client_conn:
                                local_conn = self.connection
                            else:
                                local_conn = client_conn
                            local_conn.send(data)
                        else:
                            if socket_idle < 10:
                                sleep(1)
                                socket_idle += 1
                                print('Connection {}: Waiting for data'.format(client_conn.fileno()))
                            else:
                                return
                else:
                    if socket_idle < 10:
                        sleep(1)
                        socket_idle += 1
                        print('Connection {}: Waiting for connection'.format(client_conn.fileno()))
                    else:
                        return

        def do_HEAD(self):
            super().do_HEAD()

        def do_GET(self):
            super().do_GET()

        def do_POST(self):
            self.send_response(501)
            self.end_headers()

        def do_PUT(self):
            self.send_response(501)
            self.end_headers()

        def do_DELETE(self):
            self.send_response(501)
            self.end_headers()

        def do_CONNECT(self):
            client_conn = self.get_client_conn()
            try:
                if client_conn:
                    self.log_request(200)
                    self.wfile.write('{} 200 Connection established\nProxy-agent: {}\n\n'
                                     .format(self.protocol_version, self.version_string()).encode())
                    self.send_data_to_hosts(client_conn)
            finally:
                print('Connection {}: Closing'.format(client_conn.fileno()))
                client_conn.close()
                self.connection.close()
    return Proxy


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class ProxyBox:
    def __init__(self):
        self.port = 1234
        self.base_url = 'localhost'
        while True:
            try:
                self.server = ThreadedTCPServer((self.base_url, self.port), proxy_factory())
            except OSError:
                self.port += 1
            else:
                break
        self.server_thread = Thread(target=self.server.serve_forever)

    def start(self):
        self.server_thread.start()
        print('Proxy started on http://{}:{}'.format(self.base_url, self.port))
        sleep(60)
        print('Proxy exiting by timeout')
        self.shutdown()

    def shutdown(self):
        self.server.shutdown()
        self.server.server_close()


box = ProxyBox()
box.start()
