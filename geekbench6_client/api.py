import aiohttp
import asyncio
from typing import Callable, Any, Union

from .parser import Parser
from .utils import *


class Geekbench6:
    def __init__(self, model_name:str) -> None:
        # url
        self._gb6_urls = {
            "gb6_base_url": "https://browser.geekbench.com/search?",
            # 최신
            "gb6_latest_cpu_url": "https://browser.geekbench.com/v6/cpu",
            "gb6_latest_compute_url": "https://browser.geekbench.com/v6/compute",
            "gb6_latest_ai_url": "https://browser.geekbench.com/ai/v1",
            # top
            "gb6_top_single_url": "https://browser.geekbench.com/v6/cpu/singlecore",
            "gb6_top_multi_url": "https://browser.geekbench.com/v6/cpu/multicore",
            # 차트
            "gb6_android_chart_url": "https://browser.geekbench.com/android-benchmarks",
            "gb6_ios_chart_url": "https://browser.geekbench.com/ios-benchmarks",
            "gb6_mac_chart_url": "https://browser.geekbench.com/mac-benchmarks",
            "gb6_processor_chart_url": "https://browser.geekbench.com/processor-benchmarks",
            "gb6_ml_chart_url": "https://browser.geekbench.com/ml-benchmarks",
            # 차트 - 그래픽 api
            "gb6_metal_chart_url": "https://browser.geekbench.com/metal-benchmarks",
            "gb6_opencl_chart_url": "https://browser.geekbench.com/opencl-benchmarks",
            "gb6_vulkan_chart_url": "https://browser.geekbench.com/vulkan-benchmarks",
            # 로그인
            "login_session_url": "https://browser.geekbench.com/session/new",
            "login_create_url": "https://browser.geekbench.com/session/create"
        }
        
        # 헤더
        self._gb6_headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-control": "max-age=0",
            "Connection": "keep-alive",
            "Dnt": "1",
            "Host": "browser.geekbench.com",
            "Referer:": "https://browser.geekbench.com/",
            "Sec-Ch-Ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-User": "?1",
            "Sec-Gpc": "1",
            "Upgrade-Insecure-Requests": "1",
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
            url=self._gb6_urls["login_session_url"],
            headers=self._gb6_headers
            ) as response:
            response.raise_for_status()
            
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
            url=self._gb6_urls["login_create_url"],
            headers=self._gb6_headers,
            data=payload
            ) as response:
            response.raise_for_status()
            
            pass
            
            
    # 비동기 요청 함수
    async def _fetch(
        self,
        url:str=None,
        headers:str=None,
        search_k:str=None,
        payload_change:bool=None,
        start_page:int=None,
        end_page:int=None,
        model_name:str=None,
        delay:float=None,
        parser:Callable[[str], Any]=None,
        type:str=None
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
                
                response.raise_for_status()

                text = await response.text(encoding="utf-8")
                result = parser(
                    html=text, 
                    page=payload["page"]
                    )
                
                # debug
                print(f"search: {payload["q"]} - type: {type} - page: {payload["page"]}") if not payload_change else print(f"type: {type} - page: {payload["page"]}")

                
                if check_for_last_page(text):
                    break
                
                # 비동기적으로 대기
                await asyncio.sleep(delay=delay)
        
        return result

    #  json 전용
    async def _json_fetch(self, url:str, extension:str=None):
        async with self._session.get(
            url=url+extension,
            headers=self._gb6_headers
            ) as response:
            response.raise_for_status()
            
            # json으로 변환
            return await response.json()


    # 상세한 정보 가져오기
    async def _details_fetch(self, urls:Union[list, tuple]=None, delay:float=None, parser:Callable[[str], Any]=None, type:str=None):
        for handling, url in enumerate(urls, start=1):
            if type in url:
                    
                result = await self._json_fetch(url=url, extension=".gb6")
                parser(url=url, result_data=result)
                
                # debug
                print(f"type: details {type.replace("compute", "gpu")} - handling: {handling}")
                await asyncio.sleep(delay=delay)

    # 가져오기
    async def cpu_search_fetch(
        self,
        start_page:int=1,
        end_page:int=1,
        delay:float=3
        ) -> None:
        
        # 비동기 요청 보내기
        await self._fetch(
            url=self._gb6_urls["gb6_base_url"],
            headers=self._gb6_headers,
            search_k="v6_cpu",
            payload_change=False,
            start_page=start_page,
            end_page=end_page,
            model_name=self._model_name,
            delay=delay,
            parser=self._parser.cpu_search_parse,
            type="search cpu"
            )
        

                
    # 가져오기
    async def gpu_search_fetch(
        self,
        start_page:int=1,
        end_page:int=1,
        delay:float=3
        ) -> None:

        # 비동기 요청 보내기
        await self._fetch(
            url=self._gb6_urls["gb6_base_url"],
            headers=self._gb6_headers,
            search_k="v6_compute",
            payload_change=False,
            start_page=start_page,
            end_page=end_page,
            model_name=self._model_name,
            delay=delay,
            parser=self._parser.gpu_search_parse,
            type="search gpu"
            )

        
    # 가져오기
    async def ai_search_fetch(
        self,
        start_page:int=1,
        end_page:int=1,
        delay:float=3
        ) -> None:

        # 비동기 요청 보내기
        await self._fetch(
            url=self._gb6_urls["gb6_base_url"],
            headers=self._gb6_headers,
            search_k="ai",
            payload_change=False,
            start_page=start_page,
            end_page=end_page,
            model_name=self._model_name,
            delay=delay,
            parser=self._parser.ai_search_parse,
            type="search ai"
            )
    
    
    # CPU 상세한 정보
    async def cpu_details_fetch(self, urls:Union[list, tuple], delay:float=3):
        await self._details_fetch(
            urls=urls,
            delay=delay,
            parser=self._parser.cpu_details_parse,
            type="cpu"
        )

    # GPU 상세한 정보
    async def gpu_details_fetch(self, urls:Union[list, tuple], delay:float=3):
        await self._details_fetch(
            urls=urls,
            delay=delay,
            parser=self._parser.gpu_details_parse,
            type="compute"
        )
    
    # 안드로이드 벤치마크 차트 json
    async def android_chart_json_fetch_and_get(self) -> dict:
        return await self._json_fetch(
            url=self._gb6_urls["gb6_android_chart_url"],
            extension=".json"
        )
    
    # ios 벤치마크 차트 json
    async def ios_chart_json_fetch_and_get_data(self) -> dict:
        return await self._json_fetch(
            url=self._gb6_urls["gb6_ios_chart_url"],
            extension=".json"
        )

    # mac 벤치마크 차트 json
    async def mac_chart_json_fetch_and_get_data(self) -> dict:
        return await self._json_fetch(
            url=self._gb6_urls["gb6_mac_chart_url"],
            extension=".json"
        )

    # processor 벤치마크 차트 json
    async def processor_chart_json_fetch_and_get_data(self) -> dict:
        return await self._json_fetch(
            url=self._gb6_urls["gb6_processor_chart_url"],
            extension=".json"
        )
    
    # ml 벤치마크 차트 json
    async def ml_chart_json_fetch_and_get_data(self) -> dict:
        return await self._json_fetch(
            url=self._gb6_urls["gb6_ml_chart_url"],
            extension=".json"
        )
    
    # metal 벤치마크 차트 json
    async def metal_chart_json_fetch_and_get_data(self) -> dict:
        return await self._json_fetch(
            url=self._gb6_urls["gb6_metal_chart_url"],
            extension=".json"
        )
    
    # opencl 벤치마크 차트 json
    async def opencl_chart_json_fetch_and_get_data(self) -> dict:
        return await self._json_fetch(
            url=self._gb6_urls["gb6_opencl_chart_url"],
            extension=".json"
        )
    
    # vulkan 벤치마크 차트 json
    async def vulkan_chart_json_fetch_and_get_data(self) -> dict:
        return await self._json_fetch(
            url=self._gb6_urls["gb6_vulkan_chart_url"],
            extension=".json"
        )
    
    
    # 최신 데이터 반영 가져오기
    async def latest_cpu_fetch(
        self,
        start_page:int=1,
        end_page:int=1,
        delay:float=3
        ) -> None:

        # 비동기 요청 보내기
        await self._fetch(
            url=self._gb6_urls["gb6_latest_cpu_url"],
            headers=self._gb6_headers,
            payload_change=True,
            start_page=start_page,
            end_page=end_page,
            delay=delay,
            parser=self._parser.latest_cpu_parse,
            type="latest cpu"
            )

    # 최신 데이터 반영 가져오기
    async def latest_gpu_fetch(
        self,
        start_page:int=1,
        end_page:int=1,
        delay:float=3
        ) -> None:
        
        # 비동기 요청 보내기
        await self._fetch(
            url=self._gb6_urls["gb6_latest_compute_url"],
            headers=self._gb6_headers,
            payload_change=True,
            start_page=start_page,
            end_page=end_page,
            delay=delay,
            parser=self._parser.latest_gpu_parse,
            type="latest gpu"
            )

    # 최신 데이터 반영 가져오기
    async def latest_ai_fetch(
        self,
        start_page:int=1,
        end_page:int=1,
        delay:float=3
        ) -> None:
        
        # 비동기 요청 보내기
        await self._fetch(
            url=self._gb6_urls["gb6_latest_ai_url"],
            headers=self._gb6_headers,
            payload_change=True,
            start_page=start_page,
            end_page=end_page,
            delay=delay,
            parser=self._parser.latest_ai_parse,
            type="latest ai"
            )
    
    # 싱글코어 높은 점수 정렬 데이터 가져오기
    async def cpu_top_single_fetch(
        self,
        start_page:int=1,
        end_page:int=1,
        delay:float=3
        ) -> None:
        
        # 비동기 요청 보내기
        await self._fetch(
            url=self._gb6_urls["gb6_top_single_url"],
            headers=self._gb6_headers,
            payload_change=True,
            start_page=start_page,
            end_page=end_page,
            delay=delay,
            parser=self._parser.top_single_cpu_parse,
            type="cpu top single"            
            )

    # 멀티코어 높은 점수 정렬 데이터 가져오기
    async def cpu_top_multi_fetch(
        self,
        start_page:int=1,
        end_page:int=1,
        delay:float=3
        ) -> None:
        
        # 비동기 요청 보내기
        await self._fetch(
            url=self._gb6_urls["gb6_top_multi_url"],
            headers=self._gb6_headers,
            payload_change=True,
            start_page=start_page,
            end_page=end_page,
            delay=delay,
            parser=self._parser.top_multi_cpu_parse,
            type="cpu top multi"
            )
    
    # 모든 데이터 반환 - CPU, GPU, AI...
    def get_all_data(self):
        return self._parser.emit_data(access_keys=["all"])
    
    # 단일 데이터 반환 - CPU
    def get_cpu_search_data(self):
        return self._parser.emit_data(access_keys=["search", "cpu"])
    
    # 단일 데이터 반환 - GPU
    def get_gpu_search_data(self):
        return self._parser.emit_data(access_keys=["search", "gpu"])
    
    # 단일 데이터 반환 - AI
    def get_ai_search_data(self):
        return self._parser.emit_data(access_keys=["search", "ai"])
    
    # 단일 데이터 반환 - CPU DETAILS
    def get_cpu_details_data(self):
        return self._parser.emit_data(access_keys=["details", "cpu"])
    
    # 단일 데이터 반환 - GPU DETAILS
    def get_gpu_details_data(self):
        return self._parser.emit_data(access_keys=["details", "gpu"])
    
    # 단일 데이터 반환 - LATEST CPU
    def get_latest_cpu_data(self):
        return self._parser.emit_data(access_keys=["latest", "cpu"])

    # 단일 데이터 반환 - LATEST GPU
    def get_latest_gpu_data(self):
        return self._parser.emit_data(access_keys=["latest", "gpu"])
    
    # 단일 데이터 반환 - LATEST AI
    def get_latest_ai_data(self):
        return self._parser.emit_data(access_keys=["latest", "ai"])

    # 단일 데이터 반환 - TOP SINGLE CPU
    def get_top_cpu_single_data(self):
        return self._parser.emit_data(access_keys=["top", "single_cpu"])

    # 단일 데이터 반환 - TOP MULTI CPU
    def get_top_cpu_multi_data(self):
        return self._parser.emit_data(access_keys=["top", "multi_cpu"])

    # 세션 종료
    async def session_close(self):
        await self._session.close()
