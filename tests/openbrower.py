import time
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import chardet
from selenium.webdriver.common.action_chains import ActionChains

def open_browser():   
  # 打开浏览器并跳转到目标网站
  url = 'https://chatbot.theb.ai/' #角色扮演成功，但是自动化进入
  # url = 'https://chat.wuguokai.cn/#/chat/' # 备用方案，角色扮演基本失败

  # 获取浏览器对象并打开控制台
  driver = webdriver.Chrome("C:\Program Files\Google\Driver\chromedriver") # 指定使用Chrome浏览器
  driver.get(url)
  time.sleep(1) # 等待页面加载完成


  
  driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.SHIFT + 'J')


  # 从文件中读取JavaScript脚本，并自动检测编码方式
  with open('tests/js_eyes/main.js', 'rb') as f:
      data = f.read()
      encoding = chardet.detect(data)['encoding']
      script = data.decode(encoding)
  # 在控制台执行JavaScript脚本
  driver.execute_script(script)
  # try to open a new tab
  ActionChains(driver).key_down(Keys.CONTROL).send_keys("t").key_up(Keys.CONTROL).perform()
  return