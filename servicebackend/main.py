import os

from app.database.postgres import postgres_engine, PostgresBase

"""
智能医疗助手 - 主入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.auth import router as auth_router
from app.api.chat import router as chat_router
from app.api.conversations import router as conversations_router
from app.api.medical_upload import router as medical_upload_router
from app.config.settings import settings
from app.database.mysql import engine, Base

from app.models.conversation import Conversation
from app.models.medical_document import MedicalDocument

__all__ = ["Conversation", "MedicalDocument"]


#初始化langSimth

os.environ["LANGCHAIN_TRACING_V2"] = str(settings.LANGCHAIN_TRACING_V2).lower()
os.environ["LANGCHAIN_API_KEY"] = settings.LANGCHAIN_API_KEY
os.environ["LANGCHAIN_PROJECT"] = settings.LANGCHAIN_PROJECT

# 创建数据库表
# MySQL 数据库表（用户认证）
try:
    Base.metadata.create_all(bind=engine)
    print("[OK] MySQL 数据库表创建成功")
except Exception as e:
    print(f"[WARN] MySQL 数据库表创建失败: {e}")

# PostgreSQL 数据库表（会话管理）- 延迟初始化
try:
    PostgresBase.metadata.create_all(bind=postgres_engine)
    print("[OK] PostgreSQL 数据库表创建成功")
except Exception as e:
    print(f"[WARN] PostgreSQL 数据库未创建或连接失败")
    print(f"   请先执行: psql -h 42.193.143.46 -U postgres -f init_postgres.sql")
    print(f"   错误详情: {e}")

# 创建 FastAPI 应用
app = FastAPI(
    title="智能医疗助手 API",
    description="基于 LangChain 1.0.3 和多智能体协作的医疗助手系统",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应设置具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 注册路由


app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(chat_router, prefix="/chat", tags=["chat"])
app.include_router(conversations_router, prefix="/conversations", tags=["conversations"])
app.include_router(medical_upload_router, prefix="/documents", tags=["documents"])


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "智能医疗助手 API",
        "version": "1.0.0",
        "docs": "/docs",
        "tech_stack": {
            "langchain": "1.0.3",
            "langgraph": "1.0.2",
            "python": "3.12.x"
        }
    }


if __name__ == "__main__":
    import uvicorn

    print("\n" + "=" * 50)
    print("智能医疗助手 API 启动中...")
    print("=" * 50)
    print(f"访问地址: http://{settings.HOST}:{settings.PORT}")
    print(f"API 文档: http://{settings.HOST}:{settings.PORT}/docs")
    print("=" * 50 + "\n")

    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
