# -*- Encoding: UTF-8 -*-
from urllib import request
from urllib.parse import urlencode  #Python内置的HTTP请求库
import json
import sqlite3
import urllib
import urllib.parse
import urllib.request
import time

def f_post_data(local_province_id, school_id, local_type_id, n_page, year):
    url = "https://gkcx.eol.cn/gkcx/api"
    post_data = {
        "uri":"hxsjkqt/api/gk/score/special","local_province_id":local_province_id,"school_id":school_id,"local_type_id":local_type_id,"page":n_page,"size":20,"year":year
    }
    # post_data 需要被转码成字节流。
    # 需要使用 urllib.parse.urlencode() 将字典转化为字符串，再使用 bytes() 转为字节流。
    user_agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Mobile Safari/537.36'
    headersdata = { 'User-Agent' : user_agent}
    data = bytes(urllib.parse.urlencode(post_data), encoding='utf8')
    req = request.Request(url, data=data, headers=headersdata)
    response = urllib.request.urlopen(req)
    page = response.read()
    dpage = json.loads(page.decode('utf-8'))
    item_data_len = 0;
#    if dpage['data']['item'] is None:
#        return
#    item_data_len = len(dpage['data']['item'])
    if 'data' in dpage:
        if dpage['data'] is None or isinstance(dpage['data'], str):
            return;
        else:
            item_data_len = len(dpage['data']['item'])
#            item_data_len = len(dpage['data']['item'])

    if item_data_len == 0:
        return
    items = dpage['data']['item']
    f_store_data(items)
    f_post_data(local_province_id, school_id, local_type_id, n_page + 1, year)
#    return page.decode('utf-8')
    time.sleep(1);
    return;

def f_sql_data():
    conn = sqlite3.connect('gk.db')
    cursor = conn.cursor()
    cursor.execute('select province_id, local_province_id, school_id from school');
    res = cursor.fetchall();
    conn.commit()
    conn.close()
    
    #print(res.decode('utf-8'))
    #print(res)
    return res

def f_store_data(items):
    conn = sqlite3.connect('gk.db')
    cursor = conn.cursor()
    for item in items:
        curson = conn.execute("select * from detail where id = '" + item['id'] +"'")
        conn.commit()
        rows = curson.fetchall()
        if (len(rows) >= 1):
            break;
