import os
import random
from langchain_core.tools import tool
from rag.rag_service import RagSummarizeService
from utils.logger_handler import logger

# 保留你原有的 RAG 服务实例
rag = RagSummarizeService()

# 模拟校园数据：代替原来的 external_data
# 在阶段2/3，我们会把这些数据搬到 MySQL 或通过 FastAPI 真实请求，现在先用字典模拟
STUDENT_RECORDS = {
    "1001": {"2023-秋季": "3.82", "2024-春季": "3.85"},
    "1002": {"2023-秋季": "3.20", "2024-春季": "3.20"},
    "20230001": {"2023-秋季": "3.8", "2024-春季": "3.9"}
}

# ==========================================
# 工具 1：校园知识库检索工具（必须保留的核心）
# ==========================================
@tool(description="从向量存储中检索校园规章制度、图书馆规定等参考资料。当用户询问学校规定、入馆须知等文档类信息时，必须使用此工具。")
def rag_summarize(query: str) -> str:
    # 这里原封不动调用你的 RAG 服务
    return rag.rag_summarize(query)

# ==========================================
# 工具 2：获取当前登录学生的学号
# ==========================================
@tool(description="获取当前用户的学号，以纯字符串返回。在查询个人信息前，通常需要先调用此工具获取学号。")
def get_student_id() -> str:
    # 模拟获取当前登录人的学号
    return random.choice(list(STUDENT_RECORDS.keys()))

# ==========================================
# 工具 3：查询学生绩点 (GPA)
# ==========================================
@tool(description="根据学号和学期查询学生的绩点(GPA)，以纯字符串返回。学期格式如：'2023-秋季'、'2024-春季'。如果未检索到返回空字符串。")
def query_gpa(student_id: str, semester: str) -> str:
    try:
        gpa = STUDENT_RECORDS[student_id][semester]
        return f"学号 {student_id} 在 {semester} 学期的绩点为: {gpa}"
    except KeyError:
        logger.warning(f"[query_gpa] 未能检索到学生 {student_id} 在 {semester} 的成绩数据")
        return "未能查询到该学期的绩点记录，请确认学期格式是否正确（如：2023-秋季）。"

# ==========================================
# 工具 4：查询空闲自习室/教室
# ==========================================
@tool(description="查询指定教学楼当前的空闲自习室列表。入参为主楼名称（如'教一'，'教二'，'图书馆'）。")
def query_empty_classroom(building_name: str) -> str:
    # 模拟真实系统的数据返回
    mock_classrooms = {
        "教一": "101, 105, 204",
        "教二": "302, 305",
        "图书馆": "三楼B区, 四楼A区"
    }
    classrooms = mock_classrooms.get(building_name)
    if classrooms:
        return f"{building_name} 当前空闲自习室有: {classrooms}"
    return f"目前暂无 {building_name} 的空闲教室数据。"