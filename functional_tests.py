from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser=webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_打开首页并可以再次回复打开(self):
        #张三芬听说有一个很酷的在线报动态应用
        #她去看了这个应用的首页
        self.browser.get('http://localhost:8002')

        #她注意到网页的标题和头部都包含“榆林分行报动态系统”这几个字
        self.assertIn('榆林分行报动态系统' ,self.browser.title)
        
        self.fail('结束测试')

        #应用邀请她输入一个动态事项

        #她在一个文本框中输入了“去锦界拉业务”（拉信贷业务）


        #她按回车键后，页面更新了
        #待办事项表格中显示了“1、去锦界拉业务”

        #页面中又显示了一个文本框，可以输入其他的动态事项
        #她输入了“去天宫和玉帝拉业务”

        #页面再次更新，她的清单中显示了这两个动态事项

        #张三芬想知道这个网站是否会记住她的动态事项清单
        #她看到网站为她生成了一个唯一的URL
        #而且页面中有一些文字解说这个功能

        #她访问那个URL，发现她的动态事项列表还在

        #她很满意，去睡觉了

if __name__=="__main__":
    unittest.main()
