# -*- coding: UTF-8 -*-

from random import randint

import MySQLdb
import requests
import time

class PickUpCoordinates(object):
    """拾取经纬度坐标

    从数据库中获取没有经纬度的样本
    传递到百度api获取经纬度
    将获取结果回写数据库
    """
    def __init__(self, conn):
        self.conn = conn

    def pick_ll_main(self):
        """执行获取经纬度的主函数"""
        cur_select = conn.cursor()
        cur_update = conn.cursor()
        res = self._get_samples_with_no_ll(cur_select)
        self._loop_gain_ll(res, cur_select,cur_update)
        cur_select.close()
        cur_update.close()


    def _get_samples_with_no_ll(self, cur_select):
        """从数据库中抽取没有包含经纬度的样本

        :param cur_select: 查询数据的cursor
        :return: cur_select
        """
        sql = "SELECT " \
              " registered_no," \
              " companyaddress " \
              "From test " \
              "WHERE companyaddress != ''"
        cur_select.execute(sql)
        return cur_select

    def _gain_ll(self, sample_info, cur_update):
        """获取单条样本的经纬度信息，并执行更新数据库的命令

        :param sample_info: 样本信息
        :param cur_update: 更新数据库的cursor
        """
        params = {
            'address': '%s' % sample_info[1],
            'output': 'json',
            'ak': 'S4vNqfh4my5U3Om71yuch99cUEq05Ckm'
        }
        url = 'http://api.map.baidu.com/geocoder/v2/'
        response = requests.get(url, params)
        dict = response.json()['result']['location']
        lat, lng = dict['lat'], dict['lng']
        sql_update = "UPDATE test SET " \
                     " longitude='%s'," \
                     " latitude='%s' " \
                     "WHERE registered_no='%s' " \
                  % (lat, lng, sample_info[0])
        cur_update.execute(sql_update)
        print('%s 经纬度被写入 !' % sample_info[0])

    def _loop_gain_ll(self, res, cur_select, cur_update):
        """循环获取经纬度的信息"""
        failure = 0
        while res > 0:
            try:
                sample_info = cur_select.fetchone()
                self._gain_ll(sample_info, cur_update)
                res -= 1
                i = randint(1, 100)
                time.sleep(i)
            except:
                failure += 1
                print('经纬度获取失败，累计获取失败样本：%d 条'%failure)
            finally:
                self.conn.commit()

if __name__ == "__main__":
    conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',
                           db='test',charset='utf8')
						   
    parser_address = PickUpCoordinates(conn)

    try:
        parser_address.pick_ll_main()
    except Exception as e:
        print(e)
    finally:
        conn.close()
        print('所有经纬度获取完成 !')