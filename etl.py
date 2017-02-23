# -*- coding: UTF-8 -*-
import MySQLdb
import pandas as pd

class ETL(object):

    def __init__(self,conn,file_path):
        self.conn = conn
        self.file_path = file_path

    def do_etl(self):
        self._extract()
        self._transform()
        self._load()

    def _extract(self):

        self.tmp_df = pd.read_table('%s' % self.file_path)

    def _transform(self):

        drop_vars = ['guid', 'id', 'createTime', 'linkUrl', 'isGetInfo']
        for var in drop_vars:
            del self.tmp_df['%s' % var]

        self.tmp_df.columns = ['registered_no', 'company_name',
                               'prov_id', 'company_type',
                               'legal_person', 'registered_capital',
                               'company_address', 'company_create_date',
                               'business_scope', 'registration_authority',
                               'registration_status', 'contacts',
                               'money', 'tel']

    def _load(self):
        success = 0
        failure = 0
        cur = self.conn.cursor()
        for i,row in self.tmp_df.iterrows():
            sql_insert = 'INSERT INTO craw_raw (' \
                         ' registered_no,' \
                         ' company_name,' \
                         ' prov_id,' \
                         ' company_type,' \
                         ' legal_person,' \
                         ' registered_capital,' \
                         ' company_address,' \
                         ' company_create_date,' \
                         ' business_scope,' \
                         ' registration_authority,' \
                         ' registration_status,' \
                         ' contacts,' \
                         ' money,' \
                         ' tel) ' \
                         'values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'\
                         %tuple(row)
            try:
                cur.execute(sql_insert)
                success += 1
            except:
                failure += 1
            print '导入 成功:%d Obs.；失败:%d Obs.'% (success,failure)


if __name__ == '__main__':
    file_path = 'henan1000_test.txt'
    # file_path = input('请指定原始文件地址(文件名至于引号中)：')
    conn = MySQLdb.connect(host='192.168.248.18',user='root',passwd='123456',
                           charset='utf8',db='pick_up_coordinates')

    etl_obj = ETL(conn,file_path)
    etl_obj.do_etl()
