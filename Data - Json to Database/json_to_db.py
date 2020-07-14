import sqlite3
import json

conn = sqlite3.connect('db.sqlite')
cur = conn.cursor()

cur.executescript('''
    drop table if exists user;
    drop table if exists course;
    drop table if exists member;
    
    create table user(
        id integer not null primary key autoincrement unique,
        name text unique);
        
    create table course(
        id integer not null primary key autoincrement unique,
        title text unique);
        
    create table member(
        user_id integer,
        course_id integer,
        role integer,
        primary key(user_id, course_id)
        );
           
''')

fname  = input('enter file name: ')
if len(fname) < 1: fname = 'member_data.json'

content  = open(fname).read()
data = json.loads(content)

for entry in data:
    name = entry[0]
    course = entry[1]
    role = entry[2]
    
    print(name, course, role)

    cur.execute('insert or ignore into user (name) values (?)', (name,))
    cur.execute('select id from user where name = ?', (name,))
    user_id = cur.fetchone()[0]

    cur.execute('insert or ignore into course(title) values (?)', (course,))
    cur.execute('select id from course where title = ?', (course, ))
    course_id = cur.fetchone()[0]

    cur.execute('insert or replace into member(user_id, course_id, role) values (?,?,?)', (user_id, course_id, role))

    conn.commit()