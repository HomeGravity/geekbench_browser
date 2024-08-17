import aiohttp
import asyncio

from headers import gb6_headers
from url import (
    gb6_cpu_url,
    gb6_gpu_url,
    gb6_ml_url,
    gb6_ai_url,
)
from parser import Parser
from utils import *


class Geekbench6:
    def __init__(self) -> None:
        # url
        self.gb6_cpu_url = gb6_cpu_url
        self.gb6_gpu_url = gb6_gpu_url
        self.gb6_ml_url = gb6_ml_url
        self.gb6_ai_url = gb6_ai_url
        
        # 헤더
        self.gb6_headers = gb6_headers

        # 비동기 HTTP 객체 초기화
        self.session = aiohttp.ClientSession()
        
        # 파싱 객체 초기화
        self.parser = Parser()

    # 가져오기
    async def cpu_fetch(
        self,
        model_name:str,
        start_page:int,
        end_page:int,
        delay=float
        ) -> None:
        
        # start_page 가 end_page 까지 반복.
        for page in range(start_page, end_page + 1):
            # 페이로드 작성
            cpu_payload = {
                "utf8": "✓",
                "page": page,
                "q": model_name
            }
            
            async with self.session.get(
                url=self.gb6_cpu_url,
                headers=gb6_headers,
                params=cpu_payload
                ) as response:
                
                text = await response.text()
                result = self.parser.cpu_parse(
                    html=text, 
                    page=cpu_payload["page"]
                    )

                indent_print(text=result)
                
                # 비동기적으로 대기
                await asyncio.sleep(delay=delay)


    # 가져오기
    async def gpu_fetch(
        self,
        model_name:str,
        start_page:int,
        end_page:int,
        delay=float
        ) -> None:
        pass

    # 가져오기
    async def ml_fetch(
        self,
        model_name:str,
        start_page:int,
        end_page:int,
        delay=float
        ) -> None:
        pass
    
    # 가져오기
    async def ai_fetch(
        self,
        model_name:str,
        start_page:int,
        end_page:int,
        delay=float
        ) -> None:
        pass
    
    # 세션 종료
    async def session_close(self):
        await self.session.close()


async def run():
    gb6 = Geekbench6()
    await gb6.cpu_fetch(
        start_page=1,
        end_page=2,
        model_name="sm-s928n",
        delay=2
    )
    
    
    # 세션 종료
    await gb6.session_close()

asyncio.run(run())