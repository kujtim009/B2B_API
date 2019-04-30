from db import db, ma
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from models.user import Userinfo

class ItemModel(db.Model):
    __tablename__ = 'Master_Layout'


    Record_id = db.Column(db.Integer, primary_key=True)
    License = db.Column('License_Number', db.String(40))
    Primary_Location_State = db.Column('Business_state', db.String(20))
    DBA_Fictitious_Name = db.Column('Company_name', db.String(80))
    Profession_Type_Occupation_Type = db.Column('Profession', db.String(80))
    ###################
    First_name = db.Column(db.String(80))
    Middle_Initial = db.Column(db.String(80))
    Last_name = db.Column(db.String(80))
    ######################
    License_Owner_Name = db.Column(db.String(80))
    Legal_Business_Name = db.Column('Fictitious_name', db.String(80))
    Owner_Name = db.Column('Owner_name', db.String(80))
    Business_SSN = db.Column('Business_id_number', db.String(80))
    Phone_Number = db.Column('Business_phone', db.String(80))
    email = db.Column('Business_email', db.String(80))

    Mailing_Address_Line_1 = db.Column('Business_mailing_address_1', db.String(80))
    Mailing_Address_Line_2 = db.Column('Business_mailing_address_2', db.String(80))
    Mailing_Address_City = db.Column('Business_mailing_city', db.String(40))
    Mailing_Address_State = db.Column('Business_mailing_state', db.String(20))
    Mailing_Address_Zip = db.Column('Business_mailing_zip_5', db.String(40))
    Primary_Location_Line_1 = db.Column('Business_address_1', db.String(80))
    Primary_Location_Line_2 = db.Column('Business_address_2', db.String(80))
    Primary_Location_City = db.Column('Business_city', db.String(40))
    
    Primary_Location_Zip5 = db.Column('Business_zip_5', db.String(20))
    Primary_Location_Zip4 = db.Column('Business_zip_4', db.String(20))
    Additional_Business_Address_3_Line_1 = db.Column('Location_address_1', db.String(80))
    Additional_Business_Address_3_Line_2 = db.Column('Location_address_2', db.String(80))
    Additional_Business_Address_3_City = db.Column('Location_city', db.String(40))
    Additional_Business_Address_3_State = db.Column('Location_state', db.String(20))
    Additional_Business_Address_3_Zip = db.Column('Location_zip_5', db.String(20))
    Additional_Business_Address_4_Line_1 = db.Column('Other_business_add1', db.String(20))
    Additional_Business_Address_4_Line_2 = db.Column('Other_business_add2', db.String(80))
    Additional_Business_Address_4_City = db.Column('Other_business_city', db.String(40))
    Additional_Business_Address_4_State = db.Column('Other_business_state', db.String(20))
    Additional_Business_Address_4_Zip = db.Column('Other_business_zip5', db.String(20))
    License_Owner_Address_Line_1 = db.Column('Owner_address_1', db.String(80))
    License_Owner_Address_Line_2 = db.Column('Owner_address_2', db.String(80))
    License_Owner_Address_City = db.Column('Owner_city', db.String(40))
    License_Owner_Address_State = db.Column('Owner_state', db.String(20))
    License_Owner_Address_Zip = db.Column('Owner_zip_5', db.String(20))
    County = db.Column('County', db.String(40))
    Business_Description = db.Column('Business_description', db.String(160))
    SIC_Code = db.Column('SIC_code', db.String(40))
    NAICS_Code = db.Column('NAICS_code', db.String(40))
    In_Business_Since_Info = db.Column('Location_start_date', db.String(220))
    URL_of_business_filing_license = db.Column('Business_URL', db.String(80))
    Number_of_Employees = db.Column('Number_of_employees', db.String(20))
    Longitude_Latitude = db.Column('Longitude_Latitude', db.String(80))
    Entity_Type = db.Column('Ownership_business_type', db.String(80))
    Home_Based_Business = db.Column('Home_based', db.String(20))
    Date_Reported = db.Column('Record_Date', db.String(80))
    Date_Information = db.Column('Compiled_Date', db.String(80))
    
    Certificate = db.Column('Certification_number_1', db.String(80))
    Account_Number = db.Column('Account_Number', db.String(80))
    Issue_Date = db.Column('Original_start_date', db.String(80))
    Start_Date_of_License = db.Column('Effective_date', db.String(80))
    Cancellation_Date = db.Column('Cancellation_Date', db.String(80))
    End_Date = db.Column('End_Date', db.String(80))
    Expiration_Date_of_License = db.Column('Expiration_date', db.String(80))
    Status_License_Description = db.Column('Status', db.String(80))
    Status_License_Code = db.Column('Status_of_License_Code', db.String(80))
    License_Type = db.Column('License_Acronym_description', db.String(80))
    
    License_Classifications = db.Column('License_description', db.String(80))
    Additional_Business_License_Descriptions = db.Column('Specialty', db.String(80))
    Source_of_data = db.Column('Source_of_data', db.String(80))
    URL = db.Column('Licensing_Board', db.String(220))
    Provider_Source_Data_Key = db.Column('Provider_Source_Data_Key', db.String(80))
    Data_Provider_NameID = db.Column('Vendor_Name_ID', db.String(80))
    File_name = db.Column('File_name', db.String(80))
    Source_of_data = db.Column('Source_of_data', db.String(80))

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
        result = ItemModel.query.filter_by(License=license).limit(cls.record_output).all()
        record_schema = RecordSchema(many=True, only=cls.get_user_fields())
        output = record_schema.dump(result)
        return jsonify({'Records': output})

    @classmethod
    def find_by_licence_and_state(cls, license, state, prof):
        if license is None and state is None and prof is None:
            return jsonify({'Records': 'Search input is missing!'})
        else:
            result = db.engine.execute('FilterResults_LSP ?, ?, ?, ?', [cls.record_output, license, state, prof])    

        fields = cls.get_user_fields()
        record_schema = RecordSchema(many=True, only=cls.get_user_fields())
        output = record_schema.dump(result)
        return jsonify({'Records': output})

    @classmethod
    def main_filter(cls, *fields):
        parameters = [x for x in fields]
        parameters.insert(0, cls.record_output)
        if license is None and state is None and prof is None:
            return jsonify({'Records': 'Search input is missing!'})
        else:
            result = db.engine.execute('Fgx_api_main_filter ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?', parameters)    

        fields = cls.get_user_fields()
        record_schema = RecordSchema(many=True, only=cls.get_user_fields())
        output = record_schema.dump(result)
        return jsonify({'Records': output})

    @classmethod
    def getCounts_main_filter(cls, *fields):
        result = db.engine.execute('Fgx_api_main_counter ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?', fields)
        for rowe in result:
            return rowe[0]
        return result


    @classmethod
    def find_by_state(cls, state):
        result = ItemModel.query.filter_by(Primary_Location_State=state).limit(cls.record_output).all()
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
        result = db.engine.execute('FilterResults_LON ?, ?, ?', [cls.record_output, licOwner, srch_type])
        record_schema = RecordSchema(many=True, only=cls.get_user_fields())
        output = record_schema.dump(result)
        return jsonify({'Records': output})


    @classmethod
    def find_by_compnay(cls, company, srch_type):
        result = db.engine.execute('FilterResults_C ?, ?, ?', [cls.record_output, company, srch_type])
        
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
    def getProfesionByState(cls, state):
        # sqlquery = "select DGX_Profession, count(DGX_Profession) from Master_layout with(nolock) group by DGX_Profession order by DGX_Profession asc"
        result = db.engine.execute('Fgx_api_getProfesionByState ?', [state])
        return result    

    @classmethod
    def getCounts_lsp(cls, license, state, prof):
        result = db.engine.execute('Api_record_counter_LSP ?, ?, ?', [license, state, prof])
        for rowe in result:
            return rowe[0]
        return result    

    @classmethod
    def getCounts_LON(cls, licOwner, srch_type):
        result = db.engine.execute('Api_record_counter_LON ?, ?', [licOwner, srch_type])
        for rowe in result:
            return rowe[0]
        return result   

    @classmethod
    def getCounts_CPN(cls, company, srch_type):
        result = db.engine.execute('Api_record_counter_CPN ?, ?', [company, srch_type])
        for rowe in result:
            return rowe[0]
        return result           