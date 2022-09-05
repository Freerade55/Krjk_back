
import base64

from flask import request, Flask, send_file, jsonify, g, render_template, redirect, make_response, url_for, abort, send_from_directory, flash
from flask_cors import CORS
import psycopg2
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)





def connect_db():
    return psycopg2.connect(
        host="localhost",
        user="postgres",
        password="55555",
        database="Controller",
        port="5432"
    )


def get_db():
    '''Opens a new database connection per request.'''
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db



@app.teardown_appcontext
def close_db(error):
    '''Closes the database connection at the end of request.'''
    if hasattr(g, 'db'):
        g.db.close()











@app.route('/autorization', methods=['POST'])
def autorization():
    request_data = request.get_json()

    user_request = {
        'loggin': request_data['loggin'],
        'password': request_data['password'],
    }

    cursor = get_db().cursor()
    cursor.execute(
        """SELECT * FROM "users";""")


    rows = cursor.fetchall()
    print(rows)

    for i in rows:
        if user_request['loggin'] == i[1] and user_request['password'] == i[2]:
            print('Авторизация прошла')
            print(os.listdir(path="./"))

            return jsonify({'id':i[0]})


    return jsonify('Неверный логин или пароль')

@app.route('/object_registration', methods=['POST'])
def object_registration():

    request_data = request.get_json()
    user_request = {
        'lico': request_data['lico'],
        'type': request_data['type'],
        'data': request_data['data'],
        'org_name': request_data['org_name'],
        'inn': request_data['inn'],
        'container_owner': request_data['container_owner'],
        'container_col': request_data['container_col'],
        'container_ob': request_data['container_ob'],
        'ed_izm': request_data['ed_izm'],
        'kol_ed_izm': request_data['kol_ed_izm'],
        'phone': request_data['phone'],
        'email': request_data['email'],
        'address': request_data['address'],
        'coord': request_data['coord'],
        'photo_doc': request_data['photo_doc'],
        'photo_obj': request_data['photo_obj'],
        'photo_сont': request_data['photo_сont'],
        'comment': request_data['comment'],
        'comment_voice': request_data['comment_voice']
    }

    print(user_request['coord'])

    for i in user_request:
        if user_request[i] == None:
            user_request[i] = ''


    if user_request['lico'] == 'юр. лицо':

        cursor = get_db().cursor()
        cursor.execute(
            f"""INSERT INTO "Object_add" (lico, org_name, inn, deyat_type, container_owner, container_col, container_ob, ed_izm,
            phone, email, address, coord, comment)
            VALUES ('{user_request['lico']}', '{user_request['org_name']}', '{user_request['inn']}', '{user_request['type']}',
             '{user_request['container_owner']}',
            '{user_request['container_col']}', '{user_request['container_ob']}',
            '{user_request['ed_izm']}', '{user_request['phone']}', '{user_request['email']}', '{user_request['address']}',
            '{user_request['coord']}',
            '{user_request['comment']}');""")
        g.db.commit()

        cursor = get_db().cursor()
        cursor.execute(
            """SELECT MAX(id) FROM "Object_add";""")

        id = cursor.fetchall()
        cursor.close()


        for i in user_request:
            arr = ''
            if i == 'photo_doc':
                if user_request[i]:
                    count = 1
                    if f'''{i}_{id[0][0]}''' not in os.listdir(path="./"):
                        os.mkdir(path=f'''{i}_{id[0][0]}''')

                    for e in user_request[i]:
                        path = f'''{i}_{id[0][0]}''' + '/' + f'''{user_request['data']}''' + ' ' + '' + str(id[0][0]) + \
                               ' ' + f'''{str(count)}''' + '.jpg'
                        count += 1
                        with open(path, 'wb') as save_photo:
                            save_photo.write(base64.b64decode(e))
                            arr += path + ','

                cursor = get_db().cursor()
                cursor.execute(
                    f"""UPDATE "Object_add" SET {i} = '{arr[:-1]}' WHERE id = '{id[0][0]}';""")
                g.db.commit()

            if i == 'photo_obj':
                if user_request[i]:
                    count = 1
                    if f'''{i}_{id[0][0]}''' not in os.listdir(path="./"):
                        os.mkdir(path=f'''{i}_{id[0][0]}''')

                    for e in user_request[i]:
                        path = f'''{i}_{id[0][0]}''' + '/' + f'''{user_request['data']}''' + ' ' + '' + str(id[0][0]) + \
                               ' ' + f'''{str(count)}''' + '.jpg'
                        count += 1
                        with open(path, 'wb') as save_photo:
                            save_photo.write(base64.b64decode(e))
                            arr += path + ','

                cursor = get_db().cursor()
                cursor.execute(
                    f"""UPDATE "Object_add" SET {i} = '{arr[:-1]}' WHERE id = '{id[0][0]}';""")
                g.db.commit()
    print('+++')

    return jsonify()






