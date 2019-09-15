from FindMapsExecutor.db.bigdata import BigDataFile
from FindMapsExecutor.db.locationdb import LocationDB
from FindMapsExecutor.db.preprocessors import Chunker
from FindMapsExecutor.db.preprocessors import LocationPreProcessor
import time, datetime

_data_file_path = "D:/Dev/GENIVI/Projects/TaskExecutors/FindMapsExecutor/storage/data/US.txt"
_location_db_file_path = "D:/Dev/GENIVI/Projects/TaskExecutors/FindMapsExecutor/storage/us.locations"
_mapper_db_file_path = "D:/Dev/GENIVI/Projects/TaskExecutors/FindMapsExecutor/storage/us.mapper"
_verbose_mode = True
_deep_chunking = False
_data_batch_size = 10000


def log(message):
    if _verbose_mode:
        print(message)


big_data = BigDataFile(file_path=_data_file_path, log_function=log, batch_size=_data_batch_size)
location_db = LocationDB(_location_db_file_path, LocationDB.FLAG_DB_CREATE)
mapper_db = LocationDB(_mapper_db_file_path, LocationDB.FLAG_DB_CREATE)
_num_examples = big_data.get_example_count()

log("Started generating the Location Database...")

while big_data.has_next_example():
    start_time = time.clock()

    # print("1: " + str(time.clock()))

    example_feature, example_label = big_data.get_next_example()
    current_real_ptr = big_data.get_current_example_ptr()
    # print("2.1: " + str(time.clock()))
    # Pre-processes the example feature.
    example_feature_preproc = LocationPreProcessor([example_feature])
    example_feature_preproc.pre_process()
    example_feature = example_feature_preproc.get_locations()[0]
    # print("2.2: " + str(time.clock()))

    example_feature_chunker = Chunker(to_chunk=example_feature, deep_chunking=_deep_chunking)
    example_feature_chunks = example_feature_chunker.get_chunked()
    # print("3: " + str(time.clock()))

    for example_feature_chunk in example_feature_chunks:
        existing_labels_for_chunk = location_db.get(example_feature_chunk)

        if existing_labels_for_chunk is not None:
            splt_existing_labels = existing_labels_for_chunk.split(BigDataFile.TEXT_FILE_DATA_SUB_SEPARATOR)
            splt_existing_labels.append(example_label)
            splt_existing_labels = list(set(splt_existing_labels))
            existing_labels_for_chunk = BigDataFile.TEXT_FILE_DATA_SUB_SEPARATOR.join(splt_existing_labels)
        else:
            existing_labels_for_chunk = example_label

        location_db.insert(example_feature_chunk, existing_labels_for_chunk)

    # print("4: " + str(time.clock()))

    end_time = time.clock()
    seconds_diff = end_time - start_time
    eta_total_seconds = seconds_diff * (_num_examples - current_real_ptr)
    log("Feature: " + str(current_real_ptr) + "/" + str(_num_examples) + "    ETA " + str(datetime.timedelta(seconds=eta_total_seconds)))


location_db.close()
log("Location Database successfully generated....")

big_data.refresh_pointers()

log("Started genrating the Mapper Database...")

while big_data.has_next_location():
    location_label, location_geocoords = big_data.get_next_location()
    current_real_ptr = big_data.get_current_example_ptr()
    location_geocoords = BigDataFile.TEXT_FILE_DATA_SUB_SEPARATOR.join(location_geocoord for location_geocoord in location_geocoords)

    mapper_db.insert(location_label, location_geocoords)
    log("Feature: " + str(current_real_ptr) + "/" + str(_num_examples))

mapper_db.close()
log("Mapper Database successfully generated.")

log("Database generation process successfully completed. Exiting...")
