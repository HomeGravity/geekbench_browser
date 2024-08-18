def gpu_parse(element:str, index:int) -> str:
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
    api_score_score = element.select_one(
        selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div:nth-child(2) > div:nth-child(%s) > div > div > div:nth-child(5) > span.list-col-text-score" % index
    ).get_text(strip=True) # 여백 제거

    # 링크
    gb6_data_url = "https://browser.geekbench.com" + element.select_one(
        selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div:nth-child(2) > div:nth-child(%s) > div > div > div.col-12.col-lg-4 > a" % index
    )["href"]
    
    return (
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
        )