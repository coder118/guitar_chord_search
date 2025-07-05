from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..utils.driver_manager import DriverManager
from ..crawl import url_set


def crawl_images(chord,sub_chord_information,driver_manager):
    print('crawl2222222')
    
    try:
        #url = url_set.url_setting(chord)#여러개의 url 경로가 만들어지기에, 각 url을 리스트로 묶어준다.
        
        url = url_set.url_setting2(sub_chord_information)# 다른 사이트경로로 들어가서 크롤링할 경우.
        
        driver = driver_manager.get_driver()
        if driver is None:
            print("Driver initialization failed.")
            return []
        
        print(f"Crawling URL: {url}")
        driver.get(url)

        
        # pagination = driver.find_elements(By.CSS_SELECTOR, 'nav ul li')
        # page_numbers = [li for li in pagination if li.text.isdigit()]
        # last_page = int(page_numbers[-1].text) if page_numbers else 1
        
        
        # print("페이지 수 구하기",page_numbers,last_page)
        # print(page_numbers[-1].text)
        last_page= get_last_page(driver)
        iurl=[]
        for page in range(1, last_page + 1):
        
            # 이미지 요소가 로드될 때까지 대기
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'img')))
            
            # 이미지 요소 찾기
            img_elements=driver.find_elements(By.TAG_NAME, 'img')#반복문을 통해서 이미지가 계속 추가되도록
           #print('이미지 요소 타입 정보',type(img_elements),img_elements)
            
            
            for img in img_elements:    
                width = img.size['width']
                height = img.size['height']
                if width >= 200 and height >= 200:#너무 작은 이미지를 거른다.
                    img_url = img.get_attribute('src')
                    iurl.append(img_url)#코드의 url 정보를 iurl리스트로 묶는다.
            
            if page < last_page:
            # 다음 페이지 버튼 클릭 (예: '다음' 버튼 XPATH)
                print(f"{page+1}번 페이지로 이동")
                page_btn_xpath = f'/html/body/div[1]/nav/ul/li[{page+2}]/a'
                next_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, page_btn_xpath))
                )
                next_btn.click()
                print("현재 URL:", driver.current_url)
        
        if not img_elements:
            print("이미지가 존재하지 않습니다. 반복문을 실행하지 않습니다.")
            return []
        
        

        return iurl
        
    except Exception as e:
        print(f"Error during image crawling: {e}")
        return []
    
def get_last_page(driver):
    print("마지막 페이지 찾기 함수 실행")
    last_btn = driver.find_element(By.CSS_SELECTOR, 'ul.pagination li:last-child a')
    last_btn.click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.pagination li.active'))
    )
    last_page = int(driver.find_element(By.CSS_SELECTOR, 'ul.pagination li.active').text)
    print(last_page,"현 url위치",driver.current_url)
    # 다시 1페이지로 돌아가기
    first_btn = driver.find_element(By.CSS_SELECTOR, 'ul.pagination li a')
    first_btn.click()
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'ul.pagination li.active'), '1')
    )
    print("일 페이지로 돌아왔는가? 현 url위치",driver.current_url)
    
    return last_page