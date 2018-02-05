import io
import pandas as pd
from datetime import datetime

__author__ = 'Martin Kuzdowicz'

WEEK_ENDING_KEYWORD = "Week Ending"
SOYBEAN_CONDITION_KEYWORD = "Soybean Condition"
DATA_LINE_TYPE_LABEL = '"d"'


def clean_and_load_all_sbc_data_to_df_from(files_paths_list):
    all_soybean_condition_data_frames = []
    for file_path in files_paths_list:
        file_content = _extract_soybean_condition_content_if_exist_from(file_path)
        sbc_df = _clean_and_map_sbc_file_content_to_df(file_content)
        all_soybean_condition_data_frames.append(sbc_df)

    return pd.concat(all_soybean_condition_data_frames, ignore_index=True)


def _prepare_week_ending_value_from(file_line):
    week_ending_val = file_line.split(WEEK_ENDING_KEYWORD, 1)[1] \
        .replace('"', '') \
        .strip()
    return datetime.strptime(week_ending_val, '%B %d, %Y').strftime("%Y-%m-%d")


def _extract_soybean_condition_content_if_exist_from(file_path):
    with open(file_path, encoding="ISO-8859-1") as csv_file:
        file_content = csv_file.read()
        if SOYBEAN_CONDITION_KEYWORD in file_content:
            lines = file_content.split('\n')
            data_lines = _map_to_sbc_data_comma_sep_string(lines)
            return "\n".join(data_lines)
        return ""


def _map_to_sbc_data_comma_sep_string(file_lines):
    week_ending_val = ''
    clear_lines = []
    for line in file_lines:
        if WEEK_ENDING_KEYWORD in line:
            week_ending_val = _prepare_week_ending_value_from(line)
        if DATA_LINE_TYPE_LABEL in line:
            state_col_val = line.split(",")[2]
            if state_col_val == '""':
                return clear_lines
            current_line = week_ending_val + ', ' + line
            clear_lines.append(current_line)
    return clear_lines


def _clean_and_map_sbc_file_content_to_df(file_data):
    frames = []
    main_df = pd.DataFrame()
    if file_data:
        df = pd.read_csv(io.StringIO(file_data), header=None)
        df.columns = ["Week ending", "t_num", "t_key", "State", "Very poor", "Poor", "Fair", "Good", "Excellent"]
        df.drop("t_num", axis=1, inplace=True)
        df.drop("t_key", axis=1, inplace=True)
        frames.append(df)
    if frames:
        main_df = pd.concat(frames, ignore_index=True)
    return main_df
