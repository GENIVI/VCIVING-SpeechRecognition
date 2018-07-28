from FindMapsExecutor.db.locationdb import LocationDB
from FindMapsExecutor.db.preprocessors import LocationPreProcessor


_db_file_path = "D:/GENIVI/Projects/TaskExecutors/FindMapsExecutor/db/storage/us.db"
locations_to_test = ["Weedy Shoals", "Wedge Cape", "Pristuulax Anii", "Webster Lake", "Volcan Point", "McArthur Reef", "Webfoot Prospect", "Rio Tiajuana", "Udiix", "Guys Branch", "Stellwagen Basin", "Sonom Beach", "Cape Turner"]

location_db = LocationDB(file_path=_db_file_path, db_flag=LocationDB.FLAG_DB_RDONLY)

# Pre-processes the locations.
location_pre_proc = LocationPreProcessor(locations_to_test)
location_pre_proc.pre_process()
locations_to_test = location_pre_proc.get_locations()

for location in locations_to_test:
    print(location_db.get(location))
