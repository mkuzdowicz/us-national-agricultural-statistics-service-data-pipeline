import zipfile
import io
import os
import urllib.request
from usnassdatapipeline.scrapper.usnass_web_scrapper \
    import scrape_download_links_of_all_usnass_reports_for

__author__ = 'Martin Kuzdowicz'

files_to_omit = ['prog_all_tables.csv', 'prog_help.htm', 'prog_index.htm']


def download_all_reports_for(cfg, year):
    report_files_links = scrape_download_links_of_all_usnass_reports_for(cfg, year)
    _download_and_unzip_reports_form_links(cfg, report_files_links)


def get_downloaded_files_paths_in(folder_loc):
    paths_to_traverse = []
    for root, dirs, files in os.walk(folder_loc):
        for file_ in files:
            folder_loc = os.path.join(root, file_)
            paths_to_traverse.append(folder_loc)
    return paths_to_traverse


def _download_and_unzip_reports_form_links(cfg, links):
    for zip_file_url in links:
        file_content = urllib.request.urlopen(zip_file_url).read()
        file_content_in_zip_wrapper = zipfile.ZipFile(io.BytesIO(file_content))
        folder_name = zip_file_url.rsplit('/', 1)[1].replace('zip', '')
        destination_path = cfg.RAW_DATA_MAIN_PATH + '/' + folder_name
        print('downloading files from => ' + zip_file_url + ' | to | ' + destination_path)
        file_in_archive = map(lambda fel: fel.filename,
                              file_content_in_zip_wrapper.filelist)
        files_to_extract = filter(lambda fel: fel not in files_to_omit,
                                  file_in_archive)
        file_content_in_zip_wrapper.extractall(
            path=destination_path,
            members=files_to_extract
        )
