from bs4 import BeautifulSoup
from collections import OrderedDict

def date_parse(text):
    from datetime import datetime
    import re
    
    # 생성일자 텍스트 변경
    date_string = re.search(r'(\b\w{3} \d{1,2}, \d{4}\b)', text).group()
    date_strptime = datetime.strptime(date_string, "%b %d, %Y")
    return f"{date_strptime.year}-{date_strptime.month}-{date_strptime.day}"

class Parser:
    def __init__(self) -> None:
        gb6_data = OrderedDict()
    
    def cpu_parse(self, html):
        soup = BeautifulSoup(markup=html, features="lxml")
        
        # 임시 저장
        gb6_temp = OrderedDict()
        
        # 열(col) 개수만큼 반복합니다.
        for index, element in enumerate(
            soup.find_all(name="div", attrs={"class": "col-12 list-col"}),
            start=1
            ):
            
            # 시스템 서브 타이틀
            system_sub_title = element.select_one(
                selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div:nth-child(2) > div:nth-child(%s) > div > div > div.col-12.col-lg-4 > span.list-col-subtitle" % index
            ).get_text(strip=True) # 여백 제거
            
            # 모델 이름
            model_name = element.select_one(
                selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div:nth-child(2) > div:nth-child(%s) > div > div > div.col-12.col-lg-4 > a" % index
            ).get_text(strip=True) # 여백 제거
            
            # cpu 일반정보
            cpu_info = element.select_one(
                selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div:nth-child(2) > div:nth-child(%s) > div > div > div.col-12.col-lg-4 > span.list-col-model" % index
            ).get_text(strip=True).replace("\n", " ") # 여백 제거
            
            # 업로드 시간 서브 타이틀
            uploaded_sub_title = element.select_one(
                selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div:nth-child(2) > div:nth-child(%s) > div > div > div:nth-child(2) > span.list-col-subtitle" % index
            ).get_text(strip=True) # 여백 제거
            
            # 업로드 시간
            uploaded_time = element.select_one(
                selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div:nth-child(2) > div:nth-child(%s) > div > div > div:nth-child(2) > span.list-col-text" % index
            ).get_text(strip=True).replace("\n", " ") # 여백 제거
            
            # 플랫폼 서브 타이틀
            platform_sub_title = element.select_one(
                selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div:nth-child(2) > div:nth-child(%s) > div > div > div:nth-child(3) > span.list-col-subtitle" % index
            ).get_text(strip=True) # 여백 제거
            
            # 플랫폼 이름
            platform_name = element.select_one(
                selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div:nth-child(2) > div:nth-child(%s) > div > div > div:nth-child(3) > span.list-col-text" % index
            ).get_text(strip=True) # 여백 제거 
            
            # 싱글코어 서브 타이틀
            single_core_sub_title = element.select_one(
                selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div:nth-child(2) > div:nth-child(%s) > div > div > div:nth-child(4) > span.list-col-subtitle-score" % index
            ).get_text(strip=True) # 여백 제거
            
            # 싱글코어 점수
            single_core_score = element.select_one(
                selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div:nth-child(2) > div:nth-child(%s) > div > div > div:nth-child(4) > span.list-col-text-score" % index
            ).get_text(strip=True) # 여백 제거

            # 멀티코어 서브 타이틀
            multi_core_sub_title = element.select_one(
                selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div:nth-child(2) > div:nth-child(%s) > div > div > div:nth-child(5) > span.list-col-subtitle-score" % index
            ).get_text(strip=True) # 여백 제거
            
            # 멀티코어 점수
            multi_core_score = element.select_one(
                selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div:nth-child(2) > div:nth-child(%s) > div > div > div:nth-child(5) > span.list-col-text-score" % index
            ).get_text(strip=True) # 여백 제거

            # 링크
            gb6_data_url = "https://browser.geekbench.com" + element.select_one(
                selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div:nth-child(2) > div:nth-child(%s) > div > div > div.col-12.col-lg-4 > a" % index
            )["href"] # 여백 제거
            
            print(system_sub_title)
            print(model_name)
            print(cpu_info)
            print(uploaded_sub_title)
            print(uploaded_time, date_parse(uploaded_time))
            print(platform_sub_title)
            print(platform_name)
            print(single_core_sub_title)
            print(single_core_score)
            print(multi_core_sub_title)
            print(multi_core_score)
            print(gb6_data_url) 
            print()