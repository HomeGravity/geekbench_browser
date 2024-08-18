def cpu_parse(element:str, index:int) -> str:
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
            )