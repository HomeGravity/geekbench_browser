import aiohttp
import asyncio
from typing import Callable, Any, Union


from geekbench6_parser import Parser
from utils import *


class Geekbench6:
    def __init__(self, model_name:str) -> None:
        # url은 딕셔너리 정리해줘.
        # url
        self._gb6_base_url = "https://browser.geekbench.com/search?"
        
        # 긱벤치6 최신 데이터 반영 url
        self._gb6_latest_cpu_url = "https://browser.geekbench.com/v6/cpu"
        self._gb6_latest_compute_url = "https://browser.geekbench.com/v6/compute"
        self._gb6_latest_ai_url = "https://browser.geekbench.com/ai/v1"
        
        # 긱벤치6 가장 높은 싱글/멀티 순위 반영 url
        self._gb6_top_single_url = "https://browser.geekbench.com/v6/cpu/singlecore"
        self._gb6_top_multi_url = "https://browser.geekbench.com/v6/cpu/multicore"
        
        # 긱벤치6 차트 url
        # - cpu
        self._gb6_android_chart_url = "https://browser.geekbench.com/android-benchmarks"
        self._gb6_ios_chart_url = "https://browser.geekbench.com/ios-benchmarks"
        self._gb6_mac_chart_url = "https://browser.geekbench.com/mac-benchmarks"
        self._gb6_processor_chart_url = "https://browser.geekbench.com/processor-benchmarks"
        
        # - ml
        # ml은 ai로 변할 가능성이 높아 며칠간 작업하지 않음.
        self._gb6_ml_chart_url = "https://browser.geekbench.com/ml-benchmarks"
        
        # - gpu(compute)
        self._gb6_metal_chart_url = "https://browser.geekbench.com/metal-benchmarks"
        self._gb6_opencl_chart_url = "https://browser.geekbench.com/opencl-benchmarks"
        self._gb6_vulkan_chart_url = "https://browser.geekbench.com/vulkan-benchmarks"
        
        # login url
        self._login_session_url =  "https://browser.geekbench.com/session/new"
        self._login_create_url = "https://browser.geekbench.com/session/create" # post
        
        # 헤더
        self._gb6_headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Host": "browser.geekbench.com",
            "Referer:": "https://browser.geekbench.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
        }
        
        # 비동기 HTTP 객체 초기화
        self._session = aiohttp.ClientSession()
        # 파싱 객체 초기화
        self._parser = Parser()
        
        
        # 인스턴스 변수
        self._model_name = model_name # 하나의 객체는 하나의 모델만 수집할 수 있도록 합니다.
    
    # 로그인
    async def login(self, id:str, passwrod:str):
        # 페이로드 작성 로직
        async with self._session.get(
            url=self._login_session_url,
            headers=self._gb6_headers
            ) as response:

            (
            param, 
            token, 
            submit_name, 
            submit_value, 
            login_name, 
            passwrod_name
            ) = self._parser.login_parse(html=await response.text(encoding="utf-8"))
            
            # 페이로드 작성
            payload = {
                "utf8": "✓",
                param: token,
                login_name: id,
                passwrod_name: passwrod,
                submit_name: submit_value
            }
        
        # 1초간 비동기 대기
        await asyncio.sleep(1)
        
        # 로그인 요청 로직 (비워둠)
        async with self._session.post(
            url=self._login_create_url,
            headers=self._gb6_headers,
            data=payload
            ) as response:
            pass
            
            
    # 비동기 요청 함수
    async def _fetch(
        self,
        url:str,
        headers:str,
        search_k:str,
        payload_change:bool,
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
                    } if not payload_change else {
                        "page": page
                        }
            
            async with self._session.get(
                url=url,
                headers=headers,
                params=payload
                ) as response:

                text = await response.text(encoding="utf-8")
                result = parser(
                    html=text, 
                    page=payload["page"]
                    )
                
                # debug
                print(f"search: {payload["q"]} - type: {payload["k"]} - page: {payload["page"]}") if not payload_change else print(f"page: {payload["page"]}")

                
                if check_for_last_page(text):
                    break
                
                # 비동기적으로 대기
                await asyncio.sleep(delay=delay)
        
        return result

    # 가져오기
    async def cpu_fetch(
        self,
        start_page:int=1,
        end_page:int=1,
        delay:float=3
        ) -> None:
        
        # 비동기 요청 보내기
        await self._fetch(
            url=self._gb6_base_url,
            headers=self._gb6_headers,
            search_k="v6_cpu",
            payload_change=False,
            start_page=start_page,
            end_page=end_page,
            model_name=self._model_name,
            delay=delay,
            parser=self._parser.cpu_parse
            )
        

                
    # 가져오기
    async def gpu_fetch(
        self,
        start_page:int=1,
        end_page:int=1,
        delay:float=3
        ) -> None:

        # 비동기 요청 보내기
        await self._fetch(
            url=self._gb6_base_url,
            headers=self._gb6_headers,
            search_k="v6_compute",
            payload_change=False,
            start_page=start_page,
            end_page=end_page,
            model_name=self._model_name,
            delay=delay,
            parser=self._parser.gpu_parse
            )

        
    # 가져오기
    async def ai_fetch(
        self,
        start_page:int=1,
        end_page:int=1,
        delay:float=3
        ) -> None:

        # 비동기 요청 보내기
        await self._fetch(
            url=self._gb6_base_url,
            headers=self._gb6_headers,
            search_k="ai",
            payload_change=False,
            start_page=start_page,
            end_page=end_page,
            model_name=self._model_name,
            delay=delay,
            parser=self._parser.ai_parse
            )
    
    # 상세한 정보 가져오기
    async def details_fetch(self, urls:Union[list, tuple], delay:float=3):
        for url in urls:
            async with self._session.get(
                url=url+".gb6",
                headers=self._gb6_headers
                ) as response:
                
                temp = await response.json()
                print(temp["processor_frequency"]["frequencies"])
                await asyncio.sleep(delay=delay)
                
    # 최신 데이터 반영 가져오기
    async def latest_cpu_fetch(
        self,
        start_page:int=1,
        end_page:int=1,
        delay:float=3
        ) -> None:
        pass

    # 최신 데이터 반영 가져오기
    async def latest_gpu_fetch(
        self,
        start_page:int=1,
        end_page:int=1,
        delay:float=3
        ) -> None:
        pass

    # 최신 데이터 반영 가져오기
    async def latest_ai_fetch(
        self,
        start_page:int=1,
        end_page:int=1,
        delay:float=3
        ) -> None:
        pass
    
    # 모든 데이터 반환 - CPU, GPU, AI...
    def get_all_data(self):
        return self._parser.emit_all_data()
    
    # 단일 데이터 반환 - CPU
    def get_cpu_data(self):
        return self._parser.emit_cpu_data()
    
    # 단일 데이터 반환 - GPU
    def get_gpu_data(self):
        return self._parser.emit_gpu_data()
    
    # 단일 데이터 반환 - AI
    def get_ai_data(self):
        return self._parser.emit_ai_data()
    
        
    # 세션 종료
    async def session_close(self):
        await self._session.close()


async def run():
    gb6 = Geekbench6(model_name="sm-s928n")
    # await gb6.login(id="id", passwrod="passwrod")
    
    await asyncio.gather(
        gb6.cpu_fetch(
            start_page=1,
            end_page=3,
            delay=2
        ),
        gb6.cpu_fetch(
            start_page=3,
            end_page=5,
            delay=2
        )
    )
    # await asyncio.gather(
    #     gb6.details_fetch(
    #         urls=[],
    #         delay=3
    #     ),
    #     gb6.details_fetch(
    #         urls=[],
    #         delay=3
    #     )
    # )
    
    print(gb6.get_cpu_data())
    
    # 세션 종료
    await gb6.session_close()


if __name__ == "__main__":
    asyncio.run(run())