import os
import pandas as pd

# 1. 整合和转换原始数据
def process_raw_data(folder_path, type, output_folder):
    files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
    dfs = []

    for file in files:
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path)
        dfs.append(df)

    df = pd.concat(dfs, ignore_index=True)

    # 读取文件，按时间合并并去重
    df = df.drop_duplicates(subset='Gmt time')

    # 将 'Gmt time' 转换为 "%d.%m.%Y %H:%M:%S.%f" 的表达格式
    df['Gmt time'] = pd.to_datetime(df['Gmt time'], format="%d.%m.%Y %H:%M:%S.%f", errors='coerce')

    # 将 'Gmt time' 列设置为索引
    df.set_index('Gmt time', inplace=True)

    # 进行时区转换
    df.index = df.index.tz_localize('UTC').tz_convert('Asia/Shanghai')

    # 删除bid<=0或ask<=0的数据
    df = df[(df['Close'] > 0)]

    # 输出格式
    output_format = '%Y%m%d'

    # 开始与结束的时间
    starttime = df.index.min().strftime(output_format)
    endtime = df.index.max().strftime(output_format)

    # 处理格式
    process_format = '%Y%m%d%H%M00'
    df.index = df.index.strftime(process_format)

    # 更改索引列的名字
    df = df.rename_axis('datetimes')

    # 选择要导出的列
    selected_column = df[['Close']]

    # 重命名列，将其名字设为 'new_column_name'
    if type == 'ASK':
        type1 = 'ask'
    else:
        type1 = 'bid'
    selected_column = selected_column.rename(columns={'Close': f"{type1}Close"})

    # 输出结果到CSV文件
    selected_column.to_csv(output_folder + rf"\USDCNH_{starttime}_{endtime}_{type}_raw.csv", index=True)
