from .base import FunctionalTest
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys

from brach_lists.models import Item,DayActivityUserList


import unittest,datetime
today=datetime.datetime.today().date()
today_chinese=f"{today.year}年{today.month}月{today.day}日"
class ItemValidationTest(FunctionalTest):

    def test_不能添加空白动态(self):
        #信息科技部进入一个动态清单
        self.browser.get(self.live_server_url)
        select_box=self.browser.find_element_by_id('select_box')
        Select(select_box).select_by_value('ylxxkj')
        self.browser.find_element_by_id('submit').click()


        #输入框中没有内容，他就按下了回车键
        self.fun_找到输入框().send_keys(Keys.ENTER)


        #页面刷新了，显示一个错误消息
        #提示动态内容不能为空
        self.wait_for(lambda:self.browser.find_element_by_css_selector(
            '#id_text:invalid'
        ))

        #输入文字后提交，这次就好了
        self.fun_找到输入框().send_keys('去吃饭')
        self.wait_for(lambda:self.browser.find_element_by_css_selector(
            '#id_text:valid'
        ))
        self.fun_找到输入框().send_keys(Keys.ENTER)
        self.fun_检查表格中的标题行内容(f'今日动态\n{today_chinese}：')
        self.fun_检查表格中的行内容('去吃饭。')
        


        #他比较调皮，又提交了一个空代办事项
        self.fun_找到输入框().send_keys(Keys.ENTER)


        #在清单中他又看到了一个类似的错误消息
        self.wait_for(lambda:self.browser.find_element_by_css_selector(
            '#id_text:invalid'
        ))

        #输入文字后就没问题了
        self.fun_找到输入框().send_keys('去睡觉')
        self.wait_for(lambda:self.browser.find_element_by_css_selector(
            '#id_text:valid'
        ))
        self.fun_找到输入框().send_keys(Keys.ENTER)
        self.fun_检查表格中的行内容('1、去吃饭；')
        self.fun_检查表格中的行内容('2、去睡觉。')
        
        
    def test_不能添加重复动态(self):
        #信息科技部进入一个动态清单
        self.browser.get(self.live_server_url)
        select_box=self.browser.find_element_by_id('select_box')
        Select(select_box).select_by_value('ylxxkj')
        self.browser.find_element_by_id('submit').click()


        #输入文字后提交
        self.fun_找到输入框().send_keys('去吃饭')
        self.fun_找到输入框().send_keys(Keys.ENTER)
        self.fun_检查表格中的标题行内容(f'今日动态\n{today_chinese}：')
        self.fun_检查表格中的行内容('去吃饭。')
        


        #他不小心重复输入动态事项
        self.fun_找到输入框().send_keys('去吃饭')
        self.fun_找到输入框().send_keys(Keys.ENTER)


        #在清单中他又看到了一个有用的错误消息
        self.wait_for(lambda:self.assertEqual(
            self.browser.find_element_by_css_selector(
            '.has-error').text,
            "你不能输入重复项"
        ))


        self.fail('结束测试')

