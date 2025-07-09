from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..utils.driver_manager import DriverManager
from ..crawl import url_set


def crawl_images(chord,sub_chord_information, index):#,driver_manager
    print('crawl2222222')
    
    try:
        
        driver_manager = DriverManager()  # 각 스레드마다 새로운 드라이버 인스턴스 생성
        driver_manager.start_driver()
        driver = driver_manager.get_driver()
        
        url = url_set.url_setting2(sub_chord_information)# 다른 사이트경로로 들어가서 크롤링할 경우.
        
        if driver is None:
            print("Driver initialization failed.")
            return index, []
        
        print(f"Crawling URL: {url}")
        
        
        page_num = 1
        check = 0
        iurl=[]
        while True: #각 페이지마다 이미지를 뽑아오기 위해서.
            try:
                print("현재 url 주소",driver.current_url)
                driver.get(url)
                WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'img')))
            
                # 이미지 요소 찾기
                img_elements=driver.find_elements(By.TAG_NAME, 'img')#반복문을 통해서 이미지가 계속 추가되도록
                
                if not img_elements:
                    print("이미지가 더 이상 없습니다. 반복문 종료.")
                    break
                
                found_valid_image = False
                for img in img_elements:    
                    width = img.size['width']
                    height = img.size['height']
                    if width >= 200 and height >= 200:#너무 작은 이미지를 거른다.
                        img_url = img.get_attribute('src')
                        iurl.append(img_url)#코드의 url 정보를 iurl리스트로 묶는다.
                        found_valid_image = True
                        check+=1
                
                # 유효한(사이즈 조건을 만족하는) 이미지가 없으면 종료
                if not found_valid_image:
                    print("유효한 이미지가 더 이상 없습니다. 반복문 종료.")
                    break

                page_num +=1
                url=url_set.page_update(url,str(page_num)) #페이지를 업데이트해서 url을 새로 구성해준다. 
            except Exception as e: # 페이지가 존재하지 않는다면 이미지를 가져올떄 오류가 발생할 것.그때 반복문을 나온다. 
                    print("무한 반복문에서 빠져나오기.",e)
                    break
        
        if check ==0 : # 만약 위의 사이트에서 어떤 코드도 찾지 못했다면
            print("다른 사이트 접속")
            url = url_set.url_setting(chord) # 다른 사이트에서 찾는다. 
            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'img')))
        
            # 이미지 요소 찾기
            img_elements=driver.find_elements(By.TAG_NAME, 'img')
            
            for img in img_elements:    
                width = img.size['width']
                height = img.size['height']
                if width >= 200 and height >= 200:#너무 작은 이미지를 거른다.
                    img_url = img.get_attribute('src')
                    iurl.append(img_url)#코드의 url 정보를 iurl리스트로 묶는다.
                   

        return  index,iurl
        
    except Exception as e:
        print(f"Error during image crawling: {e}")
        return index,[]
    
    finally:
        driver_manager.close_driver()  # 드라이버 종료
    


#가지고 있는 문제점 xpath로 경로를 이동함. 페이지네이션이 슬라이딩 되는 구조라 인덱스 값이 이상해진다. 