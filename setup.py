import os
from dotenv import load_dotenv, set_key
import getpass

def setup_api_keys():
    print("API 키 설정을 시작합니다...")
    print("각 API 키를 입력하세요. (입력하지 않으려면 Enter를 누르세요)\n")
    
    # .env 파일 경로
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    
    # 기존 .env 파일 로드
    load_dotenv(env_path)
    
    # OpenWeatherMap API 키
    print("\n1. OpenWeatherMap API 키")
    print("   - https://openweathermap.org/api 에서 발급 가능")
    print("   - 무료 티어: 60 calls/minute, 1,000,000 calls/month")
    weather_key = getpass.getpass("   API 키를 입력하세요: ")
    if weather_key:
        set_key(env_path, "WEATHER_API_KEY", weather_key)
        print("   ✅ OpenWeatherMap API 키가 설정되었습니다.")
    
    # ExchangeRate-API 키
    print("\n2. ExchangeRate-API 키")
    print("   - https://www.exchangerate-api.com/ 에서 발급 가능")
    print("   - 무료 티어: 1,500 calls/month")
    exchange_key = getpass.getpass("   API 키를 입력하세요: ")
    if exchange_key:
        set_key(env_path, "EXCHANGE_API_KEY", exchange_key)
        print("   ✅ ExchangeRate-API 키가 설정되었습니다.")
    
    # Google Maps API 키
    print("\n3. Google Maps API 키")
    print("   - https://cloud.google.com/maps-platform/ 에서 발급 가능")
    print("   - 무료 티어: $200 크레딧 제공 (월간)")
    maps_key = getpass.getpass("   API 키를 입력하세요: ")
    if maps_key:
        set_key(env_path, "GOOGLE_MAPS_API_KEY", maps_key)
        print("   ✅ Google Maps API 키가 설정되었습니다.")
    
    print("\nAPI 키 설정이 완료되었습니다.")
    print("설정된 API 키는 .env 파일에 안전하게 저장되었습니다.")

if __name__ == "__main__":
    setup_api_keys() 