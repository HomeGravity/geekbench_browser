from bs4 import BeautifulSoup
from collections import defaultdict


from .utils import *
from .parser_handlers.login_parse_handler import login_parse_handler
from .parser_handlers.cpu_parse_handler import cpu_parse_handler
from .parser_handlers.gpu_parse_handler import gpu_parse_handler
from .parser_handlers.ai_parse_handler import ai_parse_handler
from .parser_handlers.latest_cpu_parse_handler import latest_cpu_parse_handler
from .parser_handlers.latest_gpu_parse_handler import latest_gpu_parse_handler
from .parser_handlers.latest_ai_parse_handler import latest_ai_parse_handler

class Parser:
    def __init__(self) -> None:
        # 모든 데이터 저장
        self._all_data = defaultdict(dict)
        # 단일 데이터 저장
        # - search (검색)
        self._cpu_data = defaultdict(dict)
        self._gpu_data = defaultdict(dict)
        self._ai_data = defaultdict(dict)

        # - 상세한
        self._cpu_details_data = defaultdict(dict)
        self._gpu_details_data = defaultdict(dict)
        
        # - latest (최신)
        self._latest_cpu_data = defaultdict(dict)
        self._latest_gpu_data = defaultdict(dict)
        self._latest_ai_data = defaultdict(dict)

    # 로그인 구문분석
    def login_parse(self, html:str):
        soup = BeautifulSoup(markup=html, features="lxml")
        (
        param, 
        token, 
        submit_name, 
        submit_value, 
        login_name, 
        passwrod_name
        ) = login_parse_handler(soup=soup)
        
        return (
            param, 
            token, 
            submit_name, 
            submit_value, 
            login_name, 
            passwrod_name
            )
    
    # cpu 부분 데이터 구문 분석
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
                        "parsed date": extract_date(text=uploaded_time)
                    },
                    platform_sub_title: platform_name,
                    "scores" : {
                        single_core_sub_title: int(single_core_score),
                        multi_core_sub_title: int(multi_core_score)
                    }
                }
                
        
        # 데이터 추가
        self._add_data(
            page=page,
            data_name="GB6 CPU Results",
            all_data=self._all_data,
            data=self._cpu_data,
            data_temp=cpu_data_temp
            )
        

    # gpu 부분 데이터 구문 분석
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
                        "parsed date": extract_date(text=uploaded_time)
                    },
                    platform_sub_title: platform_name,
                    api_sub_title: api_name,
                    api_score_sub_title: int(api_score)
                }
                
        
        # 데이터 추가
        self._add_data(
            page=page,
            data_name="GB6 GPU Results",
            all_data=self._all_data,
            data=self._gpu_data,
            data_temp=gpu_data_temp
            )
        
    
    # ai 부분 데이터 구문 분석
    def ai_parse(self, html:str, page:str) -> dict:
        soup = BeautifulSoup(markup=html, features="lxml")
        
        # 임시 사전 생성
        ai_data_temp = defaultdict(dict)
        
        table = soup.find(name="table", attrs={"class": "table index-table"})
        tbody = table.find(name="tbody").find_all(name="tr") if table is not None else []

        # tr 개수만큼 반복합니다.
        for index, tr in enumerate(tbody, start=1):
            
            (
            model_name_column,
            framework_name_column,
            framework_score_1_column,
            framework_score_2_column,
            framework_score_3_column,
            model_name_row, 
            model_ap_row,
            framework_name_row,
            framework_score_1_row,
            framework_score_2_row,
            framework_score_3_row,
            gb6_data_url_row
            ) = ai_parse_handler(
                soup=soup,
                tr=tr,
                index=index
            )
            
            
            # 중복 방지를 위해 고유값인 url을 사용합니다.
            if gb6_data_url_row not in ai_data_temp:
                ai_data_temp[gb6_data_url_row] = {
                    model_name_column: {
                        "model name": model_name_row,
                        "model ap": model_ap_row
                    },
                    framework_name_column: framework_name_row,
                    "scores": {
                        framework_score_1_column: int(framework_score_1_row),
                        framework_score_2_column: int(framework_score_2_row),
                        framework_score_3_column: int(framework_score_3_row)
                    }
                }
        
        # 데이터 추가
        self._add_data(
            page=page,
            data_name="GB6 AI Results",
            all_data=self._all_data,
            data=self._ai_data,
            data_temp=ai_data_temp
            )
    

    # 상세한 정보 구문분석
    # CPU 상세한
    def cpu_details_parse(self, url:str, result_data:dict):
        # 데이터 추가
        self._add_data(
            data_name="GB6 CPU DETAILS Results",
            all_data=self._all_data,
            data=self._cpu_details_data,
            data_temp=result_data,
            url=url
            )
        
    # GPU 상세한
    def gpu_details_parse(self, url:str, result_data:dict):
        # 데이터 추가
        self._add_data(
            data_name="GB6 GPU DETAILS Results",
            all_data=self._all_data,
            data=self._gpu_details_data,
            data_temp=result_data,
            url=url
            )
    
    # 최신 CPU 데이터 반영 구문분석
    def latest_cpu_parse(self, html:str, page:str) -> dict:
        soup = BeautifulSoup(markup=html, features="lxml")

        # 임시 사전 생성
        latest_cpu_data_temp = defaultdict(dict)
        
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
            ) = latest_cpu_parse_handler(
                element=element,
                index=index
            )


            # 중복 방지를 위해 고유값인 url을 사용합니다.
            if gb6_data_url not in latest_cpu_data_temp:
                latest_cpu_data_temp[gb6_data_url] = {
                    system_sub_title: {
                        "model name": model_name,
                        "cpu info": cpu_info
                    },
                    uploaded_sub_title: {
                        "default date": uploaded_time.strip(),
                        "parsed date": extract_date(text=uploaded_time)
                    },
                    platform_sub_title: platform_name,
                    "scores" : {
                        single_core_sub_title: int(single_core_score),
                        multi_core_sub_title: int(multi_core_score)
                    }
                }

        # 데이터 추가
        self._add_data(
            page=page,
            data_name="GB6 LATEST CPU Results",
            all_data=self._all_data,
            data=self._latest_cpu_data,
            data_temp=latest_cpu_data_temp
            )


    # 최신 GPU 데이터 반영 구문분석
    def latest_gpu_parse(self, html:str, page:str) -> dict:
        soup = BeautifulSoup(markup=html, features="lxml")

        # 임시 사전 생성
        latest_gpu_data_temp = defaultdict(dict)

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
            ) = latest_gpu_parse_handler(
                element=element,
                index=index
            )
        
            # 중복 방지를 위해 고유값인 url을 사용합니다.
            if gb6_data_url not in latest_gpu_data_temp:
                latest_gpu_data_temp[gb6_data_url] = {
                    system_sub_title: {
                        "model name": model_name,
                        "cpu info": cpu_info
                    },
                    uploaded_sub_title: {
                        "default date": uploaded_time.strip(),
                        "parsed date": extract_date(text=uploaded_time)
                    },
                    platform_sub_title: platform_name,
                    api_sub_title: api_name,
                    api_score_sub_title: int(api_score)
                }

        # 데이터 추가
        self._add_data(
            page=page,
            data_name="GB6 LATEST GPU Results",
            all_data=self._all_data,
            data=self._latest_gpu_data,
            data_temp=latest_gpu_data_temp
            )

    # 최신 AI 데이터 반영 구문분석
    def latest_ai_parse(self, html:str, page:str) -> dict:
        soup = BeautifulSoup(markup=html, features="lxml")

        # 임시 사전 생성
        latest_ai_data_temp = defaultdict(dict)
        
        table = soup.find(name="table", attrs={"class": "table index-table"})
        tbody = table.find(name="tbody").find_all(name="tr") if table is not None else []
        
        # tr 개수만큼 반복합니다.
        for index, tr in enumerate(tbody, start=1):

            (
            uploaded_name_column,
            model_name_column,
            framework_name_column,
            framework_score_1_column,
            framework_score_2_column,
            framework_score_3_column,
            uploaded_name_row,
            model_name_row, 
            model_ap_row,
            framework_name_row,
            framework_score_1_row,
            framework_score_2_row,
            framework_score_3_row,
            gb6_data_url_row
            ) = latest_ai_parse_handler(
                soup=soup,
                tr=tr,
                index=index
            )
            
            
            # 중복 방지를 위해 고유값인 url을 사용합니다.
            if gb6_data_url_row not in latest_ai_data_temp:
                latest_ai_data_temp[gb6_data_url_row] = {
                    model_name_column: {
                        "model name": model_name_row,
                        "model ap": model_ap_row
                    },
                    uploaded_name_column: {
                        "default date": uploaded_name_row,
                        "parsed date": parse_full_date(text=uploaded_name_row)
                    },
                    framework_name_column: framework_name_row,
                    "scores": {
                        framework_score_1_column: int(framework_score_1_row),
                        framework_score_2_column: int(framework_score_2_row),
                        framework_score_3_column: int(framework_score_3_row)
                    }
                }


        # 데이터 추가
        self._add_data(
            page=page,
            data_name="GB6 LATEST AI Results",
            all_data=self._all_data,
            data=self._latest_ai_data,
            data_temp=latest_ai_data_temp
            )

    # 데이터 추가 함수
    def _add_data(self, page:int=None, data_name:str=None, all_data:dict=None, data:dict=None, data_temp:dict=None, url:str=None):

        # page 또는 url
        page_or_url = page if page is not None else url

        # 딕셔너리의 키 개수가 0개이면 빈 딕셔너리로 판단하여 추가하지 않음.
        if len(data_temp.keys()) != 0:
            # 모든 데이터 사전에 추가
            if page_or_url not in all_data[data_name]:
                all_data[data_name][page_or_url] = data_temp

            # 단일 데이터 사전에 추가
            if page_or_url not in data:
                data[page_or_url] = data_temp
                
    
    # 모든 데이터를 반환합니다.
    def emit_all_data(self):
        return self._all_data if len(self._all_data.keys()) != 0 else None
    
    # CPU 데이터 반환
    def emit_cpu_data(self):
        return self._cpu_data if len(self._cpu_data.keys()) != 0 else None
    
    # GPU 데이터 반환
    def emit_gpu_data(self):
        return self._gpu_data if len(self._gpu_data.keys()) != 0 else None
    
    # AI 데이터 반환
    def emit_ai_data(self):
        return self._ai_data if len(self._ai_data.keys()) != 0 else None
    
    # CPU DETAILS 데이터 반환
    def emit_cpu_details_data(self):
        return self._cpu_details_data if len(self._cpu_details_data.keys()) != 0 else None

    # GPU DETAILS 데이터 반환
    def emit_gpu_details_data(self):
        return self._gpu_details_data if len(self._gpu_details_data.keys()) != 0 else None

    # LATEST CPU 데이터 반환
    def emit_latest_cpu_data(self):
        return self._latest_cpu_data if len(self._latest_cpu_data.keys()) != 0 else None
    
    # LATEST GPU 데이터 반환
    def emit_latest_gpu_data(self):
        return self._latest_gpu_data if len(self._latest_gpu_data.keys()) != 0 else None
    
    # LATEST AI 데이터 반환
    def emit_latest_ai_data(self):
        return self._latest_ai_data if len(self._latest_ai_data.keys()) != 0 else None