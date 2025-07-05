from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

class DriverManager:
    def __init__(self):
        self.driver = None

    def start_driver(self):
        if self.driver is None:
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            #options.add_argument('--log-level=1')  # info 이하 로그 숨김
            self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    def close_driver(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

    def get_driver(self):
        return self.driver
        
        
        
# @bp.route('/search',methods=['POST'])
# def search():
#     query= request.form['query']
#     chords = [item.strip() for item in query.split(',')]
#     print("chords",chords)
    
#     init_driver()
#     image_urls=[]
#     try:
#         for c in chords:
#             image_urls.append(crawl_images2("기타"+ c + "코드" ))
#         #image_urls = crawl_images_for_chords(chords)
#     except:# 쿼리문내부에 콤마로 문자열이 나뉘지 않은경우
#         image_urls = crawl_images2("기타 "+ query + "코드")
    
#     close_driver()
#     return render_template('result.html',images = image_urls, query=chords)


# def crawl_images2(query):
#     print('crawl2222222')
#     global driver
#     try:
#         # driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
#         from urllib.parse import quote
#         encoded_query = quote(query) #기타의 #같은 특수문자를 인식을 못해서 인코딩해줌
#         url = f"https://www.google.com/search?hl=ko&tbm=isch&q={encoded_query}"
        
    
#         driver.get(url)
#         WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.XPATH, "//img[contains(@class, 'YQ4gaf')]")))
        
#         img_elements = driver.find_elements(By.XPATH, "//img[contains(@class, 'YQ4gaf')]")#[contains(@class, 'YQ4gaf')]
        
#         print("good222")
#         iurl=[]
#         i=0 #보니까 img_elements에서 이미지를 제한을 해버리면 그 페이지에 있는 이상한 이미지들도 전부다 가져와버린다. 그래서 i를 이용해 3장이상 추가되지 않게끔 바꿈/ 여기서 조정을 할 수 있는 기능을 넣어도 좋겟다.
#         for img in img_elements:
#             img_url = img.get_attribute('src')  # URL 추출
            
#             alt_text = img.get_attribute('alt') #유튜브 섬네일이미지가 추출되는것을 방지하기 위함 alt요소에 항상 사이트의 출처가 적힌 특징이있었음
        
#             natural_width = int(img.get_attribute('naturalWidth'))  # 'YQ4gaf' 이 클래스에 내가원하지 않는 이미지들이 존재해서 사이즈가 너무 작은 이미지들은 거르기 위해 사용
#             natural_height = int(img.get_attribute('naturalHeight'))
            
#             if img_url and not (natural_width < 100 and natural_height <100) and "YouTube" not in alt_text:  # 높이 넓이가 100픽셀 이하면 이미지 url에 추가하지 않는다. /유튜브 섬네일도 추가 안함
#                 iurl.append(img_url)  # 리스트에 추가
#                 i+=1
#                 if i==5:#5개의 이미지 추출
#                     break
#         return iurl
#     except Exception as e:
#         print(f"Error during image crawling: {e}")
#         return []
    