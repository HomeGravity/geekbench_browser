from bs4 import BeautifulSoup
from collections import defaultdict

from utils import *
from gb6_parse_scripts.cpu_parse import cpu_parse
from gb6_parse_scripts.gpu_parse import gpu_parse
from gb6_parse_scripts.ml_parse import ml_parse
from gb6_parse_scripts.ai_parse import ai_parse


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
    def cpu_parse(self, html:str, page:str) -> dict:
        soup = BeautifulSoup(markup=html, features="lxml")
        
        # 임시 사전 생성
        cpu_data_temp = defaultdict(dict)
        
        # 열(col) 개수만큼 반복합니다.
        for index, element in enumerate(
            soup.find_all(name="div", attrs={"class": "col-12 list-col"}),
            start=1
            ):
            
            (
                system_sub_title,
                model_name,
                cpu_info,
                uploaded_sub_title,
                uploaded_time,
                platform_sub_title,
                platform_name,
                single_core_sub_title,
                single_core_score,
                multi_core_sub_title,
                multi_core_score,
                gb6_data_url
            ) = cpu_parse(
                element=element,
                index=index
            )
            
            
            # 중복 방지를 위해 고유값인 url을 사용합니다.
            if gb6_data_url not in cpu_data_temp:
                cpu_data_temp[gb6_data_url] = {
                    system_sub_title: {
                        "model name": model_name,
                        "cpu info": cpu_info
                    },
                    uploaded_sub_title: {
                        "default date": uploaded_time.strip(),
                        "parsed date": date_parse(text=uploaded_time)
                    },
                    platform_sub_title: platform_name,
                    single_core_sub_title: single_core_score,
                    multi_core_sub_title: multi_core_score
                }
                
        
        
        # 모든 데이터 사전에 추가
        if page not in self.gb6_all_data["GB6 CPU Results"]:
            self.gb6_all_data["GB6 CPU Results"][page] = cpu_data_temp

        # 단일 데이터 사전에 추가
        if page not in self.cpu_data:
            self.cpu_data[page] = cpu_data_temp
        
        
        return self.cpu_data



    # gpu 부분 데이터
    def gpu_parse(self, html:str, page:str) -> dict:
        soup = BeautifulSoup(markup=html, features="lxml")
        
        # 임시 사전 생성
        gpu_data_temp = defaultdict(dict)
        
        # 열(col) 개수만큼 반복합니다.
        for index, element in enumerate(
            soup.find_all(name="div", attrs={"class": "col-12 list-col"}),
            start=1
            ):
            
            (
            system_sub_title,
            model_name,
            cpu_info,
            uploaded_sub_title,
            uploaded_time,
            platform_sub_title,
            platform_name,
            api_sub_title,
            api_name,
            api_score_sub_title,
            api_score_score,
            gb6_data_url
            ) = gpu_parse(
                element=element,
                index=index
            )
                
            
            # 중복 방지를 위해 고유값인 url을 사용합니다.
            if gb6_data_url not in gpu_data_temp:
                gpu_data_temp[gb6_data_url] = {
                    system_sub_title: {
                        "model name": model_name,
                        "cpu info": cpu_info
                    },
                    uploaded_sub_title: {
                        "default date": uploaded_time.strip(),
                        "parsed date": date_parse(text=uploaded_time)
                    },
                    platform_sub_title: platform_name,
                    api_sub_title: api_name,
                    api_score_sub_title: api_score_score
                }
                
        
        
        # 모든 데이터 사전에 추가
        if page not in self.gb6_all_data["GB6 GPU Results"]:
            self.gb6_all_data["GB6 GPU Results"][page] = gpu_data_temp

        # 단일 데이터 사전에 추가
        if page not in self.gpu_data:
            self.gpu_data[page] = gpu_data_temp
        
        
        return self.gpu_data
    
    # ml 부분 데이터
    def ml_parse(self, html:str, page:str) -> dict:
        pass
    
    # ai 부분 데이터
    def ai_parse(self, html:str, page:str) -> dict:
        pass
    

    # 모든 데이터를 반환합니다.
    def return_all_data(self):
        return self.gb6_all_data