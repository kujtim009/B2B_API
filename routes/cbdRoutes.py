from resources.cbdRecords import Cbd_Records_by_main_filter, Cbd_GetRecCounts_Main_filter, CbdDnldRecords, CbdgetCitiesByState


def insertCbdRoutes(api):
    api.add_resource(CbdgetCitiesByState, '/cbd_city_by_state')
    api.add_resource(Cbd_Records_by_main_filter, '/cbd_filter')
    api.add_resource(Cbd_GetRecCounts_Main_filter, '/cbd_count')
    api.add_resource(CbdDnldRecords, '/cbd_dnld')
