from flask import request, send_file
from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required,
    fresh_jwt_required,
    get_jwt_identity)
# from models.records import RecordSchema

from models.cbdRecords import CbdRecordSchema
from models.user import Userinfo, UserPrm
from models.layout import LayoutModel
import json
import os


class getCurUserFields(Resource):
    @jwt_required
    def get(self):
        prmUserID = request.args.get('uid', None)
        if prmUserID is None:
            userID = get_jwt_identity()
            record = Userinfo.get_all_user_fields(userID)
        else:
            record = Userinfo.get_all_user_fields(prmUserID)

        if record:
            # return {'User_fields': list(map(lambda x: x.json(), record))}
            return {'User_fields': [field.json() for field in record]}
        return {'User_fields': []}, 200


class getProfessions(Resource):
    @jwt_required
    def get(self):
        state = request.args.get('state', None)
        licenseType = request.args.get('license_type', 'all')

        userId = get_jwt_identity()
        try:
            userProfessions = UserPrm.getUserParameter(
                userId, 'Professions').prm_value
            userProfessions = eval(userProfessions)

            userProfessionSearch = userProfessions["professions"]
            # print("PROFESSIONS ALLOWED: ", userProfessionSearch)
            if userProfessionSearch == "":
                userProfessionSearch = None
        except:
            userProfessionSearch = None

        if state is None and licenseType == 'all':
            # print("LICENSE: ", licenseType)
            record = RecordSchema.getProfessions()
        else:
            # print("LICENSE: ", licenseType)
            record = RecordSchema.getProfesionByLictypeState(
                licenseType=licenseType, state=state, professions=userProfessionSearch)

        if record:
            test = {key: value for (key, value) in record}

            return test
        return {'message': 'record not found'}, 404


class getProfessionsBuckets(Resource):
    @jwt_required
    def get(self):
        state = request.args.get('state', None)
        licenseType = request.args.get('license_type', 'all')

        userId = get_jwt_identity()
        try:
            userProfessionsBuckets = UserPrm.getUserParameter(
                userId, 'ProfessionBuckets').prm_value
            userProfessionsBuckets = eval(userProfessionsBuckets)

            userProfessionBucketSearch = userProfessionsBuckets["ProfessionBuckets"]
            # print("PROFESSIONS ALLOWED: ", userProfessionSearch)
            if userProfessionBucketSearch == "":
                userProfessionBucketSearch = None
        except:
            userProfessionBucketSearch = None

        if state is None and licenseType == 'all':
            # print("LICENSE: ", licenseType)
            record = RecordSchema.getProfessions()
        else:
            # print("LICENSE: ", licenseType)
            record = RecordSchema.getProfesionBucketsByLictypeState(
                licenseType=licenseType, state=state, professionsBucket=userProfessionBucketSearch)

        if record:
            test = {key: value for (key, value) in record}

            return test
        return {'message': 'record not found'}, 404


class CbdgetCitiesByState(Resource):
    @jwt_required
    def get(self):
        state = request.args.get('state', None)
        print(state)
        record = CbdRecordSchema.cbdGetCityByState(state)
        # print("Records", list(record))
        result = list(record)
        # print({"city": [item[0] for item in result]})
        if record:
            return {"cities": [item[0] for item in result]}
        return {'message': 'record not found'}, 404


class getProfessionsSubBuckets(Resource):
    @jwt_required
    def get(self):
        state = request.args.get('state', None)
        professionBucket = request.args.get(
            'professionBucket', NotImplementedError)

        userId = get_jwt_identity()
        record = RecordSchema.getProfesionSubBucketsByBucketState(
            state=state, professionsBucket=professionBucket)

        if record:
            test = {key: value for (key, value) in record}

            return test
        return {'message': 'record not found'}, 404


class GetAllFieldNames(Resource):
    @jwt_required
    def get(self):
        record = LayoutModel.find_by_exportID(2071)
        if record:
            return {'Project_fields': [field.json() for field in record]}
        return {'message': 'record not found'}, 404


class dnldRecords(Resource):
    @jwt_required
    def get(self):
        print("Start")
        licenseType = request.args.get('license_type', None)
        state = request.args.get('state', None)
        state = None if state == 'all' else state
        prof = request.args.get('profession', None)

        profBucket = request.args.get('profession_bucket', None)
        profSubBucket = request.args.get('profession_sub_bucket', None)
        profSubBucket2 = request.args.get('profession_sub_bucket2', None)

        county = request.args.get('county', None)
        city = request.args.get('city', None)
        zipcode = request.args.get('zipcode', None)

        license = request.args.get('license', None)
        phone = request.args.get('phone', None)
        email = request.args.get('email', None)
        employees = request.args.get('employees', None)
        company_name = request.args.get('company_name', None)
        srch_type_comp = request.args.get('srch_type_comp', None)
        lic_owner = request.args.get('lic_owner', None)
        srch_type_licO = request.args.get('srch_type_licO', None)

        allowedProfessions = None
        allowedProfessionsBuckets = None
        record = None

