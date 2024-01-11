import pandas as pd
from scipy.interpolate import interp1d

experience_value = pd.read_excel('.\\H-V-Q.xlsx', header=None, usecols=(0, 1, 2), names=['水位', '库容', '下泄'],
                                 engine='openpyxl')
experience_value.drop(experience_value.head(1).index, inplace=True)
experience_value.reset_index(drop=True, inplace=True)


def interpolation_f(water_level: float):
    """
    给定水位插值法返回对应的库容和下泄
    :param water_level:
    :return:
    """
    x = experience_value['水位']
    y1 = experience_value['库容']
    y2 = experience_value['下泄']
    f1 = interp1d(x, y1, kind='linear')
    f2 = interp1d(x, y2, kind='linear')
    return f1(water_level).tolist(), f2(water_level).tolist()


if __name__ == '__main__':
    real_value_dict = pd.read_excel('.\\t-q.xlsx', sheet_name=None, header=None, usecols=(0, 1),
                                    names=['时间', '洪峰流量'],
                                    engine='openpyxl')
    all_result = {}
    for sheet_name in real_value_dict.keys():
        real_value = real_value_dict[sheet_name]
        real_value.drop(real_value.head(1).index, inplace=True)
        real_value.reset_index(drop=True, inplace=True)

        start_water_level = 82.8
        result = []
        last_storage, last_output_w = interpolation_f(start_water_level)
        cur_water_level = start_water_level
        # 记录第一行起始数据
        result.append([None,0, start_water_level, last_storage, last_output_w])

        for row_index in range(len(real_value)):
            # 计算当前洪峰流量的维持时间,cur_time单位为秒
            if row_index == 0:
                cur_time = (real_value['时间'][row_index + 1] - real_value['时间'][row_index]).seconds
            else:
                cur_time = (real_value['时间'][row_index] - real_value['时间'][row_index - 1]).seconds
            cur_input_w = real_value['洪峰流量'][row_index]
            # 当前水位能否维持
            if cur_input_w < last_output_w:
                # 如果当前水位高于起调水位，则开始降水位
                if cur_water_level > start_water_level:
                    while abs((cur_input_w - interpolation_f(cur_water_level)[1])*cur_time/10000 + last_storage - interpolation_f(cur_water_level)[0])>1:
                        cur_water_level -= 0.0001
                        print(f'{cur_water_level} - %s' % abs(
                            (cur_input_w - interpolation_f(cur_water_level)[1]) * cur_time / 10000 + last_storage -
                            interpolation_f(cur_water_level)[0]))
                    last_storage, last_output_w = interpolation_f(cur_water_level)
                    result.append([real_value['时间'][row_index],cur_input_w, cur_water_level, last_storage, last_output_w])
                else:
                    result.append([real_value['时间'][row_index],cur_input_w, cur_water_level, last_storage, cur_input_w])
            # 不能维持当前水位
            else:
                while abs((cur_input_w - interpolation_f(cur_water_level)[1]) * cur_time / 10000 + last_storage -
                          interpolation_f(cur_water_level)[0]) > 1:
                    # 通过步长调整cur_water_level
                    cur_water_level += 0.0001
                    print(f'{cur_water_level} - %s' % abs(
                        (cur_input_w - interpolation_f(cur_water_level)[1]) * cur_time / 10000 + last_storage -
                        interpolation_f(cur_water_level)[0]))
                last_storage, last_output_w = interpolation_f(cur_water_level)
                result.append([real_value['时间'][row_index],cur_input_w, cur_water_level, last_storage, last_output_w])
        all_result[sheet_name] = result

    writer = pd.ExcelWriter('output.xlsx')
    for sheet_name in all_result.keys():
        df = pd.DataFrame(all_result[sheet_name], columns=['时间','入库流量', '水位', '库容', '下泄流量'])
        df.to_excel(writer, sheet_name=sheet_name, index=False)
    writer.close()
