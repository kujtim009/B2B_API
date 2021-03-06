from db import db
from flask_jwt_extended import get_jwt_claims, get_jwt_identity
import json
from datetime import datetime


class UserModel(db.Model):
    __tablename__ = 'api_fgx_Users'

    ID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    access_level = db.Column(db.String(80))

    def __init__(self, username, password, access_level):
        self.username = username
        self.password = password
        self.access_level = access_level

    def json(self):
        return {
            'id': self.ID,
            'username': self.username,
            'access_level': self.access_level
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(ID=_id).first()

    @classmethod
    def is_admin(cls):
        access = int(get_jwt_claims())
        if access == 1:
            return True
        return False


class Userinfo(db.Model):
    __tablename__ = 'api_fgx_Users_info'

    ID = db.Column(db.Integer, primary_key=True)
    User_id = db.Column(db.Integer, db.ForeignKey('api_fgx_Users.ID'))
    View_state = db.Column(db.Integer)
    File_name = db.Column(db.String(100))
    Field_name = db.Column(db.String(100))
    Order = db.Column(db.Integer)
    rlFields = db.relationship('UserModel', backref='user')

    def __init__(self, User_id, View_state, File_name, Field_name, Order):
        self.User_id = User_id
        self.View_state = View_state
        self.File_name = File_name
        self.Field_name = Field_name
        self.Order = Order

    def json(self):
        return {
            'ID': self.ID,
            'User_id': self.User_id,
            'View_state': self.View_state,
            'File_name': self.File_name,
            'Field_name': self.Field_name,
            'Order': self.Order
        }

    @classmethod
    def get_user_fields(cls, userid, project='MLF'):
        return cls.query.filter_by(User_id=userid, View_state=1, File_name=project).all()

    @classmethod
    def get_all_user_fields(cls, userid, project):
        if project is None:
            return cls.query.filter_by(User_id=userid).all()
        else:
            return cls.query.filter_by(User_id=userid, File_name=project).all()

    @classmethod
    def fieldExist_in_user(cls, userID, fieldname, fileName):
        print('IF FIELD EXISTS:', userID, fieldname, fileName)
        record = cls.query.filter_by(
            User_id=userID, Field_name=fieldname, File_name=fileName).count()
        if record >= 1:
            return True
        return False

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def deletefield(cls, field_id):
        cls.query.filter_by(ID=field_id).delete()
        db.session.commit()

    @classmethod
    def deleteAllField(cls, userID):
        print("USER ID:", userID)

        cls.query.filter_by(User_id=userID).delete()
        db.session.commit()


class UserTimePeriod(db.Model):
    __tablename__ = 'Api_Fgx_User_TimePeriod'

    ID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('api_fgx_Users.ID'))
    CreatedDate = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    ExpiratioinDate = db.Column(db.DateTime, nullable=False,
                                default=datetime.utcnow)
    rlFields = db.relationship('UserModel', backref='timeUser')

    def __init__(self, User_id, CreatedDate, ExpiratioinDate):
        self.UserID = User_id
        self.CreatedDate = CreatedDate
        self.ExpiratioinDate = ExpiratioinDate

    def json(self):
        return {
            'UserID': self.UserID,
            'CreatedDate': self.CreatedDate,
            'ExpiratioinDate': self.ExpiratioinDate,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        record = self.query.filter_by(UserID=self.UserID).first()
        db.session.delete(record)
        db.session.commit()
        self.save()
        print("UPDATE SESION COMMITED")

    @classmethod
    def getTimePeriod(cls, userId):
        record = cls.query.filter_by(UserID=userId).first()
        if record:
            # return (record.ExpiratioinDate - record.CreatedDate).days
            return (record.ExpiratioinDate - datetime.now()).days

    @classmethod
    def getTimePeriodFull(cls, userId):
        record = cls.query.filter_by(UserID=userId).first()
        if record:
            return {"ExpirationDate": record.ExpiratioinDate.strftime("%m/%d/%Y"),
                    "CreatedDate": record.CreatedDate.strftime("%m/%d/%Y"),
                    "Dayes": cls.getTimePeriod(userId)
                    }
        return None

    @classmethod
    def timePeriodExists(cls, userID):
        record = cls.query.filter_by(UserID=userID).count()
        if record >= 1:
            return True
        return False


class UserCoins(db.Model):
    __tablename__ = 'api_fgx_user_coins'

    ID = db.Column(db.Integer, primary_key=True)
    User_id = db.Column(db.Integer, db.ForeignKey('api_fgx_Users.ID'))
    C_purchased = db.Column(db.Float)
    C_available = db.Column(db.Float)
    Cost_per_c = db.Column(db.Float)
    Status = db.Column(db.Integer)
    rlFields = db.relationship('UserModel', backref='UserModel')

    def __init__(self, User_id, C_purchased, C_available, Cost_per_c, Status):
        self.User_id = User_id
        self.C_purchased = C_purchased
        self.C_available = C_available
        self.Cost_per_c = Cost_per_c
        self.Status = Status

    def json(self):
        return {
            'User_id': self.User_id,
            'C_purchased': self.C_purchased,
            'C_available': self.C_available,
            'Cost_per_c': self.Cost_per_c,
            'Status': self.Status
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, userid, coins):
        record = self.query.filter_by(User_id=userid).first()
        record.C_purchased = coins
        record.C_available = record.C_available + coins
        record.Cost_per_c = 0.10 * coins
        print("coins: {}".format(coins))
        db.session.commit()

    @classmethod
    def fieldExistInUserCoins(cls, userID):
        record = cls.query.filter_by(User_id=userID).count()
        if record >= 1:
            return True
        return False

    @classmethod
    def getUserCoins(cls, userID):
        record = cls.query.filter_by(User_id=userID).first()
        return record


class UserPrm(db.Model):
    __tablename__ = 'Api_Fgx_parameters'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('api_fgx_Users.ID'))
    prm_name = db.Column(db.String(150))
    prm_value = db.Column(db.String(1000))
    prm_description = db.Column(db.String(500))
    myRlFields = db.relationship('UserModel', backref='UserForPrm')

    def __init__(self, userId, prmName, prmValue, prmDescription):
        self.uid = userId
        self.prm_name = prmName
        self.prm_value = prmValue
        self.prm_description = prmDescription

    def json(self):
        return {
            'User_id': self.userId,
            'prm_name': self.prmName,
            'prm_value': self.prmValue,
            'prm_description': self.prmDescription
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, userId, prmName, prmValue):
        record = self.query.filter_by(uid=userId, prm_name=prmName).first()
        record.prm_value = json.dumps(prmValue)
        print("parameter: {}".format(prmValue))
        db.session.commit()
        print("SESION COMMITED")

    @classmethod
    def prmExist(cls, userID, prmName):
        record = cls.query.filter_by(uid=userID, prm_name=prmName).count()
        if record >= 1:
            return True
        return False

    @classmethod
    def getUserParameter(cls, userId, prmName):
        record = cls.query.filter_by(uid=userId, prm_name=prmName).first()
        return record

    @classmethod
    def isTypeInPrm(cls, userId, prmName, licType):
        record = cls.query.filter_by(uid=userId, prm_name=prmName).first()
        if record:
            listOfTypes = eval(record.prm_value)
            listOfTypesSearched = licType.split(",")

            for item in listOfTypesSearched:
                if item not in listOfTypes:
                    return False
            return True
        else:
            return True

    @classmethod
    def isProfessionInPrm(cls, userId, prmName, prof):
        record = cls.query.filter_by(uid=userId, prm_name=prmName).first()
        if record:
            listOfAllowedProfessions = eval(record.prm_value)

            if "professions" in listOfAllowedProfessions:
                if listOfAllowedProfessions["professions"] != "":
                    if prof is not None:
                        if prof.lower() not in listOfAllowedProfessions["professions"].lower():
                            return False
        return True

    # @classmethod
    # def getAllowedProfessions(cls, userId, prmName):
    #     record = cls.query.filter_by(uid=userId, prm_name=prmName).first()

    #     if record:
    #         listOfAllowedProfessions = eval(record.prm_value)
    #         if "professions" in listOfAllowedProfessions:
    #             if listOfAllowedProfessions["professions"] != "":

    #                 return listOfAllowedProfessions["professions"]
    #         return None

    @classmethod
    def getAllowedProfessions(cls, userId, prmName):
        record = cls.query.filter_by(uid=userId, prm_name=prmName).first()

        if record:
            listOfAllowedProfessions = eval(record.prm_value)
            if prmName.lower() in listOfAllowedProfessions:
                if listOfAllowedProfessions[prmName.lower()] != "":

                    return listOfAllowedProfessions[prmName.lower()]
            return None
