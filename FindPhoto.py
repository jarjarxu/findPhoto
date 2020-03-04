import os
import random
import time
import urllib
from selenium import webdriver

#打开图片来源网址定位到每个图片所在网页，添加到页面链接合集downloadUrl
def find_Url(downloadWebsite):
    #个人觉得打开网页碍眼，设置了selenium不打开网页进行爬数据,使用过程会有个报错但是不妨碍程序运行
    option = webdriver.ChromeOptions()
    option.set_headless()
    driver = webdriver.Chrome(chrome_options = option)

    #模拟浏览器,等待5秒,等网页加载动态资源完毕
    driver.get(downloadWebsite)
    time.sleep(5)

    #定位链接位置,可通过浏览器开发者工具的源码查看具体位置
    urlList = driver.find_elements_by_xpath("//ul[@class='clearfix']/li[@class='photo-item']")

    #在所有li中随机抽取5个链接添加到链接合集
    urlList2 = random.sample(urlList , 5)
    print("urlList2:")
    print(urlList2)
    for url in urlList2:
        webUrl = url.find_element_by_tag_name("a").get_attribute("href")
        downloadUrl.append(webUrl)
        print(webUrl)

    driver.quit()

    return downloadUrl

#打开图片所在的页面链接合集里的链接,获取图片的src,并添加到图片src合集downloadList
def find_ImgSrc(downloadUrlList):
    option2 = webdriver.ChromeOptions()
    option2.set_headless()
    for url in downloadUrlList:
        browse = webdriver.Chrome(chrome_options = option2)
        browse.get(url)
        time.sleep(5)
        imgList = browse.find_elements_by_xpath("//div[@class='images']/img")
        for img in imgList:
            imgUrl = img.get_attribute("src")
            downloadList.append(imgUrl)

        browse.quit()

    return  downloadList

#获取图片src合集downloadList里的src并保存到本地文件夹
def download_img(download_file,download_url):
    try:
        if not os.path.exists(download_file):
            os.makedirs(download_file)

        count = 1
        for image in download_url:
            #获取图片后缀
            file_suffix = os.path.splitext(image)[1]

            #格式化图片命名,以数字1..10..命名
            filename = '{}{}{}{}'.format(download_file,os.sep,str(count),file_suffix)
            urllib.request.urlretrieve(image,filename=filename)
            print("正在下载第" + str(count) + "张图片")
            #等待1.5秒再下载下一张图片,提防反爬虫机制
            time.sleep(1.5)
            count+=1

        print("下载完成，共下载" + str(count) + "张图片")
    except IOError as e:
        print("IOError")
    except Exception as e:
        print("Exception")

def main():
    webUrlList = find_Url(download_Website)
    download = find_ImgSrc(webUrlList)
    download_img(downloadFile,download)


#获取图片所在的页面链接合集
downloadUrl = []

#获取图片src合集
downloadList = []

#图片来源网址
download_Website = "https://search.bilibili.com/photo?keyword=cosplay"

#图片下载路径
downloadFile = "D:\pycharm\workspace\_newTry\photo"

if __name__ == '__main__':
    main()