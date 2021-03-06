import socket
import sys
import os.path
import time


class Packet:
    number = 1

    def __init__(self):
        self.number = 1


def convert_bytes(data_bytes, precision=2):
    size = ['B', 'KB', 'MB', 'GB', 'TB']
    index = 0
    while data_bytes > 1024 and index < 4:
        index += 1
        data_bytes = data_bytes / 1024.0
    return '%.*f %s' % (precision, data_bytes, size[index])


# UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def connection_ready():
    client_socket.settimeout(100.0)
    return 1


def request_password():
    print >> sys.stderr, 'Process : Request Password'
    client_socket.sendto('1', (ip, port))
    try:
        data, server = client_socket.recvfrom(1024)
        if str(data) == '12345':
            print ' Correct Password'
        else:
            print ' Wrong Password'
            process = ' Wrong Password. Ending the connection ...'
            client_socket.sendto(process, (ip, port))
            client_socket.close()
            print ' Connection ends.'''
    except socket.timeout:
        print '[Timeout] Connection Closed.'
        client_socket.close()


def request_file():
    print >> sys.stderr, 'Process : Request File'
    client_socket.sendto('2', (ip, port))
    print ' Please enter the file name ...'
    file_name = raw_input()
    try:
        client_socket.sendto(file_name, (ip, port))
        a = time.time()
        data, address = client_socket.recvfrom(1024)
        if str(data) != 'None':
            content_part = ''
            size_receiving = 100
            size_file = int(data)
            while size_file > size_receiving:
                data, address = client_socket.recvfrom(size_receiving)
                content_part = content_part + data
                size_file = size_file - size_receiving
            data, address = client_socket.recvfrom(size_receiving)
            content_part = content_part + data
            b = time.time()
            print ' Receiving Time : ', (b - a)
            file_content = content_part
            f_name = str(file_name).split('.')[0] + '_131101019.' + str(file_name).split('.')[1]
            with open(f_name, 'w') as f:
                f.write(file_content)
            f.close()

            data, address = client_socket.recvfrom(1024)
            if str(data) == 'Done':
                print ' File transmission finished.'
        else:
            print ' File did not receive.'
    except socket.timeout:
        print '[Timeout] Connection Closed.'
        client_socket.close()


def send_file():
    print >> sys.stderr, 'Process : Send File'
    client_socket.sendto('3', (ip, port))
    print ' Please enter the file name ...'
    file_name = raw_input()
    while not os.path.exists(file_name):
        print ' File does not exist.\nPlease enter a valid file.'
        file_name = raw_input()

    buf = os.stat(file_name).st_size

    try:
        a = time.time()
        client_socket.sendto(file_name, (ip, port))
        with open(str(file_name), 'rb') as f:
            file_ = f.read(buf)
        client_socket.sendto(str(buf), (ip, port))
        size_sending = 100
        while len(file_) > size_sending:
            client_socket.sendto(file_[:size_sending], (ip, port))
            file_ = file_[size_sending:]
        client_socket.sendto(file_, (ip, port))
        b = time.time()
        print ' Sending Time : ', (b - a)
        print ' File has been send to server.'
        print str(Packet.number) + '. paket yollandi! ' + str(convert_bytes(buf))
        Packet.number = Packet.number + 1
        client_socket.sendto('Done', (ip, port))
    except socket.timeout:
        print '[Timeout] Connection Closed.'
        client_socket.close()


def run_processes():
    print 'Select Process\n\t[1] Request Password\n\t[2] Request File\n\t[3] Send File'
    id_ = raw_input()
    if str(id_) == '1':
        request_password()
    if str(id_) == '2':
        request_file()
    if str(id_) == '3':
        send_file()


if __name__ == '__main__':
    print 'Please Enter IP:Port ...'
    input_ = raw_input()
    # input_ = '127.0.0.1:1234'
    ip = input_.split(':')[0]
    port = int(input_.split(':')[1])

    print 'IP :', ip, '\nPort :', port
    while connection_ready():
        run_processes()
