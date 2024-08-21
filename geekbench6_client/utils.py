# 날짜 데이터를 구문 분석
def date_parse(text:str) -> str:
    from datetime import datetime
    import re
    
    # 생성일자 텍스트 변경
    try:
        match = re.search(r'(\b\w{3} \d{1,2}, \d{4}\b)', text.strip())
        
        if match:  # 매칭 결과가 None이 아닐 경우
            date_string = match.group()
            date_strptime = datetime.strptime(date_string, "%b %d, %Y")
            return f"{date_strptime.year}-{date_strptime.month:02d}-{date_strptime.day:02d}"
        else:
            return None  # 매칭되지 않았을 경우 None 반환

    except ValueError:
        return None  # 날짜 구문 분석 실패 시 None 반환


# 들여쓰기 프린트
def indent_print(text:str, indent:int=4): # indent를 4로 설정
    import json
    print(json.dumps(text, indent=indent))


# 마지막 페이지 확인
def check_for_last_page(text:str) -> bool:
    from bs4 import BeautifulSoup
    import re
    
    soup = BeautifulSoup(text, "lxml")
    
    # 특정 텍스트가 포함된 경우 마지막 페이지로 판단.
    pattern = r"Your search did not match any .* results\." # 정규 표현식 패턴
    
    return re.search(pattern, soup.get_text(strip=True)) is not None  # 결과가 있으면 True 반환
