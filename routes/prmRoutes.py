from resources.prmRecords import Prm_Records_by_main_filter, Prm_GetRecCounts_Main_filter, PrmDnldRecords, PrmgetZipByState


def insertCbdRoutes(api):
    api.add_resource(CbdgetZipByState, '/prm_zip_by_state')
    api.add_resource(CbdgetZip, '/prm_zip')
    api.add_resource(Cbd_Records_by_main_filter, '/prm_filter')
    api.add_resource(Cbd_GetRecCounts_Main_filter, '/prm_count')
    api.add_resource(CbdDnldRecords, '/prm_dnld')