@app.route('/organization_search', methods=['POST'])
def organization_search():
    request_data = request.get_json()

    keys = list(request_data.keys())


    if keys[0] == 'inn':
        cursor = get_db().cursor()
        cursor.execute(
            f"""SELECT inn, name, deyat_type, address, kontacty, dogovor, stad_zakluch, dogovor_nomer FROM "Object_search" 
            WHERE inn = {request_data['inn']};""")

        rows = cursor.fetchall()
        return jsonify(rows)

    if keys[0] == 'dogovor_nomer':
        cursor = get_db().cursor()
        cursor.execute(
            f"""SELECT inn, name, deyat_type, address, kontacty, dogovor, stad_zakluch, dogovor_nomer FROM "Object_search" 
            WHERE dogovor_nomer = {request_data['dogovor_nomer']};""")

        rows = cursor.fetchall()
        return jsonify(rows)

    if keys[0] == 'name':
        cursor = get_db().cursor()
        cursor.execute(
            f"""SELECT inn, name, deyat_type, address, kontacty, dogovor, stad_zakluch, dogovor_nomer FROM "Object_search" 
            WHERE name = '{request_data['name']}';""")
        rows = cursor.fetchall()

        if len(rows) == 0:
            cursor = get_db().cursor()
            cursor.execute(
                f"""SELECT inn, name, deyat_type, address, kontacty, dogovor, stad_zakluch FROM "Object_search" 
                      WHERE name ~ '[[:<:]]{request_data['name']}[[:>:]]';""")
            rows = cursor.fetchall()
            return jsonify(rows)

        return jsonify(rows)


    if keys[0] == 'address':


        cursor = get_db().cursor()
        cursor.execute(
            f"""SELECT inn, name, deyat_type, address, kontacty, dogovor, stad_zakluch FROM "Object_search" 
                   WHERE address = '{request_data['address']}';""")
        rows = cursor.fetchall()
        return jsonify(rows)


    return jsonify()




@app.route('/admin_enter', methods=['POST'])
def admin_enter():

    request_data = request.get_json()
    print(request_data)
    user_request = {
        'login': request_data['login'],
        'password': request_data['password'],

    }
    cursor = get_db().cursor()
    cursor.execute(
        f"""SELECT login, password FROM "admins";""")
    rows = cursor.fetchall()

    for i in rows:
        if user_request['login'] == i[0] and user_request['password'] == i[1]:
            return jsonify(True)
        else:
            return jsonify(False)





@app.route('/select', methods=['GET'])
def select():


    cursor = get_db().cursor()
    cursor.execute(
        f"""SELECT id, name FROM "users";""")
    rows = cursor.fetchall()

    return jsonify(rows)



@app.route('/getTask', methods=['POST'])
def getTask():
    request_data = request.get_json()

    date = datetime.strptime(request_data['dataZayavki'], "%d.%m.%Y")

    cursor = get_db().cursor()
    cursor.execute(
            f"""INSERT INTO "tasks" (id, object, address, task, contacts, comment, task_initiator, task_status,
            date, srok_ispolnenya, coords, zayavk_nomer)
                    VALUES ('{int(request_data['ispolnitelId'])}', '{request_data['object']}', '{request_data['address']}',
                    '{request_data['zadachi']}', '{request_data['contacts']}',
                    '{request_data['comment']}', '{request_data['initiator']}', False,
                    '{date}','{request_data['srokIspolnenya']}',
                    '{request_data['coords'][0][0]},{request_data['coords'][0][1]}',
                    '{request_data['nomerZayavki']}')""")
    g.db.commit()

    return jsonify()

