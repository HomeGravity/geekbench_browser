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


def task_creation_calculation(total_page, max_num_tasks):
    if total_page >= max_num_tasks:
        num_tasks = max_num_tasks
    else:
        num_tasks = total_page
    
    # 각 작업에 균등하게 페이지 할당
    pages_per_task = total_page // num_tasks
    remaining_pages = total_page % num_tasks

    return num_tasks, pages_per_task, remaining_pages

    
async def run():
    gb6 = GeekbenchBrowserAPI()
    # await gb6.login(id="id", passwrod="passwrod")
    
    # 작업량 계산
    num_page_and_keyword = [(2462, "SM-S928N"), (1602, "IPhone17,2 D94AP")]
    time_delay = 10


    for _, (fetch_func, get_func) in enumerate(zip([gb6.cpu_search_fetch], [gb6.get_search_cpu_data]), start=1):
        # 페이지 키워드 순회 참조
        for page, keyword in num_page_and_keyword:
            num_tasks, pages_per_task, remaining_pages = task_creation_calculation(total_page=page, max_num_tasks=5) # 최대 세션 생성 제한
            gb6.search_target(search_target=keyword)
            
            # 작업을 생성
            tasks = []
            for i in range(num_tasks):
                start_page = i * pages_per_task + 1
                end_page = start_page + pages_per_task - 1
                if i == num_tasks - 1:  # 마지막 작업
                    end_page += remaining_pages  # 남은 페이지 추가
                
                tasks.append(fetch_func(start_page=start_page, end_page=end_page, delay=time_delay))


            # 비동기 작업 실행
            await asyncio.gather(*tasks)
        
        save_json_to_file(data=get_func(), filename=f"test.json")
    
    
    
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
    
    
    # 작업량 계산
    # num_tasks, pages_per_task, remaining_pages = task_creation_calculation(total_page=100, max_num_tasks=6)
    # time_delay = 10

    # for index, (fetch_func, get_func) in enumerate(zip([gb6.latest_cpu_fetch, gb6.latest_gpu_fetch], [gb6.get_latest_cpu_data, gb6.get_latest_gpu_data]), start=1):
    #     # 작업을 생성
    #     tasks = []
    #     for i in range(num_tasks):
    #         start_page = i * pages_per_task + 1
    #         end_page = start_page + pages_per_task - 1
    #         if i == num_tasks - 1:  # 마지막 작업
    #             end_page += remaining_pages  # 남은 페이지 추가
            
    #         tasks.append(fetch_func(start_page=start_page, end_page=end_page, delay=time_delay))


    #     # 비동기 작업 실행
    #     await asyncio.gather(*tasks)

        
    #     save_json_to_file(data=get_func(), filename=f"test{index}.json")
    
    
    
    
    # time_delay = 6
    # await asyncio.gather(
    # # gb6.latest_gpu_fetch(start_page=1, end_page=17, delay=time_delay),
    # # gb6.latest_gpu_fetch(start_page=18, end_page=33, delay=time_delay),
    # # gb6.latest_gpu_fetch(start_page=34, end_page=50, delay=time_delay),
    # # gb6.latest_gpu_fetch(start_page=51, end_page=67, delay=time_delay),
    # # gb6.latest_gpu_fetch(start_page=68, end_page=83, delay=time_delay),
    # gb6.latest_gpu_fetch(start_page=101, end_page=102, delay=time_delay),
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