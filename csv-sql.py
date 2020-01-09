import csv

CSV_FILE = 'd:\\20191226.csv'
SQL_FILE = 'd:\\20191216.sql'

COUNT = 0
UPDATE_STATEMENT = 'update [joyokids].[dbo].[书籍资料] set'
SET_STATEMENT = ''
with open(SQL_FILE, 'w', encoding='utf-8') as WRITE_FILE:
    with open(CSV_FILE, encoding='utf-8') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            COUNT += 1
            WHERE_STATEMENT = ' where [书籍编号] = \'' + row[4].strip() + '\''
            #SET_STATEMENT += ' [标准ISBN] =\'' + row[7].strip() + '\','
            #SET_STATEMENT += ' [作者信息] =\'' + row[8].strip().replace('\'', '\'\'') + '\','
            #if not row[13]:
            #    SET_STATEMENT += ' [书籍价格] = 0.00,'
            #else:
            #    SET_STATEMENT += ' [书籍价格] = ' + row[13].strip() + ','
            #SET_STATEMENT += ' [出版社名] =\'' + row[16].strip().replace('\'', '\'\'') + '\','
            #SET_STATEMENT += ' [出版地点] =\'' + row[17].strip() + '\','
            #SET_STATEMENT += ' [书籍页码] =\'' + row[19].strip() + '\','
            #SET_STATEMENT += ' [存放位置] =\'' + row[20].strip() + '\','
            #SET_STATEMENT += ' [书籍开本] =\'' + row[21].strip() + '\','
            #SET_STATEMENT += ' [所属语种] =\'' + row[22].strip() + '\','
            #SET_STATEMENT += ' [所属丛书] =\'' + row[25].strip().replace('\'', '\'\'') + '\','
            #SET_STATEMENT += ' [印刷版面] =\'' + row[26].strip() + '\','
            #SET_STATEMENT += ' [备注信息] =\'' + row[29].strip() + '\','
            #SET_STATEMENT += ' [内容简介] =\'' + row[30].strip().replace('\'', '\'\'') + '\','
            #SET_STATEMENT += ' [类型] =\'' + row[31].strip().replace('\'', '\'\'') + '\','
            #SET_STATEMENT += ' [年龄] =\'' + row[32].strip() + '\','
            #SET_STATEMENT += ' [主题] =\'' + row[33].strip().replace('\'', '\'\'') + '\','
            SET_STATEMENT += ' [BL] =\'' + row[36].strip() + '\''
            #SET_STATEMENT += ' [书籍名称] = [书籍名称] + \' (' + row[33].strip().replace('\'', '\'\'') + ')\''
            # print(UPDATE_STATEMENT + SET_STATEMENT + WHERE_STATEMENT)
            
            WRITE_FILE.write(UPDATE_STATEMENT + SET_STATEMENT + WHERE_STATEMENT + "\r\n")
            SET_STATEMENT = ''
print(COUNT)
