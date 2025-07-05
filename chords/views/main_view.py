from flask import Blueprint,render_template,request
from ..utils.trans_chord import *
from ..utils.driver_manager import DriverManager
from ..crawl.image_crawling import crawl_images

bp = Blueprint('main', __name__, url_prefix='/')
driver_manager = DriverManager()  # 드라이버 매니저 인스턴스 생성

@bp.route('/search',methods=['POST','GET'])
def search_chord():
    print(request.form)
    chords= request.form['inform']
    chords_list = [item.strip() for item in chords.split(',')] #입력한 코드를 , 로 분리하여 리스트로 저장
    print("chords",chords_list)
    result = transform_chord(chords_list)
    print(result)
    
    sub_chord_information = chords_list
    
    driver_manager.start_driver()
    
    image_urls=[]
    try:
        for chord,chord2 in zip(result,sub_chord_information):
            print("첫번쨰 반복문 내부",chord)
            image_urls.append(crawl_images(chord,chord2,driver_manager))
    except:# 쿼리문내부에 콤마로 문자열이 나뉘지 않은경우
        image_urls = crawl_images(chords,driver_manager)
    
    driver_manager.close_driver()
    
    return render_template('result.html',images = image_urls, chord=chords_list)
    
@bp.route('/')
def index():
  
    
    return render_template('start.html')