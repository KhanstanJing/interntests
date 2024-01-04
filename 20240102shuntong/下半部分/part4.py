import pandas as pd

# 设置 Pandas 使用 XlsxWriter 引擎
pd.set_option('io.excel.xlsx.writer', 'xlsxwriter')

folder_in = './CUSHFE3-2'
folder_out = './CUSHFE4'

file_names = ['/2307.csv', r'/2308.csv', r'/2309.csv', r'/2310.csv', r'/2311.csv', r'/2312.csv', r'/2401.csv', r'/2402.csv', r'/2403.csv']
df1 = pd.read_csv(folder_in + file_names[0])
df2 = pd.read_csv(folder_in + file_names[1])
df3 = pd.read_csv(folder_in + file_names[2])
df4 = pd.read_csv(folder_in + file_names[3])
df5 = pd.read_csv(folder_in + file_names[4])
df6 = pd.read_csv(folder_in + file_names[5])
df7 = pd.read_csv(folder_in + file_names[6])
df8 = pd.read_csv(folder_in + file_names[7])
df9 = pd.read_csv(folder_in + file_names[8])
# 读取每个文件并存储

dfs = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9], ignore_index=True)

# 生成Sheet1
sheet1 = dfs.sort_values(by='dailyvolume', ascending=False)  # 根据成交量降序排序
sheet1 = sheet1.drop_duplicates(subset='date')  # 按日期保留第一个，即每日成交量最高的记录

# 生成Sheet2
sheet2 = sheet1.copy()  # 复制Sheet1的数据

# 找到换月日的日期
change_month_dates = sheet1[sheet1['contractmonth'] != sheet1['contractmonth'].shift(1)]['date'].tolist()

# 在Sheet2中替换为下个主力合约的当日数据
for date in change_month_dates:
    next_contract_row = dfs[(dfs['date'] == date) & (dfs['contractmonth'] != sheet2['contractmonth'].iloc[0])]
    if not next_contract_row.empty:
        sheet2.loc[sheet2['date'] == date, ['dailyopen', 'dailyhigh', 'dailylow', 'dailyclose', 'dailyvolume']] = next_contract_row.iloc[0][['dailyopen', 'dailyhigh', 'dailylow', 'dailyclose', 'dailyvolume']]

# 保存到Excel文件
with pd.ExcelWriter('./CUSHFE4/CU_data.xlsx', engine='xlsxwriter') as writer:
    sheet1.to_excel(writer, sheet_name='Sheet1', index=False)
    sheet2.to_excel(writer, sheet_name='Sheet2', index=False)
