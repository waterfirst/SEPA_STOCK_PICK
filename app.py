import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
from concurrent.futures import ThreadPoolExecutor
import datetime
import time
import json
import numpy as np

# 페이지 기본 설정
st.set_page_config(page_title="SEPA Strategy Dashboard", page_icon="📈", layout="wide")


def get_us_midsmall_cap_stocks():
    """
    Russell 2000 및 Midcap 주식들의 티커 목록을 가져옵니다.
    """
    try:
        # Russell 2000 대표 종목들 (시가총액 상위)
        russell2000_tickers = [
            # 산업재
            "GTLS",
            "KRNT",
            "NDSN",
            "AGCO",
            "GGG",
            "MIDD",
            "RS",
            "RBC",
            "ATKR",
            # 정보기술
            "NSIT",
            "SMCI",
            "ANET",
            "BL",
            "POWI",
            "QLYS",
            "HLIT",
            "LFUS",
            # 금융
            "EWBC",
            "FCNCA",
            "UBSI",
            "WRLD",
            "CATY",
            "HOPE",
            "BANF",
            "FFIN",
            # 의료/바이오
            "OMCL",
            "MMSI",
            "NEOG",
            "SRPT",
            "PDCO",
            "GMED",
            "HAE",
            "ACAD",
            # 소비재
            "DECK",
            "BOOT",
            "FOXF",
            "HELE",
            "JACK",
            "WING",
            "DORM",
            "MSGS",
            # 에너지
            "SM",
            "MUR",
            "CNX",
            "CIVI",
            "PBF",
            "TRGP",
            # 부동산
            "CSR",
            "EXR",
            "MAA",
            "AIV",
            "UDR",
        ]

        # Russell Midcap 대표 종목들 (시가총액 상위)
        russellmid_tickers = [
            # 정보기술
            "EPAM",
            "PAYC",
            "FSLR",
            "BR",
            "ZBRA",
            "TYL",
            "CTLT",
            "WEX",
            # 산업재
            "PWR",
            "XYL",
            "RHI",
            "JBHT",
            "CHRW",
            "EXPO",
            "TREX",
            "GLNG",
            # 금융
            "CINF",
            "AJG",
            "FNF",
            "FAF",
            "AIZ",
            "WRB",
            "RJF",
            "SEIC",
            # 의료/바이오
            "PODD",
            "TECH",
            "DXCM",
            "ALGN",
            "HOLX",
            "CRL",
            "HSIC",
            "EHC",
            # 소비재
            "GRMN",
            "DLTR",
            "DPZ",
            "CPRI",
            "TPR",
            "POOL",
            "DRI",
            "FIVE",
            # 에너지
            "DVN",
            "MRO",
            "EQT",
            "AR",
            "RRC",
            "MGY",
            # 부동산
            "MPW",
            "DEI",
            "VTR",
            "HR",
            "HIW",
        ]

        # 두 리스트 합치기
        all_tickers = list(set(russell2000_tickers + russellmid_tickers))
        return all_tickers

    except Exception as e:
        st.error(f"종목 리스트 가져오기 실패: {str(e)}")
        return []


@st.cache_data(ttl=3600)  # 1시간 캐시
def calculate_technical_indicators(df):
    """기술적 지표를 계산합니다."""
    if len(df) < 200:  # 최소 200일치 데이터 필요
        return None

    try:
        df["MA5"] = df["Close"].rolling(window=5).mean()
        df["MA50"] = df["Close"].rolling(window=50).mean()
        df["MA150"] = df["Close"].rolling(window=150).mean()
        df["MA200"] = df["Close"].rolling(window=200).mean()
        return df
    except Exception as e:
        st.error(f"지표 계산 중 오류 발생: {str(e)}")
        return None


