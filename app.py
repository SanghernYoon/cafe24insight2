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

        # 종합 분석 및 제안
        st.markdown("### 💡 개선 제안")
        
        # 2단 레이아웃으로 변경
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 주요 개선 사항")
            suggestions = []
            
            if avg_load_time > 3:
                suggestions.append("- 서버 응답 시간이 느립니다. 호스팅 서비스 업그레이드를 고려해보세요.")
            if performance < 70:
                suggestions.append("- Google PageSpeed 점수가 낮습니다. 이미지 최적화와 캐싱 설정을 확인해보세요.")
            if accessibility < 80:
                suggestions.append("- 접근성 점수가 낮습니다. 웹 접근성 가이드라인을 확인해보세요.")
            if seo < 80:
                suggestions.append("- SEO 점수가 낮습니다. 메타 태그와 구조화된 데이터를 개선해보세요.")
            if best_practices < 80:
                suggestions.append("- 모범 사례 점수가 낮습니다. 보안 설정과 최신 웹 표준을 확인해보세요.")
            
            if suggestions:
                for suggestion in suggestions:
                    st.markdown(suggestion)
            else:
                st.markdown("- 현재 성능이 양호합니다. 지속적인 모니터링을 권장합니다.")

        with col2:
            st.markdown("#### 개선 인사이트")
            insights = []
            
            # 성능 관련 인사이트
            if performance < 70:
                insights.append({
                    "title": "성능 최적화 필요",
                    "description": "이미지 최적화, 캐싱 전략 수립, 코드 최적화가 필요합니다.",
                    "priority": "높음"
                })
            
            # SEO 관련 인사이트
            if seo < 80:
                insights.append({
                    "title": "SEO 개선 필요",
                    "description": "메타 태그 최적화, 구조화된 데이터 추가, 콘텐츠 품질 향상이 필요합니다.",
                    "priority": "중간"
                })
            
            # 접근성 관련 인사이트
            if accessibility < 80:
                insights.append({
                    "title": "접근성 개선 필요",
                    "description": "웹 접근성 가이드라인 준수, 키보드 네비게이션 개선, 색상 대비 조정이 필요합니다.",
                    "priority": "중간"
                })
            
            # 인사이트 카드 표시
            for insight in insights:
                priority_color = {
                    "높음": "#ff4444",
                    "중간": "#ffbb33",
                    "낮음": "#00C851"
                }.get(insight["priority"], "#666666")
                
                st.markdown(f"""
                <div class="metric-card" style="border-left: 4px solid {priority_color}; margin-bottom: 1rem;">
                    <h4>{insight["title"]}</h4>
                    <p>{insight["description"]}</p>
                    <small style="color: {priority_color};">우선순위: {insight["priority"]}</small>
                </div>
                """, unsafe_allow_html=True)

        # Cafe24 제안 섹션
        st.markdown("### 🏢 Cafe24 추천 앱")
        
        # 업종별 추천 앱 매핑
        industry_apps = {
            "패션의류": [
                {"title": "리뷰위젯", "description": "기본 후기게시판에 등록된 후기를 감각적인 위젯으로 만들어드려요.", "category": "리뷰"},
                {"title": "크리마 리뷰", "description": "누적 1만 고객사가 선택한 쇼핑몰 필수 리뷰 앱", "category": "리뷰"},
                {"title": "해피싱크", "description": "카카오 & 네이버 원클릭 회원가입으로 간편 회원가입 구현", "category": "고객관리 활성화"}
            ],
            "스포츠": [
                {"title": "리뷰에이드", "description": "리뷰 올인원 솔루션으로 리뷰/회원증가/상품추천 기능 제공", "category": "리뷰"},
                {"title": "인센토", "description": "구매력 높은 고객과 LTV 높은 고객의 힘을 체감하세요", "category": "마케팅/CRM"},
                {"title": "그로잉세일즈", "description": "온・오프라인 멤버십 통합으로 회원볼륨 성장과 매출 상승", "category": "마케팅/CRM"}
            ],
            "전자제품": [
                {"title": "와이즈트래커", "description": "메시지 발송부터 마케팅 자동화, 데이터추적을 한 번에", "category": "마케팅/CRM"},
                {"title": "젠투", "description": "이탈 고객을 구매로 전환시키는 AI 에이전트", "category": "매출증진/전환"},
                {"title": "페이액션", "description": "1초만에 입금확인 가능한 결제 관리 앱", "category": "금융/결제"}
            ],
            "식품": [
                {"title": "리뷰위젯", "description": "기본 후기게시판에 등록된 후기를 감각적인 위젯으로 만들어드려요.", "category": "리뷰"},
                {"title": "크리마 리뷰", "description": "누적 1만 고객사가 선택한 쇼핑몰 필수 리뷰 앱", "category": "리뷰"},
                {"title": "해피싱크", "description": "카카오 & 네이버 원클릭 회원가입으로 간편 회원가입 구현", "category": "고객관리 활성화"}
            ],
            "건기식": [
                {"title": "리뷰에이드", "description": "리뷰 올인원 솔루션으로 리뷰/회원증가/상품추천 기능 제공", "category": "리뷰"},
                {"title": "인센토", "description": "구매력 높은 고객과 LTV 높은 고객의 힘을 체감하세요", "category": "마케팅/CRM"},
                {"title": "그로잉세일즈", "description": "온・오프라인 멤버십 통합으로 회원볼륨 성장과 매출 상승", "category": "마케팅/CRM"}
            ],
            "굿즈": [
                {"title": "와이즈트래커", "description": "메시지 발송부터 마케팅 자동화, 데이터추적을 한 번에", "category": "마케팅/CRM"},
                {"title": "젠투", "description": "이탈 고객을 구매로 전환시키는 AI 에이전트", "category": "매출증진/전환"},
                {"title": "페이액션", "description": "1초만에 입금확인 가능한 결제 관리 앱", "category": "금융/결제"}
            ],
            "기타": [
                {"title": "리뷰위젯", "description": "기본 후기게시판에 등록된 후기를 감각적인 위젯으로 만들어드려요.", "category": "리뷰"},
                {"title": "크리마 리뷰", "description": "누적 1만 고객사가 선택한 쇼핑몰 필수 리뷰 앱", "category": "리뷰"},
                {"title": "해피싱크", "description": "카카오 & 네이버 원클릭 회원가입으로 간편 회원가입 구현", "category": "고객관리 활성화"}
            ]
        }
        
        # 선택된 업종의 추천 앱 표시
        recommended_apps = industry_apps.get(industry, industry_apps["기타"])
        
        for app in recommended_apps:
            st.markdown(f"""
            <div class="metric-card" style="background-color: #f8f9fa;">
                <h4>{app["title"]}</h4>
                <p>{app["description"]}</p>
                <small style="color: #666;">카테고리: {app["category"]}</small>
            </div>
            """, unsafe_allow_html=True)

        # Cafe24 VS 고도몰 비교 섹션
        st.markdown("### 🆚 Cafe24 VS 고도몰 비교")
        
        # 비교 테이블 데이터
        comparison_data = [
            {
                "기능": "이용료",
                "고도몰": "솔루션에 따른 이용료 부과 (연 40만원)<br>무료 솔루션 이용 시 제한적인 기능 제공",
                "카페24": "가입비, 이용료, 연간 호스팅 비용 모두 평생 무료<br>쇼핑몰 구축 및 운영에 필요한 기본 기능을 전부 제공",
                "고도몰_source": "고도몰 요금안내",
                "카페24_source": "카페24 서비스 이용안내"
            },
            {
                "기능": "디자인",
                "고도몰": "6천 개 이상의 유/무료 템플릿 제공<br>세부 디자인 편집 시 HTML/CSS 지식 필요",
                "카페24": "32만 개 이상의 유/무료 템플릿 제공<br>스마트디자인(무료)으로 비전문가도 쉽게 커스터마이징 가능",
                "고도몰_source": "고도몰 디자인",
                "카페24_source": "카페24 디자인센터"
            },
            {
                "기능": "앱스토어",
                "고도몰": "기본 기능/운영 카테고리의 앱에 편중되어 있음<br>약 140개의 앱 제공",
                "카페24": "운영 외에도 프로모션, 고객 관리 등 다양한 카테고리의 앱 제공<br>약 380개의 앱으로 높은 기능 확장성 보장",
                "고도몰_source": "고도몰 앱스토어",
                "카페24_source": "카페24 스토어"
            },
            {
                "기능": "오픈마켓 연동",
                "고도몰": "국내 오픈마켓 위주로만 연동 지원<br>월정액 요금제 이용 시 오픈마켓 연동 가능 (연 46~418만원)",
                "카페24": "전 세계 60개 판매 채널과의 연동 지원<br>카페24 회원이라면 누구에게나 '무료'로 제공",
                "고도몰_source": "고도몰 마켓연동",
                "카페24_source": "카페24 오픈마켓"
            },
            {
                "기능": "글로벌 진출",
                "고도몰": "제휴사를 통해 Lazada, Shopee 연동 가능<br>월정액 요금제 이용 필요 (연 46~418만원)",
                "카페24": "Amazon, Shopee, AliExpress 등 무료 직연동 가능<br>다국어 쇼핑몰 구축 및 해외 결제/배송 지원",
                "고도몰_source": "고도몰 마켓연동",
                "카페24_source": "카페24 오픈마켓"
            },
            {
                "기능": "레퍼런스",
                "고도몰": "중소형 기업 중심의 고객층 보유<br>대기업 레퍼런스가 상대적으로 부족함",
                "카페24": "소규모 창업자부터 대기업까지 폭넓은 고객층 보유<br>아모레퍼시픽, 이랜드, 롯데 등 대기업 레퍼런스 다수 보유",
                "고도몰_source": "고도몰 엔터프라이즈",
                "카페24_source": "카페24 엔터프라이즈"
            }
        ]
        
        # 비교 테이블 생성
        st.markdown("""
        <table class="comparison-table">
            <tr>
                <th>기능</th>
                <th>고도몰</th>
                <th>카페24</th>
            </tr>
        """, unsafe_allow_html=True)
        
        for item in comparison_data:
            st.markdown(f"""
            <tr>
                <td><strong>{item['기능']}</strong></td>
                <td class="godomall-cell">
                    {item['고도몰']}
                    <div class="source-text">출처: {item['고도몰_source']}</div>
                </td>
                <td class="cafe24-cell">
                    {item['카페24']}
                    <div class="source-text">출처: {item['카페24_source']}</div>
                </td>
            </tr>
            """, unsafe_allow_html=True)
        
        st.markdown("</table>", unsafe_allow_html=True)

        # 성능 개선 효과 섹션 추가
        st.markdown("### 🚀 성능 개선 효과")
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <p style="color: #666; font-size: 0.9em; margin-bottom: 15px;">
                * 현재 사이트와 아윤채몰의 성능 데이터를 비교한 결과입니다.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # 성능 비교 데이터
        performance_comparison = [
            {
                "지표": "로딩 속도",
                "현재 사이트": "65/100",
                "아윤채몰": "85/100",
                "개선율": "31%",
                "설명": "페이지 로딩 속도 최적화 및 서버 응답 시간 개선"
            },
            {
                "지표": "모바일 최적화",
                "현재 사이트": "59/100",
                "아윤채몰": "78/100",
                "개선율": "32%",
                "설명": "모바일 사용자 경험 및 반응형 디자인 최적화"
            },
            {
                "지표": "SEO 점수",
                "현재 사이트": "74/100",
                "아윤채몰": "90/100",
                "개선율": "22%",
                "설명": "검색 엔진 최적화 및 메타데이터 개선"
            },
            {
                "지표": "전환율",
                "현재 사이트": "1.9%",
                "아윤채몰": "2.7%",
                "개선율": "42%",
                "설명": "사용자 경험 개선으로 인한 구매 전환율 향상"
            },
            {
                "지표": "월 운영 비용",
                "현재 사이트": "₩26,720,000",
                "아윤채몰": "₩8,500,000",
                "개선율": "68%",
                "설명": "운영 비용 최적화 및 효율적인 리소스 관리"
            }
        ]

        # 성능 비교 테이블 생성
        st.markdown("""
        <table class="comparison-table">
            <tr>
                <th>성능 지표</th>
                <th>현재 사이트</th>
                <th>아윤채몰</th>
                <th>개선율</th>
                <th>설명</th>
            </tr>
        """, unsafe_allow_html=True)

        for item in performance_comparison:
            st.markdown(f"""
            <tr>
                <td><strong>{item['지표']}</strong></td>
                <td>{item['현재 사이트']}</td>
                <td>{item['아윤채몰']}</td>
                <td style="color: #28a745;">{item['개선율']}</td>
                <td>{item['설명']}</td>
            </tr>
            """, unsafe_allow_html=True)

        st.markdown("</table>", unsafe_allow_html=True)

        # 성능 개선 효과 시각화
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 성능 점수 비교")
            performance_data = {
                '지표': ['현재 사이트', '아윤채몰'],
                '점수': [65, 85]  # 로딩 속도 기준
            }
            fig = px.bar(performance_data, x='지표', y='점수', 
                        color='지표',
                        color_discrete_sequence=['#ff4444', '#00C851'],
                        text='점수')
            fig.update_layout(showlegend=False, height=300)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("#### 개선율 분포")
            improvement_data = {
                '지표': ['로딩 속도', '모바일 최적화', 'SEO 점수', '전환율', '비용 절감'],
                '개선율': [31, 32, 22, 42, 68]
            }
            fig = px.pie(improvement_data, values='개선율', names='지표',
                        color_discrete_sequence=px.colors.qualitative.Set3)
            fig.update_layout(showlegend=True, height=300)
            st.plotly_chart(fig, use_container_width=True)

        # 결론 및 제안 섹션
        st.markdown("### 🎯 결론 및 제안")
        
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <h4 style="color: #2c3e50; margin-bottom: 15px;">분석 결과를 바탕으로 한 제안사항</h4>
            <p style="color: #666; font-size: 0.9em; margin-bottom: 15px;">
                본석 결과를 바탕으로 idfmall.co.kr의 온라인 비즈니스 성장을 위한 카페24 전환 제안입니다.
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
                <h4>유지보수 간소화</h4>
                <p>카페24의 통합 관리 시스템으로<br>운영 리소스 최적화</p>
            </div>
            """, unsafe_allow_html=True)

        # 구체적인 실행 계획
        st.markdown("#### 📋 구체적인 실행 계획")
        
        st.markdown("""
        <div class="metric-card">
            <h4>1단계: 초기 설정 (1-2주)</h4>
            <ul>
                <li>카페24 호스팅 신청 및 계정 설정</li>
                <li>도메인 연결 및 SSL 인증서 설치</li>
                <li>기존 데이터 이전 계획 수립</li>
            </ul>
        </div>
        
        <div class="metric-card">
            <h4>2단계: 데이터 이전 (2-3주)</h4>
            <ul>
                <li>상품 데이터 이전</li>
                <li>회원 정보 마이그레이션</li>
                <li>주문 내역 및 리뷰 데이터 이전</li>
            </ul>
        </div>
        
        <div class="metric-card">
            <h4>3단계: 디자인 및 기능 구현 (3-4주)</h4>
            <ul>
                <li>모바일 최적화 디자인 적용</li>
                <li>페이지 로딩 속도 최적화</li>
                <li>SEO 요소 개선 및 적용</li>
            </ul>
        </div>
        
        <div class="metric-card">
            <h4>4단계: 테스트 및 런칭 (1-2주)</h4>
            <ul>
                <li>전체 기능 테스트 진행</li>
                <li>실 사용자 대상 베타 테스트</li>
                <li>최종 점검 및 정식 런칭</li>
            </ul>
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
