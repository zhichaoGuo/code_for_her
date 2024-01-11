import pandas as pd
from scipy.interpolate import interp1d


def interpolation_f(water_level: float) -> (float, float):
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
    # 数据配置=========================================
    experience_file = '.\\H-V-Q.xlsx'  # 经验值文件
    real_file = '.\\t-q.xlsx'  # 真实数据文件
    output_file = '.\\output.xlsx'  # 输出文件
    start_water_level = 82.8  # 起调水位
    step = 0.0001  # 设置步长
    # ===============================================
    experience_value = pd.read_excel(experience_file, header=None, usecols=(0, 1, 2), names=['水位', '库容', '下泄'],
                                     engine='openpyxl')
    experience_value.drop(experience_value.head(1).index, inplace=True)
    experience_value.reset_index(drop=True, inplace=True)

    real_value_dict = pd.read_excel(real_file, sheet_name=None, header=None, usecols=(0, 1),
                                    names=['时间', '洪峰流量'],
                                    engine='openpyxl')
    # all_result储存所有的结果，{"sheet_name":[[first_line],[...],[...]]}
    all_result = {}
    # 对t-q.xlsx的每个sheet进行操作
    for sheet_name in real_value_dict.keys():
        real_value = real_value_dict[sheet_name]
        # 删除第一行表头
        real_value.drop(real_value.head(1).index, inplace=True)
        real_value.reset_index(drop=True, inplace=True)
        # 初始化本sheet表的输出结果 [[first],[...],[...]]
        result = []
        # 插值计算起调水位对应的库容和泄流
        last_storage, last_output_w = interpolation_f(start_water_level)
        # 将当前水位设置为起调水位
        cur_water_level = start_water_level
        # 记录第一行起始数据，时间为None，入库为0，水位为起调水位，库容为起调水位对应库容，泄流为起调水位对应泄流
        result.append([None, 0, start_water_level, last_storage, last_output_w])
        # 开始对每一条数据进行计算
        for row_index in range(len(real_value)):
            # 计算当前洪峰流量的维持时间，cur_time单位为秒
            # 如果为第一次洪峰流量，则时间为本次到下一次的时间；如果不是第一次，则时间为上次到本次的时间
            if row_index == 0:
                cur_time = (real_value['时间'][row_index + 1] - real_value['时间'][row_index]).seconds
            else:
                cur_time = (real_value['时间'][row_index] - real_value['时间'][row_index - 1]).seconds
            # 将本次洪峰流量设为当前入库流量
            cur_input_w = real_value['洪峰流量'][row_index]
            # 判断当前水位是否应该上调，依据为当前入库流量是否大于上次水位的理论出库流量，如果大于则应该上调水位，否则应该下调水位
            if cur_input_w < last_output_w:
                # 进入此分支则证明，水位应该下调
                # 如果当前水位高于起调水位，则开始降水位
                if cur_water_level > start_water_level:
                    # 不断的下降当前水位，直到上次水位的理论库容-本次净流出水量与本次水位的理论库容差值小于1，则停止下降水位
                    while abs((cur_input_w - interpolation_f(cur_water_level)[1]) * cur_time / 10000 + last_storage -
                              interpolation_f(cur_water_level)[0]) > 1:
                        cur_water_level -= step
                        print(f'{cur_water_level} - %s' % abs(
                            (cur_input_w - interpolation_f(cur_water_level)[1]) * cur_time / 10000 + last_storage -
                            interpolation_f(cur_water_level)[0]))
                    # 计算当前水位的理论库容和理论泄流
                    last_storage, last_output_w = interpolation_f(cur_water_level)
                    result.append(
                        [real_value['时间'][row_index], cur_input_w, cur_water_level, last_storage, last_output_w])
                # 否则应该维持水位，因为当前水位不能低于起调水位（由于cur_water_level是float数据，所以不是很准确）
                else:
                    result.append(
                        [real_value['时间'][row_index], cur_input_w, cur_water_level, last_storage, cur_input_w])
            # 不能维持当前水位
            else:
                # 不断的上升当前水位，直到上次水位的理论库容+本次净流入水量与本次水位的理论库容差值小于1，则应该停止上升水位
                while abs((cur_input_w - interpolation_f(cur_water_level)[1]) * cur_time / 10000 + last_storage -
                          interpolation_f(cur_water_level)[0]) > 1:
                    # 通过步长调整cur_water_level
                    cur_water_level += step
                    print(f'{cur_water_level} - %s' % abs(
                        (cur_input_w - interpolation_f(cur_water_level)[1]) * cur_time / 10000 + last_storage -
                        interpolation_f(cur_water_level)[0]))
                # 计算当前水位的理论库容和理论泄流
                last_storage, last_output_w = interpolation_f(cur_water_level)
                result.append(
                    [real_value['时间'][row_index], cur_input_w, cur_water_level, last_storage, last_output_w])
        # 在当前数据都循环完之后，在all_result中以sheet_name为key保存数据
        all_result[sheet_name] = result
    writer = pd.ExcelWriter(output_file)
    for sheet_name in all_result.keys():
        df = pd.DataFrame(all_result[sheet_name], columns=['时间', '入库流量', '水位', '库容', '下泄流量'])
        df.to_excel(writer, sheet_name=sheet_name, index=False)
    writer.close()
