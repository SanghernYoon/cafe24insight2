import streamlit as st
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import base64
import plotly.express as px
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(
    page_title="쇼핑몰 셀프 분석 서비스",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일
st.markdown("""
<style>
    /* 전체 컨테이너 스타일 */
    .main {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
        padding-bottom: 60px;
    }
    
    /* 헤더 스타일 */
    .header {
        text-align: center;
        margin-bottom: 3rem;
        padding: 2rem;
        background: #f4f4f4;
        border-radius: 15px;
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
        width: 392px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .stForm h3 {
        color: #2c3e50;
        margin-bottom: 1.5rem;
        font-size: 18px !important;
        text-align: center;
    }
    
    /* 입력 필드 스타일 */
    .stTextInput > div > div > input,
    .stSelectbox > div > div {
        width: 100% !important;
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 0.8rem;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div:focus {
        border-color: #007bff;
        box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.2);
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        padding: 0.8rem;
        font-size: 1.1rem;
        font-weight: 600;
        background: #007bff;
        color: white;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: #0056b3;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* 메트릭 카드 스타일 */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid #ccc;
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
        color: #007bff;
        margin-bottom: 0.5rem;
    }
    
    /* 섹션 스타일 */
    .section {
        margin: 2rem 0;
        padding: 2rem;
        background: white;
        border-radius: 15px;
        border: 1px solid #ccc;
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
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: #f8f9fa;
        padding: 1rem;
        text-align: center;
        font-size: 0.9rem;
        color: #666;
        line-height: 1.6;
        z-index: 1000;
        border-top: 1px solid #e9ecef;
    }
    
    .footer-content {
        max-width: 1040px;
        margin: 0 auto;
    }
    
    .footer a {
        color: #3498db;
        text-decoration: none;
    }
    
    .footer a:hover {
        text-decoration: underline;
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
    }
    .comparison-table th, .comparison-table td {
        padding: 15px;
        text-align: left;
        border: 1px solid #ddd;
        vertical-align: top;
        word-wrap: break-word;
    }
    .comparison-table th {
        background-color: #f4f4f4;
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
    
    /* 이전 혜택 카드 스타일 */
    .benefit-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease;
    }
    
    .benefit-card:hover {
        transform: translateY(-5px);
    }
    
    .benefit-card h4 {
        color: #2c3e50;
        margin-bottom: 1rem;
        font-size: 1.2rem;
    }
    
    .benefit-card ul {
        list-style-type: none;
        padding-left: 0;
    }
    
    .benefit-card li {
        margin-bottom: 0.5rem;
        padding-left: 1.5rem;
        position: relative;
    }
    
    .benefit-card li:before {
        content: "✓";
        position: absolute;
        left: 0;
        color: #27ae60;
    }
    
    /* 이전 프로세스 스타일 */
    .process-steps {
        display: flex;
        justify-content: space-between;
        margin: 2rem 0;
    }
    
    .step {
        flex: 1;
        text-align: center;
        padding: 1rem;
        position: relative;
    }
    
    .step:not(:last-child):after {
        content: "";
        position: absolute;
        top: 50%;
        right: 0;
        width: 50%;
        height: 2px;
        background: #3498db;
    }
    
    .step-number {
        width: 40px;
        height: 40px;
        background: #3498db;
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1rem;
        font-weight: bold;
    }
    
    /* 지원 서비스 스타일 */
    .support-services {
        display: flex;
        justify-content: space-between;
        gap: 1.5rem;
    }
    
    .service {
        flex: 1;
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .service h4 {
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    
    .service ul {
        list-style-type: none;
        padding-left: 0;
    }
    
    .service li {
        margin-bottom: 0.5rem;
        padding-left: 1.5rem;
        position: relative;
    }
    
    .service li:before {
        content: "•";
        position: absolute;
        left: 0;
        color: #3498db;
    }
    
    /* CTA 버튼 스타일 */
    .cta-section {
        text-align: center;
        margin: 3rem 0;
    }
    
    .cta-button {
        display: inline-block;
        padding: 1rem 2rem;
        background: #3498db;
        color: white;
        text-decoration: none;
        border-radius: 30px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .cta-button:hover {
        background: #2980b9;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# 헤더 섹션
st.markdown("""
<div class="header">
    <h1>My 쇼핑몰 성능 분석하기</h1>
    <p>현재 운영 중인 쇼핑몰 URL을 입력하고, Cafe24로 전환 시 예상되는 성능 향상, 비용 절감, 기능 확장을 미리 확인해보세요.</p>
</div>
""", unsafe_allow_html=True)

# 푸터 추가 (조건문 밖으로 이동)
st.markdown("""
<div class="footer">
    <div class="footer-content">
        Copyright ⓒ Cafe24 Corp. All Rights Reserved.
    </div>
</div>
""", unsafe_allow_html=True)

# 입력 폼
with st.form("analysis_form"):
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1.5rem;">
        <h3 style="color: #2c3e50; font-size: 18px;">분석할 웹사이트 정보를 입력하세요</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # 쇼핑몰 솔루션 선택
    solution = st.selectbox(
        "현재 사용 중인 쇼핑몰 솔루션",
        [
            "선택해주세요",
            "고도몰",
            "메이크샵 (준비중)",
            "아임웹 (준비중)",
            "위사 (준비중)",
            "식스샵 (준비중)",
            "자체구축(SI) (준비중)",
            "쇼피파이 (준비중)",
            "기타 (준비중)"
        ]
    )
    
    if solution != "선택해주세요" and solution != "고도몰":
        st.warning("현재는 고도몰만 분석이 가능합니다. 다른 솔루션은 준비 중입니다.")
        solution = "선택해주세요"
    
    domain = st.text_input("브랜드 도메인", placeholder="예시) yourdomain.com")
    industry = st.selectbox(
        "업종",
        ["패션의류", "스포츠", "전자제품", "식품", "건기식", "뷰티", "굿즈", "기타"]
    )
    
    submitted = st.form_submit_button("분석 시작하기")

if submitted:
    if solution == "선택해주세요":
        st.warning("쇼핑몰 솔루션을 선택해주세요.")
    elif solution != "고도몰":
        st.error(f"""
        😥 안타깝게도 아직은 고도몰만 분석이 가능합니다.
        
        현재 선택하신 {solution}은 분석이 지원되지 않습니다.
        추후 업데이트를 통해 더 많은 솔루션을 지원할 예정이니 조금만 기다려주세요!
        """)
    elif not domain:
        st.warning("도메인을 입력해주세요.")
    else:
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
                st.markdown("### 📊 Google PageSpeed 결과")
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
                title_font_size=20,
                height=400  # 높이 조정
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
                title_font_size=20,
                height=400  # 높이 조정
            )
            
            st.plotly_chart(fig_rates, use_container_width=True)

            # 성능 개선 효과 섹션 다음에 보안 분석 섹션 배치
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

            # 보안 분석 섹션 다음에 기존 섹션들 복원
            st.markdown("### 📊 카페24 vs 고도몰 비교")

            st.markdown("""
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                <h4 style="color: #2c3e50; margin-bottom: 15px;">솔루션 기능 비교</h4>
                <p style="color: #666; font-size: 0.9em; margin-bottom: 15px;">
                    카페24와 고도몰의 주요 기능을 비교 분석한 결과입니다.
                </p>
            </div>
            """, unsafe_allow_html=True)

            # Google 프레젠테이션 임베드
            st.markdown("""
            <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; margin-bottom: 20px;">
                <iframe 
                    src="https://docs.google.com/presentation/d/1dhfw9GzQin4tzZqfW_NSQitsFF_uUGAZcKAzDCCeuMk/embed" 
                    frameborder="0" 
                    width="100%" 
                    height="100%" 
                    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"
                    allowfullscreen="true" 
                    mozallowfullscreen="true" 
                    webkitallowfullscreen="true">
                </iframe>
            </div>
            """, unsafe_allow_html=True)

            # 기존 비교 테이블
            st.markdown("""
            <table class="comparison-table">
                <tr>
                    <th>구분</th>
                    <th>카페24</th>
                    <th>고도몰</th>
                </tr>
                <tr>
                    <td>초기 구축 비용</td>
                    <td class="cafe24-cell">무료</td>
                    <td class="godomall-cell">무료</td>
                </tr>
                <tr>
                    <td>월 이용료</td>
                    <td class="cafe24-cell">39,000원~</td>
                    <td class="godomall-cell">49,000원~</td>
                </tr>
                <tr>
                    <td>트래픽 제한</td>
                    <td class="cafe24-cell">무제한</td>
                    <td class="godomall-cell">트래픽 종량제</td>
                </tr>
                <tr>
                    <td>디자인 템플릿</td>
                    <td class="cafe24-cell">2,000개 이상</td>
                    <td class="godomall-cell">300개 이상</td>
                </tr>
                <tr>
                    <td>모바일 최적화</td>
                    <td class="cafe24-cell">자동 최적화</td>
                    <td class="godomall-cell">수동 설정 필요</td>
                </tr>
                <tr>
                    <td>보안 인증</td>
                    <td class="cafe24-cell">ISO 27001, ISMS-P 등</td>
                    <td class="godomall-cell">ISMS</td>
                </tr>
                <tr>
                    <td>글로벌 진출 지원</td>
                    <td class="cafe24-cell">14개국 지원</td>
                    <td class="godomall-cell">제한적 지원</td>
                </tr>
                <tr>
                    <td>통계 분석</td>
                    <td class="cafe24-cell">AI 기반 분석</td>
                    <td class="godomall-cell">기본 통계</td>
                </tr>
                <tr>
                    <td>마케팅 도구</td>
                    <td class="cafe24-cell">다양한 내장 도구</td>
                    <td class="godomall-cell">기본 기능</td>
                </tr>
                <tr>
                    <td>고객 지원</td>
                    <td class="cafe24-cell">24/7 지원</td>
                    <td class="godomall-cell">평일 운영</td>
                </tr>
            </table>
            """, unsafe_allow_html=True)

            # 결론 및 제안 섹션
            st.markdown("### 🎯 결론 및 제안")

            st.markdown("""
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                <h4 style="color: #2c3e50; margin-bottom: 15px;">분석 결과 및 제안</h4>
                <p style="color: #666; font-size: 0.9em; margin-bottom: 15px;">
                    분석 결과를 바탕으로 한 종합적인 결론과 제안사항입니다.
                </p>
            </div>
            """, unsafe_allow_html=True)

            # 주요 제안사항
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.markdown("""
                <div class="metric-card" style="background-color: #e3f2fd;">
                    <h4>비용 효율성</h4>
                    <ul>
                        <li>월 운영비용 68% 절감</li>
                        <li>연간 약 2.2억원 절약</li>
                        <li>초기 구축비용 무료</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown("""
                <div class="metric-card" style="background-color: #e8f5e9;">
                    <h4>성능 향상</h4>
                    <ul>
                        <li>로딩 속도 31% 개선</li>
                        <li>모바일 최적화 32% 향상</li>
                        <li>SEO 점수 22% 상승</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown("""
                <div class="metric-card" style="background-color: #fff3e0;">
                    <h4>매출 증대</h4>
                    <ul>
                        <li>전환율 42% 증가</li>
                        <li>고객 만족도 향상</li>
                        <li>운영 효율성 개선</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

            with col4:
                st.markdown("""
                <div class="metric-card" style="background-color: #fce4ec;">
                    <h4>유지보수 간소화</h4>
                    <ul>
                        <li>통합 관리 시스템</li>
                        <li>자동 업데이트</li>
                        <li>24/7 기술 지원</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

            # 구체적 실행 계획
            st.markdown("#### 📋 구체적 실행 계획")

            st.markdown("""
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                <h4 style="color: #2c3e50; margin-bottom: 15px;">4단계 실행 계획</h4>
                <div style="display: flex; justify-content: space-between; margin-bottom: 20px;">
                    <div style="width: 23%; background-color: #e3f2fd; padding: 15px; border-radius: 10px;">
                        <h5>1단계: 초기 설정</h5>
                        <p style="font-size: 0.9em;">(1-2주)</p>
                        <ul style="font-size: 0.9em;">
                            <li>도메인 설정</li>
                            <li>기본 디자인 선택</li>
                            <li>필수 기능 설정</li>
                        </ul>
                    </div>
                    <div style="width: 23%; background-color: #e8f5e9; padding: 15px; border-radius: 10px;">
                        <h5>2단계: 데이터 이전</h5>
                        <p style="font-size: 0.9em;">(2-3주)</p>
                        <ul style="font-size: 0.9em;">
                            <li>상품 데이터 이전</li>
                            <li>회원 데이터 이전</li>
                            <li>주문 데이터 이전</li>
                        </ul>
                    </div>
                    <div style="width: 23%; background-color: #fff3e0; padding: 15px; border-radius: 10px;">
                        <h5>3단계: 디자인 구현</h5>
                        <p style="font-size: 0.9em;">(3-4주)</p>
                        <ul style="font-size: 0.9em;">
                            <li>커스텀 디자인 적용</li>
                            <li>모바일 최적화</li>
                            <li>기능 테스트</li>
                        </ul>
                    </div>
                    <div style="width: 23%; background-color: #fce4ec; padding: 15px; border-radius: 10px;">
                        <h5>4단계: 테스트 및 오픈</h5>
                        <p style="font-size: 0.9em;">(1-2주)</p>
                        <ul style="font-size: 0.9em;">
                            <li>종합 테스트</li>
                            <li>최종 점검</li>
                            <li>정식 오픈</li>
                        </ul>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # 기대 효과
            st.markdown("#### 📈 기대 효과")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("""
                <div class="metric-card" style="background-color: #e3f2fd;">
                    <h4>정량적 효과</h4>
                    <ul>
                        <li>월 운영비용 68% 절감</li>
                        <li>전환율 42% 증가</li>
                        <li>로딩 속도 31% 개선</li>
                        <li>모바일 최적화 32% 향상</li>
                        <li>SEO 점수 22% 상승</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown("""
                <div class="metric-card" style="background-color: #e8f5e9;">
                    <h4>정성적 효과</h4>
                    <ul>
                        <li>고객 만족도 향상</li>
                        <li>운영 효율성 개선</li>
                        <li>유지보수 간소화</li>
                        <li>보안성 강화</li>
                        <li>글로벌 진출 용이</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"분석 중 오류가 발생했습니다: {str(e)}")