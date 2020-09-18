import argparse
import os
import sys
import time

import cv2
import numpy as np
import requests
import urllib3
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(InsecureRequestWarning)


def download_google_staticimages(searchurl, dirs, chromedriver_path, detect_face, headless):
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    if headless:
        options.add_argument('--headless')

    try:
        browser = webdriver.Chrome(chromedriver_path, options=options)
    except Exception as e:
        print(f'No found chromedriver in this environment.')
        print(f'Install on your machine. exception: {e}')
        sys.exit()

    browser.set_window_size(1280, 1024)
    browser.get(searchurl)
    time.sleep(1)

    print(f' Loading...')

    element = browser.find_element_by_tag_name('body')

    # Scroll down
    # for i in range(30):
    for i in range(50):
        element.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.3)

    try:
        browser.find_element_by_id('smb').click()
        for i in range(50):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)
    except:
        for i in range(10):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)

    print(f'Reached end of page.')
    time.sleep(0.5)
    print(f'Retry')
    time.sleep(0.5)

    # browser.find_element_by_xpath('//input[@value="Еще результаты"]').click()
    # Scroll down 2
    for i in range(50):
        element.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.3)

    try:
        browser.find_element_by_id('smb').click()
        for i in range(50):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)
    except:
        for i in range(10):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)

    # elements = browser.find_elements_by_xpath('//div[@id="islrg"]')
    # page_source = elements[0].get_attribute('innerHTML')
    page_source = browser.page_source

    soup = BeautifulSoup(page_source, 'lxml')
    images = soup.find_all('img')

    urls = []
    for image in images:
        try:
            url = image['data-src']
            if not url.find('https://'):
                urls.append(url)
        except:
            try:
                url = image['src']
                if not url.find('https://'):
                    urls.append(image['src'])
            except Exception as e:
                print(f'No found image sources.')
                print(e)

    count = 0
    if urls:
        for url in urls:
            try:
                res = requests.get(url, verify=False, stream=True)
                rawdata = res.raw.read()
                if detect_face:
                    try:
                        x = np.frombuffer(rawdata, dtype='uint8')
                        img = cv2.imdecode(x, cv2.IMREAD_UNCHANGED)
                        res = soft_detect_face(img)
                        if res:
                            with open(os.path.join(dirs, 'img_' + str(count) + '.jpg'), 'wb') as f:
                                f.write(rawdata)
                                count += 1
                    except ValueError:
                        pass
                else:
                    with open(os.path.join(dirs, 'img_' + str(count) + '.jpg'), 'wb') as f:
                        f.write(rawdata)
                        count += 1

            except Exception as e:
                print('Failed to write rawdata.')
                print(e)

    browser.close()
    return count


def soft_detect_face(frame):
    """
    :param object frame: frame from video
    :return: list
    """
    cv2_base_dir = os.path.dirname(os.path.abspath(cv2.__file__))
    haar_model = os.path.join(cv2_base_dir, 'data', 'haarcascade_frontalface_default.xml')
    cascade_face_detector = cv2.CascadeClassifier(haar_model)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = cascade_face_detector.detectMultiScale(gray_frame, 1.1, 3)
    return list(filter(lambda x: x[2] > 50, faces))


# Main block
def main(search_phrase, chromedriver_path, detect_face, output_folder, headless):
    search_words = search_phrase.split(' ')
    searchurl = 'https://www.google.com/search?q='
    for word in search_words:
        searchurl += word + '+'
    searchurl += '&source=lnms&tbm=isch'
    dirs = os.path.join(output_folder, search_phrase)
    if not os.path.exists(dirs):
        os.mkdir(dirs)
    t0 = time.time()
    count = download_google_staticimages(searchurl, dirs, chromedriver_path, detect_face, headless)
    t1 = time.time()

    total_time = t1 - t0
    print(f'\n')
    print(f'Download completed. [Successful count = {count}].')
    print(f'Total time is {str(total_time)} seconds.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search parameters')

    parser.add_argument('-s', dest='search_phrase', default='sth', help='Phrase for search')
    parser.add_argument('-c', dest='chromedriver', default='/usr/local/bin/chromedriver', help='path to chromedriver')
    parser.add_argument('-d', dest='detect_face', default=False, help='save images with faces only')
    parser.add_argument('-o', dest='output_folder', default='.', help='location for output results')
    parser.add_argument('-b', dest='headless', default=False,
                        help='launch google chrome to be able to see and control or do in background')

    args = parser.parse_args()

    main(args.search_phrase, args.chromedriver, args.detect_face, args.output_folder, args.headless)