# check if License type requested is allowed for current user
        if licenseType is not None and licenseType != "all":
            if UserPrm.isTypeInPrm(get_jwt_identity(), 'Lic_types', licenseType):

                if prof is not None:
                    if UserPrm.isProfessionInPrm(get_jwt_identity(), 'Professions', prof):
                        allowedProfessions = UserPrm.getAllowedProfessions(
                            get_jwt_identity(), 'Professions')
                        record = RecordSchema.mainDownload(licenseType, state, prof, allowedProfessions, profBucket, allowedProfessionsBuckets, profSubBucket, profSubBucket2, county, city, zipcode, license,
                                                           phone, email, employees, company_name, srch_type_comp, lic_owner, srch_type_licO)
                        print("FIRST: ", licenseType, state, prof, allowedProfessions, profBucket, allowedProfessionsBuckets, profSubBucket, profSubBucket2, county, city, zipcode, license,
                              phone, email, employees, company_name, srch_type_comp, lic_owner, srch_type_licO)
                elif profBucket is not None:
                    if UserPrm.isProfessionInPrm(get_jwt_identity(), 'ProfessionBuckets', profBucket):
                        allowedProfessionsBuckets = UserPrm.getAllowedProfessions(
                            get_jwt_identity(), 'ProfessionBuckets')
                        record = RecordSchema.mainDownload(licenseType, state, prof, allowedProfessions, profBucket, allowedProfessionsBuckets, profSubBucket, profSubBucket2, county, city, zipcode, license,
                                                           phone, email, employees, company_name, srch_type_comp, lic_owner, srch_type_licO)
                        print("SECOND: ", licenseType, state, prof, allowedProfessions, profBucket, allowedProfessionsBuckets, profSubBucket, profSubBucket2, county, city, zipcode, license,
                              phone, email, employees, company_name, srch_type_comp, lic_owner, srch_type_licO)

            else:
                return {'message': 'You are not authorized to access this data'}, 401
        else:
            return {'message': 'You are not authorized to access this dataaa'}, 404
        print("SCRIPT PATH: ", os.path.join(
            os.path.dirname(__file__), '../'))
        if record:
            print("SCRIPT PATH: ", os.path.join(
                os.path.dirname(__file__), '../'))
            path = os.path.dirname(os.path.dirname(
                __file__)) + "/exports/{}.csv".format(record)
            return send_file(path, as_attachment=True)
        return {'message': 'record not found'}, 404


class Cbd_Records_by_main_filter(Resource):
    @jwt_required
    def get(self):

        state = request.args.get('state', None)
        state = None if state == 'all' else state
        pBuyer = request.args.get('p_buyer', None)
        pMBuyer = request.args.get('p_multi_buyer', None)

        city = request.args.get('city', None)
        zipcode = request.args.get('zipcode', None)

        phone = request.args.get('phone', None)
        email = request.args.get('email', None)

        dobFrom = request.args.get('dob_from', None)
        dobTo = request.args.get('dob_to', None)

        allowedProfessions = None
        allowedProfessionsBuckets = None
        record = None

# check if License type requested is allowed for current user

        if state is not None:
            record = CbdRecordSchema.main_filter(
                state, pBuyer, pMBuyer, city, zipcode, phone, email, dobFrom, dobTo)

        if record:
            return record
        return {'message': 'record not found'}


class CbdDnldRecords(Resource):
    @jwt_required
    def get(self):
        state = request.args.get('state', None)
        state = None if state == 'all' else state
        pBuyer = request.args.get('p_buyer', None)
        pMBuyer = request.args.get('p_multi_buyer', None)

        city = request.args.get('city', None)
        zipcode = request.args.get('zipcode', None)

        phone = request.args.get('phone', None)
        email = request.args.get('email', None)

        dobFrom = request.args.get('dob_from', None)
        dobTo = request.args.get('dob_to', None)

        record = None

        if state is not None:
            record = CbdRecordSchema.mainDownload(
                state, pBuyer, pMBuyer, city, zipcode, phone, email, dobFrom, dobTo)

        if record:
            path = os.path.dirname(os.path.dirname(
                __file__)) + "/exports/CBD/{}.csv".format(record)
            return send_file(path, as_attachment=True)
        return {'message': 'record not found'}, 404


class Cbd_GetRecCounts_Main_filter(Resource):
    @jwt_required
    def get(self):
        state = request.args.get('state', None)
        state = None if state == 'all' else state
        pBuyer = request.args.get('p_buyer', None)
        pMBuyer = request.args.get('p_multi_buyer', None)

        city = request.args.get('city', None)
        zipcode = request.args.get('zipcode', None)

        phone = request.args.get('phone', None)
        email = request.args.get('email', None)

        dobFrom = request.args.get('dob_from', None)
        dobTo = request.args.get('dob_to', None)

        record = None

        if state is not None:
            record = CbdRecordSchema.getCounts_main_filter(
                state, pBuyer, pMBuyer, city, zipcode, phone, email, dobFrom, dobTo)
        if record:
            return {'count': record}
        return {'count': 0}
