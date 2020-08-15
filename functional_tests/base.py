from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from brach_lists.models import Item,DayActivityUserList

import time,datetime,os


MAX_WAIT=10
class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        staging_server=os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url='http://'+staging_server
        ##提前今天的数据，备以后显示使用
        self.today=datetime.datetime.today().date()
        self.browser=webdriver.Firefox()
        ##提前创建部门用户列表两个，备以后使用
        DayActivityUserList.objects.create(id='ylxxkj',order_number=13,
            brach_type='部门',full_name='信息科技部')
        DayActivityUserList.objects.create(id='806050701',order_number=15,
            brach_type='管理型支行',full_name='府谷县支行')

    def tearDown(self):
        self.browser.quit()

    def wait_for(self,fn):
        start_time=time.time()
        while True:
            try:
                return fn()
            except (AssertionError,WebDriverException) as e:
                if time.time()-start_time>MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def fun_检查表格中的行内容(self,row_text):
        start_time=time.time()
        while True:
            try:
                tables=self.browser.find_element_by_id('id_list_table')
                rows=tables.find_elements_by_tag_name('tr')
                self.assertIn(row_text,[row.text for row in rows])
                return
            except (AssertionError,WebDriverException) as e:
                if time.time()-start_time>MAX_WAIT:
                    raise e
                time.sleep(0.5)
    
    
    def fun_检查表格中的标题行内容(self,row_text):
        start_time=time.time()
        while True:
            try:
                tables=self.browser.find_element_by_id('id_list_table')
                rows=tables.find_elements_by_tag_name('th')
                self.assertIn(row_text,[row.text for row in rows])
                return
            except (AssertionError,WebDriverException) as e:
                if time.time()-start_time>MAX_WAIT:
                    raise e
                time.sleep(0.5)
    
    
    def fun_找到输入框(self):
        return self.browser.find_element_by_id('id_text')
