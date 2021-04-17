from flask import request, send_file
from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required,
    fresh_jwt_required,
    get_jwt_identity)
# from models.records import RecordSchema

from models.prmRecords import PrmRecordSchema
from models.user import Userinfo, UserPrm, UserModel
from models.layout import LayoutModel
import json
import os
from models.loging import Loging


# class getCurUserFields(Resource):
#     @jwt_required
#     def get(self):
#         prmUserID = request.args.get('uid', None)
#         if prmUserID is None:
#             userID = get_jwt_identity()
#             record = Userinfo.get_all_user_fields(userID)
#         else:
#             record = Userinfo.get_all_user_fields(prmUserID)

#         if record:
#             # return {'User_fields': list(map(lambda x: x.json(), record))}
#             return {'User_fields': [field.json() for field in record]}
#         return {'User_fields': []}, 200


# class getProfessions(Resource):
#     @jwt_required
#     def get(self):
#         state = request.args.get('state', None)
#         licenseType = request.args.get('license_type', 'all')

#         userId = get_jwt_identity()
#         try:
#             userProfessions = UserPrm.getUserParameter(
#                 userId, 'Professions').prm_value
#             userProfessions = eval(userProfessions)

#             userProfessionSearch = userProfessions["professions"]
#             # print("PROFESSIONS ALLOWED: ", userProfessionSearch)
#             if userProfessionSearch == "":
#                 userProfessionSearch = None
#         except:
#             userProfessionSearch = None

#         if state is None and licenseType == 'all':
#             # print("LICENSE: ", licenseType)
#             record = RecordSchema.getProfessions()
#         else:
#             # print("LICENSE: ", licenseType)
#             record = RecordSchema.getProfesionByLictypeState(
#                 licenseType=licenseType, state=state, professions=userProfessionSearch)

#         if record:
#             test = {key: value for (key, value) in record}

#             return test
#         return {'message': 'record not found'}, 404


# class getProfessionsBuckets(Resource):
#     @jwt_required
#     def get(self):
#         state = request.args.get('state', None)
#         licenseType = request.args.get('license_type', 'all')

#         userId = get_jwt_identity()
#         try:
#             userProfessionsBuckets = UserPrm.getUserParameter(
#                 userId, 'ProfessionBuckets').prm_value
#             userProfessionsBuckets = eval(userProfessionsBuckets)

#             userProfessionBucketSearch = userProfessionsBuckets["ProfessionBuckets"]
#             # print("PROFESSIONS ALLOWED: ", userProfessionSearch)
#             if userProfessionBucketSearch == "":
#                 userProfessionBucketSearch = None
#         except:
#             userProfessionBucketSearch = None

#         if state is None and licenseType == 'all':
#             # print("LICENSE: ", licenseType)
#             record = RecordSchema.getProfessions()
#         else:
#             # print("LICENSE: ", licenseType)
#             record = RecordSchema.getProfesionBucketsByLictypeState(
#                 licenseType=licenseType, state=state, professionsBucket=userProfessionBucketSearch)

#         if record:
#             test = {key: value for (key, value) in record}

#             return test
#         return {'message': 'record not found'}, 404


class PrmgetZipByState(Resource):
    @jwt_required
    def get(self):
        state = request.args.get('state', None)
        print(state)
        record = PrmRecordSchema.prmGetZipByState(state)
        # print("Records", list(record))
        result = list(record)
        # print({"city": [item[0] for item in result]})
        if record:
            return {"zip": [item[0] for item in result]}
        return {'message': 'record not found'}, 404


class PrmgetZip(Resource):
    @jwt_required
    def get(self):
        record = PrmRecordSchema.prmGetZip()
        result = list(record)
        if record:
            return {"zip": [item[0] for item in result]}
        return {'message': 'record not found'}, 404


class GetAllFieldNames(Resource):
    @jwt_required
    def get(self):
        record = LayoutModel.find_by_exportID(2071)
        if record:
            return {'Project_fields': [field.json() for field in record]}
        return {'message': 'record not found'}, 404


class Prm_Records_by_main_filter(Resource):
    @jwt_required
    def get(self):

        state = request.args.get('state', None)
        state = None if state == "all" else state

        zip = request.args.get('zip', None)
        zip = None if zip == "all" else zip

        status = request.args.get('status', None)
        status = None if status == "all" else status

        priceFrom = request.args.get('price_from', None)
        priceTo = request.args.get('price_to', None)

        pullRandom = request.args.get('random', None)
        record = None

# check if License type requested is allowed for current user

        # if state is not None:
        record = PrmRecordSchema.main_filter(
            state, zip, status, priceFrom, priceTo, pullRandom)

        if record:
            user = UserModel.find_by_id(get_jwt_identity())
            log = Loging(
                "PRM", get_jwt_identity(), user.username, "Search Query", json.dumps(request.args), None, str(request.remote_addr))
            log.save()
            return record
        return {'message': 'record not found'}


class PrmDnldRecords(Resource):
    @jwt_required
    def get(self):
        state = request.args.get('state', None)
        zip = request.args.get('zip', None)
        status = request.args.get('status', None)
        priceFrom = request.args.get('price_from', None)
        priceTo = request.args.get('price_to', None)
        pullRandom = request.args.get('random', None)
        record = None

        # if state is not None:
        try:
            maxDnldNum = int(UserPrm.getUserParameter(
                get_jwt_identity(), 'maxDnld').prm_value[1:-1])
        except:
            maxDnldNum = 10000

        print("USER PRM MAX DNLD:", maxDnldNum)

        record = PrmRecordSchema.mainDownload(maxDnldNum,
                                              state, zip, status, priceFrom, priceTo, pullRandom)

        if record:
            path = os.path.dirname(os.path.dirname(
                __file__)) + "/exports/PRM/{}.csv".format(record)
            user = UserModel.find_by_id(get_jwt_identity())
            log = Loging(
                "PRM", get_jwt_identity(), user.username, "Download Query", json.dumps(request.args), None, str(request.remote_addr))
            log.save()
            return send_file(path, as_attachment=True)
        return {'message': 'record not found'}, 404


class Prm_GetRecCounts_Main_filter(Resource):
    @jwt_required
    def get(self):
        state = request.args.get('state', None)
        zip = request.args.get('zip', None)
        status = request.args.get('status', None)
        priceFrom = request.args.get('price_from', None)
        priceTo = request.args.get('price_to', None)

        record = None

        record = PrmRecordSchema.getCounts_main_filter(
            state, zip, status, priceFrom, priceTo)
        if record:
            return {'count': record}
        return {'count': 0}
