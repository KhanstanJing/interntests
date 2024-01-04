import pandas as pd
from openpyxl import load_workbook
# 设置 Pandas 使用 XlsxWriter 引擎
pd.set_option('io.excel.xlsx.writer', 'xlsxwriter')

folder_in = './CUSHFE3-2'
folder_out = './CUSHFE4'

# 定义一个组内排序函数
def sort_group(group):
    return group.sort_values(by='dailyvolume', ascending=False)

# 创建一个样式函数，用于将特定行标记为黄色
def highlight_row(row, index):
    color = 'background-color: yellow'
    if row.name == index:
        return [color] * len(row)
    else:
        return [''] * len(row)

file_names = [r'/2307.csv', r'/2308.csv', r'/2309.csv', r'/2310.csv', r'/2311.csv', r'/2312.csv', r'/2401.csv', r'/2402.csv', r'/2403.csv']

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
dfs.to_csv('./CUSHFE4/final')

# 对 dfs 进行分组并在每个分组内应用排序函数
dfs = dfs.groupby('date', group_keys=False).apply(sort_group)

# 根据 'date' 列分组，然后使用 cumcount() 获取每个分组内的元素序号
dfs['ElementIndex'] = dfs.groupby('date').cumcount()

# 按照 '日期' 列分组，选择每组中成交量最大对应的合约月份, 生成Sheet1
sheet1 = dfs.loc[dfs.groupby('date')['dailyvolume'].idxmax()]
sheet1 = sheet1.drop(columns='ElementIndex')

# 删除包含缺失值的行
sheet1 = sheet1.dropna(subset=['dailyopen'])
sheet1 = sheet1.reset_index(drop=True)
# 生成Sheet2
sheet2 = sheet1.copy()  # 复制Sheet1的数据

# 找到换月日的日期
change_month_dates = sheet1[sheet1['contractmonth'] != sheet1['contractmonth'].shift(-1)]['date']

# 在Sheet2中替换为下个主力合约的当日数据
for date in change_month_dates:
    # 获取下一个主力合约的值
    condition = (dfs['date'] == date) & (dfs['ElementIndex'] == 1)
    next_contract = dfs.loc[condition]

    # 获取要替换的行的索引
    date_to_replace = sheet2[sheet2['date'] == date].index
    sheet2.style.apply(date_to_replace)
    # 使用 loc 方法替换值
    sheet2.loc[date_to_replace, ['contractmonth', 'dailyopen', 'dailyclose', 'dailyhigh', 'dailylow', 'dailyvolume']] = next_contract[['contractmonth', 'dailyopen', 'dailyclose', 'dailyhigh', 'dailylow', 'dailyvolume']].values

# 保存到Excel文件
with pd.ExcelWriter('./CUSHFE4/CU_data.xlsx', engine='xlsxwriter') as writer:
    sheet1.to_excel(writer, sheet_name='Sheet1', index=False)
    sheet2.to_excel(writer, sheet_name='Sheet2', index=False)

    # 获取 ExcelWriter 对象的 workbook 和 worksheet 对象
    workbook = writer.book
    worksheet = writer.sheets['Sheet2']

    # 创建一个样式对象
    yellow_highlight = workbook.add_format({'bg_color': 'yellow'})
    for index in change_month_dates.index:
        worksheet.set_row(index+1, None, yellow_highlight)  # 索引从0开始，所以要加1