import pandas as pd
from datetime import datetime

__author__ = 'Martin Kuzdowicz'


def transform_soybean_condition_report(base_soybean_conditions_df):
    if base_soybean_conditions_df.empty:
        return base_soybean_conditions_df

    foreign_key = 'soybean_table_id'
    conditions_table = pd.DataFrame(
        base_soybean_conditions_df,
        columns=["Very poor", "Poor", "Fair", "Good", "Excellent"]
    )
    conditions_dict_arr = []
    for row in conditions_table.iterrows():
        idx = row[0]
        value = row[1]
        for key in value.keys():
            conditions_dict = {
                foreign_key: idx,
                'Condition': key,
                'Percent': value[key]
            }
            conditions_dict_arr.append(conditions_dict)

    conditions_data_frames = pd.DataFrame(conditions_dict_arr)
    joint_table = conditions_data_frames \
        .join(base_soybean_conditions_df, on=foreign_key)
    return joint_table[['Week ending', 'State', 'Condition', 'Percent']].astype(
        dtype={'Week ending': datetime}).sort_values('Week ending')
