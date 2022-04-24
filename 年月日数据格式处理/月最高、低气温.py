import pandas as pd
import numpy as np
from pandas import DataFrame

writer = pd.ExcelWriter('汛期逐月蒸散发.xlsx')
df1 = pd.DataFrame()
for i in range(1, 2):
    print(i)
    data = pd.read_excel('D:\\大论文\\降水数据度读取\\source_data_蒸发.xlsx', sheet_name=i, header=None,
                         names=['站名', '年', '月', '日', '蒸发'], engine='openpyxl')
    n = len(data)
    # data_array = np.array(data)
    # data_list = data_array.tolist()
    # print(data['站名'])
    # print(type(data))
    # print(n)
    rain = []

    # sum = 0
    day3_rain_max1 = []
    for j in range(n - 1):
        if data['年'][j] == data['年'][j + 1]:
            if data['月'][j] == data['月'][j + 1]:
                if j != n - 2:
                    rain.append(data['蒸发'][j])
                    # sum = sum + 1
                    # print(data['年'][j])
                else:
                    rain.append(data['蒸发'][n - 1])
                    rain_dataframe = DataFrame(rain)
                    # 修改
                    day3_rain_max = rain_dataframe.sum()
                    # day3_rain_max = rain_dataframe.rolling(1).sum()
                    # day3_rain_max = day3_rain_max.min()
                    if 4 <= data['月'][j] <= 7 and 1959 <= data['年'][j] <= 2020:
                        day3_rain_max1.append(day3_rain_max)
                        rain = []
                    else:
                        rain = []
                        # sum = 0
            else:
                rain.append(data['蒸发'][j])
                rain_dataframe = DataFrame(rain)
                # 修改
                day3_rain_max = rain_dataframe.sum()
                # day3_rain_max = rain_dataframe.rolling(1).sum()
                # day3_rain_max = day3_rain_max.min()
                if 4 <= data['月'][j] <= 7 and 1959 <= data['年'][j] <= 2020:
                    day3_rain_max1.append(day3_rain_max)
                    rain = []
                else:
                    rain = []
                # sum = 0
        else:
            rain.append(data['蒸发'][j])
            rain_dataframe = DataFrame(rain)
            # 修改
            day3_rain_max = rain_dataframe.sum()
            # day3_rain_max = rain_dataframe.rolling(1).sum()
            # day3_rain_max = day3_rain_max.min()
            if 4 <= data['月'][j] <= 7 and 1959 <= data['年'][j] <= 2020:
                day3_rain_max1.append(day3_rain_max)
                rain = []
            else:
                rain = []
            # sum = 0
    df = DataFrame(day3_rain_max1)
    df1 = pd.concat([df1, df], axis=1)
    # name = 'sheet_name' + str(i)
df1.to_excel(writer, sheet_name='name', index=None, engine='openpyxl')
writer.save()
writer.close()
# print(day3_rain_max1)
# print(len(day3_rain_max1))
