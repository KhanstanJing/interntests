import pandas as pd

# 2. 生成完整分钟时间序列并匹配BID和ASK数据
def match_bid_ask(ask_path, bid_path, output_folder):
    # 读取ASK和BID文件
    ask_df = pd.read_csv(ask_path)
    bid_df = pd.read_csv(bid_path)

    # 时间的输出格式
    output_format = '%Y%m%d'

    # 开始与结束的时间
    starttime = str(ask_df['datetimes'].min())
    starttime = pd.to_datetime(starttime).strftime(output_format)
    endtime = str(ask_df['datetimes'].max())
    endtime = pd.to_datetime(endtime).strftime(output_format)

    # 生成完整分钟时间序列
    complete_minutes = pd.date_range(start=starttime, end=endtime, freq='T')
    ask_complete = pd.DataFrame({'datetimes': complete_minutes})
    bid_complete = pd.DataFrame({'datetimes': complete_minutes})

    # 使用merge_asof填充数据
    # 注意这里的format不对的话就会跳到1970默认时间
    ask_df['datetimes'] = pd.to_datetime(ask_df['datetimes'], format='%Y%m%d%H%M00')
    # 最开始使用的是下面的代码
    # ask_result = pd.merge_asof(ask_df, ask_complete, on='datetimes', direction='backward')
    # 主要是没搞懂merge_asof的连接顺序问题，应该将完整的时间序列放在左边，因为其是一个左连接函数
    # 另外之前尝试把完整的时间序列放在左边的时候，开始一小段输出的数据全是NaN，当时以为是函数使用错了，但是打开文件后发现是前八个小时没有数据，因为调整了北京时间
    ask_result = pd.merge_asof(ask_complete, ask_df, on='datetimes', direction='backward')

    bid_df['datetimes'] = pd.to_datetime(bid_df['datetimes'], format='%Y%m%d%H%M00')
    bid_result = pd.merge_asof(bid_df, bid_complete, on='datetimes', direction='backward')

    # 合并BID和ASK
    merged_result = pd.merge_asof(bid_result, ask_result, on='datetimes', direction='backward')

    # 重新命名列
    merged_result = merged_result.rename(columns={'bidClose': 'bid', 'askClose': 'ask'})

    # 更改时间格式
    process_format = '%Y%m%d%H%M00'
    merged_result['datetimes'] = merged_result['datetimes'].dt.strftime(process_format)

    # 输出结果到CSV文件
    merged_result.to_csv(output_folder + rf'\USDCNH_{starttime}_{endtime}.csv', index=False)

