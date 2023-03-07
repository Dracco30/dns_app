from flask import Flask, abort, request
from socket import *

app = Flask(__name__)

@app.route('/')

def initialize():
    return "You should visit /fibonacci with several parameters to get the IP address of the Fibonacci Server"


@app.route('/fibonacci', methods = ["GET"], endpoint="fibonacci")
def userServer():
    arg = request.args
    if not arg.get("hostname") or not arg.get("fs_port") or not arg.get("number") or not arg.get("as_ip") or not arg.get("as_port"):
        abort(400)
    else:
        hostname = arg.get("hostname")
        as_ip = arg.get("as_ip")
        num = arg.get("number")
        as_port = arg.get("as_port")
        dnsMessage = "TYPE=A\n" + "NAME=" + hostname
        userSocket = socket(AF_INET, SOCK_DGRAM)
        address = (as_ip, int(as_port))
        userSocket.sendto(dnsMessage.encode(), address)

        responseMessage, authoritativeAddress = userSocket.recvfrom(2048)
        decode = responseMessage.decode()
        response = decode.split('\n')
        for line in response:
            print(line)
            name, value = line.split('=')
            if name == 'VALUE':
                ip = value
                print(ip)
                break

        if ip == "0.0.0.0":
            return "No IP address for the input fibonacci server exists"
        else:
            return "The IP address of Fibonacci Server is: " + ip

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)