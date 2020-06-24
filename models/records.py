from db import db, ma
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from models.user import Userinfo
import pandas as pd
import json
import os


class ItemModel(db.Model):
    __tablename__ = 'Master_Layout'
    Record_id = db.Column(db.Integer, primary_key=True)


class RecordSchema(ma.ModelSchema):
    record_output = 100

    class Meta():
        model = ItemModel
        # fields = fieldlist

    @staticmethod
    def get_user_fields():
        userID = get_jwt_identity()
        record = Userinfo.get_user_fields(userID)
        if record:
            jsonRec = {'User_fields': [field.json() for field in record]}
        else:
            jsonRec = {'User_fields': []}

        # jsonRec = {'User_fields': '[]'}
        mylist = [rec["Field_name"] for rec in jsonRec["User_fields"]]
        return mylist

    @classmethod
    def find_by_licence(cls, license):
        result = ItemModel.query.filter_by(
            License_Number=license).limit(cls.record_output).all()
        record_schema = RecordSchema(many=True, only=cls.get_user_fields())
        output = record_schema.dump(result)
        return jsonify({'Records': output})

    @classmethod
    def find_by_licence_and_state(cls, license, state, prof):
        if license is None and state is None and prof is None:
            return jsonify({'Records': 'Search input is missing!'})
        else:
            result = db.engine.execute('FilterResults_LSP ?, ?, ?, ?', [
                                       cls.record_output, license, state, prof])

        fields = cls.get_user_fields()
        record_schema = RecordSchema(many=True, only=cls.get_user_fields())
        output = record_schema.dump(result)
        return jsonify({'Records': output})

    @classmethod
    def createDnldFile(cls, data, userID):
        df = pd.DataFrame(data[0])
        print("SCRIPT PATH2222: ", os.path.abspath(os.curdir))
        print("SCRIPT PATH33333: ", os.path.join(
            os.path.dirname(__file__), '..'))

        df.to_csv(os.path.join(
            os.path.dirname(__file__), '../') +
            "exports/{}.csv".format(userID))

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
                'Fgx_api_main_download ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?', parameters)

        fields = cls.get_user_fields()
        record_schema = RecordSchema(many=True, only=cls.get_user_fields())
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
        if license is None and state is None and prof is None:
            return jsonify({'Records': 'Search input is missing!'})
        else:
            print("EXECUTED", parameters)

            result = db.engine.execute(
                'Fgx_api_main_filter ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?', parameters)

        fields = cls.get_user_fields()
        record_schema = RecordSchema(many=True, only=cls.get_user_fields())
        output = record_schema.dump(result)
        return jsonify({'Records': output})

    @classmethod
    def getCounts_main_filter(cls, *fields):
        result = db.engine.execute(
            'Fgx_api_main_counter ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?', fields)
        for rowe in result:
            return rowe[0]
        return result

    @classmethod
    def find_by_state(cls, state):
        result = ItemModel.query.filter_by(
            Business_state=state).limit(cls.record_output).all()
        record_schema = RecordSchema(many=True, only=cls.get_user_fields())
        output = record_schema.dump(result)
        return jsonify({'Records': output})

    @classmethod
    def get_all_records(cls):
        result = ItemModel.query.limit(cls.record_output).all()
        record_schema = RecordSchema(many=True, only=cls.get_user_fields())
        output = record_schema.dump(result)
        return jsonify({'Records': output})

    @classmethod
    def find_by_license_owner(cls, licOwner, srch_type):
        result = db.engine.execute('FilterResults_LON ?, ?, ?', [
                                   cls.record_output, licOwner, srch_type])
        record_schema = RecordSchema(many=True, only=cls.get_user_fields())
        output = record_schema.dump(result)
        return jsonify({'Records': output})

    @classmethod
    def find_by_compnay(cls, company, srch_type):
        result = db.engine.execute('FilterResults_C ?, ?, ?', [
                                   cls.record_output, company, srch_type])

        record_schema = RecordSchema(many=True, only=cls.get_user_fields())
        output = record_schema.dump(result)
        return jsonify({'Records': output})

    @classmethod
    def getProfessions(cls):
        # sqlquery = "select DGX_Profession, count(DGX_Profession) from Master_layout with(nolock) group by DGX_Profession order by DGX_Profession asc"
        sqlquery = "select *From api_fgx_profession where count > 1 and DGX_Profession not like '%X'"
        result = db.engine.execute(sqlquery)
        return result

    @classmethod
    def getProfesionByLictypeState(cls, state=None, licenseType='all', professions=None):
        # print("GET PROFESSION: ", [None if licenseType ==
        #                            'all' else licenseType, state, professions])
        result = db.engine.execute('Fgx_api_getProfesionByState ?, ?, ?', [
                                   None if licenseType == 'all' else licenseType, state, professions])
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

    @classmethod
    def getCounts_lsp(cls, license, state, prof):
        result = db.engine.execute('Api_record_counter_LSP ?, ?, ?', [
                                   license, state, prof])
        for rowe in result:
            return rowe[0]
        return result

    @classmethod
    def getCounts_LON(cls, licOwner, srch_type):
        result = db.engine.execute(
            'Api_record_counter_LON ?, ?', [licOwner, srch_type])
        for rowe in result:
            return rowe[0]
        return result

    @classmethod
    def getCounts_CPN(cls, company, srch_type):
        result = db.engine.execute(
            'Api_record_counter_CPN ?, ?', [company, srch_type])
        for rowe in result:
            return rowe[0]
        return result
