from db import db
from flask_jwt_extended import get_jwt_claims, get_jwt_identity
import json
from datetime import datetime


class Loging(db.Model):
    __tablename__ = 'Api_Fgx_log'

    id = db.Column(db.Integer, primary_key=True)
    projectName = db.Column(db.String(40))
    userId = db.Column(db.Integer)
    userName = db.Column(db.String(40))
    actionType = db.Column(db.String(20))
    queryPrm = db.Column(db.String(500))
    recordsPulled = db.Column(db.Integer)
    ipAddress = db.Column(db.String(20))
    timeStamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, projectName, userId, userName, actionType, queryPrm, recordsPulled, ipAddress, timeStamp=None):
        self.projectName = projectName
        self.userId = userId
        self.userName = userName
        self.actionType = actionType
        self.queryPrm = queryPrm
        self.recordsPulled = recordsPulled
        self.ipAddress = ipAddress
        self.timeStamp = timeStamp

    def json(self):
        return {
            'projectName': self.userId,
            'userId': self.prmName,
            'userName': self.prmValue,
            'actionType': self.prmDescription,
            'queryPrm': self.prmDescription,
            'recordsPulled': self.prmDescription,
            'ipAddress': self.prmDescription,
            'timeStamp': self.prmDescription,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
