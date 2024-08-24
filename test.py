from geekbench6_client.api import Geekbench6
from geekbench6_client.utils import *
import asyncio

async def run():
    gb6 = Geekbench6(model_name="sm-s928n")
    # await gb6.login(id="id", passwrod="passwrod")
    
    await asyncio.gather(
        gb6.cpu_search_fetch(
            start_page=1,
            end_page=2,
            delay=2
        ),
        gb6.latest_gpu_fetch(
            start_page=1,
            end_page=2,
            delay=2
        )
    )
    # await asyncio.gather(
    #     gb6.cpu_details_fetch(
    #         urls=[],
    #         delay=3
    #     ),
    #     gb6.cpu_details_fetch(
    #         urls=[],
    #         delay=3
    #     ),
    #     # gb6.gpu_details_fetch(
    #     #     urls=[],
    #     #     delay=3
    #     # )
    # )
    
    # 병렬로 여러 요청을 수행
    # android, vulkan = await asyncio.gather(
    #     gb6.android_chart_json_fetch_and_get(),
    #     gb6.vulkan_chart_json_fetch_and_get_data()
    # )
    
    # print(android)
    # print(vulkan)
    
    # print(gb6.get_cpu_details_data())
    # print(gb6.get_gpu_details_data())
    # print(gb6.get_latest_cpu_data())
    print(gb6.get_cpu_search_data())
    # print(gb6.get_gpu_search_data())
    # print(gb6.get_ai_search_data())
    # print(gb6.get_latest_ai_data())
    print(gb6.get_latest_gpu_data())
    
    # 세션 종료
    await gb6.session_close()


asyncio.run(run())