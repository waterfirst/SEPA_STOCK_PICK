

# 미국 ETF 분석 & SEPA 전략 대시보드 📈

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://usa-etf-pick-sepa-stratage.streamlit.app/)

## 개요

이 프로젝트는 SEPA(Super Efficiency Portfolio Analysis) 전략을 사용하여 미국 중소형 주식을 분석하는 종합 대시보드를 제공합니다. 이 대시보드는 기술적 지표와 시장 동향을 분석하여 투자자들이 잠재적인 투자 기회를 발굴하는 데 도움을 줍니다.

## SEPA 전략이란?

SEPA 전략은 다음과 같은 조건을 충족하는 주식을 찾는 기술적 분석 접근 방식입니다:
- 현재가가 200일 이동평균선 위에 있음
- 150일 이동평균선이 200일 이동평균선 위에 있음
- 50일 이동평균선이 150일과 200일 이동평균선 모두의 위에 있음
- 현재가가 5일 이동평균선 위에 있음
- 200일 이동평균선이 상승 추세를 보임
- 현재가가 52주 최저가 대비 30% 이상 상승

## 주요 기능

- **실시간 분석**: 멀티스레딩을 활용한 다수 종목 동시 분석
- **대화형 대시보드**: Streamlit을 활용한 사용자 친화적 인터페이스
- **기술적 지표**: 다양한 이동평균선과 추세 계산
- **시각화**: 
  - 이동평균선이 포함된 캔들스틱 차트
  - 섹터별 분포 파이 차트
  - 시가총액 통계
- **내보내기 옵션**: CSV 및 JSON 형식으로 분석 결과 저장

## ETF 분석을 위한 유용한 리소스

### ETF 리서치 웹사이트

1. **ETF.com**
   - 종합적인 ETF 리서치와 분석
   - 상세한 펀드 정보와 비교 기능
   - 교육 자료와 시장 인사이트 제공

2. **ETFdb.com**
   - ETF 데이터베이스와 스크리닝 도구
   - 자금 흐름과 성과 분석
   - ETF 비교 및 대안 제시

3. **Morningstar.com**
   - 심층적인 ETF 분석과 등급
   - 포트폴리오 분석 도구
   - 성과 및 리스크 지표

### ETF 스크리닝 도구

1. **FinViz**
   - 고급 스크리닝 기능
   - 기술적/기본적 필터
   - 시각적 분석 도구

2. **Yahoo Finance**
   - 무료 ETF 스크리닝 도구
   - 실시간 데이터와 차트
   - 성과 비교 도구

3. **Charles Schwab ETF Screener**
   - 포괄적인 스크리닝 옵션
   - 리서치와 분석 도구
   - 포트폴리오 구축 기능

### 시장 데이터 소스

1. **Bloomberg**
   - 전문가급 시장 데이터
   - 글로벌 시장 커버리지
   - 고급 분석 기능

2. **Reuters**
   - 실시간 시장 뉴스
   - ETF 시장 분석
   - 산업 인사이트

3. **MarketWatch**
   - 시장 트렌드와 분석
   - ETF 뉴스와 해설
   - 매매 아이디어와 전략

## 사용 방법

1. [SEPA 전략 대시보드](https://usa-etf-pick-sepa-stratage.streamlit.app/) 방문
2. "분석 시작" 버튼을 클릭하여 주식 스캔 시작
3. 결과 및 분석 내용 확인
4. 제공된 버튼을 사용하여 필요한 데이터 내보내기

## 기여하기

이 프로젝트에 기여하거나 문제를 보고하고 싶으시다면, GitHub 저장소에 이슈나 풀 리퀘스트를 생성해 주세요.

## 주의사항

이 도구는 정보 제공 목적으로만 사용되며 투자 조언으로 간주되어서는 안 됩니다. 투자 결정을 내리기 전에 항상 본인의 리서치를 수행하고 전문 재무 상담가와 상담하시기 바랍니다.

## 연락처

대시보드에 대한 질문이나 피드백이 있으시다면 GitHub 저장소에 이슈를 생성하거나 Streamlit 커뮤니티 포럼을 통해 연락해 주시기 바랍니다.

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 LICENSE 파일을 참조하세요.


# US ETF Analysis & SEPA Strategy Dashboard 📈

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://usa-etf-pick-sepa-stratage.streamlit.app/)

## Overview

This project provides a comprehensive dashboard for analyzing US mid and small-cap stocks using the SEPA (Super Efficiency Portfolio Analysis) strategy. The dashboard helps investors identify potential investment opportunities by analyzing technical indicators and market trends.

## SEPA Strategy

The SEPA strategy is a technical analysis approach that looks for stocks meeting the following criteria:
- Price is above the 200-day moving average
- 150-day moving average is above the 200-day moving average
- 50-day moving average is above both 150 and 200-day moving averages
- Current price is above the 5-day moving average
- 200-day moving average shows an upward trend
- Price is at least 30% above the 52-week low

## Features

- **Real-time Analysis**: Analyzes multiple stocks simultaneously using multithreading
- **Interactive Dashboard**: Built with Streamlit for a user-friendly interface
- **Technical Indicators**: Calculates multiple moving averages and trends
- **Visualization**: 
  - Candlestick charts with moving averages
  - Sector distribution pie charts
  - Market cap statistics
- **Export Options**: Save analysis results in CSV and JSON formats

## Useful Resources for ETF Analysis

### ETF Research Websites

1. **ETF.com**
   - Comprehensive ETF research and analysis
   - Detailed fund information and comparisons
   - Educational resources and market insights

2. **ETFdb.com**
   - ETF database with screening tools
   - Fund flows and performance analysis
   - ETF comparisons and alternatives

3. **Morningstar.com**
   - In-depth ETF analysis and ratings
   - Portfolio analysis tools
   - Performance and risk metrics

### ETF Screening Tools

1. **FinViz**
   - Advanced screening capabilities
   - Technical and fundamental filters
   - Visual analysis tools

2. **Yahoo Finance**
   - Free ETF screening tool
   - Real-time data and charts
   - Performance comparison tools

3. **Charles Schwab ETF Screener**
   - Comprehensive screening options
   - Research and analysis tools
   - Portfolio building features

### Market Data Sources

1. **Bloomberg**
   - Professional-grade market data
   - Global market coverage
   - Advanced analytics

2. **Reuters**
   - Real-time market news
   - ETF market analysis
   - Industry insights

3. **MarketWatch**
   - Market trends and analysis
   - ETF news and commentary
   - Trading ideas and strategies

## Usage

1. Visit [SEPA Strategy Dashboard](https://usa-etf-pick-sepa-stratage.streamlit.app/)
2. Click "Start Analysis" to begin scanning stocks
3. View the results and analysis
4. Export data as needed using the provided buttons

## Contributing

If you'd like to contribute to this project or report issues, please feel free to create an issue or pull request on the GitHub repository.

## Disclaimer

This tool is for informational purposes only and should not be considered as financial advice. Always conduct your own research and consult with a financial advisor before making investment decisions.

## Contact

For questions or feedback about the dashboard, please create an issue in the GitHub repository or reach out through the Streamlit community forums.

## License

This project is released under the MIT License. See the LICENSE file for details.