def check_sepa_conditions(df):
    """SEPA 전략 조건을 확인합니다."""
    if df is None or len(df) < 200:
        return False, {}

    try:
        latest = df.iloc[-1]
        month_ago = df.iloc[-30]

        # SEPA 조건 체크
        criteria = {
            "현재가가 200일선 위": latest["Close"] > latest["MA200"],
            "150일선이 200일선 위": latest["MA150"] > latest["MA200"],
            "50일선이 150/200일선 위": (latest["MA50"] > latest["MA150"])
            and (latest["MA50"] > latest["MA200"]),
            "현재가가 5일선 위": latest["Close"] > latest["MA5"],
            "200일선 상승 추세": latest["MA200"] > month_ago["MA200"],
        }

        # 52주 최저가 대비 상승률 계산
        year_low = df["Low"].tail(252).min()
        price_above_low = (latest["Close"] / year_low - 1) > 0.3
        criteria["52주 최저가 대비 30% 이상"] = price_above_low

        all_conditions_met = all(criteria.values())

        return all_conditions_met, criteria

    except Exception as e:
        st.error(f"SEPA 조건 체크 중 오류 발생: {str(e)}")
        return False, {}


def analyze_stock(ticker):
    """개별 주식을 분석합니다."""
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period="max")
        if len(df) > 252:  # 1년치 데이터만 사용
            df = df.tail(252)

        if df.empty:
            return None

        df = calculate_technical_indicators(df)
        if df is None:
            return None

        meets_criteria, criteria = check_sepa_conditions(df)

        if meets_criteria:
            info = stock.info
            result = {
                "티커": ticker,
                "기업명": info.get("longName", "N/A"),
                "섹터": info.get("sector", "N/A"),
                "산업": info.get("industry", "N/A"),
                "현재가": df.iloc[-1]["Close"],
                "시가총액(M)": info.get("marketCap", 0) / 1_000_000,
                "거래량": df.iloc[-1]["Volume"],
                "criteria_details": criteria,
                "차트데이터": df,
            }
            return result

        return None

    except Exception as e:
        st.error(f"{ticker} 분석 중 오류 발생: {str(e)}")
        return None


def create_stock_chart(ticker, df):
    """주식 차트를 생성합니다."""
    fig = go.Figure()

    # 캔들스틱 차트
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name="OHLC",
        )
    )

    # 이동평균선 추가
    colors = {"MA5": "purple", "MA50": "blue", "MA150": "green", "MA200": "red"}
    for ma, color in colors.items():
        fig.add_trace(go.Scatter(x=df.index, y=df[ma], name=ma, line=dict(color=color)))

    fig.update_layout(
        title=f"{ticker} Price and Moving Averages",
        yaxis_title="Price",
        xaxis_title="Date",
        height=600,
        template="plotly_white",
    )

    return fig


def save_top_etfs_to_json(df_results):
    """상위 10개 종목 정보를 JSON 파일로 저장"""
    top_10_stocks = df_results.head(10)

    # JSON으로 저장할 데이터 준비
    stock_data = []
    for _, row in top_10_stocks.iterrows():
        stock_info = {
            "ticker": row["티커"],
            "name": row["기업명"],
            "current_price": float(row["현재가"]),
            "market_cap": float(row["시가총액(M)"]),
            "sector": row["섹터"],
            "industry": row["산업"],
        }
        stock_data.append(stock_info)

    # 현재 날짜로 파일명 생성
    current_date = datetime.datetime.now().strftime("%Y%m%d")
    filename = f"top_stocks_{current_date}.json"

    try:
        # JSON 파일 저장
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(stock_data, f, ensure_ascii=False, indent=2)
        return filename
    except Exception as e:
        raise Exception(f"파일 저장 중 오류: {str(e)}")


