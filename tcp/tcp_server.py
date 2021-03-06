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
port = 1237

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((ip, port))
server_socket.listen(1)
print >> sys.stderr, 'Server Ready ...'
while True:

    print >> sys.stderr, 'Waiting for a connection ...'
    connection, address = server_socket.accept()
    try:
        print >> sys.stderr, 'connection from', address

        password = '12345'
        while True:

            data = connection.recv(1024)
            print >> sys.stderr, 'Incoming Process: ', data
            if str(data) == '1':
                print ' Responding to the request ...'
                connection.sendall(password)
                print ' Password has been send to client.'

            if str(data) == '2':
                file_name = connection.recv(1024)
                print ' Responding to the request ...'
                if os.path.exists(file_name):
                    a = time.time()
                    buf = os.stat(file_name).st_size
                    connection.sendall(str(buf))
                    with open(file_name, 'rb') as f:
                        file_ = f.read()
                    size_sending = 100
                    while len(file_) > size_sending:
                        connection.sendall(file_[:size_sending])
                        file_ = file_[size_sending:]
                    if len(file_) > 0:
                        connection.sendall(file_)
                    b = time.time()
                    print ' Sending Time : ', (b - a)
                    print ' File has been sendall to client.'
                    print str(Packet.number) + '. paket yollandi! ' + str(convert_bytes(buf))
                    Packet.number = Packet.number + 1
                    connection.sendall('Done')
                else:
                    print ' File did not send.'
                    connection.sendall('None')

            if str(data) == '3':
                print ' Waiting to the file ...'
                data = connection.recv(1024)
                file_name = data
                data = connection.recv(1024)
                content_part = ''
                file_receiving = 100
                size_file = int(data)
                a = time.time()
                while size_file > file_receiving:
                    data = connection.recv(file_receiving)
                    content_part = content_part + data
                    size_file = size_file - file_receiving
                data = connection.recv(file_receiving)
                content_part = content_part + data
                b = time.time()
                print ' Receiving Time : ', (b - a)
                file_content = content_part
                f_name = str(file_name).split('.')[0] + '_131101019.' + str(file_name).split('.')[1]
                with open(f_name, 'w') as f:
                    f.write(file_content)
                f.close()
                data = connection.recv(1024)
                if str(data) == 'Done':
                    print ' File transmission finished.'
    finally:
        connection.close()
