import pandas as pd
from part1 import process_raw_data
from part2 import match_bid_ask
from part3 import calculate_spread_statistics

# 时间：0930-1000, 1330-1500, 1530-1600, 1630-1830

# 原始数据所在文件夹
ASK_path = r'./ASK'
BID_path = r'./BID'

# 输出数据所在文件夹
outputs = r'./outputs'

# part1
process_raw_data(ASK_path, 'ASK', outputs)
process_raw_data(BID_path, 'BID', outputs)

# part1_outputs_path
ask_path = r'./outputs/USDCNH_20200101_20230715_ASK_raw.csv'
bid_path = r'./outputs/USDCNH_20200101_20230715_BID_raw.csv'

# part2
match_bid_ask(ask_path, bid_path, outputs)

# part2_outputs_path
match_path = r'./outputs/USDCNH_20200101_20230715.csv'

# part3
calculate_spread_statistics(match_path, outputs)

# part3_outputs_path
final_path = './outputs/USDCNH_spreadmeanmedian.csv'

