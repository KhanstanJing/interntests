import pandas as pd

# 3. 统计一天内每分钟的平均价差和中值价差
def calculate_spread_statistics(file_path, output_folder):
    df = pd.read_csv(file_path)
    df['datetimes'] = pd.to_datetime(df['datetimes'], format='%Y%m%d%H%M00')

    # 计算价差
    df['spread'] = df['ask'] - df['bid']

    # 提取小时和分钟信息
    df['hour_minute'] = df['datetimes'].dt.strftime('%H%M')

    # 计算每分钟的平均价差和中值价差
    result_df = df.groupby('hour_minute')['spread'].agg(['mean', 'median']).reset_index()

    # 重新命名
    result_df = result_df.rename(columns={'hour_minute': 'times', 'mean': 'spread_mean', 'median': 'spread_median'})

    # 输出结果到文件
    result_df.to_csv(output_folder + '/USDCNH_spreadmeanmedian.csv', index=False)