# @app.route('/TableTasks', methods=['POST'])
# def TableTasks():
#     request_data = request.get_json()
#
#     cursor = get_db().cursor()
#     cursor.execute(
#         f"""SELECT zayavk_nomer, date, name, address, task, contacts, task_initiator, comment, task_status FROM "tasks"
#         INNER JOIN "users"
#         ON tasks.id = users.id
#         WHERE tasks.id = '{request_data}'
#         ;""")
#     rows = cursor.fetchall()
#
#     return jsonify(rows)






@app.route('/infoByData', methods=['POST'])
def infoByData():
    request_data = request.get_json()
    user_request = {
        'data': request_data['data'],
        'id': request_data['id'],

    }
    date = datetime.strptime(request_data['data'], "%d.%m.%Y")

    cursor = get_db().cursor()
    cursor.execute(
        f"""SELECT name, object, address, task, contacts, comment, task_initiator, task_status, date, zayavk_nomer,
         srok_ispolnenya FROM "tasks"
        INNER JOIN "users"
        ON tasks.id = users.id
        WHERE tasks.date = '{date}' AND tasks.id = '{user_request['id']}'
        ;""")
    rows = cursor.fetchall()
    print(rows)

    return jsonify(rows)





if __name__ == '__main__':
    app.run(host='0.0.0.0', port= 5020)















