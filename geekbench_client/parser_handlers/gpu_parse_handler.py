from collections import defaultdict
from .parse_utils import _basic_handler, _table_handler, _benchmark_scores_table_handler

def gpu_parse_handler(element:str, index:int) -> str:
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
    ).get_text(strip=False).replace("\n", " ") # 여백 제거 비활성화, 여백 제거는 date parse 후에 제거시도, 안 그러면 오류떠요.
    
    # 플랫폼 서브 타이틀
    platform_sub_title = element.select_one(
        selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div:nth-child(2) > div:nth-child(%s) > div > div > div:nth-child(3) > span.list-col-subtitle" % index
    ).get_text(strip=True) # 여백 제거
    
    # 플랫폼 이름
    platform_name = element.select_one(
        selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div:nth-child(2) > div:nth-child(%s) > div > div > div:nth-child(3) > span.list-col-text" % index
    ).get_text(strip=True) # 여백 제거 
    
    # api 서브 타이틀
    api_sub_title = element.select_one(
        selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div:nth-child(2) > div:nth-child(%s) > div > div > div:nth-child(4) > span.list-col-subtitle" % index
    ).get_text(strip=True) # 여백 제거
    
    # api 이름
    api_name = element.select_one(
        selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div:nth-child(2) > div:nth-child(%s) > div > div > div:nth-child(4) > span.list-col-text" % index
    ).get_text(strip=True) # 여백 제거

    # api 점수 서브 타이틀
    api_score_sub_title = element.select_one(
        selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div:nth-child(2) > div:nth-child(%s) > div > div > div:nth-child(5) > span.list-col-subtitle-score" % index
    ).get_text(strip=True) # 여백 제거
    
    # api 점수
    api_score = element.select_one(
        selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div:nth-child(2) > div:nth-child(%s) > div > div > div:nth-child(5) > span.list-col-text-score" % index
    ).get_text(strip=True) # 여백 제거

    # 링크
    gb6_data_url = "https://browser.geekbench.com" + element.select_one(
        selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div:nth-child(2) > div:nth-child(%s) > div > div > div.col-12.col-lg-4 > a" % index
    )["href"]
    
    return (
            (system_sub_title,
            uploaded_sub_title,
            platform_sub_title,
            api_sub_title,
            api_score_sub_title),
            
            (model_name,
            cpu_info,
            uploaded_time,
            platform_name,
            api_name,
            api_score),
            
            gb6_data_url
            )


# 구분 ---------------------------------

