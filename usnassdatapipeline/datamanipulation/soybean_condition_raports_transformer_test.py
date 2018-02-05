import unittest
from usnassdatapipeline.datamanipulation.soybean_condition_raports_loader \
    import clean_and_load_all_sbc_data_to_df_from
from usnassdatapipeline.datamanipulation.soybean_condition_raports_transformer \
    import transform_soybean_condition_report
import pandas as pd
from datetime import datetime

__author__ = 'Martin Kuzdowicz'


class SoybeanConBaseDfTransformationTest(unittest.TestCase):

    def test_for_transformation_of_not_empty_df(self):
        # arrange
        paths_list_that_contains_sbc_data = ['unittests_resources/file_with_sbc_report.csv']
        # act
        transformed_df = transform_soybean_condition_report(
            clean_and_load_all_sbc_data_to_df_from(paths_list_that_contains_sbc_data)
        )
        # assert
        self.assertIsNot(transformed_df.empty,
                         'returns not empty data frame if csv file contains Soybean Condition reports')
        self.assertEqual(len(transformed_df.columns), 4)
        self.assertTrue('Week ending' in transformed_df)
        self.assertTrue('State' in transformed_df)
        self.assertTrue('Condition' in transformed_df)
        self.assertTrue('Percent' in transformed_df)

    def test_for_transformation_for_columns_order_in_df(self):
        # arrange
        paths_list_that_contains_sbc_data = ['unittests_resources/file_with_sbc_report.csv']
        # act
        transformed_df = transform_soybean_condition_report(
            clean_and_load_all_sbc_data_to_df_from(paths_list_that_contains_sbc_data)
        )
        # assert
        self.assertEqual(transformed_df.columns.get_loc('Week ending'), 0)
        self.assertEqual(transformed_df.columns.get_loc('State'), 1)
        self.assertEqual(transformed_df.columns.get_loc('Condition'), 2)
        self.assertEqual(transformed_df.columns.get_loc('Percent'), 3)

    def test_for_transformation_for_state_col_clarity(self):
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

    def test_for_transformation_for_transforming_empty_df(self):
        # arrange
        empty_df = pd.DataFrame()
        # act
        transformed_df = transform_soybean_condition_report(empty_df)
        # assert
        self.assertTrue(transformed_df.empty,
                        'returns empty data frame if csv file not contains Soybean Condition reports')

    def test_for_transformation_for_week_ending_column_date_format(self):
        # arrange
        paths_list_that_contains_sbc_data = ['unittests_resources/file_with_sbc_report.csv']
        # act
        transformed_df = transform_soybean_condition_report(
            clean_and_load_all_sbc_data_to_df_from(paths_list_that_contains_sbc_data)
        )
        # assert
        for date_string in transformed_df['Week ending']:
            self.assertNotEqual(date_string, "")
            # if the format will not be correct strptime will throw exception and test wil fail
            datetime.strptime(date_string, "%Y-%m-%d")
