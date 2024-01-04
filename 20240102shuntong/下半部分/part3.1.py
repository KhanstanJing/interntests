import pandas as pd

folder_in = './CUSHFE1&2'
folder_out = './CUSHFE3-1'
# 3.1
# 调整机器误差
def operation1(value):
    tick = 10
    value = round(value / tick) * tick
    return value

# 处理文件
def operation2(para):
    df = pd.read_csv(folder_in + f'./{para}.csv')
    sc = ['open', 'close', 'high', 'low']
    df[sc].apply(operation1)
    df.to_csv(folder_out + f'./{para}.csv')


operation2(2307)

operation2(2308)

operation2(2309)

operation2(2310)

operation2(2311)

operation2(2312)

operation2(2401)

operation2(2402)

operation2(2403)

