from resources.cbdRecords import Cbd_Records_by_main_filter, Cbd_GetRecCounts_Main_filter


def insertCbdRoutes(api):
    api.add_resource(Cbd_Records_by_main_filter, '/cbd_filter')
    api.add_resource(Cbd_GetRecCounts_Main_filter, '/cbd_count')
    # api.add_resource(dnldRecords, '/cbd_dnld')
