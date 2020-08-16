import requests  # 导入requests库
import re  # 导入正则表达式库
import os  # 导入操作系统库,用于获取文件路径
import time  # 导入时间库

class WeiMeiGirls():
    def __init__(self):
        self.url_main = "https://www.vmgirls.com/"
        self.user_headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
            }
    def get_html_main(self):
        response_main = requests.get(self.url_main, headers=self.user_headers)
        assert response_main.status_code == 200  # 当响应码不是200时候，做断言报错处理
        html_main = response_main.text
        print(html_main)
        return html_main

    # 对请求返回内容进行正则表达式 获取组图详情页网址，列表返回
    def get_detail_url(self,html):
        url_detail_content = re.findall('<a class="media-content" href="(.*?)" title="(.*?) data-bg="(.*?)">', html)
        url_detail_list=[]
        for itme in url_detail_content:
            url_detail = itme[0]
            url_detail_list.append(url_detail)
        return url_detail_list

    # 获取详情页内容，然后返回text
    def get_detail_data(self,url_details):
        for detail_url in url_details:
            detail_url = self.url_main + detail_url
            respons_detail = requests.get(detail_url,headers=self.user_headers)
            assert respons_detail.status_code == 200
            html_detail = respons_detail.text
            print(html_detail)
            time.sleep(10)  # 设定10秒延时
            return html_detail

    def get_detail_picture_name(self, html_detail):
        # 获取详情页各图片网址
        url_detail = re.findall('<a href="(.*?)" alt=".*?" title=".*?">', html_detail)
        return url_detail

    # 下载并保存图片
    def get_pictures_groupname(self,url_details):
        for detail_url in url_details:
            # 拼接详情页网址
            detail_url = self.url_main + detail_url
            # 请求详情页
            respons_detail = requests.get(detail_url, headers=self.user_headers)
            assert respons_detail.status_code == 200
            html_detail = respons_detail.text

            # 对请求返回内容进行正则表达式 获取图片下载链接
            url_detail_list = re.findall('<a href="(.*?)" alt=".*?" title=".*?">', html_detail)
            # print(url_detail_list)
            groupname = re.findall('<a href=".*?" alt=".*?" title="(.*?)">', html_detail)
            print(groupname[0])
            time.sleep(5)  # 设定5秒延时

            # 使用enumerate函数,取出列表元素值和下标
            for index, picture_url_tem in enumerate(url_detail_list):
                # 拼接图片地址
                picture_url = self.url_main+picture_url_tem
                # requests get 请求
                picture_reponse = requests.get(picture_url,headers=self.user_headers)
                # 文件夹名字
                dir_name = str(groupname[0])
                file_name = str(index)+'.jpeg'

                if not os.path.exists(dir_name):  # 判断文件夹是否存在，如果不存在：
                    os.mkdir(dir_name)  # 创建一个文件夹

                with open(dir_name + '/' + file_name, 'wb') as f:  # 用wb模式打开创建文件，w写模式
                    f.write(picture_reponse.content)  # 写入二进制文件内容
                time.sleep(1)

    def run(self):
        # 获取网易内容
        html_main = self.get_html_main()
        # 获取详情页内容,筛选出每组图详情页网址
        detail_url_list = self.get_detail_url(html_main)
        # # 获取详情页内容
        # html_detail_data = self.get_detail_data(detail_url_list)
        # # 获取详情页图片链接及其图片组名称
        # print(self.get_detail_picture_name(html_detail_data))
        get_pictures = self.get_pictures_groupname(detail_url_list)


if __name__ == "__main__":
    # 实例化这个WeiMeiGirls类
    weimei = WeiMeiGirls()
    # 调用run方法
    weimei.run()