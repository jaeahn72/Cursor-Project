import streamlit as st
from travel_agent import TravelAssistant
import os
from dotenv import load_dotenv
from datetime import datetime, date, timedelta
import requests  # requests 모듈 추가

# 환경 변수 로드
load_dotenv()

# 세션 상태 초기화
if 'destination' not in st.session_state:
    st.session_state.destination = ""

# 페이지 설정
st.set_page_config(
    page_title="Sid & Teddy's Journey AI - Beta 1.0",
    layout="wide"
)

# CSS 스타일 적용
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');

/* 전체 폰트 스타일 */
html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif !important;
    font-weight: 400;
}

/* 메인 컨테이너 스타일 */
.main {
    background-color: rgba(255, 255, 255, 0.95);
    padding: 2rem;
    border-radius: 10px;
    margin: 1rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* 버전 정보 스타일 */
.version-info {
    font-size: 0.8rem;
    color: #666;
    margin-top: 0.5rem;
}

/* 나머지 스타일 */
h1 {
    font-weight: 700 !important;
    color: #1E1E1E;
    margin: 0;
}

h2, h3 {
    font-weight: 500 !important;
    color: #2E2E2E;
}

.stButton>button {
    background-color: #2E2E2E;
    color: white;
    font-weight: 500;
    border-radius: 5px;
    padding: 0.5rem 1rem;
    border: none;
    transition: all 0.3s ease;
}

.stButton>button:hover {
    background-color: #4E4E4E;
    transform: translateY(-2px);
}

.stTextInput>div>div>input {
    border-radius: 5px;
    border: 1px solid #E0E0E0;
}

.css-1d391kg {
    background-color: rgba(255, 255, 255, 0.95);
}

/* 메뉴 스타일 개선 */
.stSelectbox {
    background-color: white;
    border-radius: 5px;
    margin-bottom: 1rem;
}

.menu-item {
    display: flex;
    align-items: center;
    padding: 0.5rem;
    border-radius: 5px;
    transition: all 0.3s ease;
}

.menu-item:hover {
    background-color: rgba(0, 0, 0, 0.05);
}

/* 푸터 스타일 */
.footer {
    text-align: center;
    color: #666;
    padding: 1rem;
    font-size: 0.8rem;
}

.footer-version {
    margin-top: 0.5rem;
    font-size: 0.7rem;
}
</style>
""", unsafe_allow_html=True)

# 메인 컨테이너 시작
with st.container():
    st.markdown('<div class="main">', unsafe_allow_html=True)
    
    # 타이틀과 버전 정보
    st.title("✈️ Sid & Teddy's Journey AI")
    st.markdown('<p class="version-info">Beta 1.0</p>', unsafe_allow_html=True)
    st.markdown("여행 계획부터 숙소, 맛집까지 모든 것을 도와드립니다!")

    # 사이드바
    st.sidebar.title("🗺️ 메뉴")

    # 활성화된 메뉴와 비활성화된 메뉴 구분
    active_menus = ["🏠 홈", "🍽️ 맛집 추천", "🏨 숙소 찾기", "💱 환율 정보"]
    disabled_menus = ["🚌 교통 정보", "🎉 이벤트/축제", "🆘 비상 연락처", "🍜 현지 음식", "🛍️ 쇼핑 정보"]

    # 활성화된 메뉴 먼저 표시
    menu_options = ["🏠 홈"]
    for m in ["🍽️ 맛집 추천", "🏨 숙소 찾기", "💱 환율 정보"]:
        menu_options.append(m)

    # 메뉴 선택
    menu = st.sidebar.selectbox(
        "메뉴를 선택하세요",
        menu_options
    )

    # 비활성화된 메뉴 선택 시 알림
    if menu in disabled_menus:
        st.error("해당 기능은 현재 준비 중입니다. 다른 메뉴를 선택해주세요.")
        st.stop()

    # TravelAssistant 인스턴스 생성
    assistant = TravelAssistant()

    def show_restaurant_recommendations():
        st.title("🍽️ 맛집 추천")
        
        # 사용자 입력 (세션 상태 사용)
        location = st.text_input("지역을 입력하세요 (예: 서울, 부산)", value=st.session_state.destination)
        if location != st.session_state.destination:
            st.session_state.destination = location
        cuisine = st.selectbox("음식 종류", ["한식", "중식", "일식", "양식", "분식", "기타"])
        budget = st.selectbox("예산 범위", ["10,000원 이하", "10,000-30,000원", "30,000-50,000원", "50,000원 이상"])
        
        if st.button("맛집 찾기"):
            with st.spinner("맛집을 찾고 있습니다..."):
                # 맛집 추천
                restaurants = assistant.find_restaurants(location, cuisine=cuisine, budget=budget)
                
                if isinstance(restaurants, str):
                    st.error(restaurants)
                else:
                    st.success("맛집 추천이 완성되었습니다!")
                    
                    for i, restaurant in enumerate(restaurants, 1):
                        with st.container():
                            st.markdown(f"### {i}. {restaurant['name']}")
                            
                            # 기본 정보
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown(f"**평점**: ⭐ {restaurant['rating']}")
                                st.markdown(f"**가격대**: {restaurant['price_range']}")
                            with col2:
                                st.markdown(f"**주소**: {restaurant['address']}")
                                st.markdown(f"**영업시간**: {restaurant['opening_hours']}")
                            
                            # 설명
                            st.markdown(f"**설명**: {restaurant['description']}")
                            
                            # 대표 메뉴
                            if restaurant['specialties'] and restaurant['specialties'][0] != "메뉴 정보 없음":
                                st.markdown("**대표 메뉴**:")
                                for specialty in restaurant['specialties']:
                                    st.markdown(f"- {specialty}")
                            
                            st.markdown("---")

    # 메인 콘텐츠
    if menu == "🏠 홈":
        st.title("🧳 여행 도우미 AI")
        st.write("여행 계획을 도와드립니다!")
        
        # 여행지 입력
        destination = st.text_input("여행지를 입력하세요 (예: 서울, 도쿄, 뉴욕, 파리, 런던, 로마, 베니스, 바르셀로나, 암스테르담, 싱가포르, 방콕, 두바이)", 
                                  value=st.session_state.destination)
        
        # 검색 버튼
        if st.button("검색", use_container_width=True):
            if destination:
                if destination != st.session_state.destination:
                    st.session_state.destination = destination
                
                with st.spinner(f"{destination} 여행 정보를 불러오는 중..."):
                    # 날씨 정보
                    weather = assistant.get_weather(destination, datetime.now().strftime("%Y-%m-%d"))
                    if isinstance(weather, dict):
                        st.subheader("🌤️ 날씨 정보")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("**현재 날씨**")
                            current = weather['현재 날씨']
                            st.write(f"🌡️ 온도: {current['온도']}")
                            st.write(f"🌡️ 체감온도: {current['체감온도']}")
                            st.write(f"☁️ 날씨: {current['날씨']}")
                            st.write(f"💧 습도: {current['습도']}")
                        
                        with col2:
                            st.write("**일일 예보**")
                            forecast = weather['일일 예보']
                            st.write(f"📈 최고기온: {forecast['최고기온']}")
                            st.write(f"📉 최저기온: {forecast['최저기온']}")
                            st.write(f"🌧️ 강수확률: {forecast['강수확률']}")
                            st.write(f"☔ 강수량: {forecast['총강수량']}")
                    
                    # 환율 정보
                    exchange_info = assistant.get_exchange_info(destination)
                    if isinstance(exchange_info, dict):
                        st.subheader("💱 환율 정보")
                        currency_info = exchange_info["currency_info"]
                        rates = exchange_info["exchange_rates"]
                        base_currency = exchange_info["base_currency"]
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("**통화 정보**")
                            st.write(f"통화명: {currency_info['통화명']}")
                            st.write(f"통화 기호: {currency_info['기호']}")
                        
                        with col2:
                            st.write("**환율 정보**")
                            if base_currency == "KRW":
                                st.write("1,000원 기준:")
                                if "USD" in rates:
                                    st.write(f"USD: ${rates['USD']:.2f}")
                                if "JPY" in rates:
                                    st.write(f"JPY: ¥{rates['JPY']:.0f}")
                            elif base_currency == "JPY":
                                st.write("100엔 기준:")
                                if "KRW" in rates:
                                    st.write(f"KRW: ₩{rates['KRW']*1000:.0f}")
                                if "USD" in rates:
                                    st.write(f"USD: ${rates['USD']:.2f}")
                            elif base_currency == "USD":
                                st.write("1달러 기준:")
                                if "KRW" in rates:
                                    st.write(f"KRW: ₩{rates['KRW']:.0f}")
                                if "JPY" in rates:
                                    st.write(f"JPY: ¥{rates['JPY']:.0f}")
                            elif base_currency == "EUR":
                                st.write("1유로 기준:")
                                if "KRW" in rates:
                                    st.write(f"KRW: ₩{rates['KRW']:.0f}")
                                if "USD" in rates:
                                    st.write(f"USD: ${rates['USD']:.2f}")
                        
                        # 결제 정보
                        st.subheader("💳 결제 정보")
                        payment = currency_info["현금/카드"]
                        for method, info in payment.items():
                            with st.expander(f"**{method}**"):
                                st.write(info)
                    else:
                        st.warning(exchange_info)
            else:
                st.error("여행지를 입력해주세요.")

        # 여행지 입력 시 대표 이미지 표시
        if destination:
            photos = assistant.get_travel_photos(destination)
            if isinstance(photos, list) and photos:
                # 첫 번째 이미지만 표시
                photo = photos[0]
                try:
                    st.image(
                        photo['url'],
                        caption=photo['description'],
                        use_container_width=True
                    )
                except Exception as e:
                    st.warning(f"이미지를 불러올 수 없습니다: {photo['description']}")

    # 맛집 추천 페이지
    elif menu == "🍽️ 맛집 추천":
        show_restaurant_recommendations()

    # 숙소 찾기 페이지
    elif menu == "🏨 숙소 찾기":
        st.header("🏨 숙소 찾기")
        
        st.info("""
        💡 **Booking.com을 통한 숙소 예약 방법**
        1. [Booking.com](https://www.booking.com)에서 원하시는 지역을 검색하세요
        2. 날짜와 인원수를 선택하세요
        3. 필터를 사용하여 원하는 조건(가격, 평점, 시설 등)을 설정하세요
        4. 상세 정보를 확인하고 예약을 진행하세요
        
        **예약 시 주의사항**:
        - 예약 취소 정책을 꼭 확인하세요
        - 체크인/체크아웃 시간을 미리 확인하세요
        - 추가 요금이 있는지 확인하세요
        - 리뷰를 참고하여 선택하세요
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            location = st.text_input("지역", value=st.session_state.destination)
            if location != st.session_state.destination:
                st.session_state.destination = location
            check_in = st.date_input("체크인", date.today())
            check_out = st.date_input("체크아웃", date.today() + timedelta(days=1))
        
        with col2:
            guests = st.number_input("숙박 인원", min_value=1, max_value=10, value=2)
            budget = st.selectbox(
                "예산",
                ["5만원 이하", "5-10만원", "10-20만원", "20만원 이상"]
            )
        
        if st.button("숙소 찾기", use_container_width=True):
            booking_url = f"https://www.booking.com/searchresults.html?ss={location}"
            st.markdown(f"[Booking.com에서 {location} 숙소 보기]({booking_url})")
            
            with st.spinner("숙소를 찾고 있습니다..."):
                # 날씨 정보 표시
                weather_info = assistant.get_weather(location, check_in.strftime("%Y-%m-%d"))
                if isinstance(weather_info, dict):
                    st.info(f"**{location}의 날씨 정보**\n"
                           f"- 온도: {weather_info['현재 날씨']['온도']}\n"
                           f"- 날씨: {weather_info['현재 날씨']['날씨']}")
                
                result = assistant.find_accommodations(
                    location=location,
                    check_in=check_in,
                    check_out=check_out,
                    guests=guests,
                    budget=budget
                )
                st.success("숙소 추천이 완성되었습니다!")
                st.write(result)

    # 환율 정보 페이지
    elif menu == "💱 환율 정보":
        st.header("💱 환율 정보")
        
        location = st.text_input("국가/도시를 입력하세요 (예: 서울, 도쿄, 뉴욕, 파리, 런던)", value=st.session_state.destination)
        if location != st.session_state.destination:
            st.session_state.destination = location
        
        if st.button("환율 정보 조회", use_container_width=True):
            with st.spinner("환율 정보를 조회하고 있습니다..."):
                exchange_info = assistant.get_exchange_info(location)
                if isinstance(exchange_info, dict):
                    currency_info = exchange_info["currency_info"]
                    rates = exchange_info["exchange_rates"]
                    base_currency = exchange_info["base_currency"]
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**통화 정보**")
                        st.write(f"통화명: {currency_info['통화명']}")
                        st.write(f"통화 기호: {currency_info['기호']}")
                    
                    with col2:
                        st.write("**환율 정보**")
                        if base_currency == "KRW":
                            st.write("1,000원 기준:")
                            if "USD" in rates:
                                st.write(f"USD: ${rates['USD']:.2f}")
                            if "JPY" in rates:
                                st.write(f"JPY: ¥{rates['JPY']:.0f}")
                        elif base_currency == "JPY":
                            st.write("100엔 기준:")
                            if "KRW" in rates:
                                st.write(f"KRW: ₩{rates['KRW']*1000:.0f}")
                            if "USD" in rates:
                                st.write(f"USD: ${rates['USD']:.2f}")
                        elif base_currency == "USD":
                            st.write("1달러 기준:")
                            if "KRW" in rates:
                                st.write(f"KRW: ₩{rates['KRW']:.0f}")
                            if "JPY" in rates:
                                st.write(f"JPY: ¥{rates['JPY']:.0f}")
                        elif base_currency == "EUR":
                            st.write("1유로 기준:")
                            if "KRW" in rates:
                                st.write(f"KRW: ₩{rates['KRW']:.0f}")
                            if "USD" in rates:
                                st.write(f"USD: ${rates['USD']:.2f}")
                    
                    # 결제 정보
                    st.subheader("💳 결제 정보")
                    payment = currency_info["현금/카드"]
                    for method, info in payment.items():
                        with st.expander(f"**{method}**"):
                            st.write(info)
                else:
                    st.warning(exchange_info)

    # 교통편 찾기 페이지
    elif menu == "🚌 교통 정보":
        st.header("교통편 찾기")
        
        col1, col2 = st.columns(2)
        
        with col1:
            origin = st.text_input("출발지")
            destination = st.text_input("도착지")
        
        with col2:
            date = st.date_input("이동 날짜", datetime.date.today())
            time = st.time_input("이동 시간", datetime.time(12, 0))
        
        if st.button("교통편 찾기"):
            with st.spinner("교통편을 찾고 있습니다..."):
                # 날씨 정보 표시
                weather_info = assistant.get_weather(origin, date.strftime("%Y-%m-%d"))
                st.info(f"출발지 {origin}의 날씨: {weather_info}")
                
                result = assistant.get_transportation(
                    origin=origin,
                    destination=destination,
                    date=f"{date} {time}"
                )
                st.success("교통편 검색이 완료되었습니다!")
                st.write(result)

    # 여행지 갤러리 페이지
    elif menu == "여행지 갤러리":
        st.header("여행지 갤러리")
        
        location = st.text_input("여행지 이름을 입력하세요")
        
        if st.button("사진 검색"):
            with st.spinner("여행지 사진을 찾고 있습니다..."):
                photos = assistant.get_travel_photos(location)
                if isinstance(photos, list):
                    st.success(f"{location}의 사진을 찾았습니다!")
                    
                    # 사진 그리드 표시
                    cols = st.columns(min(3, len(photos)))
                    for i, photo in enumerate(photos):
                        with cols[i % len(cols)]:
                            img_str = assistant.get_photo_base64(photo["url"])
                            if img_str:
                                st.image(f"data:image/jpeg;base64,{img_str}")
                                st.caption(f"📷 {photo['photographer']}")
                                if photo["description"]:
                                    st.caption(photo["description"])
                else:
                    st.warning(photos)

    # 여행 일정 페이지
    elif menu == "여행 일정":
        st.header("여행 일정 관리")
        
        col1, col2 = st.columns(2)
        
        with col1:
            destination = st.text_input("여행지")
            start_date = st.date_input("출발일", datetime.date.today())
            duration = st.number_input("여행 기간 (일)", min_value=1, max_value=30)
        
        # 일정 입력
        st.subheader("일정 입력")
        activities = []
        for day in range(duration):
            with st.expander(f"Day {day+1}"):
                activities.append(st.text_area(f"Day {day+1} 일정", height=100))
        
        if st.button("일정 생성"):
            with st.spinner("여행 일정을 생성하고 있습니다..."):
                calendar = assistant.create_travel_calendar(
                    destination=destination,
                    start_date=start_date,
                    duration=duration,
                    activities=activities
                )
                
                st.success("여행 일정이 생성되었습니다!")
                
                # 캘린더 표시
                for day in calendar:
                    with st.expander(f"{day['date']} - {day['weather']}"):
                        st.write("일정:")
                        for activity in day['activities']:
                            if activity.strip():
                                st.write(f"- {activity}")

    # 경비 계산 페이지
    elif menu == "경비 계산":
        st.header("여행 경비 계산기")
        
        col1, col2 = st.columns(2)
        
        with col1:
            destination = st.text_input("여행지")
            duration = st.number_input("여행 기간 (일)", min_value=1, max_value=30)
        
        with col2:
            preferences = st.multiselect(
                "여행 스타일",
                ["럭셔리", "중간", "절약", "자연", "문화", "맛집", "쇼핑", "액티비티"]
            )
        
        if st.button("경비 계산"):
            with st.spinner("여행 경비를 계산하고 있습니다..."):
                expenses = assistant.calculate_travel_expenses(
                    destination=destination,
                    duration=duration,
                    preferences=", ".join(preferences)
                )
                st.success("여행 경비 계산이 완료되었습니다!")
                st.write(expenses)

    # 리뷰 & 평점 페이지
    elif menu == "리뷰 & 평점":
        st.header("여행지 리뷰 & 평점")
        
        tab1, tab2 = st.tabs(["리뷰 작성", "리뷰 보기"])
        
        with tab1:
            st.subheader("리뷰 작성")
            destination = st.text_input("여행지")
            rating = st.slider("평점", 1, 5, 3)
            comment = st.text_area("리뷰 내용")
            user_id = st.text_input("사용자 ID")
            
            if st.button("리뷰 등록"):
                if destination and comment and user_id:
                    review = assistant.add_review(destination, rating, comment, user_id)
                    st.success("리뷰가 등록되었습니다!")
                else:
                    st.error("모든 필드를 입력해주세요.")
        
        with tab2:
            st.subheader("리뷰 보기")
            destination = st.text_input("여행지 검색")
            
            if destination:
                reviews = assistant.get_reviews(destination)
                avg_rating = assistant.get_average_rating(destination)
                
                if avg_rating > 0:
                    st.metric("평균 평점", f"{avg_rating:.1f} / 5.0")
                
                if reviews:
                    for review in reviews:
                        with st.expander(f"⭐ {review['rating']}점 - {review['date']}"):
                            st.write(f"작성자: {review['user_id']}")
                            st.write(review['comment'])
                else:
                    st.info("아직 등록된 리뷰가 없습니다.")

    # 여행 팁 페이지
    elif menu == "여행 팁":
        st.header("여행 팁 공유")
        
        tab1, tab2 = st.tabs(["팁 작성", "팁 보기"])
        
        with tab1:
            st.subheader("여행 팁 작성")
            destination = st.text_input("여행지")
            tip = st.text_area("여행 팁")
            category = st.selectbox(
                "카테고리",
                ["숙소", "맛집", "관광지", "교통", "쇼핑", "기타"]
            )
            user_id = st.text_input("사용자 ID")
            
            if st.button("팁 등록"):
                if destination and tip and user_id:
                    travel_tip = assistant.add_travel_tip(destination, tip, category, user_id)
                    st.success("여행 팁이 등록되었습니다!")
                else:
                    st.error("모든 필드를 입력해주세요.")
        
        with tab2:
            st.subheader("여행 팁 보기")
            destination = st.text_input("여행지 검색")
            category = st.selectbox(
                "카테고리 필터",
                ["전체"] + ["숙소", "맛집", "관광지", "교통", "쇼핑", "기타"]
            )
            
            if destination:
                tips = assistant.get_travel_tips(
                    destination,
                    category if category != "전체" else None
                )
                
                if tips:
                    for tip in tips:
                        with st.expander(f"{tip['category']} - {tip['date']}"):
                            st.write(f"작성자: {tip['user_id']}")
                            st.write(tip['tip'])
                else:
                    st.info("아직 등록된 여행 팁이 없습니다.")

    # 여행지 비교 페이지
    elif menu == "여행지 비교":
        st.header("여행지 비교")
        
        # 여행지 입력
        destinations = []
        num_destinations = st.number_input("비교할 여행지 수", min_value=2, max_value=5, value=2)
        
        for i in range(num_destinations):
            destination = st.text_input(f"여행지 {i+1}")
            if destination:
                destinations.append(destination)
        
        # 비교 기준 선택
        criteria = st.multiselect(
            "비교 기준",
            ["날씨", "경비", "관광지", "교통편", "맛집", "쇼핑", "액티비티", "숙소"]
        )
        
        if st.button("여행지 비교하기"):
            if len(destinations) >= 2 and criteria:
                with st.spinner("여행지를 비교하고 있습니다..."):
                    result = assistant.compare_destinations(destinations, criteria)
                    st.success("여행지 비교가 완료되었습니다!")
                    st.write(result)
            else:
                st.error("최소 2개의 여행지와 비교 기준을 선택해주세요.")

    # 실시간 예약 페이지
    elif menu == "실시간 예약":
        st.header("실시간 예약")
        
        tab1, tab2 = st.tabs(["예약하기", "예약 내역"])
        
        with tab1:
            st.subheader("예약하기")
            
            col1, col2 = st.columns(2)
            
            with col1:
                destination = st.text_input("여행지")
                date = st.date_input("예약 날짜", datetime.date.today())
                service_type = st.selectbox(
                    "서비스 종류",
                    ["숙소", "투어", "액티비티", "레스토랑", "교통편"]
                )
            
            with col2:
                details = st.text_area("예약 상세 정보")
                user_id = st.text_input("사용자 ID")
            
            if st.button("예약 가능 여부 확인"):
                if destination and date and service_type:
                    with st.spinner("예약 가능 여부를 확인하고 있습니다..."):
                        availability = assistant.check_availability(
                            destination=destination,
                            date=date.strftime("%Y-%m-%d"),
                            service_type=service_type
                        )
                        st.write(availability)
            
            if st.button("예약하기"):
                if destination and date and service_type and details and user_id:
                    with st.spinner("예약을 진행하고 있습니다..."):
                        booking = assistant.make_booking(
                            destination=destination,
                            date=date.strftime("%Y-%m-%d"),
                            service_type=service_type,
                            details=details
                        )
                        st.success(f"예약이 완료되었습니다! 예약 번호: {booking['id']}")
                else:
                    st.error("모든 필드를 입력해주세요.")
        
        with tab2:
            st.subheader("예약 내역")
            destination = st.text_input("여행지 검색 (선택사항)")
            
            bookings = assistant.get_booking_history(destination if destination else None)
            
            if bookings:
                for dest, booking_list in bookings.items():
                    st.subheader(f"📍 {dest}")
                    for booking in booking_list:
                        with st.expander(f"예약 번호: {booking['id']} - {booking['date']}"):
                            st.write(f"서비스: {booking['service_type']}")
                            st.write(f"상태: {booking['status']}")
                            st.write(f"예약일: {booking['created_at']}")
                            st.write("상세 정보:")
                            st.write(booking['details'])
            else:
                st.info("아직 등록된 예약이 없습니다.")

    # 인기 관광지 페이지
    elif menu == "인기 관광지":
        st.header("인기 관광지 추천")
        
        col1, col2 = st.columns(2)
        
        with col1:
            location = st.text_input("여행지")
            category = st.selectbox(
                "카테고리",
                ["전체", "명소", "박물관", "공원", "쇼핑", "문화재", "자연"]
            )
        
        if st.button("관광지 검색"):
            if location:
                with st.spinner("관광지를 찾고 있습니다..."):
                    attractions = assistant.get_popular_attractions(
                        location,
                        category if category != "전체" else None
                    )
                    
                    if isinstance(attractions, list):
                        st.success(f"{location}의 인기 관광지를 찾았습니다!")
                        
                        for attraction in attractions:
                            with st.expander(f"⭐ {attraction['name']} - 평점: {attraction['rating']}"):
                                # 주소와 연락처 정보
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.write("**주소**")
                                    st.write(attraction["address"])
                                with col2:
                                    st.write("**연락처**")
                                    st.write(attraction["phone"])
                                
                                # 운영 시간
                                st.write("**운영 시간**")
                                for hours in attraction["opening_hours"]:
                                    st.write(hours)
                                
                                # 리뷰
                                if attraction["reviews"]:
                                    st.write("**최근 리뷰**")
                                    for review in attraction["reviews"]:
                                        st.write(f"⭐ {review['rating']}점 - {review['author']} ({review['time']})")
                                        st.write(review["text"])
                                        st.write("---")
                                
                                # 웹사이트 링크
                                if attraction["website"] != "웹사이트 정보 없음":
                                    st.write(f"[웹사이트 바로가기]({attraction['website']})")
                    else:
                        st.warning(attractions)
            else:
                st.error("여행지를 입력해주세요.")

    # 실시간 교통 정보 페이지
    elif menu == "실시간 교통":
        st.header("실시간 교통 정보")
        
        col1, col2 = st.columns(2)
        
        with col1:
            origin = st.text_input("출발지")
            destination = st.text_input("도착지")
        
        with col2:
            date = st.date_input("이동 날짜 (선택사항)", None)
            time = st.time_input("이동 시간 (선택사항)", None)
        
        if st.button("교통 정보 검색"):
            if origin and destination:
                with st.spinner("교통 정보를 찾고 있습니다..."):
                    # 날짜와 시간 결합
                    departure_time = None
                    if date and time:
                        departure_time = f"{date.strftime('%Y-%m-%d')} {time.strftime('%H:%M')}"
                    
                    routes = assistant.get_transportation_info(
                        origin=origin,
                        destination=destination,
                        date=departure_time
                    )
                    
                    if isinstance(routes, list):
                        st.success("교통 정보를 찾았습니다!")
                        
                        for i, route in enumerate(routes, 1):
                            with st.expander(f"경로 {i}: {route['summary']} ({route['duration']})"):
                                st.write(f"총 거리: {route['distance']}")
                                
                                for step in route["steps"]:
                                    st.write("---")
                                    st.write(f"**{step['instruction']}**")
                                    st.write(f"소요 시간: {step['duration']} ({step['distance']})")
                                    
                                    if "transit" in step:
                                        transit = step["transit"]
                                        st.write("**대중교통 정보**")
                                        st.write(f"- 노선: {transit['line']} ({transit['vehicle']})")
                                        st.write(f"- 출발: {transit['departure_stop']} ({transit['departure_time']})")
                                        st.write(f"- 도착: {transit['arrival_stop']} ({transit['arrival_time']})")
                    else:
                        st.warning(routes)
            else:
                st.error("출발지와 도착지를 입력해주세요.")

    # 이벤트 & 축제 페이지
    elif menu == "🎉 이벤트/축제":
        st.header("이벤트 & 축제 정보")
        
        col1, col2 = st.columns(2)
        
        with col1:
            location = st.text_input("여행지")
            start_date = st.date_input("시작 날짜", datetime.date.today())
        
        with col2:
            end_date = st.date_input("종료 날짜", datetime.date.today() + datetime.timedelta(days=30))
        
        if st.button("이벤트 검색"):
            if location:
                with st.spinner("이벤트 정보를 찾고 있습니다..."):
                    events = assistant.get_events_and_festivals(
                        location=location,
                        start_date=start_date,
                        end_date=end_date
                    )
                    
                    if isinstance(events, list):
                        st.success(f"{location}의 이벤트 정보를 찾았습니다!")
                        
                        for event in events:
                            with st.expander(f"🎉 {event['title']} - {event['start_time']}"):
                                # 이벤트 기본 정보
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.write("**기간**")
                                    st.write(f"시작: {event['start_time']}")
                                    st.write(f"종료: {event['end_time']}")
                                with col2:
                                    st.write("**가격**")
                                    st.write(event["price"])
                                
                                # 이벤트 이미지
                                if event["image"]:
                                    st.image(event["image"])
                                
                                # 이벤트 설명
                                st.write("**설명**")
                                st.write(event["description"])
                                
                                # 장소 정보
                                st.write("**장소**")
                                venue = event["venue"]
                                st.write(f"- 이름: {venue['name']}")
                                st.write(f"- 주소: {venue['address']}")
                                st.write(f"- 도시: {venue['city']}, {venue['region']}, {venue['country']}")
                                
                                # 카테고리
                                if event["categories"]:
                                    st.write("**카테고리**")
                                    st.write(", ".join(event["categories"]))
                                
                                # 웹사이트 링크
                                if event["url"] != "URL 정보 없음":
                                    st.write(f"[이벤트 웹사이트 바로가기]({event['url']})")
                    else:
                        st.warning(events)
            else:
                st.error("여행지를 입력해주세요.")

    # 맞춤형 여행 코스 페이지
    elif menu == "맞춤형 여행 코스":
        st.header("맞춤형 여행 코스")
        
        col1, col2 = st.columns(2)
        
        with col1:
            location = st.text_input("여행지")
            duration = st.number_input("여행 기간 (일)", min_value=1, max_value=30)
            start_date = st.date_input("출발일", datetime.date.today())
        
        with col2:
            budget = st.selectbox(
                "예산",
                ["저렴", "보통", "고급", "럭셔리"]
            )
            preferences = st.multiselect(
                "선호하는 여행 스타일",
                ["자연", "문화", "맛집", "쇼핑", "액티비티", "휴양", "역사", "예술"]
            )
        
        if st.button("여행 코스 생성"):
            if location and duration and preferences:
                with st.spinner("맞춤형 여행 코스를 생성하고 있습니다..."):
                    itinerary = assistant.recommend_personalized_itinerary(
                        location=location,
                        duration=duration,
                        preferences=preferences,
                        budget=budget,
                        start_date=start_date
                    )
                    
                    if isinstance(itinerary, dict):
                        st.success("맞춤형 여행 코스가 생성되었습니다!")
                        
                        # 여행 코스 요약
                        st.subheader("여행 코스 요약")
                        st.write(f"**여행지**: {itinerary['destination']}")
                        st.write(f"**기간**: {itinerary['duration']}일")
                        st.write(f"**예산**: {itinerary['budget']}")
                        st.write(f"**선호사항**: {', '.join(itinerary['preferences'])}")
                        
                        # 일별 계획
                        for plan in itinerary["daily_plans"]:
                            st.subheader(f"Day {plan['day']} - {plan['date']}")
                            
                            # 날씨 정보
                            if plan["weather"]:
                                st.write("**날씨 정보**")
                                for key, value in plan["weather"].items():
                                    st.write(f"- {key}: {value}")
                            
                            # 오전 계획
                            if plan["morning"]:
                                st.write("**오전**")
                                for attraction in plan["morning"]:
                                    with st.expander(f"⭐ {attraction['name']}"):
                                        st.write(f"주소: {attraction['address']}")
                                        if "photo_url" in attraction:
                                            st.image(attraction["photo_url"])
                            
                            # 오후 계획
                            if plan["afternoon"]:
                                st.write("**오후**")
                                for attraction in plan["afternoon"]:
                                    with st.expander(f"⭐ {attraction['name']}"):
                                        st.write(f"주소: {attraction['address']}")
                                        if "photo_url" in attraction:
                                            st.image(attraction["photo_url"])
                            
                            # 저녁 계획
                            if plan["evening"]:
                                st.write("**저녁**")
                                for attraction in plan["evening"]:
                                    with st.expander(f"⭐ {attraction['name']}"):
                                        st.write(f"주소: {attraction['address']}")
                                        if "photo_url" in attraction:
                                            st.image(attraction["photo_url"])
                            
                            # 이벤트
                            if plan["events"]:
                                st.write("**특별 이벤트**")
                                for event in plan["events"]:
                                    with st.expander(f"🎉 {event['title']}"):
                                        st.write(f"시간: {event['start_time']}")
                                        st.write(f"장소: {event['venue']['name']}")
                                        if event["image"]:
                                            st.image(event["image"])
                    else:
                        st.warning(itinerary)
            else:
                st.error("필수 정보를 모두 입력해주세요.")

    # 비상 연락처 페이지
    elif menu == "🆘 비상 연락처":
        st.header("비상 연락처 및 안전 정보")
        
        location = st.text_input("여행지")
        
        if st.button("정보 조회"):
            if location:
                with st.spinner("비상 정보를 조회하고 있습니다..."):
                    emergency_info = assistant.get_emergency_info(location)
                    
                    if isinstance(emergency_info, dict):
                        # 비상 연락처 정보
                        st.subheader("📞 비상 연락처")
                        contacts = emergency_info["emergency_contacts"]
                        
                        for category, info in contacts.items():
                            with st.expander(f"**{category}**"):
                                for key, value in info.items():
                                    st.write(f"**{key}**: {value}")
                        
                        # 안전 정보
                        st.subheader("🛡️ 안전 정보")
                        safety = emergency_info["safety_info"]
                        
                        for category, tips in safety.items():
                            with st.expander(f"**{category}**"):
                                for tip in tips:
                                    st.write(f"• {tip}")
                    else:
                        st.warning(emergency_info)
            else:
                st.error("여행지를 입력해주세요.")

    # 현지 음식 페이지
    elif menu == "🍜 현지 음식":
        st.header("현지 음식 및 식문화")
        
        location = st.text_input("여행지", value=st.session_state.destination)
        if location != st.session_state.destination:
            st.session_state.destination = location
        
        if st.button("정보 조회"):
            if location:
                with st.spinner("음식 정보를 조회하고 있습니다..."):
                    food_info = assistant.get_local_food_info(location)
                    
                    if isinstance(food_info, dict):
                        # 현지 음식 정보
                        st.subheader("🍽️ 현지 음식")
                        foods = food_info["local_foods"]
                        
                        for food in foods:
                            with st.expander(f"**{food['name']}**"):
                                st.write(f"**설명**: {food['description']}")
                                st.write("**주요 재료**:")
                                for ingredient in food["ingredients"]:
                                    st.write(f"• {ingredient}")
                                st.write(f"**가격대**: {food['price_range']}")
                                st.write(f"**추천 식당**: {food['where_to_eat']}")
                                st.write("**식사 예절**:")
                                for etiquette in food["dining_etiquette"]:
                                    st.write(f"• {etiquette}")
                                if food["image"]:
                                    st.image(food["image"])
                        
                        # 식문화 정보
                        st.subheader("🍜 식문화")
                        culture = food_info["food_culture"]
                        
                        st.write("**식사 시간**")
                        for meal, time in culture["식사 시간"].items():
                            st.write(f"• {meal}: {time}")
                        
                        with st.expander("**팁 문화**"):
                            st.write(culture["팁 문화"])
                        
                        st.write("**식사 예절**")
                        for etiquette in culture["식사 예절"]:
                            st.write(f"• {etiquette}")
                        
                        with st.expander("**음료 문화**"):
                            st.write(culture["음료 문화"])
                    else:
                        st.warning(food_info)
            else:
                st.error("여행지를 입력해주세요.")

    # 쇼핑 정보 페이지
    elif menu == "🛍️ 쇼핑 정보":
        st.header("쇼핑 정보")
        
        location = st.text_input("여행지", value=st.session_state.destination)
        if location != st.session_state.destination:
            st.session_state.destination = location
        
        if st.button("정보 조회"):
            if location:
                with st.spinner("쇼핑 정보를 조회하고 있습니다..."):
                    shopping_info = assistant.get_shopping_info(location)
                    
                    if isinstance(shopping_info, dict):
                        # 쇼핑 지역 정보
                        st.subheader("🛍️ 쇼핑 지역")
                        areas = shopping_info["쇼핑 지역"]
                        
                        for area in areas:
                            with st.expander(f"**{area['name']}**"):
                                st.write(f"**설명**: {area['description']}")
                                st.write(f"**특산품**: {area['specialty']}")
                                st.write(f"**영업 시간**: {area['opening_hours']}")
                                st.write(f"**최적 쇼핑 시간**: {area['best_time']}")
                                st.write("**쇼핑 팁**:")
                                for tip in area["tips"]:
                                    st.write(f"• {tip}")
                        
                        # 추천 상품 정보
                        st.subheader("🎁 추천 상품")
                        products = shopping_info["추천 상품"]
                        
                        for product in products:
                            with st.expander(f"**{product['name']}**"):
                                st.write(f"**설명**: {product['description']}")
                                st.write(f"**가격대**: {product['price_range']}")
                                st.write(f"**구매 장소**: {product['where_to_buy']}")
                                st.write("**구매 팁**:")
                                for tip in product["tips"]:
                                    st.write(f"• {tip}")
                                if product["image"]:
                                    st.image(product["image"])
                        
                        # 쇼핑 팁
                        st.subheader("💡 쇼핑 팁")
                        tips = shopping_info["쇼핑 팁"]
                        
                        for category, tip in tips.items():
                            with st.expander(f"**{category}**"):
                                st.write(tip)
                    else:
                        st.warning(shopping_info)
            else:
                st.error("여행지를 입력해주세요.")

    st.markdown('</div>', unsafe_allow_html=True)

# 푸터
st.markdown("---")
st.markdown("""
<div class="footer">
    © 2024 Sid & Teddy's Journey AI. All rights reserved.
    <div class="footer-version">Version: Beta 1.0</div>
</div>
""", unsafe_allow_html=True) 