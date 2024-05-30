import cv2

from Server.Model.User import User
from Server.Util import Connection


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
                user = User(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9],0)
            img = cv2.imread(user.avatar)
            _, img_encoded = cv2.imencode('.jpg', img)
            dataImg = img_encoded.tobytes()
            user.dataImage = dataImg
            print(user.dataImage)
            return user
        except Exception as e:
            print(e)
            return {}

    def insertNewUser(self, dic):
        try:
            sql_check_username = 'SELECT * FROM user WHERE username = %s'
            self.myCursor.execute(sql_check_username, [dic['username']])
            result = self.myCursor.fetchall()
            if result == []:
                sql = 'INSERT INTO user (username, password,phone,id_role) VALUES ( %s, %s, %s,1)'
                self.myCursor.execute(sql, [dic['username'], dic['password'], dic['phone']])
                self.connect.commit()
                get_Infor = 'SELECT * FROM user WHERE username = %s'
                self.myCursor.execute(get_Infor, [dic['username']])
                result = self.myCursor.fetchall()
                user = []
                # user = User(item[0], item[1], item[2])
                for item in result:
                    user = User(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8],
                                item[9])
                img = cv2.imread(user['avatar'])
                _, img_encoded = cv2.imencode('.jpg', img)
                dataImage = img_encoded.tobytes()
                user['dataImage'] = dataImage
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
            get_Infor = 'SELECT * FROM user WHERE username = %s'
            self.myCursor.execute(get_Infor, [dic['username']])
            result = self.myCursor.fetchall()
            user = []
            # user = User(item[0], item[1], item[2])
            for item in result:
                user = User(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9])
            img = cv2.imread(user.avatar)
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
