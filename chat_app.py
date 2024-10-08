import streamlit as st
from chat_model import ChatModel
from chat_history import ChatHistory

class ChatApp:
    """Chat 애플리케이션 클래스는 사용자의 입력과 대화 흐름을 관리한다."""
    
    def __init__(self, model: ChatModel, history: ChatHistory):
        if 'model' not in st.session_state:
            st.session_state.model = model
        self.model = st.session_state.model
        self.history = history
    
    def display_chat(self):
        """대화 기록을 화면에 표시한다."""
        for message in self.history.get_messages():
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    def handle_user_input(self):
        """사용자의 입력을 처리하고 응답을 표시한다."""
        prompt = st.chat_input("질문을 입력해주세요.")
        if prompt:
            self.history.add_message("user", prompt)
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # 모델에 사용자 입력을 전달하고 응답을 받는다
            stream = self.model.get_response(prompt)
            
            # 응답을 화면에 표시
            with st.chat_message("assistant"):
                response = st.write_stream(stream)

            self.history.add_message("assistant", response)
            