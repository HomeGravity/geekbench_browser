# 날짜 데이터를 구문 분석
def date_parse(text):
    from datetime import datetime
    import re
    
    # 생성일자 텍스트 변경
    date_string = re.search(r'(\b\w{3} \d{1,2}, \d{4}\b)', text).group()
    date_strptime = datetime.strptime(date_string, "%b %d, %Y")
    return f"{date_strptime.year}-{date_strptime.month}-{date_strptime.day}"


# 들여쓰기 프린트
def indent_print(text, indent=4): # indent를 4로 설정
    import json
    print(json.dumps(text, indent=indent), "\n\n")