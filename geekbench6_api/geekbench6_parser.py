from bs4 import BeautifulSoup
from collections import defaultdict

from utils import *
from parser_handlers.cpu_parse_handler import cpu_parse_handler
from parser_handlers.gpu_parse_handler import gpu_parse_handler
from parser_handlers.ai_parse_handler import ai_parse_handler


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
            ) = cpu_parse_handler(
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
                
        
        
        # 데이터 추가
        self._add_data(
            page=page,
            data_name="GB6 CPU Results",
            all_data=self.gb6_all_data,
            data=self.cpu_data,
            data_temp=cpu_data_temp
            )
        
        
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
            api_score,
            gb6_data_url
            ) = gpu_parse_handler(
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
                    api_score_sub_title: api_score
                }
                
        
        # 데이터 추가
        self._add_data(
            page=page,
            data_name="GB6 GPU Results",
            all_data=self.gb6_all_data,
            data=self.gpu_data,
            data_temp=gpu_data_temp
            )
        
        return self.gpu_data
    
    
    # ai 부분 데이터
    def ai_parse(self, html:str, page:str) -> dict:
        pass
    
    # 데이터 추가 함수
    def _add_data(self, page:int, data_name:str, all_data:dict, data:dict, data_temp:dict):
        # 모든 데이터 사전에 추가
        if page not in all_data[data_name]:
            all_data[data_name][page] = data_temp

        # 단일 데이터 사전에 추가
        if page not in data:
            data[page] = data_temp
    
    # 모든 데이터를 반환합니다.
    def return_all_data(self):
        return self.gb6_all_data