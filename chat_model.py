from langchain_aws.chat_models import ChatBedrock
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import AIMessage, AIMessageChunk
from langgraph.checkpoint.memory import MemorySaver
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode, tools_condition

class ChatModel:
    """Chat 모델 클래스는 주어진 모델 ID로 대화 모델을 초기화하고 요청에 대한 응답을 제공합니다."""
    
    def __init__(self, model_id):
        self.chat_model = ChatBedrock(model_id=model_id)
        # {'meesages': [msg1, msg2, msg3]}
        self.tool = TavilySearchResults(max_results=3)
        self.tools = [self.tool]
        self.tool_node = ToolNode(tools=self.tools)
        self.chat_model_with_tool = self.chat_model.bind_tools(self.tools)
        self.graph_builder = StateGraph(MessagesState)
        self.graph_builder.add_node('model', self._call_model)
        self.graph_builder.add_node('tools', self.tool_node)
        self.graph_builder.set_entry_point('model')
        self.graph_builder.add_conditional_edges(
            'model',
            tools_condition
        )
        self.graph_builder.add_edge('tools', 'model')
        self.memory = MemorySaver()
        self.graph = self.graph_builder.compile(checkpointer=self.memory)
        self.config = {'configurable': {'thread_id': '1'}}

    def _call_model(self, state: MessagesState):
        return {'messages': self.chat_model_with_tool.invoke(state['messages'])}
    
    def get_response(self, prompt: str):
        """모델에 대한 요청을 보내고 응답을 받는다."""
        for chunk, metadata in self.graph.stream(
                {'messages': prompt},
                config=self.config,
                stream_mode='messages'
            ):
            print(chunk)
            if isinstance(chunk, AIMessage):
                if isinstance(chunk.content, str):
                    yield chunk.content
                elif len(chunk.content) > 0 and \
                    chunk.content[0]['type'] == 'text':
                    yield chunk.content[0]['text']