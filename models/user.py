from db import db
from flask_jwt_extended import get_jwt_claims, get_jwt_identity


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
    def get_user_fields(cls, userid):
        return cls.query.filter_by(User_id=userid, View_state=1).all()

    @classmethod
    def get_all_user_fields(cls, userid):
        return cls.query.filter_by(User_id=userid).all()    

    @classmethod
    def fieldExist_in_user(cls, userID, fieldname):
        record = cls.query.filter_by(User_id = userID, Field_name = fieldname).count()
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
            'User_id':self.User_id,
            'C_purchased':self.C_purchased,
            'C_available':self.C_available,
            'Cost_per_c':self.Cost_per_c,
            'Status':self.Status
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self,userid, coins):
        record = self.query.filter_by(User_id=userid).first()
        record.C_purchased = coins
        record.C_available = record.C_available + coins
        record.Cost_per_c = 0.10 * coins
        print("coins: {}".format(coins))
        db.session.commit()

    @classmethod
    def fieldExistInUserCoins(cls, userID):
        record = cls.query.filter_by(User_id = userID).count()
        if record >= 1:
            return True
        return False
    
    @classmethod
    def getUserCoins(cls, userID):
        record = cls.query.filter_by(User_id = userID).first()
        return record