from db import db, ma
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from models.user import Userinfo
import pandas as pd
import json
import os


class ItemModel(db.Model):
    __tablename__ = 'CBD'
    Record_id = db.Column(db.Integer, primary_key=True)


class CbdRecordSchema(ma.ModelSchema):
    record_output = 100

    class Meta():
        model = ItemModel
        # fields = fieldlist

    @staticmethod
    def get_user_fields(project='MLF'):
        userID = get_jwt_identity()
        record = Userinfo.get_user_fields(userID, project=project)
        if record:
            jsonRec = {'User_fields': [field.json() for field in record]}
        else:
            jsonRec = {'User_fields': []}

        # jsonRec = {'User_fields': '[]'}
        mylist = [rec["Field_name"] for rec in jsonRec["User_fields"]]
        return mylist

    @classmethod
    def createDnldFile(cls, data, userID):
        df = pd.DataFrame(data[0])

        df.to_csv(os.path.dirname(os.path.dirname(__file__)) +
                  "/exports/CBD/{}.csv".format(userID))

    @classmethod
    def mainDownload(cls, *fields):
        # print("SEARCH FIELDS: ", fields)
        parameters = [x for x in fields]
        # parameters.insert(0, cls.record_output)
        if license is None and state is None and prof is None:
            return jsonify({'Records': 'Search input is missing!'})
        else:
            print("EXECUTED!!!!!!!!")

            result = db.engine.execute(
                'Fgx_api_cbd_main_downloader ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?', parameters)

        record_schema = CbdRecordSchema(
            many=True, only=cls.get_user_fields(project='CBD'))
        output = record_schema.dump(result)

        userID = get_jwt_identity()
        print("MAIN DOWNLOAD:", result)
        cls.createDnldFile(output, userID)
        return userID

    @classmethod
    def main_filter(cls, *fields):
        # print("SEARCH FIELDS: ", fields)
        parameters = [x for x in fields]
        parameters.insert(0, cls.record_output)

        result = db.engine.execute(
            'Fgx_api_cbd_main_filter ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?', parameters)

        fields = cls.get_user_fields()
        record_schema = CbdRecordSchema(
            many=True, only=cls.get_user_fields(project='CBD'))

        output = record_schema.dump(result)
        return jsonify({'Records': output})

    @classmethod
    def getCounts_main_filter(cls, *fields):
        result = db.engine.execute(
            'Fgx_api_cbd_main_counter ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?', fields)
        for rowe in result:
            return rowe[0]
        return result

    @classmethod
    def cbdGetCityByState(cls, state):
        result = db.engine.execute(
            'Fgx_api_cbd_get_cities_from_state ?', [state])
        return result

    @classmethod
    def getProfesionBucketsByLictypeState(cls, state=None, licenseType='all', professionsBucket=None):
        # print("GET PROFESSION: ", [None if licenseType ==
        #                            'all' else licenseType, state, professionsBucket])
        print("ProfessionBuckets", professionsBucket)
        result = db.engine.execute('Fgx_api_getProfesionBucketsByState ?, ?, ?', [
                                   None if licenseType == 'all' else licenseType, state, professionsBucket])
        return result

    @classmethod
    def getProfesionSubBucketsByBucketState(cls, state=None, professionsBucket=None):
        # print("GET PROFESSION: ", [None if licenseType ==
        #                            'all' else licenseType, state, professionsBucket])
        print("ProfessionBuckets", professionsBucket)
        result = db.engine.execute('Fgx_api_getProfesionSubBucketsByState ?, ?', [
            state, professionsBucket])
        return result
