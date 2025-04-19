def print_gugudan():
    # 구구단을 3단씩 나누어 출력
    for start in range(2, 10, 3):
        end = min(start + 3, 10)
        # 단 제목 출력
        print("\n" + "="*50)
        for i in range(start, end):
            print(f"{i}단".center(15), end="")
        print("\n" + "="*50)
        
        # 구구단 내용 출력
        for j in range(1, 10):
            for i in range(start, end):
                print(f"{i} x {j} = {i*j:2d}".center(15), end="")
            print()

if __name__ == "__main__":
    print("구구단을 출력합니다!")
    print_gugudan() 