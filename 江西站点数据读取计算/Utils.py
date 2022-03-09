import os


def get_file_path_list(root_path: str):
    """
    查找root地址下的所有文件夹
    :param root_path:
    :return: 所有文件夹的绝对路径list
    eg：
    ['H:\\PycharmProjects\\auto_read_text\\上饶',
     'H:\\PycharmProjects\\auto_read_text\\九江',
     'H:\\PycharmProjects\\auto_read_text\\井冈山']
    """
    dirs = os.listdir(root_path)
    # 初始化返回值
    file_path_list = []
    # 由于根目录下存在SURF_CLI_CHN_MUL_DAY_readme.txt,或者其他xlsx，设置过滤，过滤掉txt文件和xlsx文件
    for file_name in dirs:
        if len(file_name) > 4:
            if (file_name[-4:] == '.txt') | (file_name[-5:] == '.xlsx'):
                print('忽略：' + os.getcwd() + '\\江西' + '\\' + file_name)
            else:
                file_path_list.append(os.getcwd() + '\\江西' + '\\' + file_name)
                print('取得文件夹：' + os.getcwd() + '\\江西' + '\\' + file_name)
        else:
            file_path_list.append(os.getcwd() + '\\江西' + '\\' + file_name)
            print('取得文件夹：' + os.getcwd() + '\\江西' + '\\' + file_name)
    return file_path_list


def get_txt_list(path):
    """
    通过路径获取路径内的txt文件的列表
    :param path: str
    :return: list
    eg:
    ['S202106101125199941901.txt']
    """
    txt_list = []
    for file_name in os.listdir(path):
        # 取txt文件
        if file_name[-4:] == '.txt':
            # 忽略文件夹中的指定文本
            if file_name == 'SURF_CLI_CHN_MUL_DAY_readme.txt':
                print('忽略' + path + '中SURF_CLI_CHN_MUL_DAY_readme.txt')
            else:
                # 将txt文件名加入txt_list中
                txt_list.append(path + '\\' + file_name)
                print('取得txt：' + path + '\\' + file_name)
        else:
            print('忽略' + path + file_name)
    return txt_list


def return_format_data(file_name_abs_path):
    '''
    通过文件的绝对路径按格式返回文件内容
    :param file_name_abs_path: str
    :return: list
    eg:
    [上饶,    [[1980,1,1,1.08],
              [1980,1,1,1.08]
            ]
    ]
    '''
    file = open(file_name_abs_path)
    print('打开：' + file_name_abs_path)
    file_data = []
    last_line = [0, 0, 0, 0]
    while 1:
        line = file.readline()
        # 未行检测
        if not line:
            #
            break
        # ['58637', '1980', '12', '31', '0.0000', '999999.0000', '999999.0000', '1009.6000', '1.8000', '6.4000', '5.2000', '56.0000', '8.2000', '1005.7000', '-0.2000', '1013.3000', '12.8000', '4.0000', '999003.0000', '35.0000', '\n']
        line_list = line.split(' ')
        # 忽略首行
        if line_list[0] == 'V01301':
            pass
        # 不为首行时执行
        else:
            # 判断是否为重复值
            if int(line_list[3]) == last_line[2]:
                pass
            else:
                # 判断是否为fake值
                if float(line_list[9]) > 99:
                    pass
                # 不为fake值时，day自加1，sum加上真实值
                else:

                    # file_data=[1980,12,31,1.8] -> [int,int,int,float]
                    file_data.append([int(line_list[1]), int(line_list[2]), int(line_list[3]), float(line_list[9])])
                    last_line = [int(line_list[1]), int(line_list[2]), int(line_list[3]), float(line_list[9])]
    file.close()
    # 取路径名中的文件夹名作为站名
    station_name = os.path.dirname(file_name_abs_path).split('\\')[-1]
    format_data = [station_name, file_data]
    return format_data


def list_1st_list(result: list):
    list_1st = []
    for i in range(len(result)):
        list_1st.append(result[i][1])
    return list_1st

def return_season(month):
    '''
    month   return  name
     1 2     0     今年冬季
     3 4 5   1     今年春季
     6 7 8   2     今年夏季
     9 10 11 3     今年秋季
     12      4     明年冬季
    '''
    if int(month) < 3:
        return 0
    else:
        if int(month) < 6:
            return 1
        else:
            if int(month) < 9:
                return 2
            else:
                if int(month) < 12:
                    return 3
                else:
                    return 4
