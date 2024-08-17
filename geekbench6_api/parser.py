from bs4 import BeautifulSoup
from collections import defaultdict

from utils import *

class Parser:
    def __init__(self) -> None:
        # 모든 데이터 저장
        self.gb6_all_data = defaultdict(dict)
        # 단일 데이터 저장
        self.cpu_data = defaultdict(dict)
        self.gpu_data = defaultdict(dict)
        self.ml_data = defaultdict(dict)
        self.ai_data = defaultdict(dict)
    
    # cpu 부분 데이터
    def cpu_parse(self, html:str, page:str):
        soup = BeautifulSoup(markup=html, features="lxml")
        
        # 임시 사전 생성
        cpu_data_temp = defaultdict(dict)
        
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
            
            
            # 중복 방지를 위해 고유값인 url을 사용합니다.
            if gb6_data_url not in cpu_data_temp:
                cpu_data_temp[gb6_data_url] = {
                    system_sub_title: {
                        "model name": model_name,
                        "cpu info": cpu_info
                    },
                    uploaded_sub_title: {
                        "default date": uploaded_time,
                        "parsed date": date_parse(text=uploaded_time)
                    },
                    platform_sub_title: platform_name,
                    single_core_sub_title: single_core_score,
                    multi_core_sub_title: multi_core_score
                }
                
        

        # 페이지에 데이터 추가
        if page not in self.gb6_all_data["GB6 CPU Results"]:
            self.gb6_all_data["GB6 CPU Results"][page] = cpu_data_temp

        # 단일 데이터 사전에 추가
        if page not in self.cpu_data:
            self.cpu_data[page] = cpu_data_temp
        
        
        return self.cpu_data



    # gpu 부분 데이터
    def gpu_parse(self, html:str, page:str):
        pass
    
    # ml 부분 데이터
    def ml_parse(self, html:str, page:str):
        pass
    
    # ai 부분 데이터
    def ai_parse(self, html:str, page:str):
        pass
    

    # 모든 데이터를 반환합니다.
    def return_all_data(self):
        return self.gb6_all_data