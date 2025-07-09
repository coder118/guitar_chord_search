from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def url_setting(chord):
    
    base_url = "https://www.all-guitar-chords.com/chords/index"
    print("url setting!!!!!",chord) #보통 Gbm7이런식으로 값이 하나만 들어간다. 
    # 이중 배열을 순회하여 URL 생성
   
    root_chord=chord[0]
    sub = chord[1]

    # 두 번째 값 처리
    if sub == '':
        sub = 'major'  # 비어있으면 'major'로 설정
    elif sub == 'm':
        sub = 'minor'  # 'm'이면 'minor'로 변경

    # URL 조합
    chord_url = f"{base_url}/{root_chord}/{sub}"
    
    print("여기서 url 결과값 확인",chord_url)
    return chord_url

def url_setting2(chord):
    base_url ="https://jguitar.com/chordsearch?chordsearch="
    
    print('urlsetting2',chord)
    if '/' in chord or '#' in chord:
        chord=chord.replace('/', '%2F')
        chord=chord.replace('#','%23')
    
    chord_url = f"{base_url}{chord}"
    
    print("여기서 url 결과값 확인",chord_url)
    return chord_url
    
def page_update(url, page_number):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    query_params['page'] = [page_number]  # page 파라미터를 새 값으로 덮어씀
    new_query = urlencode(query_params, doseq=True)
    new_url = urlunparse(parsed_url._replace(query=new_query))
    return new_url
    

#https://jguitar.com/chordsearch/
# %2F => / 아스키코드