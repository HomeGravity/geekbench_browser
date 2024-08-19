def ai_parse_handler(soup:str, tr:str, index:int) -> str:
        # head
        model_name_head = soup.select_one(
            selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div.banff > div > div > table > thead > tr > th.device"
        ).get_text(strip=True) # 여백 제거
        
        framework_name_head = soup.select_one(
            selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div.banff > div > div > table > thead > tr > th.framework"
        ).get_text(strip=True) # 여백 제거
        
        framework_score_1_head = soup.select_one(
            selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div.banff > div > div > table > thead > tr > th:nth-child(3)"
        ).get_text(strip=True) # 여백 제거 / Single Precision
        
        framework_score_2_head = soup.select_one(
            selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div.banff > div > div > table > thead > tr > th:nth-child(4)"
        ).get_text(strip=True) # 여백 제거 / Half Precision
        
        framework_score_3_head = soup.select_one(
            selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div.banff > div > div > table > thead > tr > th:nth-child(5)"
        ).get_text(strip=True) # 여백 제거 / Quantized
        
        # body
        # "\n\n"로 생성된 빈문자열 제거 - 모델 이름, AP 
        model_name, ap = list(filter(lambda x: x.strip(), tr.select_one(
            selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div.banff > div > div > table > tbody > tr:nth-child(%s) > td.device" % index
        ).get_text(strip=False).split("\n\n")))
        
        # 프레임워크 이름
        framework_name = tr.select_one(
            selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div.banff > div > div > table > tbody > tr:nth-child(%s) > td.framework" % index
        ).get_text(strip=True) # 여백 제거
        
        # 프레임워크 점수
        framework_score_1 = tr.select_one(
            selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div.banff > div > div > table > tbody > tr:nth-child(%s) > td:nth-child(3)" % index
        ).get_text(strip=True) # 여백 제거 / Single Precision
        
        framework_score_2 = tr.select_one(
            selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div.banff > div > div > table > tbody > tr:nth-child(%s) > td:nth-child(4)" % index
        ).get_text(strip=True) # 여백 제거 / Half Precision
        
        framework_score_3 = tr.select_one(
            selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div.banff > div > div > table > tbody > tr:nth-child(%s) > td:nth-child(5)" % index
        ).get_text(strip=True) # 여백 제거 / Quantized
        
        # 링크
        gb6_data_url = "https://browser.geekbench.com" + tr.select_one(
            selector="#wrap > div > div > div > div:nth-child(3) > div.col-12.col-lg-9 > div.banff > div > div > table > tbody > tr:nth-child(%s) > td.device" % index
        ).find(name="a")["href"]
        
        return (
                model_name_head,
                framework_name_head,
                framework_score_1_head,
                framework_score_2_head,
                framework_score_3_head,
                model_name, ap,
                framework_name,
                framework_score_1,
                framework_score_2,
                framework_score_3,
                gb6_data_url
                )