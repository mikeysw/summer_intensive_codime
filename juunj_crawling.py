from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from collections import OrderedDict
#from category_classification import getCat
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
import json
import subprocess
import shutil
import chromedriver_autoinstaller
import time

ua=UserAgent(verify_ssl=False)
userAgent = ua.random


subprocess.Popen(r'C:\Users\zihn\AppData\Local\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"') # 디버거 크롬 구동
#subprocess.Popen(r'C:\Program Files\Google\ChromeBeta\Application\chrome.exe --remote-debugging-port=9222') # 디버거 크롬 구동
chromedriver_autoinstaller.install()

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress","127.0.0.1:9222")

chrome_options.add_argument(f'user-agent={userAgent}')

# driver = webdriver.Chrome('C:/Users/zihn/Downloads/chromedriver_win3/chromedriver.exe',options=chrome_options)
driver = webdriver.Chrome(options=chrome_options)

with open('./0627상품/brandProductList_juunj.json', 'r', encoding='UTF-8') as make_file:
    item_list = json.load(make_file)

#json 파일 비었으면
#item_list = []

def hasElement(xpath):
    try:
        driver.find_element(by=By.XPATH, value=xpath)
        return True
    except:
        return False

start = 0
brandName = "Juunj"
url = "https://www.ssfshop.com/Juun-J/T-Shirts/list?dspCtgryNo=SFMA42A01&brandShopNo=BDMA07A11&brndShopId=ECBJC"
driver.get(url)
driver.implicitly_wait(3)
#setId = 0
setId = len(item_list)
for i in range(start,60):
    # url에서 i번째 item 클릭
    if hasElement('//*[@id="dspGood"]/li[{}]/a/span/img'.format(i+1)):
        button = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="dspGood"]/li[{}]/a/span/img'.format(i+1))))
        driver.execute_script("arguments[0].click()",button)
    else:
        current_url = driver.current_url
        try:
            # //*[@id="dspGood"]/li[14]/a/span/img
            # /html/body/div[4]/div[2]/section[2]/div[3]/div[1]/ul/li[23]/a/span/img
            # //*[@id="dspGood"]/li[3]/a/span/img
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="dspGood"]/li[{}]/a/img'.format(i+1)))).click()
        except:
            driver.get(current_url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="dspGood"]/li[{}]/a'.format(i+1)))).click()
    driver.implicitly_wait(1)
    # xpath로 이름과 제품 링크 보냄
    item = OrderedDict()
    prodName = WebDriverWait(driver,timeout=5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="goodDtlTitle"]'))).get_attribute('innerText')
    prodLink = driver.current_url
    # xpath로 제품의 카테고리를 파악함
    '''
    제품의 카테고리
    //*[@id="location"] -> 이 부분은 전체 다 동일함
    하의 xpath: //*[@id="location"]
    제품의 이름
    xpath1: //*[@id="goodDtlTitle"] -> 이부분은 전체다 동일함.
    하의 xpath: //*[@id="goodDtlTitle"]
    '''
    try:
        prodCatNum = len(driver.find_elements(by=By.XPATH, value='//*[@id="location"]/span'))
        prodCat1 = driver.find_element(by=By.XPATH, value='//*[@id="location"]/span[{}]'.format(prodCatNum - 2)).text
        prodCat2 = driver.find_element(by=By.XPATH, value='//*[@id="location"]/span[{}]'.format(prodCatNum)).text
        prodMidCat = driver.find_element(by=By.XPATH, value='//*[@id="location"]/span[{}]'.format(prodCatNum - 1)).text

        if ("아우터" in prodCat1 or "재킷/베스트" in prodCat1):
            print("continue")
            driver.back()
            driver.implicitly_wait(2)
            continue

        if ("카디건" in prodCat2 or "베스트" in prodCat2):
            print("continue")
            driver.back()
            driver.implicitly_wait(2)
            continue
    except:
        prodCat2 = "팬츠"

    #모델 착샷 없음의 기준: 사진 10장 이내 // 사진 있는가? // 반팔인 경우는 9개까지 있고, 민소매의 경우는 8개
    '''
    이게 왜 안될지 생각해봤는데, 제품 착샷 목록에 동영상이 있으면 xpath 숫자가 달라지는 듯함.
    착샷 메인 사진://*[@id="content"]/section[2]/div[1]/div[1]/div[4]/div[1]/ul/li[1]/a/img
    전면 사진: //*[@id="content"]/section[2]/div[1]/div[1]/div[4]/div[3]/ul/li[3]/a/img
    착샷 전면 사진(동영상 x): //*[@id="content"]/section[2]/div[1]/div[1]/div[3]/div[3]/ul/li[3]/a/img
    //*[@id="content"]/section[2]/div[1]/div[1]/div[3]/div[3]/ul/li[5]/a/img
    idea: try-except 사용
    '''

    if not (hasElement('//*[@id="content"]/section[2]/div[1]/div[1]/div[3]/div[3]/ul/li[8]/a/img')
            or hasElement('//*[@id="content"]/section[2]/div[1]/div[1]/div[4]/div[3]/ul/li[8]/a/img')):
        print("continue")
        driver.back()
        driver.implicitly_wait(2)
        continue

    #elif ("반팔" in prodCat2 or "민소매" in prodCat2) and ("티셔츠" in prodMidCat) and not (hasElement('//*[@id="content"]/section[2]/div[1]/div[1]/div[3]/div[3]/ul/li[8]/a/img')):
    #    print("continue")
    #    driver.back()
    #    driver.implicitly_wait(2)
    #    continue

    #본격 크롤링
    rel_prodCatNum = 0
    rel_prodCat = ""
    rel_items = []
    if ("원피스" in prodMidCat):
        # 1번째 이미지 불러오기
        # //*[@id="content"]/section[2]/div[1]/div[1]/div[3]/div[1]/ul/li[1]/a/img
        # /html/body/div[4]/div[2]/section[2]/div[1]/div[1]/div[4]/div[1]/ul/li[1]/a/img
        # //*[@id="content"]/section[2]/div[1]/div[1]/div[4]/div[1]/ul/li[1]/a/img
        try:
            modelImgUrl = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="content"]/section[2]/div[1]/div[1]/div[3]/div[1]/ul/li[1]/a/img'))).get_attribute(
                'src')
            # 2번째 이미지 불러오기
            WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="content"]/section[2]/div[1]/div[1]/div[3]/div[3]/ul/li[2]/a/img'))).click()
            driver.implicitly_wait(1)
            itemImgUrl = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="content"]/section[2]/div[1]/div[1]/div[3]/div[1]/ul/li[2]/a/img'))).get_attribute(
                'src')
            # 3번째 이미지 불러오기
            WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="content"]/section[2]/div[1]/div[1]/div[3]/div[3]/ul/li[4]/a/img'))).click()
            driver.implicitly_wait(1)
            sideImgUrl = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="content"]/section[2]/div[1]/div[1]/div[3]/div[1]/ul/li[4]/a/img'))).get_attribute(
                'src')
            # 4번째 이미지 불러오기
            WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="content"]/section[2]/div[1]/div[1]/div[3]/div[3]/ul/li[5]/a/img'))).click()
            driver.implicitly_wait(1)
            backImgUrl = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="content"]/section[2]/div[1]/div[1]/div[3]/div[1]/ul/li[5]/a/img'))).get_attribute(
                'src')
        except:
            # //*[@id="content"]/section[2]/div[1]/div[1]/div[4]/div[3]/ul/li[3]/a/img
            modelImgUrl = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="content"]/section[2]/div[1]/div[1]/div[4]/div[1]/ul/li[1]/a/img'))).get_attribute(
                'src')
            # 2번째 이미지 불러오기
            WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="content"]/section[2]/div[1]/div[1]/div[4]/div[3]/ul/li[2]/a/img'))).click()
            driver.implicitly_wait(1)
            itemImgUrl = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="content"]/section[2]/div[1]/div[1]/div[4]/div[1]/ul/li[2]/a/img'))).get_attribute(
                'src')
            # 3번째 이미지 불러오기
            WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="content"]/section[2]/div[1]/div[1]/div[4]/div[3]/ul/li[4]/a/img'))).click()
            driver.implicitly_wait(1)
            sideImgUrl = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="content"]/section[2]/div[1]/div[1]/div[4]/div[1]/ul/li[4]/a/img'))).get_attribute(
                'src')
            # 4번째 이미지 불러오기
            WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="content"]/section[2]/div[1]/div[1]/div[4]/div[3]/ul/li[5]/a/img'))).click()
            driver.implicitly_wait(1)
            backImgUrl = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="content"]/section[2]/div[1]/div[1]/div[4]/div[1]/ul/li[5]/a/img'))).get_attribute(
                'src')

        '''
        //*[@id="content"]/section[2]/div[1]/div[1]/div[3]/div[3]/ul/li[2]/a/img
        
        '''
    elif(hasElement('//*[@id="content"]/section[2]/div[1]/div[1]/div[3]/div[3]/ul/li[3]/a/img')):
        WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="content"]/section[2]/div[1]/div[1]/div[3]/div[3]/ul/li[3]/a/img'))).click()
        driver.implicitly_wait(1)
        modelImgUrl = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="content"]/section[2]/div[1]/div[1]/div[3]/div[1]/ul/li[3]/a/img'))).get_attribute(
            'src')
        # 2번째 이미지 불러오기
        WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="content"]/section[2]/div[1]/div[1]/div[3]/div[3]/ul/li[2]/a/img'))).click()
        driver.implicitly_wait(1)
        itemImgUrl = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="content"]/section[2]/div[1]/div[1]/div[3]/div[1]/ul/li[2]/a/img'))).get_attribute(
            'src')
        # 3번째 이미지 불러오기
        WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="content"]/section[2]/div[1]/div[1]/div[3]/div[3]/ul/li[4]/a/img'))).click()
        driver.implicitly_wait(1)
        sideImgUrl = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="content"]/section[2]/div[1]/div[1]/div[3]/div[1]/ul/li[4]/a/img'))).get_attribute(
            'src')
        # 4번째 이미지 불러오기
        WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="content"]/section[2]/div[1]/div[1]/div[3]/div[3]/ul/li[5]/a/img'))).click()
        driver.implicitly_wait(1)
        backImgUrl = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="content"]/section[2]/div[1]/div[1]/div[3]/div[1]/ul/li[5]/a/img'))).get_attribute(
            'src')
    elif(hasElement('//*[@id="content"]/section[2]/div[1]/div[1]/div[4]/div[3]/ul/li[3]/a/img')):
        WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="content"]/section[2]/div[1]/div[1]/div[4]/div[3]/ul/li[3]/a/img'))).click()
        driver.implicitly_wait(1)
        modelImgUrl = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="content"]/section[2]/div[1]/div[1]/div[4]/div[1]/ul/li[3]/a/img'))).get_attribute(
            'src')
        # 2번째 이미지 불러오기
        WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="content"]/section[2]/div[1]/div[1]/div[4]/div[3]/ul/li[2]/a/img'))).click()
        driver.implicitly_wait(1)
        itemImgUrl = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="content"]/section[2]/div[1]/div[1]/div[4]/div[1]/ul/li[2]/a/img'))).get_attribute(
            'src')
        # 3번째 이미지 불러오기
        WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="content"]/section[2]/div[1]/div[1]/div[4]/div[3]/ul/li[4]/a/img'))).click()
        driver.implicitly_wait(1)
        sideImgUrl = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="content"]/section[2]/div[1]/div[1]/div[4]/div[1]/ul/li[4]/a/img'))).get_attribute(
            'src')
        # 4번째 이미지 불러오기
        WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="content"]/section[2]/div[1]/div[1]/div[4]/div[3]/ul/li[5]/a/img'))).click()
        driver.implicitly_wait(1)
        backImgUrl = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="content"]/section[2]/div[1]/div[1]/div[4]/div[1]/ul/li[5]/a/img'))).get_attribute(
            'src')

    # 연관 상품 이미지 불러오기
    j = 1
    rel_items = []
    '''
    "코디 제안 상품"의 full xpath 위치가 일관적이지 않음
    Theory의 상황에서도 비슷한 상황이 연출되었으나, 그때와 달리 경우의 수가 3가지나 있음
    그리고 코디 제안 상품이 있다고 하더라도 클릭이 되지 않는 상황 발생
    이 경우는 위의 상황처럼 이미지에도 xpath가 여러 개 있어서 생기는 문제라고 생각
    해결책: xpath의 경우를 더 분할해서 생각해봐야 할 듯함
    try-except 구문 하나 만들어두고 복사해서 해봐야 할 듯
    그리고 이건 내 가설인데, full xpath의 div 값만 다른 게 아니라면...?
    '''
    '''
    코디 제안 상품 텍스트
    xpath1: //*[@id="shortcutRelation"]/div[1]/h3
    full-xpath1: /html/body/div[5]/div[1]/section[2]/div[2]/div[14]/div[1]/h3
    
    xpath2: //*[@id="shortcutRelation"]/div[1]/h3
    full-xpath2: /html/body/div[4]/div[1]/section[2]/div[2]/div[15]/div[1]/h3 
    
    코디 제안 상품 이미지 버튼
    이미지 버튼 xpath1: //*[@id="codiPath_GM0022022896840"]/img
    이미지 버튼 full-xpath1: /html/body/div[5]/div[1]/section[2]/div[2]/div[14]/div[1]/div[1]/div/div[1]/ul/li[1]/a/img
    이미지 버튼 xpath2: //*[@id="codiPath_GM0021122248296"]/img
    이미지 버튼 full-xpath2: /html/body/div[4]/div[1]/section[2]/div[2]/div[15]/div[1]/div[1]/div/div[1]/ul/li[1]/a/img
    이미지 버튼 full-xpath3: /html/body/div[4]/div[1]/section[2]/div[2]/div[14]/div[1]/div[1]/div/div[1]/ul/li[2]/a/img
    위의 상품의 full-xpath3:/html/body/div[4]/div[1]/section[2]/div[1]/div[1]/div[3]/div[1]/ul/li[1]/a/img
    이미지 버튼 full-xpath4:/html/body/div[4]/div[1]/section[2]/div[2]/div[14]/div[1]/div[1]/div/div[1]/ul/li[2]/a/img
    위 상품의 full-xpath4(동영상x):/html/body/div[4]/div[1]/section[2]/div[1]/div[1]/div[3]/div[1]/ul/li[1]/a/img
    
    /html/body/div[4]/div[2]/section[2]/div[2]/div[13]/div[1]/div[1]/div/div[1]/ul/li[2]/a/img
    
    //*[@id="content"]/section[2]/div[1]/div[1]/div[4]/div[3]/ul/li[2]/a/img
    '''
    # 입은 옷이 있는 경우
    if hasElement('/html/body/div[5]/div[2]/section[2]/div[2]/div[15]/div[1]/div[1]/div/div[1]/ul/li/a/img'):
        while(True):
            if ("코디 제안 상품" not in driver.find_element(by= By.XPATH, value='/html/body/div[5]/div[2]/section[2]/div[2]/div[15]/div[1]/h3').text):
                print("모델이 추가로 입고 있는 옷이 없습니다.")
                time.sleep(2)
                break
            if not hasElement('/html/body/div[5]/div[2]/section[2]/div[2]/div[15]/div[1]/div[1]/div/div[1]/ul/li[{}]/a/img'.format(j)):
                print("다음 옷이 없습니다.")
                time.sleep(2)
                break
            WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[5]/div[2]/section[2]/div[2]/div[15]/div[1]/div[1]/div/div[1]/ul/li[{}]/a/img'.format(j)))).click()
            driver.implicitly_wait(1)
            try:
                rel_prodCatNum = len(driver.find_elements(by=By.XPATH, value='//*[@id="location"]/span'))
                rel_prodCat = driver.find_element(by=By.XPATH,
                                                  value='//*[@id="location"]/span[{}]'.format(rel_prodCatNum - 1)).text
            except:
                j+=1
                driver.back()
                continue
            if ("재킷/베스트" in rel_prodCat or "아우터" in rel_prodCat or "여성 슈즈" in rel_prodCat or "여성 지갑" in rel_prodCat
                    or "여성 패션잡화" in rel_prodCat or "여성 가방" in rel_prodCat or "점퍼" in rel_prodCat or "남성 패션잡화" in rel_prodCat):
                j += 1
                driver.back()
                continue
            try:
                #//*[@id="content"]/section[2]/div[1]/div[1]/div[3]/div[3]/ul/li[2]/a/img
                #//*[@id="content"]/section[2]/div[1]/div[1]/div[3]/div[1]/ul/li[2]/a/img
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="content"]/section[2]/div[1]/div[1]/div[3]/div[3]/ul/li[2]/a/img'))).click()
                driver.implicitly_wait(1)
            except:
                #//*[@id="content"]/section[2]/div[1]/div[1]/div[4]/div[3]/ul/li[2]/a/img
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="content"]/section[2]/div[1]/div[1]/div[4]/div[3]/ul/li[2]/a/img'))).click()
                driver.implicitly_wait(1)
            try:
                relateImgUrl = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="content"]/section[2]/div[1]/div[1]/div[3]/div[1]/ul/li[2]/a/img'))).get_attribute(
                'src')
                time.sleep(2)
            except:
                #//*[@id="content"]/section[2]/div[1]/div[1]/div[4]/div[1]/ul/li[2]/a/img
                relateImgUrl = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="content"]/section[2]/div[1]/div[1]/div[4]/div[1]/ul/li[2]/a/img'))).get_attribute(
                    'src')
                time.sleep(2)
            rel_items.append({"category":rel_prodCat,"img_url":relateImgUrl})
            driver.back()
            time.sleep(2)
            j += 1
    elif hasElement('/html/body/div[4]/div[1]/section[2]/div[3]/div[14]/div[1]/div[1]/div/div[1]/ul/li/a/img'):
        #/html/body/div[4]/div[2]/section[2]/div[2]/div[14]/div[1]/div[1]/div/div[1]/ul/li/a/img
        #/html/body/div[4]/div[2]/section[2]/div[2]/div[14]/div[1]/div[1]/div/div[1]/ul/li[3]/a/img
        #/html/body/div[4]/div[2]/section[2]/div[2]/div[14]/div[1]/h3
        #/html/body/div[4]/div[1]/section[2]/div[3]/div[15]/div[1]/h3
        while (True):
            # xpath://*[@id="shortcutRelation"]/div[1]/h3
            # full xpath: /html/body/div[4]/div[2]/section[2]/div[2]/div[14]/div[1]/h3
            #/html/body/div[4]/div[2]/section[2]/div[2]/div[14]/div[1]/div[1]/div/div[1]/ul/li[1]/a/img
            # /html/body/div[4]/div[2]/section[2]/div[2]/div[15]/div[1]/h3
            #/html/body/div[4]/div[2]/section[2]/div[2]/div[14]/div[1]/h3
            if ("코디 제안 상품" not in driver.find_element(by=By.XPATH,
                                                      value='/html/body/div[4]/div[2]/section[2]/div[2]/div[14]/div[1]/h3').text):
                print("모델이 추가로 입고 있는 옷이 없습니다.")
                break
            # xpath:/html/body/div[4]/div[2]/section[2]/div[2]/div[14]/div[1]/div[1]/div/div[1]/ul/li[1]/a/img
            if not hasElement(
                    '/html/body/div[4]/div[2]/section[2]/div[2]/div[14]/div[1]/div[1]/div/div[1]/ul/li[{}]/a/img'.format(
                            j)):
                print("다음 옷이 없습니다.")
                time.sleep(2)
                break
            WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                (By.XPATH,
                 '/html/body/div[4]/div[2]/section[2]/div[2]/div[14]/div[1]/div[1]/div/div[1]/ul/li[{}]/a/img'.format(j)))).click()
            driver.implicitly_wait(1)
            time.sleep(2)
            try:
                rel_prodCatNum = len(driver.find_elements(by=By.XPATH, value='//*[@id="location"]/span'))
                rel_prodCat = driver.find_element(by=By.XPATH,
                                                  value='//*[@id="location"]/span[{}]'.format(rel_prodCatNum - 1)).text
            except:
                j += 1
                driver.back()
                continue
            if("재킷/베스트" in rel_prodCat or "아우터" in rel_prodCat or "여성 슈즈" in rel_prodCat or "여성 지갑" in rel_prodCat
                    or "여성 패션잡화" in rel_prodCat or "여성 가방" in rel_prodCat or "점퍼" in rel_prodCat or "남성 패션잡화" in rel_prodCat):
                j += 1
                driver.back()
                continue
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="content"]/section/div[1]/div[1]/div[3]/div[3]/ul/li[2]/a/img'))).click()
                driver.implicitly_wait(1)

                relateImgUrl = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                    (By.XPATH,
                     '//*[@id="content"]/section[2]/div[1]/div[1]/div[3]/div[1]/ul/li[2]/a/img'))).get_attribute(
                    'src')
                time.sleep(2)
            except:
                # 에러 뜨는 곳: //*[@id="content"]/section[2]/div[1]/div[1]/div[4]/div[3]/ul/li[2]/a/img
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="content"]/section[2]/div[1]/div[1]/div[4]/div[3]/ul/li[3]/a/img'))).click()
                driver.implicitly_wait(1)

                relateImgUrl = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                    (By.XPATH,
                     '//*[@id="content"]/section[2]/div[1]/div[1]/div[4]/div[1]/ul/li[3]/a/img'))).get_attribute(
                    'src')
                time.sleep(2)
            print(f"{j}번째 옷")
            rel_items.append({"category": rel_prodCat, "img_url": relateImgUrl})
            driver.back()
            j += 1
    elif hasElement('/html/body/div[4]/div[2]/section[2]/div[2]/div[13]/div[1]/div[1]/div/div[1]/ul/li/a/img'):
        while (True):
            if ("코디 제안 상품" not in driver.find_element(by=By.XPATH,
                                                      value='/html/body/div[4]/div[2]/section[2]/div[2]/div[13]/div[1]/h3').text):
                print("모델이 추가로 입고 있는 옷이 없습니다.")
                break
            if not hasElement(
                    '/html/body/div[4]/div[2]/section[2]/div[2]/div[13]/div[1]/div[1]/div/div[1]/ul/li[{}]/a/img'.format(
                            j)):
                print("다음 옷이 없습니다.")
                time.sleep(2)
                break
            WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                (By.XPATH,
                 '/html/body/div[4]/div[2]/section[2]/div[2]/div[13]/div[1]/div[1]/div/div[1]/ul/li[{}]/a/img'.format(j)))).click()
            driver.implicitly_wait(1)
            try:
                rel_prodCatNum = len(driver.find_elements(by=By.XPATH, value='//*[@id="location"]/span'))
                rel_prodCat = driver.find_element(by=By.XPATH,
                                                  value='//*[@id="location"]/span[{}]'.format(rel_prodCatNum - 1)).text
            except:
                j += 1
                driver.back()
                continue
            if("재킷/베스트" in rel_prodCat or "아우터" in rel_prodCat or "여성 슈즈" in rel_prodCat or "여성 지갑" in rel_prodCat
                    or "여성 패션잡화" in rel_prodCat or "여성 가방" in rel_prodCat or "점퍼" in rel_prodCat or "남성 패션잡화" in rel_prodCat):
                j += 1
                driver.back()
                continue
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="content"]/section/div[1]/div[1]/div[3]/div[3]/ul/li[2]/a/img'))).click()
                driver.implicitly_wait(1)

                relateImgUrl = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                    (By.XPATH,
                     '//*[@id="content"]/section[2]/div[1]/div[1]/div[3]/div[1]/ul/li[2]/a/img'))).get_attribute(
                    'src')
                time.sleep(2)
            except:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="content"]/section[2]/div[1]/div[1]/div[4]/div[3]/ul/li[3]/a/img'))).click()
                driver.implicitly_wait(1)

                relateImgUrl = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                    (By.XPATH,
                     '//*[@id="content"]/section[2]/div[1]/div[1]/div[4]/div[1]/ul/li[3]/a/img'))).get_attribute(
                    'src')
                time.sleep(2)
            rel_items.append({"category": rel_prodCat, "img_url": relateImgUrl})
            driver.back()
            j += 1
    elif hasElement('/html/body/div[4]/div[2]/section[2]/div[2]/div[15]/div[1]/div[1]/div/div[1]/ul/li[1]/a/img'):
        while (True):
            if("코디 제안 상품" not in driver.find_element(by=By.XPATH,
                                                     value='/html/body/div[4]/div[2]/section[2]/div[2]/div[15]/div[1]/h3').text):
                print("모델이 추가로 입고 있는 옷이 없습니다.")
                break
            if not hasElement(
                '/html/body/div[4]/div[2]/section[2]/div[2]/div[15]/div[1]/div[1]/div/div[1]/ul/li[{}]/a/img'.format(j)
            ):
                print("다음 옷이 없습니다.")
                break
            WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                (By.XPATH,
                 '/html/body/div[4]/div[2]/section[2]/div[2]/div[15]/div[1]/div[1]/div/div[1]/ul/li[{}]/a/img'.format(
                     j)))).click()
            driver.implicitly_wait(1)
            try:
                rel_prodCatNum = len(driver.find_elements(by=By.XPATH, value='//*[@id="location"]/span'))
                rel_prodCat = driver.find_element(by=By.XPATH,
                                                  value='//*[@id="location"]/span[{}]'.format(rel_prodCatNum - 1)).text
            except:
                j += 1
                driver.back()
                continue
            if("재킷/베스트" in rel_prodCat or "아우터" in rel_prodCat or "여성 슈즈" in rel_prodCat or "여성 지갑" in rel_prodCat
                    or "여성 패션잡화" in rel_prodCat or "여성 가방" in rel_prodCat or "점퍼" in rel_prodCat or "남성 패션잡화" in rel_prodCat):
                j += 1
                driver.back()
                continue
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="content"]/section[2]/div[1]/div[1]/div[3]/div[3]/ul/li[2]/a/img'))).click()
                driver.implicitly_wait(1)

                relateImgUrl = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                    (By.XPATH,
                     '//*[@id="content"]/section[2]/div[1]/div[1]/div[3]/div[1]/ul/li[2]/a/img'))).get_attribute(
                    'src')
                time.sleep(2)
            except:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="content"]/section[2]/div[1]/div[1]/div[4]/div[3]/ul/li[3]/a/img'))).click()
                driver.implicitly_wait(1)

                relateImgUrl = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                    (By.XPATH,
                     '//*[@id="content"]/section[2]/div[1]/div[1]/div[4]/div[1]/ul/li[3]/a/img'))).get_attribute(
                    'src')
                time.sleep(2)
            rel_items.append({"category": rel_prodCat, "img_url": relateImgUrl})
            driver.back()
            j += 1

    elif hasElement('/html/body/div[4]/div[1]/section[2]/div[3]/div[16]/div[1]/div[1]/div/div[1]/ul/li/a/img'):
        while (True):
            if ("코디 제안 상품" not in driver.find_element(by=By.XPATH,
                                                      value='/html/body/div[4]/div[1]/section[2]/div[3]/div[16]/div[1]/h3').text):
                print("모델이 추가로 입고 있는 옷이 없습니다.")
                break
            if not hasElement(
                    '/html/body/div[4]/div[1]/section[2]/div[3]/div[16]/div[1]/div[1]/div/div[1]/ul/li[{}]/a/img'.format(
                            j)):
                print("다음 옷이 없습니다.")
                time.sleep(2)
                break
            WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                (By.XPATH,
                 '/html/body/div[4]/div[1]/section[2]/div[3]/div[16]/div[1]/div[1]/div/div[1]/ul/li[{}]/a/img'.format(j)))).click()
            driver.implicitly_wait(1)
            try:
                rel_prodCatNum = len(driver.find_elements(by=By.XPATH, value='//*[@id="location"]/span'))
                rel_prodCat = driver.find_element(by=By.XPATH,
                                                  value='//*[@id="location"]/span[{}]'.format(rel_prodCatNum - 1)).text
            except:
                j += 1
                driver.back()
                continue
            if("재킷/베스트" in rel_prodCat or "아우터" in rel_prodCat or "여성 슈즈" in rel_prodCat or "여성 지갑" in rel_prodCat
                    or "여성 패션잡화" in rel_prodCat or "여성 가방" in rel_prodCat or "점퍼" in rel_prodCat or "남성 패션잡화" in rel_prodCat):
                j += 1
                driver.back()
                continue
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="content"]/section[2]/div[1]/div[1]/div[3]/div[3]/ul/li[2]/a/img'))).click()
                driver.implicitly_wait(1)

                relateImgUrl = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                    (By.XPATH,
                     '//*[@id="content"]/section[2]/div[1]/div[1]/div[3]/div[1]/ul/li[2]/a/img'))).get_attribute(
                    'src')
                time.sleep(2)
            except:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="content"]/section[2]/div[1]/div[1]/div[4]/div[3]/ul/li[3]/a/img'))).click()
                driver.implicitly_wait(1)

                relateImgUrl = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                    (By.XPATH,
                     '//*[@id="content"]/section[2]/div[1]/div[1]/div[4]/div[1]/ul/li[3]/a/img'))).get_attribute(
                    'src')
                time.sleep(2)
            rel_items.append({"category": rel_prodCat, "img_url": relateImgUrl})
            driver.back()
            j += 1
    else:
        rel_prodCat = "None"
        relateImgUrl = "None"

    prodName = prodName.split('\n')
    prodName = prodName[0]
    print(prodName)
    setId += 1
    item["set_id"] = setId
    item["link"] = prodLink
    item["model_img_front"] = modelImgUrl
    item["model_img_side"] = sideImgUrl
    item["model_img_back"] = backImgUrl
    item["items"] = [{"category": prodCat2, "img_url": itemImgUrl}, rel_items]

    item_list.append(item)

    with open('./0627상품/brandProductList_juunj.json', 'w+', encoding='UTF-8') as f:
        json.dump(item_list, f, ensure_ascii=False, indent='\t')

    print("새로운 상품 수 : <{}>{} {}".format(0, i + 1, prodName))
    driver.back()  # 목록 페이지로 되돌아가기
    driver.implicitly_wait(2)
    time.sleep(2)