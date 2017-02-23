# -*- coding: UTF-8 -*-

import pandas as pd

# file_path = input('请指定原始文件地址(文件名至于引号中)：')
file_path = 'henan1000_test.txt'
tmp_df = pd.read_table('%s' % file_path)

drop_vars = ['guid','id','createTime','linkUrl','isGetInfo']
for var in drop_vars:
    del tmp_df['%s'%var]

tmp_df.columns = ['registered_no','company_name','prov_id','company_type',
                  'legal_person','registered_capital','company_address',
                  'company_create_date','business_scope','registration_authority',
                  'registration_status','contacts','money','tel']
print tmp_df.ix[:10,6]