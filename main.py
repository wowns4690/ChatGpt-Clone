from app_factory import AppFactory
import streamlit as st

def main():
    """메인 함수는 앱을 초기화하고 실행한다."""
    st.title("ChatGPT 클론 코딩")
    
    # 팩토리에서 앱을 생성
    app = AppFactory.create_chat_app()
    
    # 대화 내용 표시
    app.display_chat()
    
    # 사용자 입력 처리
    app.handle_user_input()

if __name__ == "__main__":
    main()