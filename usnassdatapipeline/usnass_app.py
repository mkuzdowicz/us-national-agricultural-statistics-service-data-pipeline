from usnassdatapipeline.scrapper.usnass_reports_downloader \
    import get_downloaded_files_paths_in
from usnassdatapipeline.scrapper.usnass_reports_downloader \
    import download_all_reports_for
from usnassdatapipeline.datamanipulation.soybean_condition_raports_loader \
    import clean_and_load_all_sbc_data_to_df_from
from usnassdatapipeline.datamanipulation.soybean_condition_raports_transformer \
    import transform_soybean_condition_report
import os

__author__ = 'Martin Kuzdowicz'


def run(cfg):
    reports_year = 2016
    output_file_name = 'soybean_condition_' + str(reports_year) + '.csv'

    output_dir = cfg.COOKED_DATA_MAIN_PATH + '/' + output_file_name

    # 1
    _create_directories_if_missing(cfg.RAW_DATA_MAIN_PATH)
    download_all_reports_for(cfg, reports_year)
    # 2
    downloaded_files_locations = \
        get_downloaded_files_paths_in(cfg.RAW_DATA_MAIN_PATH)
    # 2
    base_soybean_condition_df = \
        clean_and_load_all_sbc_data_to_df_from(downloaded_files_locations)
    # 3
    transformed_soybean_condition_df = \
        transform_soybean_condition_report(base_soybean_condition_df)
    # 4
    _create_directories_if_missing(cfg.COOKED_DATA_MAIN_PATH)
    transformed_soybean_condition_df.to_csv(output_dir, index=False)

    print('saved data frame as csv to ' + output_dir)
    print(transformed_soybean_condition_df)


def _create_directories_if_missing(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
