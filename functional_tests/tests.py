from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser=webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def fun_检查表格中的行内容(self,row_text):
        table=self.browser.find_element_by_id('id_list_table')
        rows=table.find_elements_by_tag_name('tr')
        self.assertIn(row_text,[row.text for row in rows])

    def test_打开首页并可以再次回复打开(self):
        #张三芬听说有一个很酷的在线报动态应用
        #她去看了这个应用的首页
        self.browser.get(self.live_server_url)

        #她注意到网页的标题和头部都包含“榆林分行报动态系统”这几个字
        self.assertIn('榆林分行报动态系统' ,self.browser.title)
        head_text=self.browser.find_element_by_tag_name('h1').text
        self.assertIn('榆林分行报动态系统' ,head_text)        

        #应用邀请她输入一个动态事项
        inputbox=self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            '请输入动态事项'
        )

        #她在一个文本框中输入了“去锦界拉业务”（拉信贷业务）
        inputbox.send_keys('去锦界拉业务')

        #她按回车键后，页面更新了
        #待办事项表格中显示了“（1）去锦界拉业务”
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.fun_检查表格中的行内容('（1）去锦界拉业务；')

        #页面中又显示了一个文本框，可以输入其他的动态事项
        #她输入了“去天宫和玉帝拉业务”
        inputbox=self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('去天宫和玉帝拉业务')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        #页面再次更新，她的清单中显示了这两个动态事项
        self.fun_检查表格中的行内容('（1）去锦界拉业务；')
        self.fun_检查表格中的行内容('（2）去天宫和玉帝拉业务；')

        
        #张三芬想知道这个网站是否会记住她的动态事项清单
        #她看到网站为她生成了一个唯一的URL
        #而且页面中有一些文字解说这个功能
        self.fail('结束测试')

        #她访问那个URL，发现她的动态事项列表还在

        #她很满意，去睡觉了

# if __name__=="__main__":
    # unittest.main()
