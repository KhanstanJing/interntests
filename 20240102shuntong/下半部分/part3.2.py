import pandas as pd

folder_in = './CUSHFE3-1'
folder_out = './CUSHFE3-2'

def operation1(para):
    df = pd.read_csv(folder_in+ f'./{para}.csv')

    df['datetime'] = pd.to_datetime(df['datetime'])

    df.set_index('datetime', inplace=True)

    # 选择每天的交易时间段（早上09:00:00开始 到 次日半夜02:29:59结束）
    daily_data = df.between_time('09:00:00', '02:29:59')

    # 以每天的起始时间为基准，进行重采样并计算统计量
    daily_data = daily_data.resample('D').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    })

    # 重命名列名
    daily_data.columns = ['dailyopen', 'dailyhigh', 'dailylow', 'dailyclose', 'dailyvolume']

    # 设置合约月份
    daily_data['contractmonth'] = para

    # 将 'datetime' 列的日期格式更改为 'YYYYMMDD'
    daily_data = daily_data.reset_index()
    daily_data['datetime'] = daily_data['datetime'].dt.strftime('%Y%m%d')

    daily_data = daily_data[['datetime', 'contractmonth', 'dailyopen', 'dailyhigh', 'dailylow', 'dailyclose', 'dailyvolume']]

    # 使用 rename 方法给列改名
    daily_data.rename(columns={'datetime': 'date'}, inplace=True)
    daily_data.reset_index()
    daily_data.to_csv(folder_out + f'./{para}.csv', index = None)

operation1(2307)

operation1(2308)

operation1(2309)

operation1(2310)

operation1(2311)

operation1(2312)

operation1(2401)

operation1(2402)

operation1(2403)




