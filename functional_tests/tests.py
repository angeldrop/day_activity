from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

from brach_lists.models import Item,DayActivityUserList


import time,datetime
import unittest

MAX_WAIT=10
class NewVisitorTest(StaticLiveServerTestCase):
    def setUp(self):
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

    def fun_检查表格中的行内容(self,row_text):
        start_time=time.time()
        while True:
            try:
                table=self.browser.find_element_by_id('id_list_table')
                rows=table.find_elements_by_tag_name('tr')
                self.assertIn(row_text,[row.text for row in rows])
                return
            except (AssertionError,WebDriverException) as e:
                if time.time()-start_time>MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_开始一个分支机构用户的动态清单(self):
        #信息科技部听说有一个很酷的在线报动态应用
        #她去看了这个应用的首页
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024,768)

        #她注意到网页的标题和头部都包含“榆林分行报动态系统”这几个字
        self.assertIn('榆林分行报动态系统' ,self.browser.title)
        head_text=self.browser.find_element_by_tag_name('h1').text
        self.assertIn('榆林分行报动态系统' ,head_text)        

        #她看到选择框完美地居中显示
        select_box=self.browser.find_element_by_id('select_box')
        self.assertAlmostEqual(
            select_box.location['x']+select_box.size['width']/2,
            512,
            delta=10
        )

        #她选择信息科技部并登录
        select_box=self.browser.find_element_by_id('select_box')
        Select(select_box).select_by_value('ylxxkj')
        self.browser.find_element_by_id('submit').click()

        #应用邀请她输入一个动态事项
        inputbox=self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            '请输入动态事项'
        )
        
        #她看到输入框完美地居中显示
        inputbox=self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x']+inputbox.size['width']/2,
            512,
            delta=10
        )
        

        #她在一个文本框中输入了“去锦界拉业务”（拉信贷业务）
        inputbox.send_keys('去锦界拉业务')

        #她按回车键后，页面更新了
        #待办事项表格中显示了“今日动态（日期）：”和“去锦界拉业务。”
        inputbox.send_keys(Keys.ENTER)
        today_chinese=f'{self.today.year}年{self.today.month}月{self.today.day}日'
        self.fun_检查表格中的行内容(f'今日动态（{today_chinese}）：')
        self.fun_检查表格中的行内容('去锦界拉业务。')

        #页面中又显示了一个文本框，可以输入其他的动态事项
        #她输入了“去天宫和玉帝拉业务！”，测试会不会去标点符号
        inputbox=self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('去天宫和玉帝拉业务！')
        inputbox.send_keys(Keys.ENTER)

        #页面再次更新，她的清单中显示了这两个动态事项
        self.fun_检查表格中的行内容('1、去锦界拉业务；')
        self.fun_检查表格中的行内容('2、去天宫和玉帝拉业务。')

        
        #信息科技部想知道这个网站是否会记住她的动态事项清单
        #她看到网站为她生成了一个唯一的URL
        #而且页面中有一些文字解说这个功能
        

        #她访问那个URL，发现她的动态事项列表还在

        #她很满意，去睡觉了
        
    def test_新用户可以通过不同的url开始一个动态清单(self):
        #信息科技部新建一个动态清单
        self.browser.get(self.live_server_url)
        select_box=self.browser.find_element_by_id('select_box')
        Select(select_box).select_by_value('ylxxkj')
        self.browser.find_element_by_id('submit').click()
        inputbox=self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('去天堂拉业务')
        inputbox.send_keys(Keys.ENTER)
        self.fun_检查表格中的行内容('去天堂拉业务。')
        
        #她注意到清单有个唯一的url
        zsf_brach_lists_url=self.browser.current_url
        self.assertRegex(zsf_brach_lists_url,'/brach_lists/.+')
        
        #现在另外一个府谷县支行访问了网站
        
        ##我们使用一个新浏览器会话
        ##确保信息科技部的信息不会从cookie中泄露出去
        self.browser.quit()
        self.browser=webdriver.Firefox()
        
        #府谷县支行访问首页
        #页面中看不到信息科技部的清单
        self.browser.get(self.live_server_url)
        select_box=self.browser.find_element_by_id('select_box')
        Select(select_box).select_by_value('806050701')
        self.browser.find_element_by_id('submit').click()
        page_text=self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('去天堂拉业务',page_text)
        self.assertNotIn('去天宫和玉帝拉业务',page_text)
        
        #府谷县支行输入一个新动态，新建一个清单
        #他不想张三芬那么兴致勃勃
        inputbox=self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('去地狱拉业务')
        inputbox.send_keys(Keys.ENTER)
        self.fun_检查表格中的行内容('去地狱拉业务。')
        
        #府谷县支行或得了他惟一的URL
        wmz_brach_lists_url=self.browser.current_url
        self.assertRegex(wmz_brach_lists_url,'/brach_lists/.+')
        self.assertNotEqual(wmz_brach_lists_url,zsf_brach_lists_url)
        
        #这个页面还是没有信息科技部的清单
        page_text=self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('去天堂拉业务',page_text)
        self.assertIn('去地狱拉业务',page_text)
        
        #两人都很满意，去睡觉了。
        self.fail('结束测试')
# if __name__=="__main__":
    # unittest.main()    测试ssh
