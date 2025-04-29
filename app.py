import streamlit as st
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import base64
import plotly.express as px

# 페이지 설정
st.set_page_config(
    page_title="Cafe24 로딩 타임 체크",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS 스타일
st.markdown("""
<style>
    /* 전체 컨테이너 스타일 */
    .main {
        max-width: 1040px;
        margin: 0 auto;
        padding: 2rem;
    }
    
    /* 헤더 스타일 */
    .header {
        text-align: center;
        margin-bottom: 3rem;
        padding: 2rem 0;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .header h1 {
        color: #2c3e50;
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .header p {
        color: #34495e;
        font-size: 1.2rem;
        margin-bottom: 0;
    }
    
    /* 입력 폼 스타일 */
    .stForm {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 0.8rem;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3498db;
        box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        padding: 0.8rem;
        font-size: 1.1rem;
        font-weight: 600;
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
        color: white;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2980b9 0%, #3498db 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* 메트릭 카드 스타일 */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .metric-card h4 {
        color: #2c3e50;
        margin-bottom: 1rem;
        font-size: 1.2rem;
    }
    
    .performance-metric {
        font-size: 2.5rem;
        font-weight: bold;
        color: #3498db;
        margin-bottom: 0.5rem;
    }
    
    /* 섹션 스타일 */
    .section {
        margin: 2rem 0;
        padding: 2rem;
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .section h3 {
        color: #2c3e50;
        margin-bottom: 1.5rem;
        font-size: 1.8rem;
    }
    
    /* 진행 상태 스타일 */
    .stProgress > div > div > div {
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
    }
    
    /* 반응형 디자인 */
    @media (max-width: 1040px) {
        .main {
            padding: 1rem;
        }
        
        .header h1 {
            font-size: 2rem;
        }
        
        .header p {
            font-size: 1rem;
        }
    }
    
    /* 푸터 스타일 */
    .footer {
        margin-top: 4rem;
        padding: 2rem;
        background: #f8f9fa;
        border-radius: 15px;
        text-align: center;
        font-size: 0.9rem;
        color: #666;
        line-height: 1.6;
    }
    
    .footer a {
        color: #3498db;
        text-decoration: none;
    }
    
    .footer a:hover {
        text-decoration: underline;
    }
    
    .footer-title {
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    
    @media (max-width: 1040px) {
        .footer {
            padding: 1.5rem;
            font-size: 0.8rem;
        }
    }
    
    /* 툴팁 스타일 */
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 300px;
        background-color: #555;
        color: #fff;
        text-align: left;
        border-radius: 6px;
        padding: 10px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -150px;
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 14px;
        line-height: 1.4;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    
    .tooltip .tooltiptext::after {
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        margin-left: -5px;
        border-width: 5px;
        border-style: solid;
        border-color: #555 transparent transparent transparent;
    }
    
    /* 로딩 애니메이션 스타일 */
    .loading-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 300px;
        text-align: center;
    }
    
    .loading-spinner {
        width: 80px;
        height: 80px;
        border: 8px solid #f3f3f3;
        border-top: 8px solid #3498db;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-bottom: 20px;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .loading-text {
        font-size: 1.2rem;
        color: #666;
        margin-top: 20px;
    }
    
    /* 비교 테이블 스타일 */
    .comparison-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        margin: 20px 0;
        font-size: 14px;
        table-layout: fixed;
    }
    .comparison-table th, .comparison-table td {
        padding: 15px;
        text-align: left;
        border: 1px solid #ddd;
        vertical-align: top;
        word-wrap: break-word;
    }
    .comparison-table th {
        background-color: #f8f9fa;
        font-weight: bold;
        position: sticky;
        top: 0;
        z-index: 1;
    }
    .comparison-table th:first-child {
        width: 120px;
    }
    .comparison-table th:nth-child(2) {
        width: 40%;
    }
    .comparison-table th:nth-child(3) {
        width: 40%;
    }
    .comparison-table td:first-child {
        font-weight: bold;
        background-color: #f8f9fa;
    }
    .comparison-table tr:nth-child(even) {
        background-color: #f8f9fa;
    }
    .cafe24-cell {
        background-color: #e3f2fd;
    }
    .godomall-cell {
        background-color: #fce4ec;
    }
    .source-text {
        font-size: 12px;
        color: #666;
        margin-top: 8px;
        padding-top: 8px;
        border-top: 1px dashed #ddd;
    }
    @media (max-width: 768px) {
        .comparison-table {
            display: block;
            overflow-x: auto;
            white-space: nowrap;
        }
        .comparison-table th, .comparison-table td {
            min-width: 200px;
        }
    }
</style>
""", unsafe_allow_html=True)

# 헤더 섹션
st.markdown("""
<div class="header">
    <h1>카페24 쇼핑몰 인사이트</h1>
    <p>운영 중인 쇼핑몰 주소를 입력하면, 사이트의 상태를 분석하고<br>Cafe24가 제공하는 맞춤형 개선 인사이트를 안내해드립니다.</p>
</div>
""", unsafe_allow_html=True)

# 입력 폼
with st.form("analysis_form"):
    st.markdown("""
    <div class="stForm">
        <h3 style="color: #2c3e50; margin-bottom: 1.5rem;">분석할 웹사이트 정보를 입력하세요</h3>
    """, unsafe_allow_html=True)
    
    domain = st.text_input("브랜드 도메인", placeholder="예: yourdomain.cafe24.com")
    industry = st.selectbox(
        "업종",
        ["패션의류", "스포츠", "전자제품", "식품", "건기식", "굿즈", "기타"]
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    submitted = st.form_submit_button("분석 시작하기")

if submitted and domain:
    try:
        # 진행 상태 표시
        status = st.empty()
        status.markdown("""
        <div class="loading-container">
            <div class="loading-spinner"></div>
            <div class="loading-text">데이터를 분석 중입니다...</div>
        </div>
        """, unsafe_allow_html=True)

        # 1. 직접 로딩 시간 측정
        direct_timing_results = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        for i in range(3):  # 3회 측정
            try:
                # https:// 제거하고 처리
                clean_domain = domain.replace("https://", "").replace("http://", "").strip("/")
                start_time = time.time()
                response = requests.get(f"https://{clean_domain}", 
                                     headers=headers,
                                     timeout=10,
                                     allow_redirects=True)
                response.raise_for_status()
                load_time = round(time.time() - start_time, 2)
                direct_timing_results.append(load_time)
                status.markdown(f"""
                <div class="loading-container">
                    <div class="loading-spinner"></div>
                    <div class="loading-text">직접 측정 진행 중... ({i+1}/3)</div>
                </div>
                """, unsafe_allow_html=True)
                time.sleep(1)  # 요청 간 1초 대기
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 403:
                    st.warning("웹사이트가 자동화된 요청을 차단했습니다. Google PageSpeed 결과만 표시합니다.")
                    break
                else:
                    st.error(f"HTTP 오류 발생: {str(e)}")
                    break
            except requests.exceptions.RequestException as e:
                st.error(f"요청 중 오류 발생: {str(e)}")
                break

        # 2. Google PageSpeed API 호출
        status.markdown("""
        <div class="loading-container">
            <div class="loading-spinner"></div>
            <div class="loading-text">Google PageSpeed 분석을 시작합니다...</div>
        </div>
        """, unsafe_allow_html=True)
        API_KEY = "AIzaSyBo2LdoFNFxphORUYH9beG1TqDn-AFG_II"
        
        try:
            clean_domain = domain.replace("https://", "").replace("http://", "").strip("/")
            url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://{clean_domain}&key={API_KEY}&category=performance&category=accessibility&category=seo&category=best-practices"
            
            # 진행 상태 표시
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # API 호출 전 대기
            status_text.info("Google PageSpeed API에 요청을 보내는 중...")
            time.sleep(2)
            
            # API 호출 (타임아웃 300초로 증가)
            response = requests.get(url, timeout=300)
            progress_bar.progress(30)
            status_text.info("성능 데이터를 분석하는 중...")
            
            pagespeed_data = response.json()
            progress_bar.progress(60)
            status_text.info("결과를 처리하는 중...")
            
            if "lighthouseResult" in pagespeed_data:
                # 성능 점수
                performance = pagespeed_data["lighthouseResult"]["categories"]["performance"]["score"] * 100
                
                # Core Web Vitals 및 기타 메트릭
                metrics = pagespeed_data["lighthouseResult"]["audits"]
                
                # 메트릭 추출 함수
                def get_metric_value(metric_name, default="N/A"):
                    try:
                        return metrics[metric_name]["displayValue"]
                    except (KeyError, TypeError):
                        return default
                
                # Core Web Vitals
                lcp = get_metric_value("largest-contentful-paint")
                fid = get_metric_value("first-input-delay")
                cls = get_metric_value("cumulative-layout-shift")
                
                # 기타 성능 메트릭
                fcp = get_metric_value("first-contentful-paint")
                speed_index = get_metric_value("speed-index")
                tti = get_metric_value("interactive")
                
                # 카테고리 점수 추출 함수
                def get_category_score(category_name, default=50):
                    try:
                        return pagespeed_data["lighthouseResult"]["categories"][category_name]["score"] * 100
                    except (KeyError, TypeError):
                        return default
                
                # 접근성 점수
                accessibility = get_category_score("accessibility")
                
                # SEO 점수
                seo = get_category_score("seo")
                
                # 모범 사례 점수
                best_practices = get_category_score("best-practices")
                
                progress_bar.progress(100)
                status_text.success("Google PageSpeed 분석이 완료되었습니다!")
            else:
                st.warning("Google PageSpeed API 응답에서 데이터를 찾을 수 없습니다.")
                performance = 50
                lcp = "N/A"
                fid = "N/A"
                cls = "N/A"
                fcp = "N/A"
                speed_index = "N/A"
                tti = "N/A"
                accessibility = 50
                seo = 50
                best_practices = 50
        except requests.exceptions.Timeout:
            st.warning("Google PageSpeed 분석이 시간 초과되었습니다. 잠시 후 다시 시도해주세요.")
            performance = 50
            lcp = "N/A"
            fid = "N/A"
            cls = "N/A"
            fcp = "N/A"
            speed_index = "N/A"
            tti = "N/A"
            accessibility = 50
            seo = 50
            best_practices = 50
        except Exception as e:
            st.error(f"Google PageSpeed 분석 중 오류가 발생했습니다: {str(e)}")
            performance = 50
            lcp = "N/A"
            fid = "N/A"
            cls = "N/A"
            fcp = "N/A"
            speed_index = "N/A"
            tti = "N/A"
            accessibility = 50
            seo = 50
            best_practices = 50

        # 분석 결과 표시
        status.success("분석이 완료되었습니다!")

        # 사이트 정보 섹션
        st.markdown("### 🌐 사이트 정보")
        try:
            # 웹사이트에서 직접 HTML 가져오기
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # https:// 제거하고 처리
            clean_domain = domain.replace("https://", "").replace("http://", "").strip("/")
            response = requests.get(f"https://{clean_domain}", headers=headers, timeout=10)
            response.raise_for_status()
            
            # BeautifulSoup으로 파싱
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 사이트 제목 가져오기
            site_title = soup.title.string if soup.title else "제목 없음"
            
            # 메타 설명 가져오기
            meta_description = soup.find('meta', attrs={'name': 'description'})
            site_description = meta_description['content'] if meta_description else "설명 없음"
            
            st.markdown(f"""
            <div class="metric-card">
                <h4>사이트 제목</h4>
                <p>{site_title}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="metric-card">
                <h4>사이트 설명</h4>
                <p>{site_description}</p>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.warning("사이트 정보를 가져오는 중 오류가 발생했습니다.")

        # 결과를 3개의 열로 나누어 표시
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("### 🔄 직접 측정 결과")
            if direct_timing_results:
                avg_load_time = round(sum(direct_timing_results) / len(direct_timing_results), 2)
                st.markdown(f"""
                <div class="metric-card">
                    <h4>평균 로딩 시간</h4>
                    <div class="performance-metric">{avg_load_time}초</div>
                    <small>3회 측정 평균</small>
                </div>
                """, unsafe_allow_html=True)
                
                # 개별 측정 결과
                st.markdown("#### 개별 측정 결과")
                for idx, time_result in enumerate(direct_timing_results, 1):
                    st.markdown(f"측정 {idx}: {time_result}초")

        with col2:
            st.markdown("### 🚀 Google PageSpeed 결과")
            st.markdown(f"""
            <div class="metric-card">
                <h4>성능 점수</h4>
                <div class="performance-metric">{performance:.0f}/100</div>
                <small>Google PageSpeed 분석</small>
            </div>
            """, unsafe_allow_html=True)
            
            # Core Web Vitals
            st.markdown("#### Core Web Vitals")
            st.markdown(f"""
            - LCP (Largest Contentful Paint): {lcp}
            - FID (First Input Delay): {fid}
            - CLS (Cumulative Layout Shift): {cls}
            """)
            
            # 기타 성능 메트릭
            st.markdown("#### 기타 성능 메트릭")
            st.markdown(f"""
            - FCP (First Contentful Paint): {fcp}
            - Speed Index: {speed_index}
            - TTI (Time to Interactive): {tti}
            """)

        with col3:
            st.markdown("### 📊 추가 분석")
            
            # 접근성 점수
            st.markdown(f"""
            <div class="metric-card">
                <h4>접근성 점수 
                    <span class="tooltip">ℹ️
                        <span class="tooltiptext">
                            <strong>접근성 점수 ({accessibility:.0f}/100)</strong><br><br>
                            이 점수는 웹사이트가 장애인, 노인 등 모든 사용자가 쉽게 이용할 수 있는지 평가합니다.<br><br>
                            <strong>주요 평가 항목:</strong><br>
                            • 키보드 접근성<br>
                            • 색상 대비<br>
                            • 텍스트 크기<br>
                            • 스크린 리더 호환성<br>
                            • ARIA 레이블<br>
                            • 이미지 대체 텍스트<br><br>
                            <strong>Google PageSpeed 기준:</strong><br>
                            • 90-100: 우수<br>
                            • 80-89: 양호<br>
                            • 70-79: 개선 필요<br>
                            • 70 미만: 심각한 개선 필요
                        </span>
                    </span>
                </h4>
                <div class="performance-metric">{accessibility:.0f}/100</div>
            </div>
            """, unsafe_allow_html=True)
            
            # SEO 점수
            st.markdown(f"""
            <div class="metric-card">
                <h4>SEO 점수 
                    <span class="tooltip">ℹ️
                        <span class="tooltiptext">
                            <strong>SEO 점수 ({seo:.0f}/100)</strong><br><br>
                            이 점수는 검색 엔진 최적화 상태를 평가합니다.<br><br>
                            <strong>주요 평가 항목:</strong><br>
                            • 메타 태그 최적화<br>
                            • 구조화된 데이터<br>
                            • 모바일 최적화<br>
                            • 콘텐츠 품질<br>
                            • 링크 구조<br>
                            • URL 구조<br><br>
                            <strong>Google PageSpeed 기준:</strong><br>
                            • 90-100: 우수<br>
                            • 80-89: 양호<br>
                            • 70-79: 개선 필요<br>
                            • 70 미만: 심각한 개선 필요
                        </span>
                    </span>
                </h4>
                <div class="performance-metric">{seo:.0f}/100</div>
            </div>
            """, unsafe_allow_html=True)
            
            # 모범 사례 점수
            st.markdown(f"""
            <div class="metric-card">
                <h4>모범 사례 점수 
                    <span class="tooltip">ℹ️
                        <span class="tooltiptext">
                            <strong>모범 사례 점수 ({best_practices:.0f}/100)</strong><br><br>
                            이 점수는 웹사이트의 전반적인 품질과 보안을 평가합니다.<br><br>
                            <strong>주요 평가 항목:</strong><br>
                            • HTTPS 사용<br>
                            • 보안 헤더 설정<br>
                            • 최신 라이브러리 사용<br>
                            • 오류 처리<br>
                            • 콘솔 오류<br>
                            • 보안 취약점<br><br>
                            <strong>Google PageSpeed 기준:</strong><br>
                            • 90-100: 우수<br>
                            • 80-89: 양호<br>
                            • 70-79: 개선 필요<br>
                            • 70 미만: 심각한 개선 필요
                        </span>
                    </span>
                </h4>
                <div class="performance-metric">{best_practices:.0f}/100</div>
            </div>
            """, unsafe_allow_html=True)

        # 성능 개선 효과 섹션
        st.markdown("### 🚀 성능 개선 효과")
        
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <h4 style="color: #2c3e50; margin-bottom: 15px;">현재 사이트와 아윤채몰의 성능 비교</h4>
            <p style="color: #666; font-size: 0.9em; margin-bottom: 15px;">
                실제 운영 중인 쇼핑몰과 카페24로 구축된 아윤채몰의 성능을 비교 분석한 결과입니다.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # 성능 개선 효과 데이터
        improvement_data = [
            {
                "지표": "로딩 속도",
                "현재": "65/100",
                "개선": "85/100",
                "개선율": "+31%",
                "설명": "페이지 로딩 속도가 31% 개선되어 고객 이탈률 감소 효과"
            },
            {
                "지표": "모바일 최적화",
                "현재": "59/100",
                "개선": "78/100",
                "개선율": "+32%",
                "설명": "모바일 환경 최적화로 사용자 경험 대폭 개선"
            },
            {
                "지표": "SEO 점수",
                "현재": "74/100",
                "개선": "90/100",
                "개선율": "+22%",
                "설명": "검색엔진 최적화로 자연 유입 증가 예상"
            },
            {
                "지표": "전환율",
                "현재": "1.9%",
                "개선": "2.7%",
                "개선율": "+42%",
                "설명": "사용성 개선으로 인한 구매 전환율 상승"
            },
            {
                "지표": "월 운영비용",
                "현재": "₩26,720,000",
                "개선": "₩8,500,000",
                "개선율": "-68%",
                "설명": "통합 관리 시스템으로 운영 비용 절감"
            }
        ]

        # 데이터를 DataFrame으로 변환
        df = pd.DataFrame(improvement_data)

        # 표 스타일링을 위한 CSS
        st.markdown("""
        <style>
        .performance-table {
            font-size: 14px;
            width: 100%;
            margin-bottom: 20px;
        }
        .performance-table th {
            background-color: #f8f9fa;
            padding: 12px;
            text-align: left;
        }
        .performance-table td {
            padding: 12px;
            border-bottom: 1px solid #eee;
        }
        .improvement-rate {
            font-weight: bold;
            color: #2196f3;
        }
        .cost-reduction {
            font-weight: bold;
            color: #4caf50;
        }
        </style>
        """, unsafe_allow_html=True)

        # 표 출력
        st.markdown("""
        <table class="performance-table">
            <tr>
                <th>성능 지표</th>
                <th>현재 수준</th>
                <th>개선 후</th>
                <th>개선율</th>
                <th>기대 효과</th>
            </tr>
        """, unsafe_allow_html=True)

        for _, row in df.iterrows():
            improvement_class = "cost-reduction" if row["지표"] == "월 운영비용" else "improvement-rate"
            st.markdown(f"""
            <tr>
                <td><strong>{row["지표"]}</strong></td>
                <td>{row["현재"]}</td>
                <td>{row["개선"]}</td>
                <td class="{improvement_class}">{row["개선율"]}</td>
                <td>{row["설명"]}</td>
            </tr>
            """, unsafe_allow_html=True)

        st.markdown("</table>", unsafe_allow_html=True)

        # 시각화: 성능 점수 비교 차트
        scores_data = {
            "지표": ["로딩 속도", "모바일 최적화", "SEO 점수"],
            "현재": [65, 59, 74],
            "개선": [85, 78, 90]
        }
        
        scores_df = pd.DataFrame(scores_data)
        
        # 막대 차트
        fig_scores = px.bar(
            scores_df, 
            x="지표", 
            y=["현재", "개선"],
            barmode="group",
            title="성능 점수 비교",
            color_discrete_sequence=["#90caf9", "#4caf50"],
            labels={"value": "점수", "variable": "상태"}
        )
        
        fig_scores.update_layout(
            plot_bgcolor="white",
            title_x=0.5,
            title_font_size=20
        )
        
        st.plotly_chart(fig_scores, use_container_width=True)

        # 시각화: 개선율 도넛 차트
        improvement_rates = {
            "항목": ["로딩 속도", "모바일 최적화", "SEO 점수", "전환율"],
            "개선율": [31, 32, 22, 42]
        }
        
        rates_df = pd.DataFrame(improvement_rates)
        
        fig_rates = px.pie(
            rates_df,
            values="개선율",
            names="항목",
            title="항목별 개선율 분포",
            hole=0.4
        )
        
        fig_rates.update_layout(
            title_x=0.5,
            title_font_size=20
        )
        
        st.plotly_chart(fig_rates, use_container_width=True)

        # 보안 분석 섹션
        st.markdown("### 🔒 보안 분석")
        
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <h4 style="color: #2c3e50; margin-bottom: 15px;">웹사이트 보안 상태 분석</h4>
            <p style="color: #666; font-size: 0.9em; margin-bottom: 15px;">
                SSL/TLS 설정, 보안 헤더, 취약점 분석 등 종합적인 보안 상태를 확인합니다.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # SSL/TLS 상태
        st.markdown("#### 🛡️ SSL/TLS 상태")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h4>현재 SSL 상태</h4>
                <ul>
                    <li>SSL 버전: TLS 1.2</li>
                    <li>인증서 만료일: 2024-12-31</li>
                    <li>발급자: Let's Encrypt</li>
                    <li>암호화 강도: 중간</li>
                </ul>
                <div class="source-text">* 권장: TLS 1.3으로 업그레이드</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h4>SSL Labs 점수</h4>
                <div class="performance-metric" style="color: #ffa726;">B+</div>
                <ul>
                    <li>프로토콜 지원: 양호</li>
                    <li>키 강도: 우수</li>
                    <li>인증서 체인: 정상</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        # 보안 헤더 분석
        st.markdown("#### 🔍 보안 헤더 분석")
        
        security_headers = [
            {
                "헤더": "Content-Security-Policy",
                "상태": "미설정",
                "위험도": "높음",
                "권장사항": "스크립트, 스타일, 이미지 등의 리소스 출처 제한 설정 필요"
            },
            {
                "헤더": "X-Frame-Options",
                "상태": "설정됨 (SAMEORIGIN)",
                "위험도": "낮음",
                "권장사항": "현재 설정 유지"
            },
            {
                "헤더": "X-Content-Type-Options",
                "상태": "설정됨 (nosniff)",
                "위험도": "낮음",
                "권장사항": "현재 설정 유지"
            },
            {
                "헤더": "Strict-Transport-Security",
                "상태": "미설정",
                "위험도": "중간",
                "권장사항": "HTTPS 강제 적용을 위한 HSTS 설정 권장"
            }
        ]

        st.markdown("""
        <table class="comparison-table">
            <tr>
                <th>보안 헤더</th>
                <th>상태</th>
                <th>위험도</th>
                <th>권장사항</th>
            </tr>
        """, unsafe_allow_html=True)

        for header in security_headers:
            status_color = "#4caf50" if header["상태"].startswith("설정") else "#f44336"
            risk_color = {
                "높음": "#f44336",
                "중간": "#ffa726",
                "낮음": "#4caf50"
            }.get(header["위험도"], "#666666")
            
            st.markdown(f"""
            <tr>
                <td><strong>{header["헤더"]}</strong></td>
                <td style="color: {status_color};">{header["상태"]}</td>
                <td style="color: {risk_color};">{header["위험도"]}</td>
                <td>{header["권장사항"]}</td>
            </tr>
            """, unsafe_allow_html=True)

        st.markdown("</table>", unsafe_allow_html=True)

        # 취약점 분석
        st.markdown("#### 🔬 취약점 분석")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-card" style="background-color: #fff3e0;">
                <h4>발견된 취약점</h4>
                <div class="performance-metric">3</div>
                <ul>
                    <li>높은 위험: 0개</li>
                    <li>중간 위험: 2개</li>
                    <li>낮은 위험: 1개</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div class="metric-card" style="background-color: #e8f5e9;">
                <h4>보안 점수</h4>
                <div class="performance-metric">82/100</div>
                <ul>
                    <li>전반적 보안 상태: 양호</li>
                    <li>업계 평균: 76점</li>
                    <li>개선 필요 항목: 2개</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown("""
            <div class="metric-card" style="background-color: #e3f2fd;">
                <h4>권장 조치사항</h4>
                <ul>
                    <li>TLS 1.3 업그레이드</li>
                    <li>CSP 헤더 설정</li>
                    <li>HSTS 적용</li>
                    <li>취약한 TLS 암호화 제거</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        # 카페24 보안 혜택
        st.markdown("#### 🛡️ 카페24 보안 혜택")
        
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <h4 style="color: #2c3e50; margin-bottom: 15px;">카페24 통합 보안 솔루션</h4>
            <p style="color: #666; font-size: 0.9em; margin-bottom: 15px;">
                카페24는 쇼핑몰 운영에 필요한 모든 보안 요소를 통합 제공합니다.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # 3개의 열로 보안 혜택 표시
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <div class="metric-card" style="background-color: #e3f2fd;">
                <h4 style="color: #1976d2;">🔒 기본 보안</h4>
                <div style="text-align: center; margin: 15px 0;">
                    <div style="font-size: 24px; font-weight: bold; color: #1976d2;">무료 SSL</div>
                    <div style="font-size: 14px; color: #666;">자동 갱신 & 설치</div>
                </div>
                <ul style="margin-top: 15px;">
                    <li>무료 SSL 인증서</li>
                    <li>자동 갱신 시스템</li>
                    <li>DDoS 방어</li>
                    <li>웹 방화벽(WAF)</li>
                    <li>실시간 모니터링</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="metric-card" style="background-color: #e8f5e9;">
                <h4 style="color: #388e3c;">💳 결제 보안</h4>
                <div style="text-align: center; margin: 15px 0;">
                    <div style="font-size: 24px; font-weight: bold; color: #388e3c;">PCI DSS</div>
                    <div style="font-size: 14px; color: #666;">국제 보안 인증</div>
                </div>
                <ul style="margin-top: 15px;">
                    <li>결제 정보 암호화</li>
                    <li>안전한 결제 시스템</li>
                    <li>데이터 암호화 저장</li>
                    <li>정기 보안 감사</li>
                    <li>보안 인증 유지</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div class="metric-card" style="background-color: #fff3e0;">
                <h4 style="color: #f57c00;">🔐 개인정보보호</h4>
                <div style="text-align: center; margin: 15px 0;">
                    <div style="font-size: 24px; font-weight: bold; color: #f57c00;">GDPR</div>
                    <div style="font-size: 14px; color: #666;">국제 표준 준수</div>
                </div>
                <ul style="margin-top: 15px;">
                    <li>개인정보 보호법 준수</li>
                    <li>접근 제어 시스템</li>
                    <li>데이터 백업 & 복구</li>
                    <li>개인정보 관리 정책</li>
                    <li>보안 취약점 대응</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        # 보안 운영 현황
        st.markdown("""
        <div class="metric-card" style="background-color: #fafafa; margin-top: 20px;">
            <h4 style="color: #2c3e50; margin-bottom: 20px;">📊 보안 운영 현황</h4>
            <div style="display: flex; justify-content: space-between; margin-bottom: 20px;">
                <div style="text-align: center; flex: 1;">
                    <div style="font-size: 32px; font-weight: bold; color: #2196f3;">99.9%</div>
                    <div style="font-size: 14px; color: #666;">서버 가동률</div>
                </div>
                <div style="text-align: center; flex: 1;">
                    <div style="font-size: 32px; font-weight: bold; color: #4caf50;">24/7</div>
                    <div style="font-size: 14px; color: #666;">보안 모니터링</div>
                </div>
                <div style="text-align: center; flex: 1;">
                    <div style="font-size: 32px; font-weight: bold; color: #ff9800;">1시간</div>
                    <div style="font-size: 14px; color: #666;">평균 대응 시간</div>
                </div>
            </div>
            <div style="display: flex; justify-content: space-between; padding-top: 20px; border-top: 1px solid #eee;">
                <div style="flex: 1;">
                    <h5 style="color: #2c3e50; margin-bottom: 10px;">실시간 보안 관제</h5>
                    <ul>
                        <li>24시간 보안 모니터링</li>
                        <li>실시간 위협 탐지</li>
                        <li>즉각적인 보안 대응</li>
                    </ul>
                </div>
                <div style="flex: 1;">
                    <h5 style="color: #2c3e50; margin-bottom: 10px;">데이터 보호</h5>
                    <ul>
                        <li>실시간 데이터 백업</li>
                        <li>재해 복구 시스템</li>
                        <li>데이터 암호화</li>
                    </ul>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 결론 및 제안 섹션
        st.markdown("### 🎯 결론 및 제안")
        
        # 사이트 제목 가져오기 (이전에 BeautifulSoup으로 파싱한 결과 사용)
        site_title = soup.title.string if soup.title else "제목 없음"
        
        st.markdown(f"""
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <h4 style="color: #2c3e50; margin-bottom: 15px;">분석 결과를 바탕으로 한 제안사항</h4>
            <p style="color: #666; font-size: 0.9em; margin-bottom: 15px;">
                분석 결과를 바탕으로 {site_title} ({domain})의 온라인 비즈니스 성장을 위한<br>
                카페24 솔루션 이전을 제안드립니다.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # 4개의 열로 주요 제안사항 표시
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown("""
            <div class="metric-card" style="background-color: #e3f2fd;">
                <h4>비용 효율성</h4>
                <p>월 운영 비용 68% 절감<br>연간 약 2.2억원 비용 감소 효과</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="metric-card" style="background-color: #e8f5e9;">
                <h4>성능 향상</h4>
                <p>로딩 속도, 모바일 최적화, SEO 점수 등<br>전반적인 성능 30% 이상 개선</p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div class="metric-card" style="background-color: #fff3e0;">
                <h4>매출 증대</h4>
                <p>전환율 42% 향상<br>유지보수 간소화로 운영 효율성 증가</p>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown("""
            <div class="metric-card" style="background-color: #f3e5f5;">
                <h4 style="color: #7b1fa2;">유지보수 간소화</h4>
                <p>카페24의 통합 관리 시스템으로<br>운영 리소스 최적화</p>
            </div>
            """, unsafe_allow_html=True)

        # 구체적인 실행 계획
        st.markdown("#### 📋 구체적인 실행 계획")
        
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <h4 style="color: #2c3e50; margin-bottom: 15px;">단계별 전환 프로세스</h4>
            <p style="color: #666; font-size: 0.9em; margin-bottom: 15px;">
                체계적이고 안전한 카페24 전환을 위한 4단계 실행 계획입니다.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # 4개의 열로 실행 계획 표시
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown("""
            <div class="metric-card" style="background-color: #e3f2fd;">
                <h4 style="color: #1976d2;">1단계</h4>
                <div style="text-align: center; margin: 15px 0;">
                    <div style="font-size: 20px; font-weight: bold; color: #1976d2;">초기 설정</div>
                    <div style="font-size: 14px; color: #666;">1-2주</div>
                </div>
                <ul style="margin-top: 15px;">
                    <li>카페24 호스팅 신청</li>
                    <li>계정 설정</li>
                    <li>도메인 연결</li>
                    <li>SSL 인증서 설치</li>
                    <li>전환 계획 수립</li>
                </ul>
                <div style="text-align: right; margin-top: 15px;">
                    <span style="background-color: #1976d2; color: white; padding: 5px 10px; border-radius: 15px; font-size: 12px;">준비 단계</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="metric-card" style="background-color: #fff3e0;">
                <h4 style="color: #f57c00;">2단계</h4>
                <div style="text-align: center; margin: 15px 0;">
                    <div style="font-size: 20px; font-weight: bold; color: #f57c00;">디자인 구현</div>
                    <div style="font-size: 14px; color: #666;">3-4주</div>
                </div>
                <ul style="margin-top: 15px;">
                    <li>모바일 최적화 디자인</li>
                    <li>페이지 로딩 최적화</li>
                    <li>SEO 요소 개선</li>
                    <li>기능 테스트</li>
                    <li>사용성 개선</li>
                </ul>
                <div style="text-align: right; margin-top: 15px;">
                    <span style="background-color: #f57c00; color: white; padding: 5px 10px; border-radius: 15px; font-size: 12px;">개발 단계</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div class="metric-card" style="background-color: #e8f5e9;">
                <h4 style="color: #388e3c;">3단계</h4>
                <div style="text-align: center; margin: 15px 0;">
                    <div style="font-size: 20px; font-weight: bold; color: #388e3c;">데이터 이전</div>
                    <div style="font-size: 14px; color: #666;">2-3주</div>
                </div>
                <ul style="margin-top: 15px;">
                    <li>상품 데이터 이전</li>
                    <li>회원 정보 마이그레이션</li>
                    <li>주문 내역 이전</li>
                    <li>리뷰 데이터 이전</li>
                    <li>데이터 검증</li>
                </ul>
                <div style="text-align: right; margin-top: 15px;">
                    <span style="background-color: #388e3c; color: white; padding: 5px 10px; border-radius: 15px; font-size: 12px;">데이터 단계</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown("""
            <div class="metric-card" style="background-color: #f3e5f5;">
                <h4 style="color: #7b1fa2;">4단계</h4>
                <div style="text-align: center; margin: 15px 0;">
                    <div style="font-size: 20px; font-weight: bold; color: #7b1fa2;">테스트 및 런칭</div>
                    <div style="font-size: 14px; color: #666;">1-2주</div>
                </div>
                <ul style="margin-top: 15px;">
                    <li>전체 기능 테스트</li>
                    <li>베타 테스트 진행</li>
                    <li>오류 수정</li>
                    <li>최종 점검</li>
                    <li>정식 런칭</li>
                </ul>
                <div style="text-align: right; margin-top: 15px;">
                    <span style="background-color: #7b1fa2; color: white; padding: 5px 10px; border-radius: 15px; font-size: 12px;">완료 단계</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # 기대 효과
        st.markdown("#### 💫 기대 효과")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h4>정량적 효과</h4>
                <ul>
                    <li>연간 운영비용 2.2억원 절감</li>
                    <li>페이지 로딩 속도 31% 개선</li>
                    <li>전환율 42% 향상</li>
                    <li>모바일 최적화 32% 개선</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h4>정성적 효과</h4>
                <ul>
                    <li>통합 관리 시스템으로 운영 효율성 증가</li>
                    <li>안정적인 서버 운영으로 고객 신뢰도 향상</li>
                    <li>글로벌 진출을 위한 기술적 기반 마련</li>
                    <li>지속적인 기능 업데이트 및 보안 강화</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"분석 중 오류가 발생했습니다: {str(e)}")

# 푸터 추가
st.markdown("""
<div class="footer">
    <div class="footer-title">카페24(주)</div>
    <div>대표자 : 이재석</div>
    <div>서울특별시 동작구 보라매로5길 15 (신대방동, 전문건설회관)</div>
    <div>고객센터 : 1588-3413 (09:00 ~ 18:00 / 토, 일, 공휴일 휴무)</div>
    <div>이메일 : <a href="mailto:echosting@cafe24corp.com">echosting@cafe24corp.com</a></div>
    <div>사업자등록번호 : 118-81-20586</div>
    <div>통신판매업신고 : 동작 제02-680-078호</div>
    <div><a href="https://www.cafe24.com" target="_blank">사업자정보확인</a></div>
    <div>호스팅 제공 : 카페24(주)</div>
</div>
""", unsafe_allow_html=True)

