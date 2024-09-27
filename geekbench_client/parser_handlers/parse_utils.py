from collections import defaultdict
from geekbench_client.utils import format_date

def _basic_handler(parent:str):
    data_temp = defaultdict(dict)

    # 모델 이름
    data_temp["model name"] = parent.select_one(
        selector="#wrap > div > div.primary.col-lg-9.order-lg-first > div.page-header"
        ).find(name="h1").get_text(strip=True) # 여백제거

    # CPU 성능 데이터
    cpus = parent.find(name="div", attrs={"class" : "table-wrapper compute"})
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

    # 두 개의 클래스 목록을 정의
    class_pairs = [
        {"name": "td"},
        {"name": "th"}
    ]

    # 전체 테이블
    tables = parent.find_all(name="table", attrs={"class": "table benchmark-table"})
    for tr in tables[index].find_all("tr"):
        col, row, col_index = None, None, 0 # 임시 초기화

        for classes in class_pairs:
            col = tr.find(name=classes["name"], attrs={"class": "name"})
            row = tr.find(name=classes["name"], attrs={"class": "score"})
            col_index += 1

            if (col is not None) and (row is not None):
                break  # 유효한 col, row를 찾으면 루프 종료
        
        # index 값이 1 이면
        if col_index == 1: 
            task_name = col.get_text(strip=True)
            score, score_description = list(filter(lambda x: x.strip(),row.get_text(strip=False).split("\n")))
            data_temp[task_name] = {"score": int(score), "description": score_description}
        else:
            data_temp[col.get_text(strip=True)] = {"score": int(row.get_text(strip=True))}

    return data_temp