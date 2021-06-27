import socket
import os
import os.path
import sqlite3
from data_dedup import data_dedup_handler


class server(object):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.total_file = 0
        self.total_file_size = 0
        self.spacer = "SEPARATOR"
        self.IP = socket.gethostbyname(socket.gethostname())
        self.PORT = 4444
        self.ADDR = (self.IP, self.PORT)
        self.FORMAT = "utf-8"
        self.Buffer_size = 2048
        self.temp_path = "E:/Arpit/Personal n Clg/4th yr project dedupliction/Main Project/DataDedup/server/temp"
        self.user_database_path = "E:/Arpit/Personal n Clg/4th yr project dedupliction/Main Project/DataDedup/server/database/user_database.db"
        self.db_files_path = "E:/Arpit/Personal n Clg/4th yr project dedupliction/Main Project/DataDedup/server/database/db_files"

    def server_listerner(self):
        print("[STARTING] Server is Starting..")
        self.sock.bind(self.ADDR)
        self.sock.listen(1)
        print("[LISTENING] Server is listening.")

        while True:
            self.conn, addr = self.sock.accept()
            print(f'[NEW CONNECTION] {addr} connected. Authentication is required.')

            self.data = self.conn.recv(self.Buffer_size).decode(self.FORMAT).split(self.spacer)

            if self.data[0] == 'auth':
                self.username = str(self.data[1])
                self.password = str(self.data[2])

                rslt = self.user_db(self.username, self.password)
                if rslt == 1:
                    self.conn.send('Login Successful'.encode(self.FORMAT))
                else:
                    self.conn.send('Login Unseccessful'.encode(self.FORMAT))

            elif self.data[0] == 'filename':
                self.rawfilename = self.data[1]
                self.filename = os.path.basename(self.rawfilename)
                print(f"[RECV] Filename received {self.filename}")

                self.filedata = self.data[3]
                print("[RECV] File data received")
                complete_name = os.path.join(self.temp_path, self.filename)
                file = open(complete_name, "w")
                file.write(self.filedata)
                self.conn.send("File is uploaded successfully".encode(self.FORMAT))
                file.close()

            elif self.data[0] == "userinfo":
                username = self.data[1]
                user_info = self.user_file_info(username)
                self.conn.send(user_info.encode(self.FORMAT))
                print("user info sended")

            elif self.data[0] == "data-dedup":
                msg = data_dedup_handler()
                self.conn.send(f"{msg}{self.spacer}".encode(self.FORMAT))
                print(f"data sent: {msg}")

            elif self.data[0] == "refresh":
                try:
                    total_files, files_size = self.file_info()
                    # return f"{total_files}{self.spacer}{files_size}"
                    self.conn.send(f"{total_files}{self.spacer}{files_size}".encode(self.FORMAT))
                    print("Refresh Done.")
                except Exception as e:
                    print(e)
                    self.conn.send("nill".encode(self.FORMAT))

            elif self.data[0] == "logout":
                self.conn.send("Log out successfully".encode(self.FORMAT))
                self.conn.close()


    def user_file_info(self, uname):
        # sql for fetching the name of the username
        con = sqlite3.connect(self.user_database_path)
        c = con.cursor()
        statment = f"SELECT name from user_index WHERE username='{uname}'"
        c.execute(statment)
        raw_name = c.fetchone()
        name = ' '.join([str(elem) for elem in raw_name])
        total_files, files_size = self.file_info()
        return f"{name}{self.spacer}{total_files}{self.spacer}{files_size}"

    def file_info(self):
        # files information in main database folder
        files = os.listdir(self.db_files_path)
        total_files_db = len(files)
        file_size_db = 0

        for i in range(total_files_db):
            complete_path = os.path.join(self.db_files_path, files[i])
            rawfile_size = os.path.getsize(complete_path)
            file_size_db += rawfile_size

        self.total_file = total_files_db
        self.total_file_size = file_size_db

        # files information in temp folder
        file_size_temp = 0
        files_temp = os.listdir(self.temp_path)
        total_files_temp = len(files_temp)

        for i in range(total_files_temp):
            complete_path_temp = os.path.join(self.temp_path, files_temp[i])
            rawfile_size_temp = os.path.getsize(complete_path_temp)
            file_size_temp += rawfile_size_temp

        self.total_file += total_files_temp
        self.total_file_size += file_size_temp
        # return f"{self.total_file}{self.spacer}{self.total_file_size}"
        return self.total_file, self.total_file_size

    def user_db(self, us, ps):
        flag = 1
        con = sqlite3.connect(
            "E:/Arpit/Personal n Clg/4th yr project dedupliction/Main Project/DataDedup/server/database/user_database.db")
        c = con.cursor()
        c.execute("""CREATE  TABLE IF NOT EXISTS user_index (
                                        id  INTEGER PRIMARY KEY NOT NULL,
                                        name    TEXT,
                                        user_id     CHAR(50),
                                        username    TEXT,
                                        password   CHAR(50))""")
        # for update value in a particular field using where clause
        # UPDATE user_index SET name='admin' WHERE username='admin' AND password='admin'
        statement = f"SELECT username from user_index WHERE username='{us}' AND Password = '{ps}'"
        c.execute(statement)
        if not c.fetchone():
            print(c.fetchone())
            print('not matched')
            return 0
        else:
            print('Matched')
            return flag


connect = server()
connect.server_listerner()
