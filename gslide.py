#-*- coding: utf-8 -*-

import os, time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from PIL import Image

def capture_gslide(gslide_url):
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get(gslide_url)
    time.sleep(3)

    title = driver.title.split('.',1)[0]

    # get the number of slides
    actions = ActionChains(driver)
    actions.send_keys(Keys.END)
    actions.perform()
    max_page = int(driver.current_url.rsplit('.',1)[-1][1:])
    print("Total Number of Slides: " + str(max_page))
    time.sleep(3)

    # start the presentation from first slide in full screen
    keys = Keys()
    actions = ActionChains(driver)
    actions.send_keys(keys.CONTROL + keys.SHIFT + keys.F5)
    actions.key_down(keys.SHIFT).key_down(keys.CONTROL).send_keys(keys.F5)
    actions.perform()
    time.sleep(8)

    # move to next page until the end
    actions = ActionChains(driver)
    slide_no = 0
    image_list = []
    if not os.path.exists(title):
        os.mkdir(title)

    while slide_no < int(max_page):

        # take sreenshot and store it in title folder
        png_file = '{}.png'.format(str(slide_no).zfill(2))
        pdf_file = title + ".pdf"
        save_png = os.path.join(title, png_file)
        save_pdf = os.path.join(title, pdf_file)
        driver.save_screenshot(save_png)
        
        print('Page '+str(slide_no) + ' was captured.')

        im = Image.open(save_png)
        image = im.convert('RGB')
        image_list.append(image)

        slide_no = int(driver.current_url.rsplit('.',1)[-1][1:])    

        actions.click()
        actions.perform()

        time.sleep(2)  

    image_list[0].save(save_pdf, save_all=True, append_images=image_list[1:]) 

    print('Done')

url = input("Please enter Google Slides Link - ")

capture_gslide(url)