
#한글 깨짐방지
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')

sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

#코드 시작
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

df1 = pd.read_excel("./DATA/온라인전용펀드_운용사_8월말기준.xls", header = 1)

df1_extract = df1[['운용회사', '펀드명', 'Unnamed: 2', '설정일', '펀드유형', '설정원본', 'NAV']].copy()

df1_extract.loc[df1_extract['운용회사']=="미래에셋자산운용", '운용회사'] = "미래에셋"
df1_extract.loc[df1_extract['운용회사'].str.contains('삼성'), '운용회사'] = "삼성"
df1_extract.loc[df1_extract['운용회사']=="케이비자산운용", '운용회사'] = "KB"
df1_extract.loc[df1_extract['운용회사']=="한국투자신탁운용", '운용회사'] = "한투"
df1_extract.loc[df1_extract['운용회사']=="엔에이치아문디자산운용", '운용회사'] = "NH"
df1_extract.loc[df1_extract['운용회사']=="신영자산운용", '운용회사'] = "신영"

df1_extract_2 = df1_extract.loc[df1_extract['운용회사'].isin(["삼성", "한투", "NH", "KB", "신영", "미래에셋"]), :].copy()

# 백만원 -> 억 단위로 변경

df1_extract_2['NAV'] = df1_extract_2['NAV'].apply(lambda x : x / 100)

df1_extract_2.groupby(['운용회사'])[['NAV']].agg(['sum', 'mean', 'max', 'std'])

df1_graph = df1_extract_2.groupby(['운용회사'])[['NAV']].sum()

df1_graph.reset_index(inplace=True)

writer = pd.ExcelWriter('./RESULT/fund_example.xlsx', engine = 'xlsxwriter')

df1_graph.to_excel(writer, sheet_name = 'Sheet1', index = False)

workbook = writer.book
worksheet = writer.sheets['Sheet1']

chart = workbook.add_chart({'type' : 'column'})

chart.add_series({
    'values' : '=Sheet1!$B$2:$B$7',
    'categories' : '=Sheet1!$A$2:$A$7',
    'gap' : 100
})\

chart.set_x_axis({'name' : '펀드운용사', 'num_font' : {'rotation' : 45}})
chart.set_y_axis({'name' : 'NAV(단위: 억)', 'major_gridlines' : {'visible' : True}})

chart.set_legend({'position' : 'none'})

worksheet.insert_chart('D2', chart)

header_format = workbook.add_format({
    'size' : 10,
    'bold' : True,
    'text_wrap' : True,
    'valign' : 'top',
    'align' : 'center',
    'fg_color' : '#D7E4BC',
    'border' : 1
})

for col_num, value in enumerate(df1_graph.columns.values):
    worksheet.write(0, col_num, value, header_format)

format1=  workbook.add_format({'num_format' : '#, ##0.00' })
format2=  workbook.add_format({'num_format' :  '#, ##0.00'})

worksheet.set_column('A:A', 20, format1)

worksheet.set_column('B:B', 15, format2)

worksheet.write(0, 2, "(단위:억)")
writer.save()

##상품판매 TOP 5

result = df1_extract_2.sort_values(['운용회사', 'NAV'], ascending = False)[['운용회사', '펀드명', 'NAV']]

kb = result[result.운용회사 == 'KB'].head(5)
samsung = result[result.운용회사 == '삼성'].head(5)
nh = result[result.운용회사 == 'NH'].head(5)
mirae = result[result.운용회사 == '미래에셋'].head(5)

writer = pd.ExcelWriter('./RESULT/fund_example2.xlsx', engine = 'xlsxwriter')

df1_graph.to_excel(writer, sheet_name = 'Sheet1', index = False)

workbook = writer.book
worksheet = writer.sheets['Sheet1']

chart = workbook.add_chart({'type' : 'column'})

chart.add_series({
    'values' : '=Sheet1!$B$2:$B$7',
    'categories' : '=Sheet1!$A$2:$A$7',
    'gap' : 100
})\

chart.set_x_axis({'name' : '펀드운용사', 'num_font' : {'rotation' : 45}})
chart.set_y_axis({'name' : 'NAV(단위: 억)', 'major_gridlines' : {'visible' : True}})

chart.set_legend({'position' : 'none'})

worksheet.insert_chart('D2', chart)

header_format = workbook.add_format({
    'size' : 10,
    'bold' : True,
    'text_wrap' : True,
    'valign' : 'top',
    'align' : 'center',
    'fg_color' : '#D7E4BC',
    'border' : 1
})

for col_num, value in enumerate(df1_graph.columns.values):
    worksheet.write(0, col_num, value, header_format)

format1=  workbook.add_format({'num_format' : '#,##0.00' })
format2=  workbook.add_format({'num_format' :  '#,##0.00'})

worksheet.set_column('A:A', 20, format1)

worksheet.set_column('B:B', 15, format2)

worksheet.write(0, 2, "(단위:억)")

kb.to_excel(writer, sheet_name = 'Top 5', index = False)
nh.to_excel(writer, sheet_name = 'Top 5', startrow = 10, index = False)
samsung.to_excel(writer, sheet_name = 'Top 5', startrow = 20, index = False)
mirae.to_excel(writer, sheet_name = 'Top 5', startrow = 30, index = False)

worksheet2 = writer.sheets['Top 5']
worksheet2.set_column('A:A', 20)
worksheet2.set_column('B:B', 55)
worksheet2.set_column('C:C', 20, format1)

writer.save()
