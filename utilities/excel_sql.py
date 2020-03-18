# pylint: disable=missing-docstring
import pandas as pd

EXCEL_FILE = 'd:\\20200311.xlsx'
SQL_FILE = 'd:\\20200311.sql'

COUNT = 0
UPDATE_STATEMENT = 'update [joyokids].[dbo].[书籍资料] set'
SET_STATEMENT = ''
with open(SQL_FILE, 'w', encoding='utf-8') as WRITE_FILE:
    # read excel file
    DF = pd.read_excel(EXCEL_FILE, encoding='utf-8-sig', converters={"书籍编号": str})
    DATA = {}
    for header in DF.columns:
        for i in DF.index:
            strValue = str(DF[header][i]).strip()
            if strValue == 'nan':
                strValue = ''
            try:
                DATA[header].append(strValue)
            except KeyError:
                DATA[header] = [strValue]

    #convert
    for i in range(len(DATA["书籍编号"])):
        COUNT += 1
        WHERE_STATEMENT = ' where [书籍编号] = \'' + DATA["书籍编号"][i].zfill(6) + '\''
        SET_STATEMENT += ' [标准isbn] =\'' + DATA["标准isbn"][i] + '\','
        SET_STATEMENT += ' [作者信息] =\'' + DATA["作者信息"][i].replace('\'', '\'\'') + '\','
        if not DATA["书籍价格"][i]:
            SET_STATEMENT += ' [书籍价格] = 0.00,'
        else:
            SET_STATEMENT += ' [书籍价格] = ' + DATA["书籍价格"][i] + ','
        SET_STATEMENT += ' [出版社名] =\'' + DATA["出版社名"][i].replace('\'', '\'\'') + '\','
        SET_STATEMENT += ' [出版地点] =\'' + DATA["出版地点"][i] + '\','
        SET_STATEMENT += ' [书籍页码] =\'' + DATA["书籍页码"][i] + '\','
        # SET_STATEMENT += ' [存放位置] =\'' + DATA["存放位置"][i] + '\','
        # SET_STATEMENT += ' [书籍开本] =\'' + DATA["书籍开本"][i] + '\','
        SET_STATEMENT += ' [所属语种] =\'' + DATA["所属语种"][i] + '\','
        SET_STATEMENT += ' [所属丛书] =\'' + DATA["所属丛书"][i].replace('\'', '\'\'') + '\','
        SET_STATEMENT += ' [印刷版面] =\'' + DATA["印刷版面"][i] + '\','
        SET_STATEMENT += ' [备注信息] =\'' + DATA["备注信息"][i] + '\','
        SET_STATEMENT += ' [内容简介] =\'' + DATA["内容简介"][i].replace('\'', '\'\'') + '\','
        SET_STATEMENT += ' [类型] =\'' + DATA["类型"][i].replace('\'', '\'\'') + '\','
        SET_STATEMENT += ' [年龄] =\'' + DATA["年龄"][i] + '\','
        SET_STATEMENT += ' [主题] =\'' + DATA["主题"][i].replace('\'', '\'\'') + '\','
        SET_STATEMENT += ' [BL] =\'' + DATA["BL"][i] + '\','
        SET_STATEMENT += ' [书籍名称] = \'' + DATA["书籍名称"][i].replace('\'', '\'\'') + '\''
        # print(UPDATE_STATEMENT + SET_STATEMENT + WHERE_STATEMENT)

        WRITE_FILE.write(UPDATE_STATEMENT + SET_STATEMENT + WHERE_STATEMENT + "\r\n")
        SET_STATEMENT = ''
print(COUNT)
