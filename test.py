from geekbench6_client.api import Geekbench6
from geekbench6_client.utils import *
import asyncio

async def run():
    gb6 = Geekbench6(model_name="sm-s928n")
    # await gb6.login(id="id", passwrod="passwrod")
    
    await asyncio.gather(
        gb6.latest_cpu_fetch(
            start_page=1,
            end_page=1,
            delay=2
        ),
        gb6.cpu_fetch(
            start_page=3,
            end_page=5,
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
    
    # indent_print(gb6.get_cpu_details_data())
    # indent_print(gb6.get_gpu_details_data())
    indent_print(gb6.get_cpu_data())
    
    # 세션 종료
    await gb6.session_close()


asyncio.run(run())