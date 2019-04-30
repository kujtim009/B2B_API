from db import db
from flask_jwt_extended import get_jwt_claims, get_jwt_identity


class LayoutModel(db.Model):
    __tablename__ = 'ExportMappings'

    ExportID = db.Column(db.Integer)
    FieldID = db.Column(db.Integer, primary_key=True)
    LayoutField = db.Column(db.String(80))
    ExportField = db.Column(db.String(80))
    

    def __init__(self, ExportID, FieldID, LayoutField, ExportField):
        self.ExportID = ExportID

    def json(self):
        return {
            'ExportID': self.ExportID,
            'FieldID': self.FieldID,
            'LayoutField': self.LayoutField,
            'ExportField': self.ExportField
            }

    @classmethod
    def find_by_exportID(cls, exp_id):
        return cls.query.filter_by(ExportID=exp_id).all()
