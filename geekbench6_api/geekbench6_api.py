import aiohttp
import asyncio
from typing import Callable, Any

from headers import gb6_headers
from url import gb6_base_url
from geekbench6_parser import Parser
from utils import *


class Geekbench6:
    def __init__(self, model_name:str) -> None:
        # url
        self.gb6_base_url = gb6_base_url
        # 헤더
        self.gb6_headers = gb6_headers
        # 비동기 HTTP 객체 초기화
        self.session = aiohttp.ClientSession()
        # 파싱 객체 초기화
        self.parser = Parser()
        # 인스턴스 변수
        self.model_name = model_name # 하나의 객체는 하나의 모델만 수집할 수 있도록 합니다.
    
    # 비동기 요청 함수
    async def _fetch(
        self,
        url:str,
        headers:str,
        search_k:str,
        start_page:int,
        end_page:int,
        model_name:str,
        delay:float,
        parser:Callable[[str], Any]
        ) -> dict:
        
        
        # start_page 가 end_page 까지 반복.
        for page in range(start_page, end_page + 1):
            # 페이로드 작성
            payload = {
                "k": search_k,
                "utf8": "✓",
                "page": page,
                "q": model_name
            }
            
            async with self.session.get(
                url=url,
                headers=headers,
                params=payload
                ) as response:

                text = await response.text(encoding="utf-8")
                result = parser(
                    html=text, 
                    page=payload["page"]
                    )
                
                print(payload)

                if check_for_last_page(text):
                    break
                
                # 비동기적으로 대기
                await asyncio.sleep(delay=delay)
        
        return result

    # 가져오기
    async def cpu_fetch(
        self,
        start_page:int,
        end_page:int,
        delay=float
        ) -> None:
        
        # 비동기 요청 보내기
        text = await self._fetch(
            url=self.gb6_base_url,
            headers=self.gb6_headers,
            search_k="v6_cpu",
            start_page=start_page,
            end_page=end_page,
            model_name=self.model_name,
            delay=delay,
            parser=self.parser.cpu_parse
            )
        
        # indent_print(text=text)

                
    # 가져오기
    async def gpu_fetch(
        self,
        start_page:int,
        end_page:int,
        delay=float
        ) -> None:

        # 비동기 요청 보내기
        text = await self._fetch(
            url=self.gb6_base_url,
            headers=self.gb6_headers,
            search_k="v6_compute",
            start_page=start_page,
            end_page=end_page,
            model_name=self.model_name,
            delay=delay,
            parser=self.parser.gpu_parse
            )
        # indent_print(text=text)
        
        
    # 가져오기
    async def ai_fetch(
        self,
        start_page:int,
        end_page:int,
        delay=float
        ) -> None:

        # 비동기 요청 보내기
        text = await self._fetch(
            url=self.gb6_base_url,
            headers=self.gb6_headers,
            search_k="ai",
            start_page=start_page,
            end_page=end_page,
            model_name=self.model_name,
            delay=delay,
            parser=self.parser.ai_parse
            )
        
    def all_data(self):
        indent_print(self.parser.return_all_data())
    
    # 세션 종료
    async def session_close(self):
        await self.session.close()


async def run():
    gb6 = Geekbench6(model_name="sm-s928n")
    await asyncio.gather(
        gb6.cpu_fetch(
            start_page=1,
            end_page=3,
            delay=2
        ),
        gb6.gpu_fetch(
            start_page=1,
            end_page=3,
            delay=2
        )
    )
    
    gb6.all_data()
    
    # 세션 종료
    await gb6.session_close()

asyncio.run(run())