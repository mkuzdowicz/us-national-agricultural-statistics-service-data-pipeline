import bs4 as bs4
import urllib.request

__author__ = 'Martin Kuzdowicz'


def scrape_download_links_of_all_usnass_reports_for(cfg, year):
    page_raw_html = urllib.request \
        .urlopen(cfg.US_NATIONAL_AGRICULTURAL_STATISTICS_SERVICE_URL) \
        .read()
    html = bs4.BeautifulSoup(page_raw_html, "html5lib")
    a_tags_with_download_links = html \
        .find("div", {"id": "n" + str(year)}) \
        .select("a[href]")
    href_attr_values = map(lambda tag: tag['href'],
                           a_tags_with_download_links)
    only_zip_files_links = filter(lambda s: s.endswith('.zip'),
                                  href_attr_values)
    return only_zip_files_links
