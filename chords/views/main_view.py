from flask import Blueprint,render_template,request
from ..utils.trans_chord import *
from ..utils.driver_manager import DriverManager
from ..crawl.image_crawling import crawl_images
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures


bp = Blueprint('main', __name__, url_prefix='/')
#driver_manager = DriverManager()  # 드라이버 매니저 인스턴스 생성

@bp.route('/search',methods=['POST','GET'])
def search_chord():
    print(request.form)
    chords= request.form['inform']
    chords_list = [item.strip() for item in chords.split(',')] #입력한 코드를 , 로 분리하여 리스트로 저장
    
    result = transform_chord(chords_list)
    print("trans된 코드",result)
    
    sub_chord_information = chords_list
    print("코드의 나열",sub_chord_information)
    
    
    #driver_manager.start_driver() 멀티태스킹 사용하지 않을떄 
    
    # image_urls=[]
    image_urls = [[] for _ in range(len(chords_list))] #이미지의 url을 이중리스트에 저장할 수 있게 구현
    try:
        with ThreadPoolExecutor() as executor:
            futures=[]
            for i,(chord,chord2) in enumerate(zip(result, sub_chord_information)):
                print("첫번쨰 반복문 내부")
                # image_urls.append(crawl_images(chord,chord2,driver_manager))
                
                futures.append(executor.submit(crawl_images,chord,chord2,i))
                
            for future in concurrent.futures.as_completed(futures):
                # image_urls.append(future.result())
                index, images = future.result()
                image_urls[index] = images  # 올바른 인덱스에 이미지 저장
                
    except Exception as e:# 쿼리문내부에 콤마로 문자열이 나뉘지 않은경우
        # image_urls = crawl_images(chords,driver_manager)
        print('error',e)
    
    # driver_manager.close_driver()
    
    return render_template('result.html',images = image_urls, chord=chords_list)
    
@bp.route('/')
def index():
  
    
    return render_template('start.html')