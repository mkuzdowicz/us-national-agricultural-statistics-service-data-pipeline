import usnassdatapipeline.usnass_app as usnass_app
import usnass_app_config as cfg
import sys

__author__ = 'Martin Kuzdowicz'

if sys.version_info[0] < 3:
    raise "This applicaion requiers Python 3"

if __name__ == '__main__':
    usnass_app.run(cfg)
