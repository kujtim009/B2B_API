
from resources.prmRecords import Prm_Records_by_main_filter, Prm_GetRecCounts_Main_filter, PrmDnldRecords, PrmgetZipByState, PrmgetZip


def insertPrmRoutes(api):
    api.add_resource(PrmgetZipByState, '/prm_zip_by_state')
    api.add_resource(PrmgetZip, '/prm_zip')
    api.add_resource(Prm_Records_by_main_filter, '/prm_filter')
    api.add_resource(Prm_GetRecCounts_Main_filter, '/prm_count')
    api.add_resource(PrmDnldRecords, '/prm_dnld')
