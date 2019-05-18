#!/user/bin/env python
# -*- coding:utf-8 -*-


import configparser
import smtplib
from email.mime.text import MIMEText

#import pymysql
#import sqlalchemy
#from sqlalchemy.orm import sessionmaker
#import job_store

DB_CONFIG_PATH = 'config/db.config'


def get_db_config_by_section(section_name):
    config = configparser.ConfigParser()
    config.read(DB_CONFIG_PATH)
    return dict(config.items(section_name))


def read_sql_script(script_path):
    with open(script_path,'r',encoding="utf-8") as script:
        sql_list = script.read().split(';');
    return sql_list

def get_db_connection(db_name):
    db_config = get_db_config_by_section(db_name)
    con_string =("mysql+pymysql://%s:%s@%s:%s/%s" % (db_config['username'], db_config['password'], db_config['host'], db_config['port'], db_config['database']))
    return con_string


def set_mail_msg(from_addr,to_addr,sub,body):
    msg = MIMEText(body,'plain','utf-8')
    msg['Subject'] = sub
    msg['From'] = from_addr
    msg['To'] = to_addr
    return msg


def get_smtp_server(smtp_host, smtp_port, username, password):
    smtp_server = smtplib.SMTP(smtp_host, smtp_port)
    smtp_server.login(username, password)
    return smtp_server


def send_mail(smtp_server,from_addr,to_addr,msg):
    try:
        smtp_server.sendmail(from_addr, to_addr, msg.as_string())
    except Exception:
        return False
    return True









