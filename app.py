from flask import Flask, render_template, request, jsonify, make_response
import pymysql

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/category/<type>')
def category(type):
    type_dict={'cafe':'음식점', 'conbini':'편의점', 'shop':'마트', 'clothes':'의류', 'pharmacy':'약국', 'hospital':'병원', 'bookshop':'서점'}
    conn = pymysql.connect(host='localhost', user='root', password='-----PASSWORD-----', db='covid19')
    latitude = request.cookies.get('latitude')
    longitude = request.cookies.get('longitude')
    try:
        with conn.cursor() as cursor:
            if type == 'cafe':
                sql = "SELECT *, (6371*acos(cos(radians({0}))*cos(radians(latitude))*cos(radians(longitude)-radians({1}))+sin(radians({2}))*sin(radians(latitude)))) AS distance FROM store_list WHERE sector LIKE '일반휴게음식%' HAVING distance <= 1 ORDER BY distance"
            elif type == 'conbini':
                sql = "SELECT *, (6371*acos(cos(radians({0}))*cos(radians(latitude))*cos(radians(longitude)-radians({1}))+sin(radians({2}))*sin(radians(latitude)))) AS distance FROM store_list WHERE sector = '유통업 영리 - 편 의 점' HAVING distance <= 1 ORDER BY distance"
            elif type == 'shop':
                sql = "SELECT *, (6371*acos(cos(radians({0}))*cos(radians(latitude))*cos(radians(longitude)-radians({1}))+sin(radians({2}))*sin(radians(latitude)))) AS distance FROM store_list WHERE sector = '유통업 영리 - 슈퍼마켓' or sector = '유통업 비영리 - 농,축협 직영매장' HAVING distance <= 1 ORDER BY distance"
            elif type == 'clothes':
                sql = "SELECT *, (6371*acos(cos(radians({0}))*cos(radians(latitude))*cos(radians(longitude)-radians({1}))+sin(radians({2}))*sin(radians(latitude)))) AS distance FROM store_list WHERE sector LIKE '의류%' HAVING distance <= 1 ORDER BY distance"
            elif type == 'pharmacy':
                sql = "SELECT *, (6371*acos(cos(radians({0}))*cos(radians(latitude))*cos(radians(longitude)-radians({1}))+sin(radians({2}))*sin(radians(latitude)))) AS distance FROM store_list WHERE sector = '약국 - 약국' HAVING distance <= 1 ORDER BY distance"
            elif type == 'hospital':
                sql = "SELECT *, (6371*acos(cos(radians({0}))*cos(radians(latitude))*cos(radians(longitude)-radians({1}))+sin(radians({2}))*sin(radians(latitude)))) AS distance FROM store_list WHERE sector LIKE '%병원%' AND sector NOT LIKE '%동물병원' AND sector NOT LIKE '%약국' or sector LIKE '%의원%' HAVING distance <= 1 ORDER BY distance"
            elif type == 'bookshop':
                sql = "SELECT *, (6371*acos(cos(radians({0}))*cos(radians(latitude))*cos(radians(longitude)-radians({1}))+sin(radians({2}))*sin(radians(latitude)))) AS distance FROM store_list WHERE name LIKE '%서점%' or name LIKE '%문고' HAVING distance <= 1 ORDER BY distance"
            cursor.execute(sql.format(latitude, longitude, latitude))
            data = cursor.fetchall()
    finally:
        conn.close()
    return render_template('category.html', data=data, category=type_dict[type], latitude=latitude, longitude=longitude)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        conn = pymysql.connect(host='localhost', user='root', password='-----PASSWORD-----', db='covid19')
        latitude = request.cookies.get('latitude')
        longitude = request.cookies.get('longitude')
        search = request.form['search']
        try:
            with conn.cursor() as cursor:
                sql = "SELECT *, (6371*acos(cos(radians({0}))*cos(radians(latitude))*cos(radians(longitude)-radians({1}))+sin(radians({2}))*sin(radians(latitude)))) AS distance FROM store_list WHERE name like '%{3}%' ORDER BY distance LIMIT 25"
                cursor.execute(sql.format(latitude, longitude, latitude, search))
                data = cursor.fetchall()
        finally:
            conn.close()
        return render_template('search.html', data=data, search=search, latitude=latitude, longitude=longitude)
    return render_template('search.html')

