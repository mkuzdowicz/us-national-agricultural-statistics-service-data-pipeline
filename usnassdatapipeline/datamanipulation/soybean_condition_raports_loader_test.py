import unittest
from usnassdatapipeline.datamanipulation.soybean_condition_raports_loader \
    import clean_and_load_all_sbc_data_to_df_from
from datetime import datetime

__author__ = 'Martin Kuzdowicz'


class SoybeanConCSVDataLoadTest(unittest.TestCase):

    def test_for_loading_csv_that_contains_soybean_condition_report(self):
        # arrange
        paths_list_that_contains_sbc_data = ['unittests_resources/file_with_sbc_report.csv']
        # act
        base_df = clean_and_load_all_sbc_data_to_df_from(paths_list_that_contains_sbc_data)
        # assert
        self.assertIsNot(base_df.empty, 'returns not empty data frame if csv file contains Soybean Condition reports')
        self.assertEqual(len(base_df.columns), 7)
        self.assertTrue('Week ending' in base_df)
        self.assertTrue('State' in base_df)
        self.assertTrue('Very poor' in base_df)
        self.assertTrue('Poor' in base_df)
        self.assertTrue('Fair' in base_df)
        self.assertTrue('Good' in base_df)
        self.assertTrue('Excellent' in base_df)

    def test_for_loading_csv_that_not_contains_soybean_condition_report(self):
        # arrange
        paths_list_that_contains_sbc_data = ['unittests_resources/file_without_sbc_report.csv']
        # act
        base_df = clean_and_load_all_sbc_data_to_df_from(paths_list_that_contains_sbc_data)
        # assert
        self.assertTrue(base_df.empty, 'returns empty data frame if csv file not contains Soybean Condition reports')

    def test_for_week_ending_column_date_format(self):
        # arrange
        paths_list_that_contains_sbc_data = ['unittests_resources/file_with_sbc_report.csv']
        # act
        base_df = clean_and_load_all_sbc_data_to_df_from(paths_list_that_contains_sbc_data)
        # assert
        for date_string in base_df['Week ending']:
            self.assertNotEqual(date_string, "")
            # if the format will not be correct strptime will throw exception and test wil fail
            datetime.strptime(date_string, "%Y-%m-%d")

    def test_for_state_col_clarity_for_base_df(self):
        # arrange
        paths_list_that_contains_sbc_data = ['unittests_resources/file_with_sbc_report.csv']
        # act
        base_df = clean_and_load_all_sbc_data_to_df_from(paths_list_that_contains_sbc_data)
        state_cols = base_df['State']
        # assert
        self.assertIsNot(('"' in state_cols), 'there is no " character in state column')
        self.assertEqual(state_cols.isnull().sum(), 0)
        for c in state_cols:
            self.assertNotEquals(c, "Previous week")
            self.assertNotEquals(c, "Previous year")
