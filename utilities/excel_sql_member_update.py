# pylint: disable=missing-docstring
import pandas as pd

EXCEL_FILE = 'D:\\apps\\liberden\\utilities\\20200303members.xlsx'
SQL_FILE = 'D:\\apps\\liberden\\utilities\\20200303.sql'

COUNT = 0
SELECT_STATEMENT = 'select * from [joyokids].[dbo].[读者资料] where [读者编号] in ('
UPDATE_STATEMENT = 'update [joyokids].[dbo].[读者资料] set'
SET_STATEMENT = ''
with open(SQL_FILE, 'w', encoding='utf-8') as WRITE_FILE:
    # read excel file
    DF = pd.read_excel(EXCEL_FILE, encoding='utf-8-sig')
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
    for i in range(len(DATA["读者编号"])):
        COUNT += 1
        SELECT_STATEMENT += '\'' + DATA["读者编号"][i].zfill(5) + '\', '

        WHERE_STATEMENT = ' where [读者编号] = \'' + DATA["读者编号"][i].zfill(5) + '\''
        # SET_STATEMENT += ' [截止日期] =\'' + DATA["截止日期"][i] + '\', '
        # SET_STATEMENT += ' [备注信息] =\'' + DATA["备注信息"][i] + '\''
        SET_STATEMENT += ' [读者类型] =\'' + DATA["读者类型"][i] + '\', '
        SET_STATEMENT += ' [会费金额] =\'' + DATA["会费金额"][i] + '\''

        WRITE_FILE.write(UPDATE_STATEMENT + SET_STATEMENT + WHERE_STATEMENT + "\r\n")
        SET_STATEMENT = ''

    WRITE_FILE.write(SELECT_STATEMENT + '\'\')')
print(COUNT)
