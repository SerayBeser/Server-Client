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


ip = '127.0.0.1'
port = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((ip, port))
print >> sys.stderr, 'Server Ready ...'

password = '12345'

while True:

    data, address = server_socket.recvfrom(1024)
    print >> sys.stderr, 'Incoming Process: ', data
    if str(data) == '1':
        print ' Responding to the request ...'
        server_socket.sendto(password, address)
        print ' Password has been send to client.'
    if str(data) == '2':
        data, address = server_socket.recvfrom(1024)
        file_name = data
        print ' Responding to the request ...'
        if os.path.exists(file_name):
            a = time.time()
            size_file = os.stat(file_name).st_size
            with open(file_name, 'rb') as f:
                file_ = f.read()
            server_socket.sendto(str(size_file), address)
            size_sending = 100
            while len(file_) > size_sending:
                server_socket.sendto(file_[:size_sending], address)
                file_ = file_[size_sending:]
            server_socket.sendto(file_, address)
            b = time.time()
            print ' Sending Time : ', (b - a)
            print ' File has been send to client.'
            i = 1
            print str(Packet.number) + '. paket yollandi! ' + str(convert_bytes(size_file))
            Packet.number = Packet.number + 1
            server_socket.sendto('Done', address)

        else:
            print ' File did not send.'
            server_socket.sendto('None', address)
    if str(data) == '3':
        print ' Waiting to the file ...'
        data, address = server_socket.recvfrom(1024)
        file_name = data
        data, address = server_socket.recvfrom(1024)
        content_part = ''
        size_receiving = 100
        size_file = int(data)
        a = time.time()
        while size_file > size_receiving:
            data, address = server_socket.recvfrom(size_receiving)
            content_part = content_part + data
            size_file = size_file - size_receiving
        data, address = server_socket.recvfrom(size_receiving)
        content_part = content_part + data
        b = time.time()
        print ' Receiving Time : ', (b - a)
        file_content = content_part
        f_name = str(file_name).split('.')[0] + '_131101019.' + str(file_name).split('.')[1]
        with open(f_name, 'w') as f:
            f.write(file_content)
        f.close()
        data, address = server_socket.recvfrom(1024)
        if str(data) == 'Done':
            print ' File transmission finished.'
