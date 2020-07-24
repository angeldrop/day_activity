from .base import FunctionalTest
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys

from brach_lists.models import Item,DayActivityUserList


import unittest

class ItemValidationTest(FunctionalTest):

    def test_不能添加空白动态(self):
        #信息科技部新建一个动态清单
        #输入框中没有内容，他就按下了回车键

        #首页刷新了，显示一个错误消息
        #提示动态内容不能为空

        #输入文字后提交，这次就好了

        #他比较调皮，又提交了一个空代办事项

        #在清单中他又看到了一个类似的错误消息

        #输入文字后就没问题了

        self.fail('结束测试')