#        print(item)
        for key in item.keys():
            if item[key] == '--':
                item[key] = -1;
        for kn in ['level2_name', 'elective', 'level1_name', 'level3_name', 'local_type_name']:
            if kn in item:
                continue;
            else:
                item[kn] = 'none';
        cursor.execute('insert into detail values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (item['id'], item['level2_name'], str(item['year']), str(item['local_province_id']), str(item['local_type_id']), str(item['min']), str(item['elective']), str(item['school_id']),item['level1_name'],str(item['max']),str(item['special_id']),item['local_province_name'],item['local_batch_name'],item['spname'],str(item['local_batch_id']),item['level3_name'],item['name'],item['local_type_name'],str(item['f211']),str(item['school_type']),str(item['type']),str(item['is_recruitment']),str(item['dual_class']),str(item['level']),str(item['province_id']),str(item['f985']),item['dual_class_name']));
        conn.commit()
    conn.close()

if __name__ == '__main__':
    sList = f_sql_data();
    for one in sList:
        f_post_data(one[1], one[2], 1, 1, 2018);
        f_post_data(one[1], one[2], 2, 1, 2018);
        f_post_data(one[1], one[2], 1, 1, 2017);
        f_post_data(one[1], one[2], 2, 1, 2017);
        f_post_data(one[1], one[2], 1, 1, 2016);
        f_post_data(one[1], one[2], 2, 1, 2016);
        f_post_data(one[1], one[2], 1, 1, 2015);
        f_post_data(one[1], one[2], 2, 1, 2015);
        f_post_data(one[1], one[2], 1, 1, 2014);
        f_post_data(one[1], one[2], 2, 1, 2014);
#    f_post_data(13, 49, 1, 1, 2017);
#    f_sql_data();


#    province_id = 11;
#    page = 2;
#    url3 = "https://api.eol.cn/web/api?uri=hxsjkqt/api/gk/score/school";
#    url = "https://api.eol.cn/web/api?uri=hxsjkqt/api/gk/score/school&callback=jQuery1830722843089595979_1558508940996&local_province_id=13&province_id="+ str(province_id) + "&local_type_id=2&year=2018&page="+ str(page) +"&size=10&_=1558509020786";
#    user_agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Mobile Safari/537.36'
#    headers = { 'User-Agent' : user_agent}
#    req = request.Request(url, headers=headers)
#    response = request.urlopen(req)
#    page = response.read()
#    page = page.decode('utf-8').split('(')[1][:-1]
#    dpage = json.loads(page)
#    #print(page.decode('utf-8'))
#    print(len(dpage['data']['item']))
#    tmp = dpage['data']['item']
#    for inode in tmp:
#        print(inode['all'])
#        conn = sqlite3.connect('gk.db')
#        cursor = conn.cursor()
##        sqlstr = 'insert into school values('+ inode['id'] +','+ inode['name'] +','+ str(inode['province_id']) +','+ str(inode['local_type_id']) +','+ str(inode['year']) +','+ str(inode['local_province_id']) +','+ str(inode['school_id']) +','+ str(inode['all']) +')';
#        cursor.execute('insert into school values(?,?,?,?,?,?,?,?)', (inode['id'], inode['name'], str(inode['province_id']), str(inode['local_type_id']), str(inode['year']), str(inode['local_province_id']), str(inode['school_id']), str(inode['all'])));
#        conn.commit()
##        break;
##        print(sqlstr)
##        cursor.execute(sqlstr)
#    conn.close()
##    conn.close()


#
#    user_agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Mobile Safari/537.36'
#    headers = { 'User-Agent' : user_agent}
#
#    for i in [11,12,13,14,15,21,22,23,31,32,33,34,35,36,37,41,42,43,44,45,46,50,51,52,53,54,61,62,63,64,65]:
#        print(i)
#        province_id = i;
#        item_data_len = 1;
#        npage = 0;
#        while (item_data_len):
#            npage = npage + 1;
#            url = "https://api.eol.cn/web/api?uri=hxsjkqt/api/gk/score/school&callback=jQuery1830722843089595979_1558508940996&local_province_id=13&province_id="+ str(province_id) + "&local_type_id=2&year=2018&page="+ str(npage) +"&size=10&_=1558509020786";
#            req = request.Request(url, headers=headers)
#            response = request.urlopen(req)
#            page = response.read()
#            page = page.decode('utf-8').split('(')[1][:-1]
#            dpage = json.loads(page)
#            item_data_len = len(dpage['data']['item'])
#            tmp = dpage['data']['item']
#            conn = sqlite3.connect('gk.db')
#            cursor = conn.cursor()
#            for inode in tmp:
#                print(inode['id']),
#                print(inode['all'])
#                curson = conn.execute("select * from school where id = '" + inode['id'] +"'")
#                conn.commit()
#                rows = curson.fetchall()
#                if (len(rows) >= 1):
#                    break;
#        #        sqlstr = 'insert into school values('+ inode['id'] +','+ inode['name'] +','+ str(inode['province_id']) +','+ str(inode['local_type_id']) +','+ str(inode['year']) +','+ str(inode['local_province_id']) +','+ str(inode['school_id']) +','+ str(inode['all']) +')';
#                cursor.execute('insert into school values(?,?,?,?,?,?,?,?)', (inode['id'], inode['name'], str(inode['province_id']), str(inode['local_type_id']), str(inode['year']), str(inode['local_province_id']), str(inode['school_id']), str(inode['all'])));
#                conn.commit()
#        #        break;
#        #        print(sqlstr)
#        #        cursor.execute(sqlstr)
#            conn.close()
#        #    conn.close()
#            
#
