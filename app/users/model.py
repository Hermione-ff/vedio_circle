from flask import Flask, request, jsonify
from peewee import *
from werkzeug.security import generate_password_hash, check_password_hash #加密密码及验证
import time

db = MySQLDatabase("data",user='root',password='123456',host='127.0.0.1',port=3306,charset='utf8mb4')

class BaseModel(Model):
    class Meta:
        database = db

class Videodata(BaseModel):
    id = AutoField(primary_key=True)
    date = DateTimeField()
    username = CharField()
    url = CharField()
    content = CharField(null=True)
    type_choices = ((1,'1'),(2,'2'))
    type = IntegerField(choices=type_choices)

    class Meta:
        # 表名
        table_name = 'Videodata'

class Users(BaseModel):
    id = AutoField(primary_key=True)
    username = CharField()
    password = CharField()
    email = CharField()
    login_time = DateTimeField(null=True)

    class Meta:
        # 表名
        table_name = 'users'


def set_password(password):
    return generate_password_hash(password)  #密码生成函数

def check_password(hash, password):
    return check_password_hash(hash, password)  #密码延展函数

#需要一个user对象
def get(user):
    try:
        connect_db()
        result = user
        return result
    except Exception as e:
        db.rollback()
        reason = str(e)
        return reason
    finally:
        close_db()

#需要一个user对象
def add(user):
    try:
        connect_db()
        result = user.save()
        return result
    except Exception as e:
        db.rollback()
        reason = str(e)
        return reason
    finally:
        close_db()

#需要一个user对象
def update(user):
    add(user)

#需要一个user对象
def delete(user):
    try:
        connect_db()
        result = user.delete_instance()
        return result
    except Exception as e:
        db.rollback()
        reason = str(e)
        return reason
    finally:
        close_db()



def connect_db():
    if db.is_closed():
        db.connect()

def close_db():
    if not db.is_closed():
        db.close()

def commit(work):
    try:
        connect_db()
        work.save()
    except Exception as e:
        db.rollback()
        reason = str(e)
        return reason
    finally:
        close_db()

# date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
# user = Users(username='saad',password='sadad',email='1',login_time=date)
# user = Users.update(username='nonohappy').where(Users.id==2).execute()
# user = Users.get_or_none(Users.id==1)
# print(get(user))
# password = "123456"
# print(set_password(password))
# connect_db()
# Users.create_table()
# close_db()