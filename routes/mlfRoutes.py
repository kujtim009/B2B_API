
from models.user import UserModel
import models.parameters as prm
from resources.records import (
    Record_by_license,
    RecordList,
    Record_by_state,
    Record_by_Individual_name,
    Record_by_license_and_state_prof,
    Record_by_company_name,
    getProfessions,
    getProfessionsBuckets,
    getProfessionsSubBuckets,
    Record_by_license_owner,
    GetRecCounts_LSP,
    GetRecCounts_LON,
    GetRecCounts_CPN,
    Records_by_main_filter,
    GetRecCounts_Main_filter,
    dnldRecords)


def insertMlfRoutes(api):
    api.add_resource(Record_by_license, '/licence/<int:license>')
    api.add_resource(Record_by_state, '/state/<string:state>')
    api.add_resource(Record_by_Individual_name, '/full_name')
    api.add_resource(RecordList, '/all_records')

    api.add_resource(Records_by_main_filter, '/mlf_filter')
    api.add_resource(GetRecCounts_Main_filter, '/mlf_count')
    api.add_resource(dnldRecords, '/mlf_dnld')

    api.add_resource(Record_by_license_and_state_prof, '/lic_state')
    api.add_resource(Record_by_company_name, '/company_name/<string:company>')
    api.add_resource(Record_by_license_owner,
                     '/license_owner/<string:licOwner>')
    api.add_resource(getProfessions, '/professions')
    api.add_resource(getProfessionsBuckets, '/professions_buckets')
    api.add_resource(getProfessionsSubBuckets, '/professions_subbuckets')
    api.add_resource(GetRecCounts_LSP, '/get_counts_lsp')
    api.add_resource(GetRecCounts_LON, '/get_counts_LON/<string:licOwner>')
    api.add_resource(GetRecCounts_CPN, '/get_counts_CPN/<string:company>')
