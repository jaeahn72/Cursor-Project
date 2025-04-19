import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta
import json
import base64
from io import BytesIO
from PIL import Image

# 환경 변수 로드
load_dotenv()

class TravelAssistant:
    def __init__(self):
        # API 키 설정
        self.weather_api_key = os.getenv("WEATHER_API_KEY")
        self.unsplash_api_key = os.getenv("UNSPLASH_API_KEY")
        self.google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        self.event_api_key = os.getenv("EVENT_API_KEY")
        self.exchange_api_key = os.getenv("EXCHANGE_API_KEY")
        self.naver_client_id = os.getenv("NAVER_CLIENT_ID")
        self.naver_client_secret = os.getenv("NAVER_CLIENT_SECRET")
        # 리뷰 데이터 저장소 (실제로는 데이터베이스를 사용하는 것이 좋습니다)
        self.reviews = {}
        self.travel_tips = {}
        self.bookings = {}
    
    def compare_destinations(self, destinations, criteria):
        """여행지를 비교합니다."""
        try:
            # 실제 구현에서는 API를 통해 데이터를 가져와야 합니다
            # 여기서는 예시 데이터를 반환합니다
            comparison = {}
            for destination in destinations:
                comparison[destination] = {
                    "advantages": [
                        "아름다운 자연 경관",
                        "다양한 문화 체험",
                        "접근성 좋은 교통"
                    ],
                    "disadvantages": [
                        "비싼 물가",
                        "혼잡한 관광지"
                    ],
                    "recommended_time": "봄, 가을",
                    "estimated_cost": "1인당 100-200만원",
                    "major_attractions": [
                        "유명 관광지 1",
                        "유명 관광지 2",
                        "유명 관광지 3"
                    ],
                    "transportation": [
                        "지하철",
                        "버스",
                        "택시"
                    ]
                }
            return comparison
        except Exception as e:
            return f"여행지 비교 중 오류가 발생했습니다: {str(e)}"
    
    def check_availability(self, destination, date, service_type):
        """실시간 예약 가능 여부를 확인합니다."""
        try:
            # 실제 구현에서는 API를 통해 데이터를 가져와야 합니다
            # 여기서는 예시 데이터를 반환합니다
            return {
                "available": True,
                "options": [
                    {
                        "name": "호텔 A",
                        "price": "100,000원",
                        "rating": 4.5
                    },
                    {
                        "name": "호텔 B",
                        "price": "150,000원",
                        "rating": 4.8
                    }
                ]
            }
        except Exception as e:
            return f"예약 가능 여부 확인 중 오류가 발생했습니다: {str(e)}"
    
    def make_booking(self, destination, date, service_type, details):
        """예약을 진행합니다."""
        try:
            booking_id = f"BK{datetime.now().strftime('%Y%m%d%H%M%S')}"
            booking = {
                "id": booking_id,
                "destination": destination,
                "date": date,
                "service_type": service_type,
                "details": details,
                "status": "예약 완료",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            if destination not in self.bookings:
                self.bookings[destination] = []
            self.bookings[destination].append(booking)
            
            return booking
        except Exception as e:
            return f"예약 중 오류가 발생했습니다: {str(e)}"
    
    def get_booking_history(self, destination=None):
        """예약 내역을 조회합니다."""
        try:
            if destination:
                return self.bookings.get(destination, [])
            return self.bookings
        except Exception as e:
            return f"예약 내역 조회 중 오류가 발생했습니다: {str(e)}"
    
    def add_review(self, destination, rating, comment, user_id):
        """여행지 리뷰를 추가합니다."""
        if destination not in self.reviews:
            self.reviews[destination] = []
        
        review = {
            "user_id": user_id,
            "rating": rating,
            "comment": comment,
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        self.reviews[destination].append(review)
        return review
    
    def get_reviews(self, destination):
        """여행지의 리뷰를 가져옵니다."""
        if destination not in self.reviews:
            return []
        return self.reviews[destination]
    
    def get_average_rating(self, destination):
        """여행지의 평균 평점을 계산합니다."""
        if destination not in self.reviews or not self.reviews[destination]:
            return 0
        ratings = [review["rating"] for review in self.reviews[destination]]
        return sum(ratings) / len(ratings)
    
    def add_travel_tip(self, destination, tip, category, user_id):
        """여행 팁을 추가합니다."""
        if destination not in self.travel_tips:
            self.travel_tips[destination] = []
        
        travel_tip = {
            "user_id": user_id,
            "tip": tip,
            "category": category,
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        self.travel_tips[destination].append(travel_tip)
        return travel_tip
    
    def get_travel_tips(self, destination, category=None):
        """여행지의 팁을 가져옵니다."""
        if destination not in self.travel_tips:
            return []
        
        tips = self.travel_tips[destination]
        if category:
            tips = [tip for tip in tips if tip["category"] == category]
        return tips
    
    def get_weather(self, location, date):
        try:
            # 예시 날씨 데이터 반환
            return {
                "현재 날씨": {
                    "온도": "23°C",
                    "체감온도": "22°C",
                    "날씨": "맑음",
                    "습도": "65%",
                    "바람": "5km/h",
                    "강수량": "0mm"
                },
                "일일 예보": {
                    "최고기온": "26°C",
                    "최저기온": "18°C",
                    "평균기온": "22°C",
                    "강수확률": "10%",
                    "총강수량": "0mm",
                    "자외선지수": "3"
                }
            }
        except Exception as e:
            return f"날씨 정보를 가져오는 중 오류가 발생했습니다: {str(e)}"
    
    def get_travel_photos(self, location):
        """
        Returns representative photos for specific travel destinations.
        """
        destination_photos = {
            "서울": [
                {
                    "url": "https://images.unsplash.com/photo-1538485399081-7c8272e31ecb?w=800",
                    "description": "남산서울타워와 도시 야경"
                }
            ],
            "도쿄": [
                {
                    "url": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=800",
                    "description": "도쿄타워와 도시 야경"
                }
            ],
            "파리": [
                {
                    "url": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=800",
                    "description": "에펠탑의 웅장한 모습"
                }
            ],
            "런던": [
                {
                    "url": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=800",
                    "description": "빅벤과 웨스트민스터 궁전"
                }
            ],
            "뉴욕": [
                {
                    "url": "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=800",
                    "description": "맨해튼 스카이라인"
                }
            ]
        }

        if location in destination_photos:
            return destination_photos[location]
        else:
            # Return default image for locations without predefined photos
            return [{
                "url": f"https://source.unsplash.com/featured/?{location}+city&w=800",
                "description": f"{location}의 도시 전경"
            }]
    
    def get_photo_base64(self, photo_url):
        """사진 URL을 base64로 변환합니다."""
        try:
            response = requests.get(photo_url)
            img = Image.open(BytesIO(response.content))
            
            # 이미지 크기를 50% 수준으로 조정
            max_size = (400, 300)  # 기존 800x600에서 400x300으로 변경
            img.thumbnail(max_size, Image.LANCZOS)
            
            # base64로 변환
            buffered = BytesIO()
            img.save(buffered, format="JPEG", quality=85)  # quality 파라미터 추가로 파일 크기 최적화
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            return img_str
            
        except Exception as e:
            print(f"Error converting photo to base64: {str(e)}")
            return None
    
    def create_travel_calendar(self, destination, start_date, duration, activities):
        """여행 일정 캘린더를 생성합니다."""
        calendar = []
        current_date = start_date
        
        for day in range(duration):
            daily_activities = activities[day] if day < len(activities) else []
            calendar.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "activities": daily_activities,
                "weather": self.get_weather(destination, current_date.strftime("%Y-%m-%d"))
            })
            current_date += timedelta(days=1)
        
        return calendar
    
    def calculate_travel_expenses(self, destination, duration, preferences):
        """여행 경비를 계산합니다."""
        query = f"""
        {destination}에서 {duration}일 동안 여행할 때의 예상 경비를 계산해주세요.
        선호사항: {preferences}
        다음 항목별로 상세히 계산해주세요:
        1. 숙박비
        2. 식비
        3. 교통비
        4. 관광지 입장료
        5. 쇼핑비
        6. 기타 경비
        """
        return self.get_recommendations(query)
    
    def get_recommendations(self, query):
        """여행 관련 추천을 제공합니다."""
        # 실제 구현에서는 모델을 통해 추천을 가져와야 합니다
        # 여기서는 예시 추천을 반환합니다
        return "예시 추천 결과입니다."
    
    def plan_trip(self, destination, duration, preferences):
        """여행 계획을 세웁니다."""
        # 날씨 정보 추가
        weather_info = self.get_weather(destination, datetime.now().strftime("%Y-%m-%d"))
        
        query = f"""
        {destination}에서 {duration}일 동안 여행 계획을 세워주세요.
        선호사항: {preferences}
        현재 날씨: {weather_info}
        """
        return self.get_recommendations(query)
    
    def find_restaurants(self, location, cuisine=None, budget=None):
        """맛집을 추천합니다."""
        try:
            # 도시별 맛집 데이터
            restaurant_data = {
                "서울": [
                    {
                        "name": "삼청동 수제비",
                        "cuisine": "한식",
                        "description": "전통 한식의 맛을 즐길 수 있는 곳",
                        "price_range": "10,000-30,000원",
                        "rating": 4.5,
                        "address": "서울 종로구 삼청동",
                        "opening_hours": "매일 11:00-21:00",
                        "specialties": ["수제비", "칼국수", "김치찌개"]
                    },
                    {
                        "name": "을지로 양념갈비",
                        "cuisine": "한식",
                        "description": "숨은 맛집으로 유명한 갈비집",
                        "price_range": "30,000-50,000원",
                        "rating": 4.7,
                        "address": "서울 중구 을지로",
                        "opening_hours": "매일 11:30-22:00",
                        "specialties": ["양념갈비", "된장찌개", "냉면"]
                    }
                ],
                "도쿄": [
                    {
                        "name": "스시 긴자",
                        "cuisine": "일식",
                        "description": "최고급 스시를 맛볼 수 있는 곳",
                        "price_range": "50,000원 이상",
                        "rating": 4.8,
                        "address": "도쿄도 긴자",
                        "opening_hours": "매일 11:30-14:00, 17:00-22:00",
                        "specialties": ["오마카세", "스시", "사시미"]
                    },
                    {
                        "name": "라멘 이치란",
                        "cuisine": "일식",
                        "description": "유명한 돈코츠 라멘 체인점",
                        "price_range": "10,000-30,000원",
                        "rating": 4.5,
                        "address": "도쿄도 시부야",
                        "opening_hours": "24시간 영업",
                        "specialties": ["돈코츠라멘", "계란", "챠슈"]
                    }
                ],
                "파리": [
                    {
                        "name": "Le Chateaubriand",
                        "cuisine": "프랑스식",
                        "description": "현대적인 프렌치 다이닝",
                        "price_range": "50,000원 이상",
                        "rating": 4.6,
                        "address": "파리 11구",
                        "opening_hours": "화-토 19:30-23:00",
                        "specialties": ["코스요리", "와인", "디저트"]
                    },
                    {
                        "name": "L'Ami Louis",
                        "cuisine": "프랑스식",
                        "description": "클래식한 프랑스 비스트로",
                        "price_range": "30,000-50,000원",
                        "rating": 4.4,
                        "address": "파리 3구",
                        "opening_hours": "매일 12:00-14:30, 19:00-23:00",
                        "specialties": ["로스트 치킨", "감자 요리", "와인"]
                    }
                ],
                "뉴욕": [
                    {
                        "name": "Katz's Delicatessen",
                        "cuisine": "미국식",
                        "description": "뉴욕의 상징적인 델리",
                        "price_range": "10,000-30,000원",
                        "rating": 4.5,
                        "address": "뉴욕 로어 이스트 사이드",
                        "opening_hours": "매일 08:00-22:30",
                        "specialties": ["파스트라미 샌드위치", "루벤 샌드위치", "매티 버거"]
                    },
                    {
                        "name": "Peter Luger Steak House",
                        "cuisine": "스테이크",
                        "description": "브루클린의 전설적인 스테이크하우스",
                        "price_range": "50,000원 이상",
                        "rating": 4.7,
                        "address": "브루클린 윌리엄스버그",
                        "opening_hours": "매일 11:45-21:45",
                        "specialties": ["포터하우스 스테이크", "베이컨", "감자"]
                    }
                ],
                "런던": [
                    {
                        "name": "Dishoom",
                        "cuisine": "인도식",
                        "description": "현대적인 뭄바이식 레스토랑",
                        "price_range": "30,000-50,000원",
                        "rating": 4.6,
                        "address": "런던 코벤트 가든",
                        "opening_hours": "매일 08:00-23:00",
                        "specialties": ["베이컨 난", "블랙 달", "비리야니"]
                    },
                    {
                        "name": "The Clove Club",
                        "cuisine": "현대식 영국",
                        "description": "미쉐린 스타 레스토랑",
                        "price_range": "50,000원 이상",
                        "rating": 4.8,
                        "address": "런던 쇼디치",
                        "opening_hours": "화-토 18:00-22:30",
                        "specialties": ["시즌 코스", "와인 페어링", "디저트"]
                    }
                ]
            }

            # 기본 맛집 데이터
            default_restaurants = [
                {
                    "name": "로컬 레스토랑",
                    "cuisine": cuisine if cuisine else "다양한 요리",
                    "description": "현지 특색을 살린 맛집",
                    "price_range": "10,000-30,000원",
                    "rating": 4.0,
                    "address": f"{location} 시내",
                    "opening_hours": "매일 11:00-22:00",
                    "specialties": ["현지 특선 요리", "시그니처 메뉴", "계절 특선"]
                }
            ]

            # 해당 도시의 맛집 정보 가져오기
            restaurants = restaurant_data.get(location, default_restaurants)

            # 요리 종류로 필터링
            if cuisine and cuisine != "기타":
                restaurants = [r for r in restaurants if cuisine in r["cuisine"]]

            # 예산으로 필터링
            if budget:
                budget_ranges = {
                    "10,000원 이하": lambda r: "10,000원 이하" in r["price_range"],
                    "10,000-30,000원": lambda r: "10,000-30,000원" in r["price_range"],
                    "30,000-50,000원": lambda r: "30,000-50,000원" in r["price_range"],
                    "50,000원 이상": lambda r: "50,000원 이상" in r["price_range"]
                }
                
                if budget in budget_ranges:
                    restaurants = [r for r in restaurants if budget_ranges[budget](r)]

            return restaurants if restaurants else default_restaurants

        except Exception as e:
            return f"맛집 추천 중 오류가 발생했습니다: {str(e)}"
    
    def find_accommodations(self, location, check_in, check_out, guests, budget):
        """숙소를 추천합니다."""
        # 날씨 정보 추가
        weather_info = self.get_weather(location, check_in)
        
        query = f"""
        {location}에서 {check_in}부터 {check_out}까지 
        {guests}명이 묵을 수 있는 숙소를 추천해주세요.
        예산: {budget}
        날씨 정보: {weather_info}
        """
        return self.get_recommendations(query)
    
    def get_transportation(self, origin, destination, date):
        """교통편을 추천합니다."""
        # 날씨 정보 추가
        weather_info = self.get_weather(origin, date)
        
        query = f"""
        {origin}에서 {destination}까지 {date}에 갈 수 있는 
        교통편을 알려주세요.
        출발지 날씨: {weather_info}
        """
        return self.get_recommendations(query)
    
    def get_events_and_festivals(self, location, start_date=None, end_date=None):
        """여행지의 특별 이벤트와 축제 정보를 제공합니다."""
        try:
            # Event API 호출
            url = "https://api.eventful.com/json/events/search"
            params = {
                "app_key": self.event_api_key,
                "location": location,
                "date": f"{start_date.strftime('%Y%m%d') if start_date else 'Today'}-{end_date.strftime('%Y%m%d') if end_date else 'Future'}",
                "category": "festivals_parades,music,performing_arts,sports,conferences",
                "sort_order": "popularity",
                "page_size": 10,
                "include": "categories,description,venue,price,url"
            }
            response = requests.get(url, params=params)
            data = response.json()
            
            if "events" not in data or not data["events"]:
                return f"{location}에서 예정된 이벤트가 없습니다."
            
            events = []
            for event in data["events"]["event"]:
                event_info = {
                    "title": event["title"],
                    "description": event.get("description", "설명 없음"),
                    "start_time": event["start_time"],
                    "end_time": event.get("end_time", "종료 시간 없음"),
                    "venue": {
                        "name": event["venue_name"],
                        "address": event["venue_address"],
                        "city": event["city_name"],
                        "region": event["region_name"],
                        "country": event["country_name"]
                    },
                    "categories": [cat["name"] for cat in event.get("categories", {}).get("category", [])],
                    "price": event.get("price", "가격 정보 없음"),
                    "url": event.get("url", "URL 정보 없음"),
                    "image": event.get("image", {}).get("medium", {}).get("url")
                }
                events.append(event_info)
            
            return events
            
        except Exception as e:
            return f"이벤트 정보를 가져오는 중 오류가 발생했습니다: {str(e)}"
    
    def recommend_personalized_itinerary(self, location, duration, preferences, budget, start_date=None):
        """사용자 맞춤형 여행 코스를 추천합니다."""
        try:
            # 관광지 정보 가져오기
            attractions = self.get_popular_attractions(location)
            if not isinstance(attractions, list):
                return f"관광지 정보를 가져올 수 없습니다: {attractions}"
            
            # 이벤트 정보 가져오기
            events = self.get_events_and_festivals(
                location,
                start_date,
                start_date + timedelta(days=duration) if start_date else None
            )
            
            # 날씨 정보 가져오기
            weather = self.get_weather(location, start_date.strftime("%Y-%m-%d") if start_date else None)
            
            # 여행 코스 생성
            itinerary = {
                "destination": location,
                "duration": duration,
                "preferences": preferences,
                "budget": budget,
                "start_date": start_date.strftime("%Y-%m-%d") if start_date else None,
                "daily_plans": []
            }
            
            # 일별 계획 생성
            for day in range(duration):
                daily_plan = {
                    "day": day + 1,
                    "date": (start_date + timedelta(days=day)).strftime("%Y-%m-%d") if start_date else None,
                    "weather": weather.get("일일 예보", {}) if isinstance(weather, dict) else None,
                    "morning": [],
                    "afternoon": [],
                    "evening": [],
                    "events": []
                }
                
                # 관광지 배치
                attractions_per_day = min(3, len(attractions) // duration)
                for i in range(attractions_per_day):
                    if attractions:
                        attraction = attractions.pop(0)
                        if i == 0:
                            daily_plan["morning"].append(attraction)
                        elif i == 1:
                            daily_plan["afternoon"].append(attraction)
                        else:
                            daily_plan["evening"].append(attraction)
                
                # 이벤트 배치
                if isinstance(events, list):
                    for event in events:
                        event_date = datetime.strptime(event["start_time"], "%Y-%m-%d %H:%M:%S").date()
                        if start_date and event_date == start_date + timedelta(days=day):
                            daily_plan["events"].append(event)
                
                itinerary["daily_plans"].append(daily_plan)
            
            return itinerary
            
        except Exception as e:
            return f"여행 코스를 생성하는 중 오류가 발생했습니다: {str(e)}"
    
    def get_emergency_info(self, location):
        """여행지의 비상 연락처 및 안전 정보를 제공합니다."""
        try:
            # 실제 구현에서는 API를 통해 데이터를 가져와야 합니다
            # 여기서는 예시 데이터를 반환합니다
            return {
                "emergency_contacts": {
                    "대사관": {
                        "전화": "+82-2-3210-0404",
                        "주소": "대사관 주소",
                        "비상연락처": "+82-10-1234-5678"
                    },
                    "응급서비스": {
                        "경찰": "112",
                        "소방서": "119",
                        "응급의료": "119"
                    },
                    "기타": {
                        "관광안내소": "+82-2-1330",
                        "여행자보험": "+82-2-1234-5678"
                    }
                },
                "safety_info": {
                    "주의사항": [
                        "밤늦은 시간 혼자 돌아다니지 않기",
                        "귀중품은 호텔 금고에 보관",
                        "현지 법률과 관습 존중",
                        "응급 상황 시 대사관 연락"
                    ],
                    "건강": [
                        "필요한 예방접종 확인",
                        "기본 의약품 준비",
                        "식수 안전 확인",
                        "현지 병원 정보 확인"
                    ],
                    "교통": [
                        "대중교통 이용 시 주의",
                        "택시 이용 시 미터기 확인",
                        "야간 운전 주의",
                        "보행 시 교통 신호 준수"
                    ]
                }
            }
        except Exception as e:
            return f"비상 정보 조회 중 오류가 발생했습니다: {str(e)}"
    
    def get_exchange_info(self, location):
        """여행지의 통화 및 환율 정보를 제공합니다."""
        try:
            # 위치에 따른 통화 정보 매핑
            location_info = {
                # 한국
                "서울": {"country": "한국", "currency": "KRW"},
                "부산": {"country": "한국", "currency": "KRW"},
                "제주": {"country": "한국", "currency": "KRW"},
                "인천": {"country": "한국", "currency": "KRW"},
                # 일본
                "도쿄": {"country": "일본", "currency": "JPY"},
                "오사카": {"country": "일본", "currency": "JPY"},
                "교토": {"country": "일본", "currency": "JPY"},
                "후쿠오카": {"country": "일본", "currency": "JPY"},
                "삿포로": {"country": "일본", "currency": "JPY"},
                # 중국
                "베이징": {"country": "중국", "currency": "CNY"},
                "상하이": {"country": "중국", "currency": "CNY"},
                "광저우": {"country": "중국", "currency": "CNY"},
                "청두": {"country": "중국", "currency": "CNY"},
                # 미국
                "뉴욕": {"country": "미국", "currency": "USD"},
                "LA": {"country": "미국", "currency": "USD"},
                "샌프란시스코": {"country": "미국", "currency": "USD"},
                "시카고": {"country": "미국", "currency": "USD"},
                "라스베가스": {"country": "미국", "currency": "USD"},
                "보스턴": {"country": "미국", "currency": "USD"},
                # 유럽
                "파리": {"country": "프랑스", "currency": "EUR"},
                "런던": {"country": "영국", "currency": "GBP"},
                "로마": {"country": "이탈리아", "currency": "EUR"},
                "베니스": {"country": "이탈리아", "currency": "EUR"},
                "바르셀로나": {"country": "스페인", "currency": "EUR"},
                "마드리드": {"country": "스페인", "currency": "EUR"},
                "베를린": {"country": "독일", "currency": "EUR"},
                "뮌헨": {"country": "독일", "currency": "EUR"},
                "암스테르담": {"country": "네덜란드", "currency": "EUR"},
                "비엔나": {"country": "오스트리아", "currency": "EUR"},
                "취리히": {"country": "스위스", "currency": "CHF"},
                # 아시아
                "방콕": {"country": "태국", "currency": "THB"},
                "싱가포르": {"country": "싱가포르", "currency": "SGD"},
                "타이페이": {"country": "대만", "currency": "TWD"},
                "홍콩": {"country": "홍콩", "currency": "HKD"},
                "마카오": {"country": "마카오", "currency": "MOP"},
                "하노이": {"country": "베트남", "currency": "VND"},
                "호치민": {"country": "베트남", "currency": "VND"},
                "쿠알라룸푸르": {"country": "말레이시아", "currency": "MYR"},
                # 중동
                "두바이": {"country": "아랍에미리트", "currency": "AED"},
                "이스탄불": {"country": "터키", "currency": "TRY"}
            }

            # 기본값으로 한국/KRW 설정
            country_info = location_info.get(location, {"country": "한국", "currency": "KRW"})
            base_currency = country_info["currency"]

            # 예시 환율 데이터 (실제로는 API를 통해 가져와야 함)
            exchange_rates = {
                "KRW": {
                    "USD": 0.00075,  # 1원 기준
                    "EUR": 0.0007,   # 1원 기준
                    "JPY": 0.11,     # 1원 기준
                    "CNY": 0.0054    # 1원 기준
                },
                "JPY": {
                    "KRW": 9.1,      # 1엔 기준
                    "USD": 0.0067,   # 1엔 기준
                    "EUR": 0.0063,   # 1엔 기준
                    "CNY": 0.048     # 1엔 기준
                },
                "USD": {
                    "KRW": 1330.0,   # 1달러 기준
                    "JPY": 150.0,    # 1달러 기준
                    "EUR": 0.93,     # 1달러 기준
                    "CNY": 7.2       # 1달러 기준
                },
                "EUR": {
                    "KRW": 1430.0,   # 1유로 기준
                    "USD": 1.07,     # 1유로 기준
                    "JPY": 158.0,    # 1유로 기준
                    "CNY": 7.7       # 1유로 기준
                },
                "GBP": {
                    "KRW": 1670.0,   # 1파운드 기준
                    "USD": 1.25,     # 1파운드 기준
                    "EUR": 1.17,     # 1파운드 기준
                    "JPY": 187.0     # 1파운드 기준
                },
                "CNY": {
                    "KRW": 185.0,    # 1위안 기준
                    "USD": 0.14,     # 1위안 기준
                    "EUR": 0.13,     # 1위안 기준
                    "JPY": 20.8      # 1위안 기준
                }
            }

            # 국가별 통화 정보
            currency_info = {
                "한국": {
                    "통화명": "대한민국 원",
                    "기호": "₩",
                    "소수점": 0,
                    "현금/카드": {
                        "현금": "소액 거래 및 전통 시장에서 현금 선호",
                        "카드": "대부분의 가게에서 신용카드 사용 가능",
                        "ATM": "은행 및 편의점에서 ATM 이용 가능"
                    }
                },
                "일본": {
                    "통화명": "일본 엔",
                    "기호": "¥",
                    "소수점": 0,
                    "현금/카드": {
                        "현금": "현금 사용이 일반적",
                        "카드": "대형 상점에서만 신용카드 사용 가능",
                        "ATM": "편의점에서 ATM 이용 가능"
                    }
                },
                "중국": {
                    "통화명": "중국 위안",
                    "기호": "¥",
                    "소수점": 2,
                    "현금/카드": {
                        "현금": "현금 사용이 일반적",
                        "카드": "대형 상점에서만 신용카드 사용 가능",
                        "ATM": "은행에서 ATM 이용 가능"
                    }
                },
                "미국": {
                    "통화명": "미국 달러",
                    "기호": "$",
                    "소수점": 2,
                    "현금/카드": {
                        "현금": "소액 거래에 현금 사용이 편리",
                        "카드": "대부분의 가게에서 신용카드 사용 가능",
                        "ATM": "은행 및 편의점에서 ATM 이용 가능"
                    }
                },
                "프랑스": {
                    "통화명": "유로",
                    "기호": "€",
                    "소수점": 2,
                    "현금/카드": {
                        "현금": "소액 거래에 현금 사용이 편리",
                        "카드": "대부분의 가게에서 신용카드 사용 가능",
                        "ATM": "은행 및 편의점에서 ATM 이용 가능"
                    }
                },
                "영국": {
                    "통화명": "영국 파운드",
                    "기호": "£",
                    "소수점": 2,
                    "현금/카드": {
                        "현금": "소액 거래에 현금 사용이 편리",
                        "카드": "대부분의 가게에서 신용카드 사용 가능",
                        "ATM": "은행 및 편의점에서 ATM 이용 가능"
                    }
                },
                "이탈리아": {
                    "통화명": "유로",
                    "기호": "€",
                    "소수점": 2,
                    "현금/카드": {
                        "현금": "소액 거래에 현금 사용이 편리",
                        "카드": "대부분의 가게에서 신용카드 사용 가능",
                        "ATM": "은행 및 편의점에서 ATM 이용 가능"
                    }
                },
                "스페인": {
                    "통화명": "유로",
                    "기호": "€",
                    "소수점": 2,
                    "현금/카드": {
                        "현금": "소액 거래에 현금 사용이 편리",
                        "카드": "대부분의 가게에서 신용카드 사용 가능",
                        "ATM": "은행 및 편의점에서 ATM 이용 가능"
                    }
                }
            }

            # 기본 통화 정보가 없는 경우 기본값 설정
            if country_info["country"] not in currency_info:
                currency_info[country_info["country"]] = {
                    "통화명": f"{country_info['country']}의 {base_currency}",
                    "기호": base_currency,
                    "소수점": 2,
                    "현금/카드": {
                        "현금": "현금 사용 가능",
                        "카드": "주요 신용카드 사용 가능",
                        "ATM": "은행 ATM 이용 가능"
                    }
                }

            # 해당 통화의 환율 정보가 없는 경우 기본값 설정
            if base_currency not in exchange_rates:
                exchange_rates[base_currency] = {
                    "KRW": 1000.0,  # 예시 환율
                    "USD": 1.0,
                    "EUR": 0.9,
                    "JPY": 110.0
                }

            rates = exchange_rates[base_currency]
            country = country_info["country"]

            return {
                "exchange_rates": rates,
                "currency_info": currency_info[country],
                "base_currency": base_currency
            }

        except Exception as e:
            return f"환율 정보 조회 중 오류가 발생했습니다: {str(e)}"
    
    def get_local_food_info(self, location):
        """여행지의 현지 음식 및 식문화 정보를 제공합니다."""
        try:
            # 실제 구현에서는 API를 통해 데이터를 가져와야 합니다
            # 여기서는 예시 데이터를 반환합니다
            return {
                "local_foods": [
                    {
                        "name": "현지 음식 1",
                        "description": "전통적인 현지 음식입니다.",
                        "ingredients": ["재료 1", "재료 2", "재료 3"],
                        "price_range": "10,000-20,000원",
                        "where_to_eat": "전통 시장",
                        "dining_etiquette": [
                            "맛있게 드세요",
                            "식사 후 정리"
                        ],
                        "image": None
                    }
                ],
                "food_culture": {
                    "식사 시간": {
                        "아침": "07:00-09:00",
                        "점심": "12:00-14:00",
                        "저녁": "18:00-20:00"
                    },
                    "팁 문화": "팁이 포함되어 있음",
                    "식사 예절": [
                        "식사 전 인사",
                        "식사 후 인사"
                    ],
                    "음료 문화": "식사와 함께 차를 마시는 것이 일반적"
                }
            }
        except Exception as e:
            return f"음식 정보 조회 중 오류가 발생했습니다: {str(e)}"
    
    def get_shopping_info(self, location):
        """여행지의 쇼핑 정보를 제공합니다."""
        try:
            # 실제 구현에서는 API를 통해 데이터를 가져와야 합니다
            # 여기서는 예시 데이터를 반환합니다
            return {
                "쇼핑 지역": [
                    {
                        "name": "쇼핑몰 A",
                        "description": "대형 쇼핑몰",
                        "specialty": "의류, 액세서리",
                        "opening_hours": "10:00-22:00",
                        "best_time": "평일 오후",
                        "tips": [
                            "할인 기간 확인",
                            "세금 환급 가능"
                        ]
                    }
                ],
                "추천 상품": [
                    {
                        "name": "현지 특산품",
                        "description": "전통 공예품",
                        "price_range": "10,000-50,000원",
                        "where_to_buy": "전통 시장",
                        "tips": [
                            "품질 확인",
                            "가격 흥정 가능"
                        ],
                        "image": None
                    }
                ],
                "쇼핑 팁": {
                    "흥정": "시장에서 흥정이 가능",
                    "세금 환급": "일정 금액 이상 구매 시 세금 환급 가능",
                    "배송": "국제 배송 서비스 이용 가능",
                    "품질 확인": "구매 전 품질 확인 필수"
                }
            }
        except Exception as e:
            return f"쇼핑 정보 조회 중 오류가 발생했습니다: {str(e)}"

# 간단한 테스트 코드
if __name__ == "__main__":
    assistant = TravelAssistant()
    
    # 테스트 쿼리
    test_query = "서울에서 부산까지 가는 방법을 알려주세요"
    response = assistant.get_recommendations(test_query)
    print(response) 