from .base import FunctionalTest
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys

from brach_lists.models import Item,DayActivityUserList


import unittest

class ItemValidationTest(FunctionalTest):

    def test_不能添加空白动态(self):
        #信息科技部进入一个动态清单
        self.browser.get(self.live_server_url)
        select_box=self.browser.find_element_by_id('select_box')
        Select(select_box).select_by_value('ylxxkj')
        self.browser.find_element_by_id('submit').click()


        #输入框中没有内容，他就按下了回车键
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)


        #页面刷新了，显示一个错误消息
        #提示动态内容不能为空
        self.wait_for(lambda:self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            '不能输入空白内容'
        ))

        #输入文字后提交，这次就好了
        self.browser.find_element_by_id('id_new_item').send_keys('去吃饭')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.fun_检查表格中的标题行内容(f'今日动态\n{today_chinese}：')
        self.fun_检查表格中的行内容('去吃饭')


        #他比较调皮，又提交了一个空代办事项
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)


        #在清单中他又看到了一个类似的错误消息
        self.wait_for(lambda:self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            '不能输入空白内容'
        ))

        #输入文字后就没问题了
        self.browser.find_element_by_id('id_new_item').send_keys('去睡觉')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.fun_检查表格中的行内容('1、去吃饭；')
        self.fun_检查表格中的行内容('2、去睡觉。')


        self.fail('结束测试')

