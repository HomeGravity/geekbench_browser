from geekbench_client.api import GeekbenchBrowserAPI
from geekbench_client.utils import *
import asyncio

import json
import time
from pprint import pprint

# JSON 파일로 저장하는 함수
def save_json_to_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

async def run():
    gb6 = GeekbenchBrowserAPI()
    # await gb6.login(id="id", passwrod="passwrod")
    
    # for search in ["sm-s918n", "sm-s928n"]: 
    #     gb6.search_target(search_target=search)
        
    #     await asyncio.gather(
    #         gb6.cpu_search_fetch(
    #             start_page=1,
    #             end_page=10,
    #             delay=2
    #         ),
    #         gb6.cpu_search_fetch(
    #             start_page=11,
    #             end_page=20,
    #             delay=2
    #         )
    #     )
    
    # save_json_to_file(data=gb6.get_search_cpu_data(), filename="test3.json")
    
    # for search in ["sm-s928n", "sm-s918n"]:    
    #     gb6 = GeekbenchBrowserAPI(search_target=search)
    #     await asyncio.gather(
    #         gb6.cpu_search_fetch(
    #             start_page=1,
    #             end_page=2,
    #             delay=2
    #         ),
    #         gb6.gpu_search_fetch(
    #             start_page=1,
    #             end_page=2,
    #             delay=2
    #         )
    #     )
        
    #     print(gb6.get_search_cpu_data())
    #     print(gb6.get_search_gpu_data())
        
        
    #     # 세션 종료
    #     await gb6.session_close()

    
    # total_page = 1000 
    # time_delay = 6
    # await asyncio.gather(
    # gb6.latest_cpu_fetch(start_page=1, end_page=17, delay=time_delay),
    # gb6.latest_cpu_fetch(start_page=18, end_page=33, delay=time_delay),
    # gb6.latest_cpu_fetch(start_page=34, end_page=50, delay=time_delay),
    # gb6.latest_cpu_fetch(start_page=51, end_page=67, delay=time_delay),
    # gb6.latest_cpu_fetch(start_page=68, end_page=83, delay=time_delay),
    # gb6.latest_cpu_fetch(start_page=84, end_page=100, delay=time_delay),
    # )
    
    
    total_page = 100
    time_delay = 6
    num_tasks = 6  # 작업 수

    # 각 작업에 균등하게 페이지 할당
    pages_per_task = total_page // num_tasks
    remaining_pages = total_page % num_tasks

    # 작업을 생성
    tasks = []
    for i in range(num_tasks):
        start_page = i * pages_per_task + 1
        end_page = start_page + pages_per_task - 1
        if i == num_tasks - 1:  # 마지막 작업
            end_page += remaining_pages  # 남은 페이지 추가
        
        tasks.append(gb6.latest_cpu_fetch(start_page=start_page, end_page=end_page, delay=time_delay))


    # 비동기 작업 실행
    await asyncio.gather(*tasks)

    
    save_json_to_file(data=gb6.get_latest_cpu_data(), filename="test1.json")
    
    
    # time_delay = 6
    # await asyncio.gather(
    # gb6.latest_gpu_fetch(start_page=1, end_page=17, delay=time_delay),
    # gb6.latest_gpu_fetch(start_page=18, end_page=33, delay=time_delay),
    # gb6.latest_gpu_fetch(start_page=34, end_page=50, delay=time_delay),
    # gb6.latest_gpu_fetch(start_page=51, end_page=67, delay=time_delay),
    # gb6.latest_gpu_fetch(start_page=68, end_page=83, delay=time_delay),
    # gb6.latest_gpu_fetch(start_page=84, end_page=100, delay=time_delay),
    # )
    
    # save_json_to_file(data=gb6.get_latest_gpu_data(), filename="gpu_test.json")
    
    
    # 병렬로 여러 요청을 수행
    # android, vulkan = await asyncio.gather(
    #     gb6.android_chart_json_fetch_and_get_data(),
    #     gb6.vulkan_chart_json_fetch_and_get_data()
    # )
    
    # print(type(android))
    # print(vulkan)
    
    # await gb6.gpu_details_fetch(urls=["https://browser.geekbench.com/v6/compute/2698404"], delay=2, login_status=False)
    # await gb6.latest_ai_fetch(start_page=1, end_page=2, delay=2)
    
    # print(gb6.get_details_cpu_data())
    # print(gb6.get_details_gpu_data())
    # print(gb6.get_latest_cpu_data())
    # print(gb6.get_search_cpu_data())
    # print(gb6.get_search_gpu_data())
    # print(gb6.get_search_ai_data())
    # print(gb6.get_latest_ai_data())
    # print(gb6.get_latest_gpu_data())
    # print(gb6.get_search_cpu_data())
    # print(gb6.get_search_gpu_data())
    # print(gb6.get_details_cpu_data(login_status=False))
    # print(gb6.get_details_gpu_data(login_status=False))

    
    
    # 세션 종료
    await gb6.session_close()


asyncio.run(run())