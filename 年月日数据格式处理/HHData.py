import openpyxl


def hh_load_excel(path,sheet_num):
    pass

def hh_check_data(data):
    pass

class HHData:
    def __init__(self):
        # 在init中就将类型创建好
        self.data = {'1999': {'11': {'29': '1.6543',
                                     '30': '1.6543'
                                     },
                              '12': {'1': '1.6543',
                                     '2': '1.6543'
                                     }
                              },
                     '2000': {'1': {'1': '1.6543',
                                    '2': '1.6543'
                                    }
                              }
                     }

    def __iter__(self):
        return iter(self.data.keys())

    def __getitem__(self, item):
        return HHYearData(self.data[item]) # 输入一个年份返回一个年类型

    def year_list(self):
        return list(self.data.keys())

    def sum(self):
        pass


class HHYearData:
    def __init__(self, data: dict):
        self.data = data

    def __iter__(self):
        return iter(self.data.keys())

    def __getitem__(self, item):
        return HHMouthData(self.data[item])  # 输入一个月份返回一个月类型

    def mouth_list(self):
        return list(self.data.keys())

    def sum(self):
        pass

    def avg(self):
        pass

    def max(self):
        pass

    def day_num(self):
        pass


class HHMouthData:
    def __init__(self, data: dict):
        self.data = data

    def __iter__(self):
        return iter(self.data.keys())

    def __getitem__(self, item):
        return self.data[item]  # 输入一个日期返回一个日期的值

    def day_list(self):
        return list(self.data.keys())

    def sum(self):
        sum_data = 0
        for value in list(self.data.values()):
            sum_data = sum_data + float(value)
        return sum_data

    def avg(self):
        pass

    def max(self):
        pass

    def day_num(self):
        return len(self.data.keys())



if __name__ == '__main__':
    excel = openpyxl.load_workbook('source_data_蒸发.xlsx')
    print('h')
    print(excel.sheetnames)
    table = excel[excel.sheetnames[0]]
    all_data = {}
    year_data = {}
    mouth_data = {}
    for row in range(table.max_row):
        year = table.cell(row+1,2).value
        mouth = table.cell(row+1,3).value
        day = table.cell(row+1,4).value
        value = table.cell(row+1,5).value
        if row < table.max_row-2:
            pass
