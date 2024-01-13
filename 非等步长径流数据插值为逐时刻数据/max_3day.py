import pandas as pd
if __name__ == '__main__':
    file_name = ".\\output_file.xlsx"
    output_file = ".\\max_3day_output.xlsx"
    data_dict = pd.read_excel(file_name, sheet_name=None, header=None, usecols=(0, 1, 2, 3, 4),
                              names=['时间', '入库流量', '水位', '库容', '下泄流量'], engine='openpyxl')
    all_result_dict = {}
    for sheet_name in data_dict.keys():
        data = data_dict[sheet_name]
        data.drop(data.head(1).index, inplace=True)
        data.reset_index(drop=True, inplace=True)
        if len(data['下泄流量']) < 72:
            print(f'{sheet_name}-少于72个数据（3天）!')
            continue
        df = data['下泄流量'].rolling(72).sum()
        max_index = df.idxmax()+1
        new_df = data.iloc[max_index-72:max_index,]
        all_result_dict[sheet_name] = new_df
    writer = pd.ExcelWriter(output_file)
    for sheet_name in all_result_dict.keys():
        all_result_dict[sheet_name].to_excel(writer,sheet_name=sheet_name,index=False)
    writer.close()