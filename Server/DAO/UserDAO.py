import os
import sys

import cv2

from Server.Model.User import User
from Server.Util import Connection

current_directory = os.path.dirname(os.path.abspath(__file__)) + '\\'
# sys.path.append(current_directory)
class UserDAO:
    def __init__(self):
        self.connect = Connection.getConnect()
        self.myCursor = self.connect.cursor()

    def findByUsernameAndPassword(self, dic):
        try:

            sql = 'SELECT * FROM user WHERE username = %s AND password = %s'
            self.myCursor.execute(sql, [dic['username'], dic['password']])
            result = self.myCursor.fetchall()
            # item = result[0]
            user = []
            # user = User(item[0], item[1], item[2])
            for item in result:
                user = User(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9],0,0)
            # print(current_directory)
            img = cv2.imread(current_directory + user.avatar)
            _, img_encoded = cv2.imencode('.jpg', img)
            dataImg = img_encoded.tobytes()
            user.dataImage = dataImg
            return user
        except Exception as e:
            print(e)
            return {}

    def insertNewUser(self, dic):
        try:
            print("header")
            sql_check_username = 'SELECT * FROM user WHERE username = %s'
            self.myCursor.execute(sql_check_username, [dic['username']])
            result = self.myCursor.fetchall()
            if result == []:
                sql = 'INSERT INTO user (username, password,phone,avatar,id_role) VALUES ( %s, %s, %s,"E:/PBL_2/PBL5/Server/DB/images.jpg",1)'
                self.myCursor.execute(sql, [dic['username'], dic['password'], dic['phone']])
                self.connect.commit()
                get_Infor = 'SELECT * FROM user WHERE username = %s'
                self.myCursor.execute(get_Infor, [dic['username']])
                result = self.myCursor.fetchall()
                user = []
                # user = User(item[0], item[1], item[2])
                for item in result:
                    user = User(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8],
                                item[9],0,0)
                img = cv2.imread(current_directory + user.avatar)

                _, img_encoded = cv2.imencode('.jpg', img)
                dataImage = img_encoded.tobytes()
                user.dataImage = dataImage
                print(user)
                return user
            else:
                msg = "username already exists"
                return msg
        except Exception as e:
            print(e)

    def UpdateUser(self, dic):
        try:

            sql = 'UPDATE user SET  lastname = %s ,firstname = %s ,email = %s, gender = %s , phone = %s, avatar = %s WHERE username = %s'
            self.myCursor.execute(sql, [dic['lastname'],dic['firstname'],dic['email'],dic['gender'],dic['phone'],dic['dataImage'],dic['username']])
            self.connect.commit()
            print("edit succeed")
            get_Infor = 'SELECT * FROM user WHERE username = %s'
            self.myCursor.execute(get_Infor, [dic['username']])
            result = self.myCursor.fetchall()
            user = []
            # user = User(item[0], item[1], item[2])
            for item in result:
                user = User(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9],0,0)
            img = cv2.imread(current_directory + user.avatar)
            _, img_encoded = cv2.imencode('.jpg', img)
            dataImg = img_encoded.tobytes()
            user.dataImage = dataImg
            print(user)
            return user
        except Exception as e:
            print(e)

    def Change_Password(self, dic):
        try:
            sql = 'UPDATE user SET  password = %s WHERE username = %s'
            self.myCursor.execute(sql, [dic['password'], dic['username']])
            self.connect.commit()
        except Exception as e:
            print(e)

    def Delete_User(self,dic):
        try:
            sql_delete = 'DELETE FROM user WHERE id = %s'
            self.myCursor.execute(sql_delete, [dic['id']])
            self.connect.commit()

            sql = 'SELECT * FROM user'
            self.myCursor.execute(sql)
            result = self.myCursor.fetchall()
            # item = result[0]
            users = []
            # user = User(item[0], item[1], item[2])
            for item in result:
                user = User(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9], 0,0)
                img = cv2.imread(current_directory + user.avatar)
                _, img_encoded = cv2.imencode('.jpg', img)
                dataImg = img_encoded.tobytes()
                user.dataImage = dataImg
                users.append(user)
            return users
        except Exception as e:
            print(e)
    def getAllUser(self):
        try:
            sql = 'SELECT * FROM user'
            self.myCursor.execute(sql)
            result = self.myCursor.fetchall()
            # item = result[0]
            users = []
            # user = User(item[0], item[1], item[2])
            for item in result:
                user = User(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9], 0,0)
                img = cv2.imread(current_directory + user.avatar)
                _, img_encoded = cv2.imencode('.jpg', img)
                dataImg = img_encoded.tobytes()
                user.dataImage = dataImg
                users.append(user)
            return users
        except Exception as e:
            print(e)

    def getListRank(self,dic):
        try:
            sql = 'SELECT user.ID,user.lastname,user.firstname,user.email,user.username,user.`password`,user.gender,user.id_role,user.avatar,user.phone,SUM(user_word.`point`) AS point FROM user INNER JOIN user_word ON user_word.ID_user = user.ID GROUP BY user.ID,user.lastname,user.firstname,user.email,user.username,user.`password`,user.gender,user.id_role,user.avatar,user.phone ORDER BY point DESC;'
            self.myCursor.execute(sql)
            result = self.myCursor.fetchall()
            # item = result[0]
            users = []
            # user = User(item[0], item[1], item[2])
            for item in result:
                user = User(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9], 0, item[10])
                img = cv2.imread(current_directory + user.avatar)
                _, img_encoded = cv2.imencode('.jpg', img)
                dataImg = img_encoded.tobytes()
                user.dataImage = dataImg
                users.append(user)
            return users
        except Exception as e:
            print(e)

    def getWord(self,dic):
        try:
            sql = 'SELECT word.word FROM word INNER JOIN user_word ON word.ID = user_word.ID_word WHERE user_word.ID_user = %s'
            self.myCursor.execute(sql,[dic['id']])
            result = self.myCursor.fetchall()
            # item = result[0]
            word = []
            # user = User(item[0], item[1], item[2])
            for item in result:
                word.append(item)
            return word
        except Exception as e:
            print(e)
