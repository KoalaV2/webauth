#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import bcrypt
import mariadb
from dotenv import load_dotenv
from os import getenv

load_dotenv()

DB_USER = getenv("DB_USER")
DB_PASSWD = getenv("DB_PASSWD")
DB_IP = getenv("DB_IP")
DB_DATABASE = getenv("DB_DATABASE")


try:
    conn = mariadb.connect(
        user=DB_USER,
        password=DB_PASSWD,
        host=DB_IP,
        port=3306,
        database=DB_DATABASE

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    exit()


class User:
    def __init__(self):
        self.salt = bcrypt.gensalt()
        self.c = conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS web (username VARCHAR(255),password VARCHAR(255))''')
        conn.commit()

    def createuser(self,username,password):
        self.c.execute("SELECT username from web")
        self.username = username
        self.c.execute(f"SELECT EXISTS(SELECT username FROM web WHERE username='{self.username}');")
        for row in self.c:
            if row[0] == 1:
                print("Username exists, exiting..")
                return("Username exists.")

        self.password = password.encode("utf-8")

        hashedpasswd = bcrypt.hashpw(self.password,self.salt)
        self.c.execute("INSERT INTO web VALUES (?,?);", (username, hashedpasswd))
        conn.commit()

def main():
    user = User()
    user.createuser("theo","lösenord")

if __name__ == "__main__":
    main()
