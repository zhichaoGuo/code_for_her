"""
非等步长径流数据插值为逐时刻数据
"""
import calendar
from datetime import datetime

import pandas as pd
from scipy.interpolate import interp1d

def toTimestamp(d):
    return calendar.timegm(d.timetuple())
def interpolation_f(raw_data, _time) -> (float, float, float, float):
    """
    给定水位插值法返回对应的库容和下泄
    """
    _time = toTimestamp(_time)
    x = raw_data['时间'].apply(toTimestamp)
    y1 = raw_data['入库流量']
    y2 = raw_data['水位']
    y3 = raw_data['库容']
    y4 = raw_data['下泄流量']
    f1 = interp1d(x, y1, kind='linear')
    f2 = interp1d(x, y2, kind='linear')
    f3 = interp1d(x, y3, kind='linear')
    f4 = interp1d(x, y4, kind='linear')
    return f1(_time).tolist(), f2(_time).tolist(), f3(_time).tolist(), f4(_time).tolist()


if __name__ == '__main__':
    file_name = ".\\花凉亭调洪演算 起调水位82.8(1954-2021).xlsx"
    output_file = ".\\output_file.xlsx"
    data_dict = pd.read_excel(file_name, sheet_name=None, header=None, usecols=(0, 1, 2, 3, 4),
                              names=['时间', '入库流量', '水位', '库容', '下泄流量'], engine='openpyxl')
    all_result_dict = {}
    for sheet_name in data_dict.keys():
        cur_sheet_result = []
        data = data_dict[sheet_name]
        data.drop(data.head(2).index, inplace=True)
        data.reset_index(drop=True, inplace=True)

        for _index in range(len(data['时间'])):
            if type(data['时间'][_index]) == str:
                data['时间'][_index] = datetime.strptime(data['时间'][_index],"%Y/%m/%d %H:%M:%S")
        first = data['时间'][0]
        last = data['时间'][len(data['时间']) - 1]
        result_time = pd.date_range(start=first, end=last, freq='H')
        for cur_time in result_time:
            discharge_in, level, storage, discharge_out = interpolation_f(data, cur_time.to_pydatetime())
            cur_sheet_result.append([cur_time,discharge_in, level, storage, discharge_out])
        all_result_dict[sheet_name] = cur_sheet_result
    writer = pd.ExcelWriter(output_file)
    for sheet_name in all_result_dict.keys():
        df = pd.DataFrame(all_result_dict[sheet_name], columns=['时间', '入库流量', '水位', '库容', '下泄流量'])
        df.to_excel(writer, sheet_name=sheet_name, index=False)
    writer.close()
    # ======================================================================================================
