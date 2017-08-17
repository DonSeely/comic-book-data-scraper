import urllib
import re
import urllib.request
from bs4 import BeautifulSoup
import sqlite3

conn = sqlite3.connect('comics.sqlite')
cur = conn.cursor()

# Create table in database
cur.executescript('''
DROP TABLE IF EXISTS Comics;

CREATE TABLE Comics (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    sales_index  INTEGER,
    comic_name   TEXT,
    issue_num    INTEGER,
    price        REAL,
    publisher    TEXT,
    sales_volume INTEGER,
    month        INTEGER,
    year         INTEGER
)
''')

staticurl = 'http://www.comichron.com/monthlycomicssales/'
year = 1996
month = 9

#year = 2002
#month = 8

while year < 2017:
    while month < 13:
        
        records = 0

        except_cont = 0

        month_text = str(month)
        if month < 10:
            month_text = "0" + str(month)
        if year <= 1996 and month <= 8 :
            url = staticurl + "/" + str(year) + "/" + str(year) + "-" + month_text + "Diamond.html"
        else:
            url = staticurl + "/" + str(year) + "/" + str(year) + "-" + month_text + ".html"

#        print(url)

        with urllib.request.urlopen(url) as response:
            html = response.read()

        soup = BeautifulSoup(html, "lxml")

        tags = soup("td")
        counter = 0

        for tag in tags:
            item = str(tag)
            temp_tag = re.findall("([x][l][0-9]+)", item)
            int_data = re.findall(">(.+)<", item)

            try :
                if int_data[0] == "1":
                    index_tag = temp_tag
                    break
                else:
                    counter = counter + 1
            except:
                counter = counter + 1
                continue

        counter = counter + 1
        item = str(tags[counter])
        title_tag = re.findall("([x][l][0-9]+)", item)

        counter = counter + 1
        item = str(tags[counter])
        issue_tag = re.findall("([x][l][0-9]+)", item)
        if month == 11 and year == 1996 :
            issue_tag = "xl70"
            counter = counter - 1
        if month == 4 and year == 2007 :
            issue_tag = "xl69"
            counter = counter - 1
        if month == 5 and year == 2007 :
            issue_tag = "xl69"
            counter = counter - 1


        counter = counter + 1
        item = str(tags[counter])
        cost_tag = re.findall("([x][l][0-9]+)", item)

        counter = counter + 1
        item = str(tags[counter])
        publisher_tag = re.findall("([x][l][0-9]+)", item)

        counter = counter + 1
        item = str(tags[counter])
        count_tag = re.findall("([x][l][0-9]+)", item)

        index_load_tacker = 0

        for tag in tags:
            item = str(tag)
#            print(item)
            item = re.sub("\n"," ",item)
#            print(item)

            temp_class_tag = re.findall("([x][l][0-9]+)", item)
#            if temp_class_tag == index_tag :
            if temp_class_tag == index_tag :
                index_tmp = re.findall(">(.+)<", item)
#                print(index_tmp)
#                test_var = re.findall("<br",index_temp[0
                try:
                    index_load = int(index_tmp[0])
                except:
                    try: 
                        if index_tmp[0] == "<br/> " and year > 2014 and except_cont == 0:
                            except_cont = except_cont + 1
                        elif index_tmp[0] == "<br/> " and year <= 2014 :
                            break
                        elif index_tmp[0] == "<br/> " and year > 2014 and except_cont == 1 :
                            break
                        elif not index_tmp[0] :
                            break
                        else:
                            continue
                    except:
                        if year == 2002 and month == 1 and except_cont == 0:
                            continue
                            except_cont = except_cont + 1
                        elif year == 2002 and month == 8 and except_cont == 0:
                            continue
                            except_cont = except_cont + 1
                        else:
                            break
#                if index_load_tacker > index_load :
#                if index_load is None : 
#                    break
#                else :
#                    index_load_tracker = index_load
            elif temp_class_tag == title_tag :
                title_tmp = re.findall(">(.+)<", item)
                try:
                    title_load = title_tmp[0]
#                    print(title_load)
                    title_load = re.sub("<span(.+);\S>","",title_load)
                    title_load = re.sub("</span>","",title_load)
                    title_load = re.sub("&amp;","&",title_load)
                    next = 1
                except: 
#                    print(item)
#                    print(index_load)
                    continue
            elif temp_class_tag == issue_tag or next == 1:
                issue_tmp = re.findall(">(.+)<", item)
                try:
                    issue_load = issue_tmp[0]
                    next = 0
                except:
                    issue_load = ""
                    next = 0
                    continue
            elif temp_class_tag == cost_tag :
                cost_tmp = re.findall(">\S(.+)<", item)
                try:
                    cost_load = float(cost_tmp[0])
                except:
                    continue
            elif temp_class_tag == publisher_tag :
                publisher_tmp = re.findall(">(.+)<", item)
                try: 
                    publisher_load = publisher_tmp[0]
                except:
                    continue
            elif temp_class_tag == count_tag :
                count_tmp = re.findall(">(.+)<", item)
                try:
                    count_load = count_tmp[0]
                    count_load = re.sub(",","",count_load)
                except:
                    continue

                try:
                    cur.execute('''INSERT INTO Comics
                    (sales_index, comic_name, issue_num, price, publisher, sales_volume, month, year) VALUES ( ?, ?, ?, ?, ?, ?, ?, ? )''', 
                    ( index_load, title_load, issue_load, cost_load, publisher_load, count_load, month, year ) )

                    records = records + 1
                except: continue

#                conn.commit()

            else:
                continue
        conn.commit()
        print("Done with month:", month, "year:", year)
        print("Updated:", records, "records")
        month = month + 1

    month = 1
    year = year + 1
    
    if month == 10 and year == 2016:
        month = 13
        year = 2017
        break

print("That's all folks!")