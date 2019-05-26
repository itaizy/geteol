# -*- Encoding: UTF-8 -*-
from urllib import request
from urllib.parse import urlencode  #Python内置的HTTP请求库
import json
import sqlite3

def get_page(offset):
    params = {
        'local_province_id':'13',
        'province_id': '11',
        'local_type_id':'2',
        'year':'2018',
        'page':'2',
        'size':'10',
        '_' : '1558512524231',
    }
    url = 'https://api.eol.cn/web/api?uri=hxsjkqt/api/gk/score/school'+ urlencode(params)  #拼接URL
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()  # 返回json格式的响应内容
    except:
        return None

if __name__ == '__main__':
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



    user_agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Mobile Safari/537.36'
    headers = { 'User-Agent' : user_agent}

    for i in [11,12,13,14,15,21,22,23,31,32,33,34,35,36,37,41,42,43,44,45,46,50,51,52,53,54,61,62,63,64,65]:
        print(i)
        province_id = i;
        item_data_len = 1;
        npage = 0;
        while (item_data_len):
            npage = npage + 1;
            url = "https://api.eol.cn/web/api?uri=hxsjkqt/api/gk/score/school&callback=jQuery1830722843089595979_1558508940996&local_province_id=13&province_id="+ str(province_id) + "&local_type_id=2&year=2018&page="+ str(npage) +"&size=10&_=1558509020786";
            req = request.Request(url, headers=headers)
            response = request.urlopen(req)
            page = response.read()
            page = page.decode('utf-8').split('(')[1][:-1]
            dpage = json.loads(page)
            item_data_len = len(dpage['data']['item'])
            tmp = dpage['data']['item']
            conn = sqlite3.connect('gk.db')
            cursor = conn.cursor()
            for inode in tmp:
                print(inode['id']),
                print(inode['all'])
                curson = conn.execute("select * from school where id = '" + inode['id'] +"'")
                conn.commit()
                rows = curson.fetchall()
                if (len(rows) >= 1):
                    break;
        #        sqlstr = 'insert into school values('+ inode['id'] +','+ inode['name'] +','+ str(inode['province_id']) +','+ str(inode['local_type_id']) +','+ str(inode['year']) +','+ str(inode['local_province_id']) +','+ str(inode['school_id']) +','+ str(inode['all']) +')';
                cursor.execute('insert into school values(?,?,?,?,?,?,?,?)', (inode['id'], inode['name'], str(inode['province_id']), str(inode['local_type_id']), str(inode['year']), str(inode['local_province_id']), str(inode['school_id']), str(inode['all'])));
                conn.commit()
        #        break;
        #        print(sqlstr)
        #        cursor.execute(sqlstr)
            conn.close()
        #    conn.close()
            

