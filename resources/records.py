from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required,
    fresh_jwt_required,
    get_jwt_identity)
from models.records import RecordSchema
from models.user import Userinfo
from models.layout import LayoutModel

class Record_by_license(Resource):
    @jwt_required
    def get(self, license):
        record = RecordSchema.find_by_licence(license)
        if record:
            return record
        return {'message': 'record not found'}, 404


class Record_by_license_and_state_prof(Resource):
    @jwt_required
    def get(self):
        license = request.args.get('license', None)
        state = request.args.get('state', None)
        prof = request.args.get('profession', None)

        record = RecordSchema.find_by_licence_and_state(license, state, prof)
        if record:
            return record
        return {'message': 'record not found'}, 404


class RecordList(Resource):
    @jwt_required
    def get(self):
        record = RecordSchema.get_all_records()
        if record:
            return record
        return {'message': 'records not found'}, 404


class Record_by_state(Resource):
    @jwt_required
    def get(self, state):
        record = RecordSchema.find_by_state(state)
        if record:
            return record
        return {'message': 'record not found'}, 404


class Record_by_Individual_name(Resource):
    @jwt_required
    def get(self):
        first_name = request.args.get('fName', None)
        middle_name = request.args.get('mName', None)
        last_name = request.args.get('lName', None)

        record = RecordSchema.find_by_individual(first_name, middle_name, last_name)
        if record:
            return record
        return {'message': 'record not found'}, 404


class Record_by_company_name(Resource):
    @jwt_required
    def get(self, company):
        srch_type = request.args.get('src_tp', None)
        record = RecordSchema.find_by_compnay(company, srch_type)
        if record:
            return record
        return {'message': 'record not found'}, 404


class Record_by_license_owner(Resource):
    @jwt_required
    def get(self, licOwner):
        srch_type = request.args.get('src_tp', None)
        record = RecordSchema.find_by_license_owner(licOwner, srch_type)
        if record:
            return record
        return {'message': 'record not found'}, 404        


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
        return {'message': 'No columns available!'}, 404        


class getProfessions(Resource):
    @jwt_required
    def get(self):
        state = request.args.get('state', None)
        if state is None:
            record = RecordSchema.getProfessions()
        else:
            record = RecordSchema.getProfesionByState(state)
        if record:
            test =  {key: value for (key, value) in record}
            return test
        return {'message': 'record not found'}, 404  


class GetAllFieldNames(Resource):
    @jwt_required
    def get(self):
        record = LayoutModel.find_by_exportID(2068)
        if record:
            return {'Project_fields': [field.json() for field in record]}
        return {'message': 'record not found'}, 404    


class GetRecCounts_LSP(Resource):
    @jwt_required
    def get(self):

        license = request.args.get('license', None)
        state = request.args.get('state', None)
        prof = request.args.get('profession', None)

        record = RecordSchema.getCounts_lsp(license, state, prof)
        if record:
            return {'count':record}
        return {'message': 'record not found'}, 404   


class GetRecCounts_LON(Resource):
    @jwt_required
    def get(self, licOwner):
        srch_type = request.args.get('src_tp', None)
        record = RecordSchema.getCounts_LON(licOwner, srch_type)
        if record:
            return {'count':record}
        return {'message': 'record not found'}, 404               


class GetRecCounts_CPN(Resource):
    @jwt_required
    def get(self, company):
        srch_type = request.args.get('src_tp', None)
        record = RecordSchema.getCounts_CPN(company, srch_type)
        if record:
            return {'count':record}
        return {'message': 'record not found'}, 404   


class Records_by_main_filter(Resource):
    @jwt_required
    def get(self):
        
        state = request.args.get('state', None)
        prof = request.args.get('profession', None)
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
        


        record = RecordSchema.main_filter(state, prof, county, city, zipcode, license, 
                                            phone, email, employees, company_name, srch_type_comp, lic_owner, srch_type_licO)
        if record:
            return record
        return {'message': 'record not found'}, 404


class GetRecCounts_Main_filter(Resource):
    @jwt_required
    def get(self):

        state = request.args.get('state', None)
        prof = request.args.get('profession', None)
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

        record = RecordSchema.getCounts_main_filter(state, prof, county, city, zipcode, license, 
                                            phone, email, employees, company_name, srch_type_comp, lic_owner, srch_type_licO)
        if record:
            return {'count':record}
        return {'message': 'record not found'}, 404