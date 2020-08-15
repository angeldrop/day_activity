from .base import FunctionalTest
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys



class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
         #信息科技部听说有一个很酷的在线报动态应用
        #她去看了这个应用的首页
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024,768)

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

        #她看到输入框完美地居中显示
        inputbox=self.fun_找到输入框()
        self.assertAlmostEqual(
            inputbox.location['x']+inputbox.size['width']/2,
            512,
            delta=10
        )

