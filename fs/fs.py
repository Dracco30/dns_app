from http.server import BaseHTTPRequestHandler, HTTPServer
from socket import *

class FibonacciServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/fibonacci'):
            try:
                num = int(self.path.split('/')[-1])
            except ValueError:
                self.send_error(400, "Wrong Parameter Type!")
                return

            def helper(n):
                a, b = 1, 1
                for i in range(n - 1):
                    a, b = b, a + b
                return a

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(str(helper(num)).encode())
        else:
            self.send_error(404, "Not Found")

    def do_PUT(self):
        if self.path == '/register':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode()
            try:
                json_body = json.loads(body)
            except json.JSONDecodeError:
                self.send_error(400, "Bad Request")
                return

            hostname = json_body.get('hostname')
            ip = json_body.get('ip')
            as_ip = json_body.get('as_ip')
            as_port = json_body.get('as_port')

            dnsMessage = "TYPE=A\n" + "NAME=" + hostname + "\nVALUE=" + ip + "\nTTL=10"
            address = (ip, 53533)

            fibonacciSocket = socket(AF_INET, SOCK_DGRAM)
            fibonacciSocket.sendto(dnsMessage.encode(), address)

            response, addr = fibonacciSocket.recvfrom(2048)
            print(response.decode())

            self.send_response(201)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Registration Finished!')
        else:
            self.send_error(404, "Not Found")

def run_server():
    server_address = ('', 9090)
    httpd = HTTPServer(server_address, FibonacciServer)
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()