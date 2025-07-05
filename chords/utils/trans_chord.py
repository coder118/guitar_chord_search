import re
def transform_chord(chords):
    transformed_chords = []

    for chord in chords:
        
        chord = chord[0].upper() + chord[1:]#앞글자만 대문자로 변경
        
        if '#' in chord and chord[1] == '#':
            # '#'이 두 번째 위치에 있는 경우
            base_note = chord[0] + '_sharp'  # '#'을 '_sharp'으로 변환
            sharp_remaining = chord[2:]  # 나머지 부분
            sharp_remaining = transform_remaining(sharp_remaining)
            transformed_chords.append([base_note, sharp_remaining])  # 변환된 코드와 나머지를 리스트에 추가
        else:
            # '#'이 없는 경우, 기본 음과 추가 정보를 분리
            match = re.match(r'([A-G][b#]?)(.*)', chord)
            if match:
                base_note = match.group(1)  # 기본 음
                major_remaining = match.group(2)  # 추가 정보
                major_remaining = transform_remaining(major_remaining)  
                transformed_chords.append([base_note, major_remaining])  # 기본 음과 추가 정보를 리스트에 추가

    return transformed_chords

# 모든 #을 *로 바꿔줘야 한다. () 값내부의 값이 한개 일 경우는 ()를 생략하고 () 내부의 값이 2개 이상이면 %28,%29로 바꾼다. 
def transform_remaining(remaining):
    """
    주어진 문자열에서 '#'을 '*'로 바꾸고,
    괄호 처리 규칙에 따라 변환합니다.
    """
    # 모든 '#'을 '*'로 변환
    remaining = remaining.replace('#', '*')
    
    # 괄호 처리
    if '(' in remaining and ')' in remaining:
        # 괄호 내부의 값 추출
        inner_content = remaining[remaining.index('(')+1:remaining.index(')')]
        inner_parts = inner_content.split(',')
        
        if len(inner_parts) == 1:
            # 하나의 값일 경우 괄호 생략
            remaining = remaining.replace(f'({inner_content})', inner_content)
        elif len(inner_parts) > 1:
            # 두 개 이상의 값일 경우 %28, %29로 변경
            remaining = remaining.replace('(', '%28').replace(')', '%29')
    
    return remaining