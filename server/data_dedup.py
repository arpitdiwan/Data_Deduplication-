import sqlite3
import hashlib
import os.path
import shutil


class data_dedup_func(object):
    def __init__(self):
        self.temp_path = r"E:/Arpit/Personal n Clg/4th yr project dedupliction/Main Project/DataDedup/server/temp/"

    def hash_cal(self, filename):
        h = hashlib.sha1()
        f_path = r"E:/Arpit/Personal n Clg/4th yr project dedupliction/Main Project/DataDedup/server/temp/"
        with open(f_path + filename, "rb") as file:
            chunk = 0
            while chunk != b'':
                chunk = file.read(1024)
                h.update(chunk)
        print(f"Hash value successfully created: {filename}")
        return h.hexdigest()

    def file_delete(self, fname):
        file_name = fname
        file_path = r"E:\Arpit\Personal n Clg\4th yr project dedupliction\Main Project\DataDedup\server\temp"
        complete_fname = os.path.join(file_path, file_name)
        try:
            os.remove(complete_fname)
        except Exception as e:
            return f"Unable to delete the file due to Error: {e}"

    def file_move(self, fname):
        file_temp_path = r"E:\Arpit\Personal n Clg\4th yr project dedupliction\Main Project\DataDedup\server\temp"
        complete_src_path = os.path.join(file_temp_path, fname)
        file_db_path = r"E:\Arpit\Personal n Clg\4th yr project dedupliction\Main Project\DataDedup\server\database\db_files"
        try:
            shutil.move(complete_src_path, file_db_path)
        except Exception as e:
            print(e)

    def database(self, file_n, hash_v):
        conn = sqlite3.connect(r'E:\Arpit\Personal n Clg\4th yr project dedupliction\Main Project\DataDedup\server\database\hash_index.db')

        self.c = conn.cursor()

        self.c.execute("""CREATE  TABLE IF NOT EXISTS hash_index (
                                    id  INTEGER PRIMARY KEY NOT NULL,
                                    filename    TEXT,
                                    hashv   CHAR(50))""")

        # Comparing the hash values with the existing ones in the hash index
        statment = f"SELECT filename FROM hash_index WHERE hashv='{hash_v}'"
        self.c.execute(statment)
        if not self.c.fetchone():
            self.c.execute("insert into hash_index (filename, hashv) values (?,?)", (f'{file_n}', f'{hash_v}'))
            conn.commit()
            conn.close()
            self.file_move(file_n)
            return f'No Duplicate file detected.\n {file_n} Saved Successfully.'
        else:
            raw_fn = self.c.execute(f"SELECT filename FROM hash_index WHERE hashv='{hash_v}'")
            raw_fn = self.c.fetchone()
            fname = ' '.join([str(elem) for elem in raw_fn])
            self.file_delete(file_n)
            msg = f"Duplicate Hash Value is detected: {hash_v} \n\nOriginal File: {fname} \n[DELETING]  Duplicate file: {file_n}"
            conn.close()
            return msg

    def hash_db(self, file_n):
        filename = file_n
        msg = self.database(filename, self.hash_cal(filename))
        return msg


def data_dedup_handler():
    temp_path = r"E:/Arpit/Personal n Clg/4th yr project dedupliction/Main Project/DataDedup/server/temp/"
    files = os.listdir(temp_path)
    no_files = len(files)
    if no_files != 0:
        for i in range(no_files):
            file_name = files[i]
            print("***************************************************")
            hash_handler = data_dedup_func()
            msg = hash_handler.hash_db(file_name)

        return msg
    else:
        return f"{no_files} Duplicate File is found in the server."
