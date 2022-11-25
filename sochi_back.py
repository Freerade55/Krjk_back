
import base64

from flask import request, Flask, jsonify, g
from flask_cors import CORS
import pymysql
import os
from datetime import datetime


app = Flask(__name__)
CORS(app)





def connect_db():
    return pymysql.connect(
    host="server131.hosting.reg.ru",
    user="",
    password="",
    database = "",
    cursorclass=pymysql.cursors.DictCursor

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
        f"""SELECT id, name FROM users;""")
    rows = cursor.fetchall()

    return jsonify(rows)






@app.route('/getTasks', methods=['GET'])
def getTasks():

    now = datetime.now()
    date = datetime.date(now)

    cursor = get_db().cursor()
    cursor.execute(
        f"""SELECT task_id, name, object, address, task, contacts, comment, task_initiator, task_status, date, 
        zayavk_nomer, srok_ispolnenya FROM tasks
        INNER JOIN users
        ON tasks.id = users.id
        WHERE tasks.date = '{date}'
        ORDER BY tasks.task_id
        ;""")
    rows = cursor.fetchall()
    for i in rows:
        i['date'] = i['date'].strftime("%d.%m.%Y")



    return jsonify(rows)








@app.route('/setTask', methods=['POST'])
def setTask():
    request_data = request.get_json()

    date = datetime.strptime(request_data['dataZayavki'], "%d.%m.%Y")

    cursor = get_db().cursor()
    cursor.execute(
            f"""INSERT INTO tasks (id, object, address, task, contacts, comment, task_initiator, task_status,
            date, srok_ispolnenya, coords, zayavk_nomer)
                    VALUES ('{int(request_data['ispolnitelId'])}', '{request_data['object']}', '{request_data['address']}',
                    '{request_data['zadachi']}', '{request_data['contacts']}',
                    '{request_data['comment']}', '{request_data['initiator']}', False,
                    '{date}','{request_data['srokIspolnenya']}',
                    '{request_data['coords'][0][0]},{request_data['coords'][0][1]}',
                    '{request_data['nomerZayavki']}')""")
    g.db.commit()

    return jsonify()





@app.route('/taskUpdate', methods=['POST'])
def taskUpdate():
    request_data = request.get_json()
    print(request_data)
    date = datetime.strptime(request_data['dataZayavki'], "%d.%m.%Y")


    cursor = get_db().cursor()
    cursor.execute(
            f"""UPDATE tasks SET id = '{int(request_data['ispolnitelId'])}', 
            object = '{request_data['object']}', 
            address = '{request_data['address']}', 
            task = '{request_data['zadachi']}', 
            contacts = '{request_data['contacts']}', 
            comment = '{request_data['comment']}', 
            task_initiator = '{request_data['initiator']}', 
            date = '{date}', 
            srok_ispolnenya = '{request_data['srokIspolnenya']}', 
            zayavk_nomer = '{request_data['nomerZayavki']}'
            WHERE task_id = '{int(request_data['bdID'])}'""")
    g.db.commit()

    return jsonify()





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
    app.run()











