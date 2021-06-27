import socket
import math


class client_server_cnnt(object):
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.IP = socket.gethostbyname(socket.gethostname())
        self.PORT = 4444
        self.addr = (self.IP, self.PORT)
        self.FORMAT = 'utf-8'
        self.spacer = "SEPARATOR"
        self.size = 2048
        self.client.connect(self.addr)

    def connect_server_auth(self, usern, pswrd):
        self.username = usern
        self.password = pswrd
        self.client.send(f"auth{self.spacer}{self.username}{self.spacer}{self.password}".encode(self.FORMAT))
        msg = self.client.recv(self.size).decode(self.FORMAT)
        print(f"[SERVER] {msg}")
        if msg == 'Login Successful':
            return 1
        else:
            self.client.close()
            return 0

    def file_upload_handler(self, filename):
        self.filename = filename
        # self.client.connect(self.addr)
        try:
            file = open(self.filename, 'r')
            data = file.read()
            # ("command-type"{self.spacer}
            self.client.send(
                f"filename{self.spacer}{self.filename}{self.spacer}filedata{self.spacer}{data}".encode(self.FORMAT))

            msg = self.client.recv(self.size).decode(self.FORMAT).split(self.spacer)
            return msg
        except Exception as e:
            print(e)

    def convert_size(self, size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    def user_info_fetch(self, uname):
        # self.client.connect(self.addr)
        self.client.send(f"userinfo{self.spacer}{uname}".encode(self.FORMAT))
        recv_data = self.client.recv(self.size).decode(self.FORMAT).split(self.spacer)
        name = recv_data[0]
        total_file = recv_data[1]
        files_size = recv_data[2]
        return name, total_file, self.convert_size(int(files_size))

    def data_refresh_handler(self):
        self.client.send(f"refresh{self.spacer}".encode(self.FORMAT))
        recv_data = self.client.recv(self.size).decode(self.FORMAT).split(self.spacer)
        return recv_data

    def data_dedup(self):
        # sending signal to server for checking data deduplication
        self.client.send(f"data-dedup{self.spacer}".encode(self.FORMAT))
        check_msg = self.client.recv(self.size).decode(self.FORMAT).split(self.spacer)[0]
        return check_msg

    def logout(self):
        self.client.send(f"logout{self.spacer}".encode(self.FORMAT))
        check_status = self.client.recv(self.size).decode(self.FORMAT)
        print(check_status)


def auth(username, password):
    client = client_server_cnnt()
    flag = client.connect_server_auth(username, password)
    return flag


# It feches the user name and file information after successful login
def user_fetch(uname):
    info = client_server_cnnt()
    data = info.user_info_fetch(uname)
    return data


# If uploads the file in the server and get msg in return
def file_upload_server(filename):
    handle = client_server_cnnt()
    msg = handle.file_upload_handler(filename)
    return msg


# It sends the command to the server for check data redundancy
def data_dedup_check():
    data_check = client_server_cnnt()
    msg = data_check.data_dedup()
    return msg


# Refresh the files and get the files details
def data_refresh_func():
    try:
        data = client_server_cnnt()
        msg = data.data_refresh_handler()
        return msg
    except Exception as e:
        print(e)


def logout_handler():
    logout_handle = client_server_cnnt()
    logout_handle.logout()
