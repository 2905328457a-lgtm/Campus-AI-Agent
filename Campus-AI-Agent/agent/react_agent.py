from langchain.agents import create_agent
from models.factory import chat_model
from utils.prompt_loader import load_system_prompts
from agent.tools.agent_tools import rag_summarize, get_student_id, query_gpa, query_empty_classroom
from agent.tools.middleware import monitor_tool, log_before_model, report_prompt_switch
from langchain_core.messages import AIMessage

class ReactAgent:
    def __init__(self):
        self.agent = create_agent(
            model=chat_model,
            system_prompt=load_system_prompts(),
            tools=[rag_summarize, get_student_id, query_gpa, query_empty_classroom],
            middleware=[monitor_tool, log_before_model, report_prompt_switch]
        )

    def execute_stream(self, query: str):
        input_dict = {
            "messages": [
                {"role": "user", "content": query}
            ]
        }
        # 第三个参数context就是上下文runtime中的信息，就是我们做提示词切换的标记
        for chunk in self.agent.stream(input_dict, stream_mode="values", context={"report": False}):
            latest_message = chunk["messages"][-1]
            if not isinstance(latest_message, AIMessage):
                continue
            if latest_message.content:
                raw_text: str = latest_message.content.strip() + "\n"

                # 2. 脱敏：如果包含 Final Answer，只截取后面的正式回答
                if "Final Answer:" in raw_text:
                    clean_text = raw_text.split("Final Answer:")[-1].strip()
                elif "Final Answer：" in raw_text:  # 兼顾中文冒号
                    clean_text = raw_text.split("Final Answer：")[-1].strip()
                elif raw_text.startswith("Thought:") or raw_text.startswith("Thought："):
                    # 纯思考过程，直接隐蔽，不播报给用户
                    continue
                else:
                    # 学期报告或其他场景，正常展示
                    clean_text = raw_text

                if clean_text:
                    yield clean_text + "\n"


if __name__ == '__main__':
    agent = ReactAgent()
    for chunk in agent.execute_stream("给我生成我的使用报告"):
        print(chunk, end="", flush=True)