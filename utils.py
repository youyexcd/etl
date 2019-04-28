#!/user/bin/env python
# -*- coding:utf-8 -*-


import configparser
import pymysql
import sqlalchemy


DB_CONFIG_PATH = 'config/db.config'


def get_db_config_by_section(section_name):
    config = configparser.ConfigParser()
    config.read(DB_CONFIG_PATH)
    return dict(config.items(section_name))


def read_sql_script(script_path):
    with open(script_path,'r',encoding="utf-8") as script:
        sql_list = script.read().split(';');
    return sql_list


con = pymysql.connect('127.0.0.1', 'root', 'password')
cursor = con.cursor()

a = read_sql_script('test_data/init_tables.sql')
for sql in a:
    print(sql)
    cursor.execute(sql)
    print('-----')
#engine = sqlalchemy.create_engine("mysql+mysqldb://root:password@127.0.0.1:3306/DB1")


