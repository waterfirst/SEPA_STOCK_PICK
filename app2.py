import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
from concurrent.futures import ThreadPoolExecutor
import requests
import io


class SEPAScreener:
    def __init__(self):
        self.today = datetime.now()
        self.start_date = self.today - timedelta(days=730)  # 2년치 데이터

    def get_us_stock_list(self):
        """미국 주식 목록 가져오기"""
        # NASDAQ
        nasdaq_url = "https://old.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download"
        # NYSE
        nyse_url = "https://old.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nyse&render=download"

        try:
            # NASDAQ 종목
            nasdaq_df = pd.read_csv(nasdaq_url)
            # NYSE 종목
            nyse_df = pd.read_csv(nyse_url)

            # 데이터프레임 합치기
            all_stocks = pd.concat([nasdaq_df, nyse_df])

            # 중소형주 필터링 (시가총액 $300M ~ $10B)
            all_stocks = all_stocks[
                (all_stocks["Market Cap"] >= 300000000)
                & (all_stocks["Market Cap"] <= 10000000000)
            ]

            return all_stocks["Symbol"].tolist()
        except:
            # 백업 방법: S&P 600 Small Cap 지수 구성종목 사용
            sp600 = pd.read_html(
                "https://en.wikipedia.org/wiki/List_of_S%26P_600_companies"
            )[0]
            return sp600["Symbol"].tolist()

    def analyze_stock(self, ticker):
        """개별 주식 SEPA 분석"""
        try:
            # 주식 데이터 가져오기
            stock = yf.Ticker(ticker)
            df = stock.history(start=self.start_date)

            if len(df) < 200:  # 충분한 데이터가 없으면 제외
                return None

            # 기술적 지표 계산
            df = self.calculate_indicators(df)

            # SEPA 조건 체크
            sepa_result = self.check_sepa_conditions(df)

            if sepa_result["matches_criteria"]:
                return {
                    "ticker": ticker,
                    "company_name": stock.info.get("longName", ""),
                    "current_price": df["Close"].iloc[-1],
                    "market_cap": stock.info.get("marketCap", 0),
                    "sector": stock.info.get("sector", ""),
                    "industry": stock.info.get("industry", ""),
                    "criteria_details": sepa_result["criteria"],
                }
            return None

        except Exception as e:
            return None

    def calculate_indicators(self, df):
        """기술적 지표 계산"""
        # 이동평균선
        df["MA5"] = df["Close"].rolling(window=5).mean()
        df["MA50"] = df["Close"].rolling(window=50).mean()
        df["MA150"] = df["Close"].rolling(window=150).mean()
        df["MA200"] = df["Close"].rolling(window=200).mean()

        # 52주 최고/최저
        df["52W_High"] = df["High"].rolling(window=252).max()
        df["52W_Low"] = df["Low"].rolling(window=252).min()

        return df

    def check_sepa_conditions(self, df):
        """SEPA 전략 조건 체크"""
        latest = df.iloc[-1]
        month_ago = df.iloc[-30]

        criteria = {
            "현재가가 200일선 위": latest["Close"] > latest["MA200"],
            "150일선이 200일선 위": latest["MA150"] > latest["MA200"],
            "50일선이 150/200일선 위": latest["MA50"] > latest["MA150"]
            and latest["MA50"] > latest["MA200"],
            "현재가가 5일선 위": latest["Close"] > latest["MA5"],
            "200일선 상승 추세": latest["MA200"] > month_ago["MA200"],
            "52주 최저가 대비 30% 이상": (latest["Close"] / latest["52W_Low"] - 1)
            > 0.3,
        }

        return {"matches_criteria": all(criteria.values()), "criteria": criteria}

    def screen_stocks(self, progress_bar=None):
        """전체 주식 스크리닝"""
        stocks = self.get_us_stock_list()
        results = []

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {
                executor.submit(self.analyze_stock, ticker): ticker for ticker in stocks
            }

            for i, future in enumerate(futures):
                if progress_bar:
                    progress_bar.progress((i + 1) / len(stocks))

                result = future.result()
                if result:
                    results.append(result)

        return results


