import pandas as pd
df = pd.DataFrame({'Data' : [10, 20, 30, 40, 50, 60, 70]})

writer = pd.ExcelWriter('D:\quant\pandas_example_1.xlsx', engine = 'xlsxwriter')

df.to_excel(writer, sheet_name = 'Sheet1')

#엑셀에 그래프 추가하기
writer = pd.ExcelWriter('./pandas_example_2.xlsx', engine = 'xlsxwriter')
df.to_excel(writer, sheet_name = 'Sheet1')

workbook = writer.book
worksheet = writer.sheets['Sheet1']

chart = workbook.add_chart({'type' : 'column'})

chart.add_series({'values' : '=Sheet1!$B$2:$B$8',
                'gap' : 100})

chart.set_x_axis({'name' : 'index', 'num_font' : {'rotation' : 45}})
chart.set_y_axis({'name' : 'Value', 'major_gridlines' : {'visible' : True}})

chart.set_legend({'position' : 'none'})

worksheet.insert_chart('D2', chart)

writer.save()

#엑셀 셀 포맷팅

df = pd.DataFrame({'숫자' : [12500, 22500, 62100, 189500, 1500, 45500, 12000],
                    '퍼센트' : [0.1, 0.2, 0.66, .25, .05, .75, .23]})

writer = pd.ExcelWriter("./pandas_example_3.xlsx", engine='xlsxwriter')

df.to_excel(writer, sheet_name = 'Sheet1')

workbook = writer.book
worksheet = writer.sheets['Sheet1']

format1 = workbook.add_format({'num_format' : '#,##0.00'})
format2 = workbook.add_format({'num_format' : '0%'})

worksheet.set_column('B:B', 20, format1)
worksheet.set_column('C:C', 15, format2)

writer.save()

#엑셀의 헤더 부분 포맷팅

writer = pd.ExcelWriter("./pandas_example_4.xlsx", engine = 'xlsxwriter')

df.to_excel(writer, sheet_name = 'Sheet1')

workbook = writer.book
worksheet = writer.sheets['Sheet1']

header_format = workbook.add_format({'size' : 15, 'bold' : True,
                                    'text_wrap' : True, 'valign' : 'top',
                                    'align' : 'center', 'fg_color' : '#D7E4BC',
                                    'border' : 1})
for col_num, value in enumerate(df.columns.values):
    worksheet.write(0, col_num + 1, value, header_format)

format1 = workbook.add_format({'num_format' : '#,##0.00'})
format2 = workbook.add_format({'num_format' : '0%'})

worksheet.set_column('B:B', 20, format1)
worksheet.set_column('C:C', 15, format2)

writer.save()

#다수의 DataFrame을 하나의 엑셀에 저장하기

df1 = pd.DataFrame({'Data' : [11, 12, 13, 14]})
df2 = pd.DataFrame({'Data' : [21, 22, 23, 24]})
df3 = pd.DataFrame({'Data' : [31, 32, 33, 34]})
df4 = pd.DataFrame({'Data' : [41, 42, 43, 44]})

writer = pd.ExcelWriter('./pandas_example_5.xlsx', engine = 'xlsxwriter')

df1.to_excel(writer, sheet_name = 'Sheet1')
df2.to_excel(writer, sheet_name = 'Sheet1', startcol = 3)
df3.to_excel(writer, sheet_name = 'Sheet1', startrow = 6)

df4.to_excel(writer, sheet_name = 'Sheet1', startrow = 7, startcol = 4, header=False, index=False)

writer.save()
