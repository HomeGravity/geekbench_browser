from collections import defaultdict
from geekbench_client.utils import format_date

# 검색 cpu 데이터 parse 처리
def cpu_parse_handler(element:str, index:int) -> str:
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
    
    
    return (
            (system_sub_title,
            uploaded_sub_title,
            platform_sub_title,
            single_core_sub_title,
            multi_core_sub_title),
            
            (model_name,
            cpu_info,
            uploaded_time,
            platform_name,
            single_core_score,
            multi_core_score),
            
            gb6_data_url
            )


# 구분 ---------------------------------
# 최신순 또는 가장 높은 순으로 정렬된 cpu 데이터 parse 처리
def latest_or_top_cpu_parse_handler(element:str, index:int) -> str:
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
    
    # 싱글코어 서브 타이틀
    single_core_sub_title = element.select_one(
        selector="#wrap > div > div > div:nth-child(1) > div > div:nth-child(%s) > div > div > div:nth-child(4) > span.list-col-subtitle-score" % index
    ).get_text(strip=True) # 여백 제거
    
    # 싱글코어 점수
    single_core_score = element.select_one(
        selector="#wrap > div > div > div:nth-child(1) > div > div:nth-child(%s) > div > div > div:nth-child(4) > span.list-col-text-score" % index
    ).get_text(strip=True) # 여백 제거

    # 멀티코어 서브 타이틀
    multi_core_sub_title = element.select_one(
        selector="#wrap > div > div > div:nth-child(1) > div > div:nth-child(%s) > div > div > div:nth-child(5) > span.list-col-subtitle-score" % index
    ).get_text(strip=True) # 여백 제거
    
    # 멀티코어 점수
    multi_core_score = element.select_one(
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
            single_core_sub_title,
            multi_core_sub_title),
            
            (model_name,
            cpu_info,
            uploaded_time,
            platform_name,
            single_core_score,
            multi_core_score),
            
            gb6_data_url
            )



# 구분 ---------------------------------
# 기본 데이터 처리
def _basic_handler(parent:str):
    data_temp = defaultdict(dict)

    # 모델 이름
    data_temp["model name"] = parent.select_one(
        selector="#wrap > div > div.primary.col-lg-9.order-lg-first > div.page-header"
        ).find(name="h1").get_text(strip=True) # 여백제거

    # CPU 성능 데이터
    cpus = parent.find(name="div", attrs={"class" : "table-wrapper cpu"})
    names = cpus.find_all(name="div", attrs={"class": "note"})
    scores = cpus.find_all(name="div", attrs={"class": "score"})
    for col, row in zip(names, scores):
        data_temp["scores"][col.get_text(strip=True)] = int(row.get_text(strip=True)) # 여백제거
        
    # 플랫폼 데이터
    data_temp["platform info"] = cpus.find(name="div", attrs={"class" : "platform-info"}).get_text(strip=True) # 여백 제거

    return data_temp


# 테이블 데이터 처리
def _table_handler(parent:str, index:int):
    data_temp = defaultdict(dict)

    # 전체 테이블
    tables = parent.find_all(name="table", attrs={"class": "table system-table"})

    # 두 개의 클래스 목록을 정의
    class_pairs = [
        {"name": "system-name", "value": "system-value"},
        {"name": "name", "value": "value"}
    ]

    for tr in tables[index].find_all(name="tr"):
        col, row = None, None
        
        # 두 개의 클래스 쌍을 순회하며 데이터 찾기
        for classes in class_pairs:
            col = tr.find(name="td", attrs={"class": classes["name"]})
            row = tr.find(name="td", attrs={"class": classes["value"]})
            
            if (col is not None) and (row is not None):
                break  # 유효한 col, row를 찾으면 루프 종료

        if (col is not None) and (row is not None):
            # 텍스트가 업로드 시간이면
            if col.get_text(strip=True).upper() == "Upload Date".upper():
                data_temp["Dates"][col.get_text(strip=True)] = row.get_text(strip=True) # 여백제거
                data_temp["Dates"]["Parsed Date"] = format_date(text=row.get_text(strip=True), strpt="%B %d %Y %I:%M %p", strft="%Y-%m-%d %p %I:%M") # 여백제거

            # 로그 조회수 값을 정수형으로
            elif col.get_text(strip=True).upper() == "Views".upper():
                data_temp[col.get_text(strip=True)] = int(row.get_text(strip=True)) # 여백제거
                
            else:
                data_temp[col.get_text(strip=True)] = row.get_text(strip=True) # 여백제거
                
            
    return data_temp


# 벤치마크 세부적인 점수 테이블 처리
def _benchmark_scores_table_handler(parent:str, index:int):
    data_temp = defaultdict(dict)

    # 전체 테이블
    tables = parent.find_all(name="table", attrs={"class": "table benchmark-table"})
    for tr in tables[index].find_all("tr"):
        col = tr.find(name="td", attrs={"class": "name"})
        row = tr.find(name="td", attrs={"class": "score"})

        if (col is not None) and (row is not None): 
            task_name = col.get_text(strip=True)
            score, score_description = list(filter(lambda x: x.strip(),row.get_text(strip=False).split("\n")))
            data_temp[task_name] = {"score": int(score), "description": score_description}
        else:
            col = tr.find(name="th", attrs={"class": "name"})
            row = tr.find(name="th", attrs={"class": "score"})
            data_temp[col.get_text(strip=True)] = {"score": int(row.get_text(strip=True))}

    return data_temp


# cpu 점수의 세부적인 데이터 Parse 처리자
def details_cpu_parse_handler(soup:str):
    data_temp = defaultdict(dict)

    main_column = soup.find(name="div", attrs={"class" : "primary col-lg-9 order-lg-first"})
    # 기본 정보
    basic_handler = _basic_handler(parent=main_column)
    data_temp["Basic Information"] = basic_handler
    
    # 0 ~ 3 테이블 정보
    # 0 = Result Information
    # 1 = System Information
    # 2 = CPU Information
    # 3 = Memory Information
    col = ["Result Information", "System Information", "CPU Information", "Memory Information"]
    for index in range(4):
        table_handler = _table_handler(parent=main_column, index=index)
        data_temp[col[index]] = table_handler

    # 0 ~ 1 index
    # 0 = Single-Core Performance
    # 1 = Multi-Core Performance
    col = ["Single-Core Performance", "Multi-Core Performance"]
    for index in range(2):
        benchmark_score_table = _benchmark_scores_table_handler(parent=main_column, index=index)
        data_temp[col[index]] = benchmark_score_table
    
    return data_temp