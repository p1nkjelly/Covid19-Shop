import csv, pymysql
data = []

def get_gdata():
    check_duplicate = {}
    with open('gdata.csv', 'r', encoding='EUC-KR', errors='ignore') as f:
        rdr = csv.DictReader(f)
        for line in rdr:
            value_len = len(list(filter(None, list(line.values()))))
            check_list = []
            check_list.append(line['업종명(종목명)'])
            check_list.append(value_len)
            check_list.append(len(data))
            try:
                if check_duplicate[line['상호명']+line['시군명']][1] < check_list[1]:
                    data[check_duplicate[line['상호명']+line['시군명']][2]] = line
                    check_duplicate[line['상호명']+line['시군명']] = check_list


            except:
                check_duplicate[line['상호명']+line['시군명']] = check_list
                data.append(line)
        print(len(data))

def db_insert():
    conn = pymysql.connect(host='localhost', user='root', password='-----PASSWORD-----', db='covid19')
    try:
        for store in data:
            with conn.cursor() as cursor:
                sql = 'INSERT INTO store_list VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ST_GeomFromText(%s))'
                if store['위도'] == '':
                    store['위도'] = '0'
                if store['경도'] == '':
                    store['경도'] = '0'
                cursor.execute(sql, (store['시군명'], store['상호명'], store['업종명(종목명)'], store['소재지도로명주소'], store['소재지지번주소'], store['전화번호'], store['우편번호'], store['위도'], store['경도'], store['데이터기준일자'], 'POINT('+store['위도']+' '+ store['경도']+')'))
            conn.commit()
    finally:
        conn.close()

if __name__ == "__main__":
    get_gdata()
    db_insert()