def main():
    # Initialize session state
    if "df_results" not in st.session_state:
        st.session_state.df_results = None
    if "analysis_done" not in st.session_state:
        st.session_state.analysis_done = False

    st.title("SEPA Strategy Dashboard 📈")
    st.markdown("---")

    # 분석 시작 버튼
    if not st.session_state.analysis_done and st.button("분석 시작"):
        # 분석 시작 시간 기록
        start_time = time.time()

        # 중소형 주식 리스트 가져오기
        with st.spinner("주식 목록 가져오는 중..."):
            tickers = get_us_midsmall_cap_stocks()
            if not tickers:
                st.error("종목 리스트를 가져오는데 실패했습니다.")
                return

            st.info(f"총 {len(tickers)}개 종목 분석 시작...")

        # 멀티스레딩으로 병렬 처리
        sepa_stocks = []
        progress_bar = st.progress(0)
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_stock = {
                executor.submit(analyze_stock, ticker): ticker for ticker in tickers
            }

            completed = 0
            for future in future_to_stock:
                result = future.result()
                if result is not None:
                    sepa_stocks.append(result)
                completed += 1
                progress_bar.progress(completed / len(tickers))

        # 결과를 데이터프레임으로 변환
        if sepa_stocks:
            st.session_state.df_results = pd.DataFrame(sepa_stocks)
            # 시가총액 순으로 정렬
            st.session_state.df_results = st.session_state.df_results.sort_values(
                "시가총액(M)", ascending=False
            )
            st.session_state.analysis_done = True

            # 결과 저장 - CSV
            current_date = datetime.datetime.now().strftime("%Y%m%d")
            csv_filename = f"sepa_stocks_{current_date}.csv"
            st.session_state.df_results.to_csv(
                csv_filename, index=False, encoding="utf-8-sig"
            )

            st.rerun()

    # 분석이 완료된 경우에만 결과 표시
    if st.session_state.analysis_done and st.session_state.df_results is not None:
        df_results = st.session_state.df_results

        st.success(f"분석 완료! {len(df_results)}개 종목이 SEPA 조건을 충족합니다.")

        # 상위 10개 종목 JSON 저장 버튼
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("상위 10개 종목 JSON 저장"):
                try:
                    filename = save_top_etfs_to_json(df_results)
                    st.success(f"저장 완료! 파일명: {filename}")

                    # 다운로드 버튼 추가
                    with open(filename, "r", encoding="utf-8") as f:
                        json_data = f.read()
                        st.download_button(
                            label="JSON 파일 다운로드",
                            data=json_data,
                            file_name=filename,
                            mime="application/json",
                        )
                except Exception as e:
                    st.error(f"저장 중 오류 발생: {str(e)}")

        st.markdown("---")

        # 섹터별 분포 차트
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("섹터별 분포")
            sector_fig = px.pie(
                df_results,
                names="섹터",
                values="시가총액(M)",
                title="섹터별 시가총액 분포",
            )
            st.plotly_chart(sector_fig)

        with col2:
            st.subheader("주요 통계")
            st.metric("총 종목 수", len(df_results))
            st.metric("평균 시가총액 (M$)", f"{df_results['시가총액(M)'].mean():,.2f}")
            st.metric(
                "중간값 시가총액 (M$)", f"{df_results['시가총액(M)'].median():,.2f}"
            )

        # 종목 선택 및 상세 분석
        st.markdown("---")
        st.subheader("종목 상세 분석")

        selected_stock = st.selectbox(
            "분석할 종목 선택",
            df_results["티커"].tolist(),
            format_func=lambda x: f"{x} - {df_results[df_results['티커']==x]['기업명'].iloc[0]}",
        )

        if selected_stock:
            stock_data = df_results[df_results["티커"] == selected_stock].iloc[0]

            col1, col2 = st.columns([3, 1])

            with col1:
                # 차트 표시
                chart = create_stock_chart(stock_data["티커"], stock_data["차트데이터"])
                st.plotly_chart(chart, use_container_width=True)

            with col2:
                # 종목 정보 표시
                st.subheader("종목 정보")
                metrics = {
                    "현재가": f"${stock_data['현재가']:.2f}",
                    "시가총액": f"${stock_data['시가총액(M)']:.2f}M",
                    "섹터": stock_data["섹터"],
                    "산업": stock_data["산업"],
                }

                for key, value in metrics.items():
                    st.metric(key, value)

            # SEPA 조건 상세
            st.subheader("SEPA 조건 상세")
            conditions_df = pd.DataFrame(
                {
                    "조건": stock_data["criteria_details"].keys(),
                    "충족여부": stock_data["criteria_details"].values(),
                }
            )
            st.dataframe(conditions_df)

        # 전체 종목 리스트
        st.markdown("---")
        st.subheader("전체 종목 리스트")
        st.dataframe(
            df_results[["티커", "기업명", "섹터", "산업", "현재가", "시가총액(M)"]],
            use_container_width=True,
        )

    # 분석이 완료되지 않은 경우 시작 메시지 표시
    if not st.session_state.analysis_done:
        st.info("'분석 시작' 버튼을 클릭하여 SEPA 조건을 충족하는 종목을 찾아보세요.")


if __name__ == "__main__":
    main()