#
#
# app = Flask(__name__)
# CORS(app)
#
#
#
#
# def connect_db():
#     return pymysql.connect(
#     host="mysql104.1gb.ru",
#     user="gb_abon",
#     password="Gk-ApPV78FXZ",
#     database = "gb_abon",
#     cursorclass = pymysql.cursors.DictCursor
#     )
#
#
# def get_db():
#     '''Opens a new database connection per request.'''
#     if not hasattr(g, 'db'):
#         g.db = connect_db()
#     return g.db
#
#
#
# @app.teardown_appcontext
# def close_db(error):
#     '''Closes the database connection at the end of request.'''
#     if hasattr(g, 'db'):
#         g.db.close()
#
#
#
#
#
# @app.route('/autorization', methods=['POST'])
# def autorization():
#
#     request_data = request.get_json()
#
#     user_request = {
#         'user': request_data['user'],
#         'pass': request_data['pass'],
#     }
#
#
#     cursor = get_db().cursor()
#     cursor.execute(
#         """SELECT * FROM users;""")
#     cursor.close()
#     rows = cursor.fetchall()
#
#
#
#     for i in rows:
#         if user_request['user'] == i['user'] and user_request['pass'] == i['pass']:
#             cursor = get_db().cursor()
#             cursor.execute(
#                 """SELECT id_obj, geo, name, addr, inn FROM objects LIMIT 2""") #### потом убрать лимит
#             cursor.close()
#             data = cursor.fetchall()
#             res = [[{n:k[n]} if n != 'geo' else {n:{'долгота':k[n].split(',')[0], 'широта': k[n].split(',')[1]}} for n in k] for k in data]
#
#             return jsonify([i['user'], i['pass']], res)
#
#     return jsonify('Неверный логин или пароль')
#
#
#
#
# @app.route('/check_inn', methods=['POST'])
# def check_inn():
#     request_data = request.get_json()
#     req = {
#         'inn': request_data['inn']
#     }
#
#     cursor = get_db().cursor()
#     cursor.execute(
#         """SELECT INN, name FROM dogovor;""")
#     cursor.close()
#     row = cursor.fetchall()
#
#
#
#     for i in row:
#         if req['inn'] == i['INN']:
#             return jsonify({
#                 'inn': i['INN'],
#                 'name': i['name'],
#                 'status': True
#             })
#
#
#     return jsonify({
#         'status': False
#         })
#
#
#
#
#
#
#
#
# @app.route('/enter_side', methods=['GET'])
# def enter_side():
#     cursor = get_db().cursor()
#     cursor.execute(
#         """SELECT * FROM list;""")
#     cursor.close()
#     rows = cursor.fetchall()
#
#
#     res = []
#     for i in rows:
#         i['type_org'] = i['type_org'].replace('?', '²').split(',')
#         arr = []
#         for e in i['type_org']:
#             arr.append(e.split(':'))
#         res.append({'type_obj': rows[0]['type_obj'].split(','), 'type_org': arr})
#
#
#     return jsonify(res)
#
#
#
#
#
# @app.route('/object_registration', methods=['POST'])
# def object_registration():
#
#     request_data = request.get_json()
#     user_request = {
#         'type': request_data['type'],
#         'name': request_data['name'],
#         'kol_projiv': request_data['kol_projiv'],
#         'response_name': request_data['kol_projiv'],
#         'vid_containera': request_data['vid_containera'],
#         'konteiner_inn': request_data['konteiner_inn'],
#         'vid_dogovora_status':request_data['vid_dogovora_status'],
#         'addr': request_data['addr'],
#         'inn': request_data['inn'],
#         'fio': request_data['fio'],
#         'geo': request_data['geo'],
#         'email': request_data['email'],
#         'phone': request_data['phone'],
#         'photo_doc': request_data['photo_doc'],
#         'photo_obj': request_data['photo_obj'],
#         'geo_device': request_data['geo_device'],
#         'type_org': request_data['type_org'],
#         'znach': request_data['znach'],
#         'ed_izm': request_data['ed_izm'],
#         'comment': request_data['comment'],
#         'data': request_data['data']
#         # 'voice': request_data['voice']
#     }
#
#     for i in user_request:
#         if user_request[i] == None:
#             user_request[i] = ''
#
#     print(user_request)
#     if user_request['type'] == 'юр. лицо':
#         cursor = get_db().cursor()
#         cursor.execute(
#             f"""INSERT INTO objects (type, name, vid_containera, konteiner_inn ,addr, inn, fio, geo, email, phone, geo_device, type_org, znach, ed_izm, comment)
#             VALUES ('{user_request['type']}', '{user_request['name']}', '{user_request['vid_containera']}',
#             '{user_request['konteiner_inn']}', '{user_request['addr']}',
#             '{user_request['inn']}', '{user_request['fio']}', '{user_request['geo']}', '{user_request['email']}',
#             '{user_request['phone']}', '{user_request['geo_device']}', '{user_request['type_org']}', '{user_request['znach']}',
#             '{user_request['ed_izm']}', '{user_request['comment']}');""")
#         g.db.commit()
#
#         cursor = get_db().cursor()
#         cursor.execute(
#             """SELECT MAX(id_obj), name FROM objects;""")
#         cursor.close()
#         id = cursor.fetchall()
#         for i in user_request:
#             arr = ''
#             if i == 'photo_doc' or i == 'photo_obj':
#                 if user_request[i]:
#                     count = 1
#                     for e in user_request[i]:
#                         path = f'''{i}''' + '/' + f'''{user_request['data']}''' + ' ' + '' + str(id[0]['MAX(id_obj)']) + \
#                                ' ' + f'''{str(count)}''' + '.jpg'
#                         count += 1
#                         with open(path, 'wb') as save_photo:
#                             save_photo.write(base64.b64decode(e))
#                             arr += path + ','
#                 cursor = get_db().cursor()
#                 cursor.execute(
#                     f"""UPDATE objects SET {i} = '{arr[:-1]}' WHERE id_obj = '{id[0]['MAX(id_obj)']}';""")
#                 g.db.commit()
#
#             # if i == i['voice']:
#             #     if user_request[i]:
#             #         for e in user_request[i]:
#             #             path = f'''{i}''' + '/' + f'''{user_request['data']}''' + ' ' + str(id[0]['MAX(id_obj)']) + '.mp3'
#             #             with open(path, 'wb') as save_photo:
#             #                 save_photo.write(base64.b64decode(e))
#             #                 arr += path + ','
#             #     cursor = get_db().cursor()
#             #     cursor.execute(
#             #         f"""UPDATE objects SET {i} = '{arr[:-1]}' WHERE id_obj = '{id[0]['MAX(id_obj)']}';""")
#             #     g.db.commit()
#         return jsonify()
#
#     if user_request['type'] == 'частное лицо':
#         cursor = get_db().cursor()
#         cursor.execute(
#             f"""INSERT INTO objects (type, name, kol_projiv, vid_containera, konteiner_inn, vid_dogovora_status, addr, inn, fio, geo, email, phone, geo_device, type_org, znach, ed_izm, comment)
#                     VALUES ('{user_request['type']}', '{user_request['name']}', '{user_request['kol_projiv']}', '{user_request['vid_containera']}',
#                     '{user_request['konteiner_inn']}', '{user_request['vid_dogovora_status']}', '{user_request['addr']}',
#                     '{user_request['inn']}', '{user_request['fio']}', '{user_request['geo']}', '{user_request['email']}',
#                     '{user_request['phone']}', '{user_request['geo_device']}', '{user_request['type_org']}', '{user_request['znach']}',
#                     '{user_request['ed_izm']}', '{user_request['comment']}');""")
#         g.db.commit()
#
#         cursor = get_db().cursor()
#         cursor.execute(
#             """SELECT MAX(id_obj), name FROM objects;""")
#         cursor.close()
#         id = cursor.fetchall()
#         for i in user_request:
#             arr = ''
#             if i == 'photo_doc' or i == 'photo_obj':
#                 if user_request[i]:
#                     count = 1
#                     for e in user_request[i]:
#                         path = f'''{i}''' + '/' + f'''{user_request['data']}''' + ' ' + '' + str(
#                             id[0]['MAX(id_obj)']) + \
#                                ' ' + f'''{str(count)}''' + '.jpg'
#                         count += 1
#                         with open(path, 'wb') as save_photo:
#                             save_photo.write(base64.b64decode(e))
#                             arr += path + ','
#                 cursor = get_db().cursor()
#                 cursor.execute(
#                     f"""UPDATE objects SET {i} = '{arr[:-1]}' WHERE id_obj = '{id[0]['MAX(id_obj)']}';""")
#                 g.db.commit()
#
#             # if i == i['voice']:
#             #     if user_request[i]:
#             #         for e in user_request[i]:
#             #             path = f'''{i}''' + '/' + f'''{user_request['data']}''' + ' ' + str(id[0]['MAX(id_obj)']) + '.mp3'
#             #             with open(path, 'wb') as save_photo:
#             #                 save_photo.write(base64.b64decode(e))
#             #                 arr += path + ','
#             #     cursor = get_db().cursor()
#             #     cursor.execute(
#             #         f"""UPDATE objects SET {i} = '{arr[:-1]}' WHERE id_obj = '{id[0]['MAX(id_obj)']}';""")
#             #     g.db.commit()
#
#         return jsonify()
#
#     if user_request['type'] == 'мкд':
#         cursor = get_db().cursor()
#         cursor.execute(
#             f"""INSERT INTO objects (type, name, kol_projiv, response_name, vid_containera, konteiner_inn, vid_dogovora_status, addr, inn, fio, geo, email, phone, geo_device, type_org, znach, ed_izm, comment)
#                     VALUES ('{user_request['type']}', '{user_request['name']}', '{user_request['kol_projiv']}', '{user_request['response_name']}',
#                     '{user_request['vid_containera']}',
#                     '{user_request['konteiner_inn']}', '{user_request['vid_dogovora_status']}', '{user_request['addr']}',
#                     '{user_request['inn']}', '{user_request['fio']}', '{user_request['geo']}', '{user_request['email']}',
#                     '{user_request['phone']}', '{user_request['geo_device']}', '{user_request['type_org']}', '{user_request['znach']}',
#                     '{user_request['ed_izm']}', '{user_request['comment']}');""")
#         g.db.commit()
#
#         cursor = get_db().cursor()
#         cursor.execute(
#             """SELECT MAX(id_obj), name FROM objects;""")
#         cursor.close()
#         id = cursor.fetchall()
#         for i in user_request:
#             arr = ''
#             if i == 'photo_doc' or i == 'photo_obj':
#                 if user_request[i]:
#                     count = 1
#                     for e in user_request[i]:
#                         path = f'''{i}''' + '/' + f'''{user_request['data']}''' + ' ' + '' + str(
#                             id[0]['MAX(id_obj)']) + \
#                                ' ' + f'''{str(count)}''' + '.jpg'
#                         count += 1
#                         with open(path, 'wb') as save_photo:
#                             save_photo.write(base64.b64decode(e))
#                             arr += path + ','
#                 cursor = get_db().cursor()
#                 cursor.execute(
#                     f"""UPDATE objects SET {i} = '{arr[:-1]}' WHERE id_obj = '{id[0]['MAX(id_obj)']}';""")
#                 g.db.commit()
#
#             # if i == i['voice']:
#             #     if user_request[i]:
#             #         for e in user_request[i]:
#             #             path = f'''{i}''' + '/' + f'''{user_request['data']}''' + ' ' + str(id[0]['MAX(id_obj)']) + '.mp3'
#             #             with open(path, 'wb') as save_photo:
#             #                 save_photo.write(base64.b64decode(e))
#             #                 arr += path + ','
#             #     cursor = get_db().cursor()
#             #     cursor.execute(
#             #         f"""UPDATE objects SET {i} = '{arr[:-1]}' WHERE id_obj = '{id[0]['MAX(id_obj)']}';""")
#             #     g.db.commit()
#
#         return jsonify()
#
#
#
# @app.route('/object_edit', methods=['POST'])
# def object_edit():
#     request_data = request.get_json()
#     user_request = {
#         'id_obj': request_data['id_obj']
#
#     }
#     cursor = get_db().cursor()
#     cursor.execute(
#         f"""SELECT * FROM objects WHERE id_obj = {user_request['id_obj']};""")
#     cursor.close()
#     object = cursor.fetchall()
#
#     for i in object:
#         for e in i:
#             if i[e] and (e == 'photo_doc' or e == 'photo_obj' or e == 'voice'):
#                 i[e] = i[e].split(',')
#                 encode_arr = []
#                 for pict in i[e]:
#                     if pict[pict.index('/') + 1:] in os.listdir('photo_obj'):
#                         with open(pict, 'rb') as imagefile:
#                             encoded_photo = base64.b64encode(imagefile.read())
#                             image_deoce = encoded_photo.decode('utf-8')
#                             encode_arr.append(image_deoce)
#
#                 i[e] = encode_arr
#
#     return jsonify(object)
#
#
#
# @app.route('/test_loader2', methods=['POST'])
# def test_loader2():
#
#
#
#     with open(f'''photo_doc/12.01.2022 11-50 162 2.jpg''', 'rb') as imagefile:
#         encoded_string = str(base64.b64encode(imagefile.read()))
#         print(type(encoded_string))
#
#
#         return jsonify(encoded_string)
# @app.route('/test_geter', methods=['POST'])
# def test_geter():
#     request_data = request.get_json()
#     user_request = {'pict': request_data['pict']}
#     print(user_request)
#
#     for i in user_request['pict']:
#         print(i)
#
#         path = f'''photo_doc/118881.jpg'''
#
#         with open(path, 'wb') as save_photo:
#             save_photo.write(base64.b64decode(i))
#
#
#
#                 # for e in user_request[i]:
#                 #     path = f'''{i}''' + '/' + f'''{user_request['data']}''' + ' ' + '' + str(id[0]['MAX(id_obj)']) + \
#                 #            ' ' + f'''{str(count)}''' + '.jpg'
#                 #     count += 1
#                 #     with open(path, 'wb') as save_photo:
#                 #         save_photo.write(base64.b64decode(e))
#                 #         arr += path + ','
#
#     # imgdata = base64.b64decode(user_request['voice'][0])
#     # filename = 'voice/11.01.2022 148.mp3'
#     # print(type(imgdata))
#     # with open(filename, 'wb') as f:
#     #     f.write(imgdata)
#     #
#     #
#
#     return jsonify()
#
#
#
#
#
# if __name__ == '__main__':
#     app.run(host='0.0.0.0')

