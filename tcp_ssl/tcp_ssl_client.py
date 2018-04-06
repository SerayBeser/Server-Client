import socket
import sys
import ssl
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


# TCP SSL
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ssl_socket = ssl.wrap_socket(client_socket,
                             ca_certs='server.crt',
                             cert_reqs=ssl.CERT_REQUIRED)


def connection_ready():
    client_socket.settimeout(100.0)
    return 1


def request_password():
    print >> sys.stderr, 'Process : Request Password'
    ssl_socket.write('1')
    try:
        data = ssl_socket.read()
        if str(data) == '12345':
            print ' Correct Password'
        else:
            print ' Wrong Password'
            process = ' Wrong Password. Ending the connection ...'
            ssl_socket.write(process)
            ssl_socket.close()
            print ' Connection ends.'''
    except socket.timeout:
        print '[Timeout] Connection Closed.'
        ssl_socket.close()


def request_file():
    print >> sys.stderr, 'Process : Request File'
    ssl_socket.write('2')
    print ' Please enter the file name ...'
    file_name = raw_input()
    try:
        ssl_socket.write(file_name)
        a = time.time()
        data = ssl_socket.read(1024)
        if str(data) != 'None':
            content_part = ''
            size_receiving = 100
            size_file = int(data)
            while size_file > size_receiving:
                data = ssl_socket.read(size_receiving)
                content_part = content_part + data
                size_file = size_file - size_receiving
            data = ssl_socket.read(size_receiving)
            content_part = content_part + data
            b = time.time()
            print ' Receiving Time : ', (b - a)
            file_content = content_part
            f_name = str(file_name).split('.')[0] + '_131101019.' + str(file_name).split('.')[1]
            with open(f_name, 'wb') as f:
                f.write(file_content)
            f.close()
            data = ssl_socket.read(1024)
            if str(data) == 'Done':
                print ' File transmission finished.'
        else:
            print ' File did not receive.'
    except socket.timeout:
        print '[Timeout] Connection Closed.'
        ssl_socket.close()


def send_file():
    print >> sys.stderr, 'Process : Send File'
    ssl_socket.write('3')
    print ' Please enter the file name ...'
    file_name = raw_input()
    while not os.path.exists(file_name):
        print ' File does not exist.\nPlease enter a valid file.'
        file_name = raw_input()

    buf = os.stat(file_name).st_size

    try:
        a = time.time()
        ssl_socket.write(file_name)
        with open(str(file_name), 'rb') as f:
            file_ = f.read(buf)
        ssl_socket.write(str(buf))
        size_sending = 100
        while len(file_) > size_sending:
            ssl_socket.write(file_[:size_sending])
            file_ = file_[size_sending:]
        ssl_socket.write(file_)
        b = time.time()
        print ' Sending Time : ', (b - a)
        print ' File has been write to server.'
        print str(Packet.number) + '. paket yollandi! ' + str(convert_bytes(buf))
        Packet.number = Packet.number + 1
        ssl_socket.write('Done')
    except socket.timeout:
        print '[Timeout] Connection Closed.'
        ssl_socket.close()


def run_processes():
    print 'Select Process\n\t[1] Request Password\n\t[2] Request File\n\t[3] Send File '
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
    # input_ = '127.0.0.1:1231'
    ip = input_.split(':')[0]
    port = int(input_.split(':')[1])
    print 'IP :', ip, '\nPort :', port
    ssl_socket.connect((ip, port))

    while connection_ready():
        run_processes()
