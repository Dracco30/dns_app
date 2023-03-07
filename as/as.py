from socket import *

# Create a socket and bind it to port 53533
dns_socket = socket(AF_INET, SOCK_DGRAM)
dns_socket.bind(('', 53533))

while True:
    # Receive a DNS request from a client
    request, client_address = dns_socket.recvfrom(2048)
    request = request.decode()

    # Print the request for debugging purposes
    print("Received request:", request)

    # Parse the request to determine if it's a query or registration
    lines = request.split('\n')
    if len(lines) == 2:
        # This is a query, extract the hostname from the request
        query_hostname = lines[1].split('=')[1]

        # Search for the IP address in the DNS.txt file
        found = False
        with open("DNS.txt", "r") as dns_file:
            for line in dns_file:
                name, ip = line.strip().split('=')
                if name == query_hostname:
                    response_ip = ip
                    found = True
                    break

        # If the IP address was found, send a response to the client
        if found:
            response = f"TYPE=A\nNAME={query_hostname}\nVALUE={response_ip}\nTTL=10"
        else:
            response = "NOT FOUND"

        # Send the response to the client
        dns_socket.sendto(response.encode(), client_address)
    else:
        # This is a registration, extract the hostname and IP address from the request
        hostname = lines[1].split('=')[1]
        ip = lines[2].split('=')[1]

        # Add the hostname and IP address to the DNS.txt file
        with open("DNS.txt", "a") as dns_file:
            dns_file.write(f"{hostname}={ip}\n")

        # Send a response to the client
        response = "REGISTERED"
        dns_socket.sendto(response.encode(), client_address)