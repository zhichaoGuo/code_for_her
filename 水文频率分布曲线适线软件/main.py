# -*- coding: UTF-8 -*-
import os

import xlrd
import xlwt
from pywinauto import Application


def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。
    print(f'Hi, {name}')  # 按 Ctrl+F8 切换断点。
    # 设置应用所在位置
    app_path = 'G:\\CurveFitting\\CurveFitting.exe'
    # 设置数据文件所在位置
    file_path = 'G:\\CurveFitting\\Sample1.txt'
    # 55个参数表单
    input_file_path = 'G:\\CurveFitting\\value_input.xls'
    # 实例化应用
    app = Application(backend="uia").start(app_path)
    # 定位窗口页面
    win_page = app.window(title='水文频率分布曲线适线软件（教学版）')
    win_page.print_control_identifiers()
    # 点击获取数据
    win_page['Button11'].click()
    # 切换窗口
    open_file_windows = app.window(title='打开')
    # 输入文件名
    open_file_windows['文件名(N):Edit'].type_keys(file_path)
    # 点击确定
    open_file_windows['打开(O)'].click()
    # 切换页面
    win_page = app.window(title='水文频率分布曲线适线软件（教学版） - 连续系列')
    # 点击参数估计
    win_page['参数估计'].click()
    # 点击绘制曲线
    win_page['绘制曲线'].click()
    # 点击反查
    win_page['CheckBox2'].click()
    # 打开55个参数文件
    input_file = xlrd.open_workbook(input_file_path)
    # 选定sheet1表
    input_sheet = input_file.sheet_by_name('Sheet1')
    # 创建输出文件并规定字符集编码
    output_file = xlwt.Workbook(encoding='utf-8')
    # 创建输出文件工作sheet
    output_sheet = output_file.add_sheet('My Worksheet')
    # 开始循环
    for line in range(55):
        # 输出计数
        print(line)
        # 取得输入设计值
        input_value = int(input_sheet.cell_value(line, 0))
        # 输入设计值
        win_page['Edit6'].type_keys(input_value)
        # 点击立即查询
        win_page['立即查询'].click()
        # 获取设计频率
        output_value = win_page['Edit7'].legacy_properties()['Value']
        # 存对应数据
        output_sheet.write(line, 0, label=input_value)
        output_sheet.write(line, 1, label=output_value)
    # 保存输出文件
    output_file.save(f"{os.path.abspath('.')}\\value_output.xls")


if __name__ == '__main__':
    print_hi('PyCharm')