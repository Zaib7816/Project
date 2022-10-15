
import mysql.connector
from django.shortcuts import render

con = mysql.connector.connect(

    host="localhost",
    user="root",
    passwd="",
    database="rs"
)
db = con.cursor()


def insert(name, email, password, confirm_password, city, role):
    name = name
    email = email
    password = password
    confirm_password = confirm_password
    city = city
    role = role

    db.execute("INSERT INTO students (name, email, password, confirm_password, city, role) VALUES ('" +
               name+"', '"+email+"','"+password+"','"+confirm_password+"' , '"+city+"' , '"+role+"')")
    con.commit()
    print("Data inserted")
    return True


def login_funtion(email, password):
    email = email
    password = password
    db.execute("SELECT * FROM students WHERE email = '" +
               email+"' AND password = '"+password+"'")
    login_data = db.fetchall()
    if len(login_data):
        return login_data
    else:
        return False


def students_data():
    db.execute("SELECT * FROM students")
    students_data = db.fetchall()
    return students_data


def admin_data():
    db.execute("SELECT * FROM students WHERE role = 'admin'")
    admin_data = db.fetchall()
    return admin_data


def update_admin(id, name, email, city):
    id = id
    name = name
    email = email

    city = city
    db.execute("UPDATE students SET name = '"+name+"', email = '" +
               email+"', city = '"+city+"' WHERE id = '"+id+"'")
    con.commit()
    return True


def update_user(id, name, email, city):
    id = id
    name = name
    email = email

    city = city
    db.execute("UPDATE students SET name = '"+name+"', email = '" +
               email+"', city = '"+city+"' WHERE id = '"+id+"'")
    con.commit()
    return True


def only_student_data():
    db.execute("SELECT * FROM students WHERE role = 'user'")
    only_student_data = db.fetchall()
    return only_student_data


def delete(id):
    id = id
    db.execute("DELETE FROM students WHERE id = {}".format(id))
    db.execute("DELETE FROM wish_list WHERE student_id = {}".format(id))
    con.commit()
    return True


def student_data_by_id(id):
    db.execute("SELECT * FROM students WHERE id = {}".format(id))
    student_data = db.fetchall()
    return student_data


def uni_delete(id):
    id = id
    db.execute("DELETE FROM rsapp_university WHERE id = {}".format(id))
    db.execute("DELETE FROM merit WHERE uni_id = {}".format(id))
    con.commit()
    return True


def add_city(city):
    city = city
    db.execute("INSERT INTO city (city) VALUES ('"+city+"')")
    con.commit()
    return True


def cities_data():
    db.execute("SELECT * FROM city")
    cities_data = db.fetchall()
    return cities_data


def select_city_for_university(city_id):
    db.execute("SELECT * FROM city WHERE id = {}".format(city_id))
    city_data = db.fetchall()
    return city_data


def add_merit(id, year, course, merit):
    id = id
    year = year
    merit = merit
    db.execute("INSERT INTO merit (uni_id, year ,course, merit) VALUES ('{}','{}','{}','{}')".format(
        id, year, course, merit))
    con.commit()
    return True


def merit_data(id):
    id = id
    print(id)
    db.execute("SELECT * FROM merit WHERE uni_id = {}".format(id))
    merit_data = db.fetchall()

    return merit_data


def student_search(search):
    db.execute("select  * from students where (name LIKE '%" +
               search+"%') AND role = 'user' ")
    student_data = db.fetchall()
    return student_data


def delete_merit(id):
    id = id
    db.execute("DELETE FROM merit WHERE id = {}".format(id))
    con.commit()
    return True


def add_feedback(name, feedback):
    name = name
    feedback = feedback
    db.execute("INSERT INTO feedback (student_id, feedback) VALUES ('{}','{}')".format(
        name, feedback))
    con.commit()
    return True


def feedback_data():
    db.execute("SELECT * FROM feedback")
    feedback_data = db.fetchall()
    return feedback_data


def delete_feedback(id):
    id = id
    db.execute("DELETE FROM feedback WHERE id = {}".format(id))
    con.commit()
    return True


def add_to_wishlist(id, student_id):
    id = id
    student_id = student_id
    db.execute("INSERT INTO wish_list (uni_id, student_id) VALUES ('{}','{}')".format(
        id, student_id))
    con.commit()
    return True


def check_wishlist(id):
    id = id
    db.execute("SELECT * FROM wish_list WHERE uni_id = {}".format(id))
    wish_list_data = db.fetchall()
    return wish_list_data


def wishlist_data(student_id):
    student_id = student_id
    db.execute(
        "SELECT * FROM wish_list where student_id = {}".format(student_id))
    wishlist_data = db.fetchall()
    return wishlist_data


def update_student(id, name, email, password, city):
    id = id
    name = name
    email = email
    password = password
    city = city
    db.execute("UPDATE students SET name = '"+name+"', email = '" +
               email+"', password = '"+password+"', confirm_password = '"+password+"', city = '"+city+"' WHERE id = '"+id+"'")
    con.commit()
    return True


def delete_wishlist(id, student_id):
    id = id
    student_id = student_id
    db.execute("DELETE FROM wish_list WHERE uni_id = {} AND student_id = {}".format(
        id, student_id))
    con.commit()
    return True


def send_mail(first_name,last_name, email, msg):
    first_name = first_name
    last_name = last_name
    email = email
    msg = msg
    db.execute("INSERT INTO mails (first_name, last_name, email, msg) VALUES ('{}','{}','{}','{}')".format(
        first_name, last_name, email, msg))
    con.commit()
    return True


def mails_data():
    db.execute("SELECT * FROM mails")
    mails_data = db.fetchall()
    return mails_data

def delete_mail(id):
    id = id
    db.execute("DELETE FROM mails WHERE id = {}".format(id))
    con.commit()
    return True

import MySQLdb 
 

def add_about(about):
    about = about    
    about = MySQLdb.escape_string(about)
    db.execute("UPDATE about SET about = '{}' ".format(about))
    con.commit()
    return True

def about_data():
    db.execute("SELECT * FROM about")
    about_data = db.fetchall()
    return about_data