def latest_gpu_parse_handler(element:str, index:int) -> str:
    # 시스템 서브 타이틀
    system_sub_title = element.select_one(
        selector="#wrap > div > div > div:nth-child(1) > div > div:nth-child(%s) > div > div > div.col-12.col-lg-4 > span.list-col-subtitle" % index
    ).get_text(strip=True) # 여백 제거
    
    # 모델 이름
    model_name = element.select_one(
        selector="#wrap > div > div > div:nth-child(1) > div > div:nth-child(%s) > div > div > div.col-12.col-lg-4 > a" % index
    ).get_text(strip=True) # 여백 제거
    
    # cpu 일반정보
    cpu_info = element.select_one(
        selector="#wrap > div > div > div:nth-child(1) > div > div:nth-child(%s) > div > div > div.col-12.col-lg-4 > span.list-col-model" % index
    ).get_text(strip=True).replace("\n", " ") # 여백 제거
    
    # 업로드 시간 서브 타이틀
    uploaded_sub_title = element.select_one(
        selector="#wrap > div > div > div:nth-child(1) > div > div:nth-child(%s) > div > div > div:nth-child(2) > span.list-col-subtitle" % index
    ).get_text(strip=True) # 여백 제거
    
    # 업로드 시간
    uploaded_time = element.select_one(
        selector="#wrap > div > div > div:nth-child(1) > div > div:nth-child(%s) > div > div > div:nth-child(2) > span.list-col-text" % index
    ).get_text(strip=False).replace("\n", " ") # 여백 제거 비활성화, 여백 제거는 date parse 후에 제거시도, 안 그러면 오류떠요.
    
    # 플랫폼 서브 타이틀
    platform_sub_title = element.select_one(
        selector="#wrap > div > div > div:nth-child(1) > div > div:nth-child(%s) > div > div > div:nth-child(3) > span.list-col-subtitle" % index
    ).get_text(strip=True) # 여백 제거
    
    # 플랫폼 이름
    platform_name = element.select_one(
        selector="#wrap > div > div > div:nth-child(1) > div > div:nth-child(%s) > div > div > div:nth-child(3) > span.list-col-text" % index
    ).get_text(strip=True) # 여백 제거 
    
    # api 서브 타이틀
    api_sub_title = element.select_one(
        selector="#wrap > div > div > div:nth-child(1) > div > div:nth-child(%s) > div > div > div:nth-child(4) > span.list-col-subtitle" % index
    ).get_text(strip=True) # 여백 제거
    
    # api 이름
    api_name = element.select_one(
        selector="#wrap > div > div > div:nth-child(1) > div > div:nth-child(%s) > div > div > div:nth-child(4) > span.list-col-text" % index
    ).get_text(strip=True) # 여백 제거

    # api 점수 서브 타이틀
    api_score_sub_title = element.select_one(
        selector="#wrap > div > div > div:nth-child(1) > div > div:nth-child(%s) > div > div > div:nth-child(5) > span.list-col-subtitle-score" % index
    ).get_text(strip=True) # 여백 제거
    
    # api 점수
    api_score = element.select_one(
        selector="#wrap > div > div > div:nth-child(1) > div > div:nth-child(%s) > div > div > div:nth-child(5) > span.list-col-text-score" % index
    ).get_text(strip=True) # 여백 제거

    # 링크
    gb6_data_url = "https://browser.geekbench.com" + element.select_one(
        selector="#wrap > div > div > div:nth-child(1) > div > div:nth-child(%s) > div > div > div.col-12.col-lg-4 > a" % index
    )["href"] # 여백 제거
    
    
    return (
            (system_sub_title,
            uploaded_sub_title,
            platform_sub_title,
            api_sub_title,
            api_score_sub_title),
            
            (model_name,
            cpu_info,
            uploaded_time,
            platform_name,
            api_name,
            api_score),
            
            gb6_data_url
            )


# 구분 ---------------------------------

# gpu 점수의 세부적인 데이터 Parse 처리자
def details_gpu_parse_handler(soup:str):
    data_temp = defaultdict(dict)

    main_column = soup.find(name="div", attrs={"class" : "primary col-lg-9 order-lg-first"})
    # 기본 정보
    basic_handler = _basic_handler(parent=main_column)
    data_temp["Basic Information"] = basic_handler
    
    table_cols = main_column.find_all(name="th", attrs={"class": "rounded-top"})
    headings = main_column.find_all(name="div", attrs={"class": "heading"})
    
    # 테이블 컬럼 텍스트 추출
    table_col = [x.get_text(strip=True) for x in table_cols]
    
    # 헤딩 텍스트 추출 및 "System Information" 제거
    heading = [x.find(name="h3").get_text(strip=True) for x in headings if x.find(name="h3").get_text(strip=True) != "System Information"]
    
    # "Result Information"을 찾아서 첫 번째에 삽입
    res_info_index = heading[heading.index("Result Information")]
    if res_info_index in heading:
        table_col.insert(0, res_info_index)
        heading.remove(res_info_index)

    # 0 ~ 3 테이블 정보
    # 0 = Result Information
    # 1 = System Information
    # 2 = CPU Information
    # 3 = Memory Information
    # 4 = ~ Information
    for index in range(5):
        table_handler = _table_handler(parent=main_column, index=index)
        data_temp[table_col[index]] = table_handler

    # 0 index
    # 0 = ~ Performance
    for index in range(1):
        benchmark_score_table = _benchmark_scores_table_handler(parent=main_column, index=index)
        data_temp[heading[index]] = benchmark_score_table
    
    return data_temp