# this is tentatively put this for modifying in the future

import socket

def connect_to_cmw500(ip_address, port):
    """Connects to a CMW500 device on the specified IP address and port."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip_address, port))
    return sock

def send_command_to_cmw500(sock, command):
    """Sends a command to a CMW500 device over the socket."""
    sock.sendall(command.encode('utf-8'))

def receive_response_from_cmw500(sock):
    """Receives the response from a CMW500 device over the socket."""
    response = b""
    while True:
        data = sock.recv(1024)
        response += data
        if len(data) < 1024:
            break
    return response.decode()

def detect_equipment(ip_addr, port):
    """Detects the equipment connected to the socket."""
    cmd = '*IDN?' + '\r\n'
    sock = connect_to_cmw500(ip_addr, port)
    send_command_to_cmw500(sock, cmd)
    response = receive_response_from_cmw500(sock)

    print(response)

def main():
    """Connects to a CMW500 device and detects the equipment."""
    ip_addr = "192.168.1.100"
    port = 4882
    detect_equipment(ip_addr, port)


if __name__ == "__main__":
    main()