def main():
    st.set_page_config(page_title="SEPA 전략 스크리너", layout="wide")
    st.title("📊 SEPA 전략 중소형주 스크리너")

    if "screener_results" not in st.session_state:
        st.session_state.screener_results = None

    # 스크리닝 시작 버튼
    if st.button("스크리닝 시작"):
        screener = SEPAScreener()
        progress_bar = st.progress(0)
        st.write("스크리닝 중... 잠시만 기다려주세요.")

        results = screener.screen_stocks(progress_bar)
        st.session_state.screener_results = results

        progress_bar.empty()
        st.success(f"스크리닝 완료! {len(results)}개의 종목이 SEPA 조건에 부합합니다.")

    # 결과 표시
    if st.session_state.screener_results:
        results_df = pd.DataFrame(st.session_state.screener_results)

        # 필터링 옵션
        st.sidebar.header("필터 옵션")

        if "sector" in results_df.columns:
            sectors = ["전체"] + list(results_df["sector"].unique())
            selected_sector = st.sidebar.selectbox("섹터 선택", sectors)

            if selected_sector != "전체":
                results_df = results_df[results_df["sector"] == selected_sector]

        # 시가총액 범위 필터
        min_cap, max_cap = st.sidebar.slider(
            "시가총액 범위 (백만 달러)",
            min_value=300,
            max_value=10000,
            value=(300, 10000),
        )

        results_df = results_df[
            (results_df["market_cap"] >= min_cap * 1000000)
            & (results_df["market_cap"] <= max_cap * 1000000)
        ]

        # 결과 테이블 표시
        st.subheader("SEPA 조건 부합 종목")

        # 테이블에 표시할 컬럼 포맷팅
        display_df = results_df.copy()
        display_df["current_price"] = display_df["current_price"].round(2)
        display_df["market_cap"] = (display_df["market_cap"] / 1000000).round(2)
        display_df = display_df.rename(
            columns={
                "ticker": "티커",
                "company_name": "기업명",
                "current_price": "현재가",
                "market_cap": "시가총액(M)",
                "sector": "섹터",
                "industry": "산업",
            }
        )

        st.dataframe(display_df)

        # 선택한 종목 상세 분석
        st.subheader("종목 상세 분석")
        selected_ticker = st.selectbox(
            "분석할 종목 선택", options=results_df["ticker"].tolist()
        )

        if selected_ticker:
            stock = yf.Ticker(selected_ticker)
            df = stock.history(period="2y")

            # 차트 그리기
            fig = go.Figure()

            fig.add_trace(
                go.Candlestick(
                    x=df.index,
                    open=df["Open"],
                    high=df["High"],
                    low=df["Low"],
                    close=df["Close"],
                    name="주가",
                )
            )

            # 이동평균선 추가
            for ma, color in zip(
                ["MA5", "MA50", "MA150", "MA200"], ["purple", "blue", "orange", "red"]
            ):
                df[ma] = df["Close"].rolling(window=int(ma[2:])).mean()
                fig.add_trace(
                    go.Scatter(
                        x=df.index, y=df[ma], name=f"{ma}일선", line=dict(color=color)
                    )
                )

            fig.update_layout(
                title=f"{selected_ticker} 차트",
                yaxis_title="가격",
                xaxis_title="날짜",
                height=600,
            )

            st.plotly_chart(fig, use_container_width=True)

            # SEPA 조건 상세 표시
            st.write("### SEPA 조건 충족 여부")
            criteria = results_df[results_df["ticker"] == selected_ticker][
                "criteria_details"
            ].iloc[0]
            for criterion, value in criteria.items():
                if value:
                    st.success(f"✅ {criterion}")
                else:
                    st.error(f"❌ {criterion}")


if __name__ == "__main__":
    main()
