def ai_parse_handler(soup:str, tr:str, index:int) -> str:
    # head
    (
    model_name_column,
    framework_name_column,
    framework_score_1_column,
    framework_score_2_column,
    framework_score_3_column
    ) = thead(soup=soup)
    
    # body
    (
    model_name_row, 
    model_ap_row,
    framework_name_row,
    framework_score_1_row,
    framework_score_2_row,
    framework_score_3_row,
    gb6_data_url_row
    ) = tbody(tr=tr, index=index)

    
    return (
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
            )



# thead
def thead(soup:str) -> str:
    model_name_column = soup.select_one(
        selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div.banff > div > div > table > thead > tr > th.device"
    ).get_text(strip=True) # 여백 제거
    
    framework_name_column = soup.select_one(
        selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div.banff > div > div > table > thead > tr > th.framework"
    ).get_text(strip=True) # 여백 제거
    
    framework_score_1_column = soup.select_one(
        selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div.banff > div > div > table > thead > tr > th:nth-child(3)"
    ).get_text(strip=True) # 여백 제거 / Single Precision
    
    framework_score_2_column = soup.select_one(
        selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div.banff > div > div > table > thead > tr > th:nth-child(4)"
    ).get_text(strip=True) # 여백 제거 / Half Precision
    
    framework_score_3_column = soup.select_one(
        selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div.banff > div > div > table > thead > tr > th:nth-child(5)"
    ).get_text(strip=True) # 여백 제거 / Quantized

    return (
            model_name_column,
            framework_name_column,
            framework_score_1_column,
            framework_score_2_column,
            framework_score_3_column
            )

# tbody
def tbody(tr:str, index:int) -> str:
    # "\n\n"로 생성된 빈문자열 제거 - 모델 이름, AP 
    model_name_row, model_ap_row = list(filter(lambda x: x.strip(), tr.select_one(
        selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div.banff > div > div > table > tbody > tr:nth-child(%s) > td.device" % index
    ).get_text(strip=False).split("\n\n")))
    
    # 프레임워크 이름
    framework_name_row = tr.select_one(
        selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div.banff > div > div > table > tbody > tr:nth-child(%s) > td.framework" % index
    ).get_text(strip=True) # 여백 제거
    
    # 프레임워크 점수
    framework_score_1_row = tr.select_one(
        selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div.banff > div > div > table > tbody > tr:nth-child(%s) > td:nth-child(3)" % index
    ).get_text(strip=True) # 여백 제거 / Single Precision
    
    framework_score_2_row = tr.select_one(
        selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div.banff > div > div > table > tbody > tr:nth-child(%s) > td:nth-child(4)" % index
    ).get_text(strip=True) # 여백 제거 / Half Precision
    
    framework_score_3_row = tr.select_one(
        selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div.banff > div > div > table > tbody > tr:nth-child(%s) > td:nth-child(5)" % index
    ).get_text(strip=True) # 여백 제거 / Quantized
    
    # 링크
    gb6_data_url_row = "https://browser.geekbench.com" + tr.select_one(
        selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div.banff > div > div > table > tbody > tr:nth-child(%s) > td.device" % index
    ).find(name="a")["href"]

    return (
            model_name_row, 
            model_ap_row,
            framework_name_row,
            framework_score_1_row,
            framework_score_2_row,
            framework_score_3_row,
            gb6_data_url_row
            )