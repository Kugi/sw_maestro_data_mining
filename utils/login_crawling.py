#coding: utf-8
from selenium import webdriver
from time import sleep
driver = webdriver.Chrome()
def cafe_monitoring(query):
    driver.get('https://nid.naver.com/nidlogin.login')
    elm_email = driver.find_element_by_id("id")
    elm_paswd = driver.find_element_by_id("pw")
    elm_signIn = driver.find_element_by_class_name("btn_login")
    elm_email.send_keys('naverid')
    elm_paswd.send_keys('pwd')
    elm_signIn.click()
    driver.get('http://cafe.naver.com/joonggonara/')
    elm_cafe_search = driver.find_element_by_id("topLayerQueryInput")
    elm_cafe_search.send_keys(query)
    driver.execute_script("searchBoard()")
    sleep(0.2)
    driver.save_screenshot("/home/newmoni/test/d.png")


cafe_monitoring(u'레티나 15')

