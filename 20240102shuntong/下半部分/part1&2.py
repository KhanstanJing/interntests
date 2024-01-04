from __future__ import print_function, absolute_import

import pandas as pd
from gm.api import *

set_token('c2fddade98204fb7b6e3d077da6c265b63133627')

# output1是保存的原始下载文件，output2是保存的处理后文件
output1 = './CUSHFEoriginal'
output2 = './CUSHFE1&2'

def get_data(para, output1, output2):
    # 下载文件
    history_data = history(symbol=f'SHFE.cu{para}', frequency='900s', start_time='2023-07-07', end_time='2024-01-02', adjust= ADJUST_NONE, df=True)

    # 导出保存原文件
    history_data.to_csv(output1 + f'/{para}.csv', index=False)

    # 新建合约到期月
    history_data['contractmonth'] = para

    # 修改开始时间列的名字
    history_data.rename(columns={'bob': 'datetime'}, inplace=True)

    # 选择要导出的列
    selected_columns = ['datetime', 'contractmonth', 'open', 'high', 'low', 'close', 'volume']
    selected_df = history_data[selected_columns]

    # 导出到 CSV 文件
    selected_df.to_csv(output2 + f'/{para}.csv', index=False)

get_data(2307, output1, output2)

get_data(2308, output1, output2)

get_data(2309, output1, output2)

get_data(2310, output1, output2)

get_data(2311, output1, output2)

get_data(2312, output1, output2)

get_data(2401, output1, output2)

get_data(2402, output1, output2)

get_data(2403, output1, output2)


