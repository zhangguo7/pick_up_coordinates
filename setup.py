# -*- coding: UTF-8 -*-

import MySQLdb

class Setup(object):

    def __init__(self,conn):
        self.conn = conn
        self.drop_db = 'DROP DATABASE IF EXISTS `pick_up_coordinates`'
        self.create_db = 'CREATE database IF NOT EXISTS `pick_up_coordinates`'
        self.select_db = 'USE `pick_up_coordinates`'
        self.drop_table = 'DROP TABLE IF EXISTS `craw_raw`'
        self.create_table = 'CREATE TABLE IF NOT EXISTS`craw_raw` (' \
                          ' `id` int(11) NOT NULL AUTO_INCREMENT,' \
                          ' `registered_no` char(20) NOT NULL,' \
                          ' `company_name` varchar(30) DEFAULT NULL,' \
                          ' `prip_id` varchar(20) DEFAULT NULL,' \
                          ' `company_type` varchar(20) DEFAULT NULL,' \
                          ' `legal_person` varchar(10) DEFAULT NULL,' \
                          ' `registered_capital` varchar(255) DEFAULT NULL,' \
                          ' `company_address` varchar(255) NOT NULL,' \
                          ' `company_create_date` varchar(11) DEFAULT NULL,' \
                          ' `business_scope` text,' \
                          ' `registration_authority` varchar(255) DEFAULT NULL,' \
                          ' `registration_status` varchar(100) DEFAULT NULL,' \
                          ' `contacts` varchar(255) DEFAULT NULL,' \
                          ' `money` varchar(20) DEFAULT NULL,' \
                          ' `tel` varchar(11) DEFAULT NULL,' \
                          ' `longitude` decimal(19,16) DEFAULT NULL,' \
                          ' `latitude` decimal(19,16) DEFAULT NULL,' \
                          ' PRIMARY KEY (`id`)' \
                          ') ENGINE=InnoDB AUTO_INCREMENT=9122 DEFAULT CHARSET=utf8'
    def setup(self):
        cur = self.conn.cursor()
        cur.execute(self.drop_db)
        cur.execute(self.create_db)
        cur.execute(self.select_db)
        cur.execute(self.create_table)
        self.conn.commit()
        cur.close()
        self.conn.close()

if __name__ == '__main__':
    print u'正在安装 获取经纬度模块...'
    conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',
                           charset='utf8',db='pick_up_coordinates')
    init_obj = Setup(conn)
    init_obj.setup()
    print u'安装完毕!'
