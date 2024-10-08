import streamlit as st

class ChatHistory:
    """대화 기록을 관리하는 클래스"""
    
    def __init__(self):
        if "messages" not in st.session_state:
            st.session_state.messages = []
    
    def add_message(self, role: str, content: str):
        """대화 메시지를 추가한다."""
        st.session_state.messages.append({"role": role, "content": content})
    
    def get_messages(self):
        """모든 대화 메시지를 가져온다."""
        return st.session_state.messages