@app.route('/api', methods=['POST'])
def api():
    if request.method == 'POST':
        data = {}
        conn = pymysql.connect(host='localhost', user='root', password='-----PASSWORD-----', db='covid19')
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        try:
            with conn.cursor() as cursor:
                cafe_sql = "SELECT *, (6371*acos(cos(radians({0}))*cos(radians(latitude))*cos(radians(longitude)-radians({1}))+sin(radians({2}))*sin(radians(latitude)))) AS distance FROM store_list WHERE sector LIKE '일반휴게음식%' HAVING distance <= 1 ORDER BY distance"
                cursor.execute(cafe_sql.format(latitude, longitude, latitude))
                cafe_len = len(cursor.fetchall())

                conbini_sql = "SELECT *, (6371*acos(cos(radians({0}))*cos(radians(latitude))*cos(radians(longitude)-radians({1}))+sin(radians({2}))*sin(radians(latitude)))) AS distance FROM store_list WHERE sector = '유통업 영리 - 편 의 점' HAVING distance <= 1 ORDER BY distance"
                cursor.execute(conbini_sql.format(latitude, longitude, latitude))
                conbini_len = len(cursor.fetchall())

                shop_sql = "SELECT *, (6371*acos(cos(radians({0}))*cos(radians(latitude))*cos(radians(longitude)-radians({1}))+sin(radians({2}))*sin(radians(latitude)))) AS distance FROM store_list WHERE sector = '유통업 영리 - 슈퍼마켓' or sector = '유통업 비영리 - 농,축협 직영매장' HAVING distance <= 1 ORDER BY distance"
                cursor.execute(shop_sql.format(latitude, longitude, latitude))
                shop_len = len(cursor.fetchall())

                clothes_sql = "SELECT *, (6371*acos(cos(radians({0}))*cos(radians(latitude))*cos(radians(longitude)-radians({1}))+sin(radians({2}))*sin(radians(latitude)))) AS distance FROM store_list WHERE sector LIKE '의류%' HAVING distance <= 1 ORDER BY distance"
                cursor.execute(clothes_sql.format(latitude, longitude, latitude))
                clothes_len = len(cursor.fetchall())

                pharmacy_sql = "SELECT *, (6371*acos(cos(radians({0}))*cos(radians(latitude))*cos(radians(longitude)-radians({1}))+sin(radians({2}))*sin(radians(latitude)))) AS distance FROM store_list WHERE sector = '약국 - 약국' HAVING distance <= 1 ORDER BY distance"
                cursor.execute(pharmacy_sql.format(latitude, longitude, latitude))
                pharmacy_len = len(cursor.fetchall())

                hospital_sql = "SELECT *, (6371*acos(cos(radians({0}))*cos(radians(latitude))*cos(radians(longitude)-radians({1}))+sin(radians({2}))*sin(radians(latitude)))) AS distance FROM store_list WHERE sector LIKE '%병원%' AND sector NOT LIKE '%동물병원' AND sector NOT LIKE '%약국' or sector LIKE '%의원%' HAVING distance <= 1 ORDER BY distance"
                cursor.execute(hospital_sql.format(latitude, longitude, latitude))
                hospital_len = len(cursor.fetchall())

                bookshop_sql = "SELECT *, (6371*acos(cos(radians({0}))*cos(radians(latitude))*cos(radians(longitude)-radians({1}))+sin(radians({2}))*sin(radians(latitude)))) AS distance FROM store_list WHERE name LIKE '%서점%' or name LIKE '%문고' HAVING distance <= 1 ORDER BY distance"
                cursor.execute(bookshop_sql.format(latitude, longitude, latitude))
                bookshop_len = len(cursor.fetchall())
        finally:
            conn.close()

        data['cafe'] = cafe_len
        data['conbini'] = conbini_len
        data['shop'] = shop_len
        data['clothes'] = clothes_len
        data['pharmacy'] = pharmacy_len
        data['hospital'] = hospital_len
        data['bookshop'] = bookshop_len
        return jsonify(data)
    return render_template('Only POST')

@app.route('/setcookie', methods=['POST'])
def setcookie():
    if request.method == 'POST':
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        response = make_response("Cookie Success!")
        response.set_cookie('latitude', latitude)
        response.set_cookie('longitude', longitude)
        return response
    return render_template('Only POST')