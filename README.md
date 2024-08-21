# geekbench6-api
Geekbench6의 비공식(non-officia) API입니다.

## 개발 개요
2024년 8월 16일, Geekbench6 non-officia api의 개발을 시작합니다. 본 API는 Geekbench Browser를 기반으로 하여 CPU, GPU(Compute), 인공지능(AI) 등 다양한 성능 벤치마크 데이터를 스크래핑할 수 있도록 설계되었습니다.

## 라이브러리 사용 안내
이 라이브러리는 Primate Labs에서 제공하는 Geekbench Browser를 바탕으로 구축되었습니다. 사용자는 이 API를 통해 Geekbench의 성능 데이터를 효율적으로 수집하고 분석할 수 있습니다.

### 저작권 및 책임
모든 결과 및 데이터에 대한 저작권 및 책임은 Primate Labs에 귀속됩니다. 이 라이브러리를 상업적으로 사용하거나 불법적인 용도로 활용할 경우, 개발자는 어떠한 책임도 지지 않습니다. 사용자는 라이브러리의 사용에 있어 관련 법률 및 규정을 준수해야 합니다.

## 기능
- **CPU 성능 스크래핑**: CPU 벤치마크 결과를 수집합니다.
- **GPU(Compute) 성능 스크래핑**: GPU 벤치마크 결과를 수집합니다.
- **AI 성능 스크래핑**: AI 벤치마크 결과를 수집합니다.
- **상세한 정보 스크래핑**: CPU/GPU 성능 스크래핑의 상세한 정보를 수집합니다. (*.gb6)
- **최신 성능 스크래핑**: CPU/GPU/AI의 Latest(Recent) 성능 데이터를 수집합니다.
- **로그인 기능**: 상세한 정보 스크래핑을 하기위해 로그인 기능을 지원합니다.


## 결론
Geekbench6 non-officia api는 성능 벤치마크 데이터를 수집하고 분석하는 데 최적화된 도구입니다. 사용자는 본 라이브러리를 통해 Geekbench에서 제공하는 다양한 데이터를 손쉽게 활용할 수 있습니다. 

추가적인 질문이나 지원이 필요하시면 언제든지 문의해 주시기 바랍니다.

## 라이선스(License)
Geekbench6 non officia api는 MIT 라이선스(MIT License)로 제공됩니다. 라이선스 전문은 아래와 같습니다:

```
MIT License

Copyright (c) 2024 HomeGravity

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```