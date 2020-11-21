# using selenium to crawl img in google
# cf: https://selenium-python.readthedocs.io/getting-started.html

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time  # 시간 지연을 위해
import urllib.request

driver = webdriver.Chrome()  # 크롬으로 다룰 것이기 때문에
driver.get("https://www.google.co.kr/imghp?hl=en&tab=wi&ogbl")
elem = driver.find_element_by_name("q")  # 구글 내에서 어떤 검색어 창 가져와
elem.send_keys("대한민국 태극기")  # 검색창에 '태극기' 입력
elem.send_keys(Keys.RETURN)  # 엔터를 누름

### 이제 각각의 img를 다운로드 받아보자. ###

# (1) 스크롤을 내리면서 50 장 이상의 이미지를 다운로드 받게 하자!
# https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python
#####################################################################################################

SCROLL_PAUSE_TIME = 1  # 스크롤이 충분히 될 수 있도록 지연 시간을 늘려준다.

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")  # 자바스크립트 코드 실행. 브라우저의 높이를 자바스크립트로 찾음

while True:  # 무한 반복
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # 브라우저 끝까지 스크롤 내림

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")  # 새로 구한 높이

    if new_height == last_height:  # 이전 높이 = 새 높이는 스크롤이 끝까지 갔다는 것을 함축
        try:
            driver.find_element_by_css_selector("mye4qd").click()  # 그러할 때, 결과 더 보기를 클릭. mye..은 그것에 대한 css
        except:  # 위 코드를 시도했는데, 실패할 경우 (스크롤이 다 내려간 경우) 중단
            break
    last_height = new_height  # 그렇지 않으면 스크롤 내림

##############################################################################################

# (2) 작은 이미지 클릭 (f12에서 태그의 특징이 무엇인지 확인)
# (3) 클릭
# driver.find_elements_by_css_selector(".rg_i.Q4LuWd")[0].click() # inspector > css class check. [0]을 씀으로써 첫 번째 사진만을 클릭
images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")

cnt = 1
for img in images:  # 개개의 이미지를 순서대로

    try:
        img.click()  # 하나 클릭
        time.sleep(2)  # 2초 지연
        imgUrl = driver.find_element_by_xpath('/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img').get_attribute("src")
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(imgUrl, "./crawled_img/flag"+str(cnt) + ".jpg")  # 해당 이미지를 다운로드
        cnt = cnt + 1

    except:
        pass



driver.close()  # 웹 닫기
