import pymysql

from config import host, user, password, db_name

try:
    connection = pymysql.connect(
        host=host,
        port=3307,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    print("successfully connected...")
    print("#" * 20)

    try:
        cursor = connection.cursor()
        with connection.cursor() as cursor:
            insert_query = "INSERT INTO `equipment` (typ_eq,model,ser_number,model,cnc_typ) VALUES ('токарный', 'VT27GLMC1000', '8332202001', 'Fanuc0iTF(IHMI)');"
            cursor.execute(insert_query)
            connection.commit()  # чтобы данные сохранились в базе нужно закоммитить их

        # with connection.cursor() as cursor:
        #     cursor.execute("SELECT * FROM `equipment`")
        #     rows = cursor.fetchall()
        #     for row in rows:
        #         print(row)
        #         print("#" * 20)

    finally:
        connection.close()

except Exception as ex:
    print("connection refused...")
    print(ex)
