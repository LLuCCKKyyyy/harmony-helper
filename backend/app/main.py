"""
Harmony Helper - FastAPI Backend Server
提供和声生成的REST API接口
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
import os

from app.harmony_engine.core import HarmonyGenerator, HarmonyType

# 创建 FastAPI 应用
app = FastAPI(
    title="Harmony Helper API",
    description="AI-Powered Vocal Harmony Generation API",
    version="0.1.0"
)

# 配置 CORS（允许前端跨域访问）
# 从环境变量读取允许的域名，默认允许所有
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if allowed_origins != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化和声生成器
harmony_generator = HarmonyGenerator()


# ===== 数据模型定义 =====

class NoteInput(BaseModel):
    """单个音符输入模型"""
    pitch: str = Field(..., description="音高，例如: C4, D#5, Bb3", example="C4")
    duration: float = Field(1.0, description="时值（秒）", example=1.0)
    offset: float = Field(0.0, description="起始时间（秒）", example=0.0)


class HarmonyRequest(BaseModel):
    """和声生成请求模型"""
    melody: List[NoteInput] = Field(..., description="旋律音符列表")
    harmony_type: str = Field(
        "third", 
        description="和声类型: third, fifth, parallel_fourth, parallel_sixth, contrary, oblique, pedal",
        example="third"
    )


class NoteOutput(BaseModel):
    """单个音符输出模型"""
    pitch: str
    duration: float
    offset: float


class HarmonyResponse(BaseModel):
    """和声生成响应模型"""
    melody: List[NoteOutput]
    harmony: List[NoteOutput]
    harmony_type: str
    message: str = "Harmony generated successfully"


# ===== API 路由 =====

@app.get("/")
async def root():
    """API根路径，返回欢迎信息"""
    return {
        "message": "Welcome to Harmony Helper API",
        "version": "0.1.0",
        "docs": "/docs",
        "harmony_types": [ht.value for ht in HarmonyType]
    }


@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy"}


@app.get("/harmony-types")
async def get_harmony_types():
    """获取所有支持的和声类型"""
    return {
        "harmony_types": [
            {
                "value": HarmonyType.THIRD.value,
                "name": "三度和声",
                "description": "经典的三度平行和声"
            },
            {
                "value": HarmonyType.FIFTH.value,
                "name": "五度和声",
                "description": "纯五度平行和声"
            },
            {
                "value": HarmonyType.PARALLEL_FOURTH.value,
                "name": "平行四度",
                "description": "现代感的四度平行和声"
            },
            {
                "value": HarmonyType.PARALLEL_SIXTH.value,
                "name": "平行六度",
                "description": "温暖的六度平行和声"
            },
            {
                "value": HarmonyType.CONTRARY.value,
                "name": "反向运动",
                "description": "旋律上行时和声下行，反之亦然"
            },
            {
                "value": HarmonyType.OBLIQUE.value,
                "name": "斜向运动",
                "description": "和声保持固定音高，旋律自由移动"
            },
            {
                "value": HarmonyType.PEDAL.value,
                "name": "持续音",
                "description": "一个持续的低音贯穿整个旋律"
            }
        ]
    }


@app.post("/generate-harmony", response_model=HarmonyResponse)
async def generate_harmony(request: HarmonyRequest):
    """
    生成和声
    
    Args:
        request: 包含旋律和和声类型的请求
        
    Returns:
        包含原始旋律和生成的和声的响应
    """
    try:
        # 验证和声类型
        try:
            harmony_type = HarmonyType(request.harmony_type)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid harmony type: {request.harmony_type}. "
                       f"Valid types: {[ht.value for ht in HarmonyType]}"
            )
        
        # 转换输入格式
        melody_notes = [
            {
                'pitch': note.pitch,
                'duration': note.duration,
                'offset': note.offset
            }
            for note in request.melody
        ]
        
        # 生成和声
        harmony_notes = harmony_generator.generate_harmony(
            melody_notes,
            harmony_type
        )
        
        # 构建响应
        return HarmonyResponse(
            melody=[NoteOutput(**note) for note in melody_notes],
            harmony=[NoteOutput(**note) for note in harmony_notes],
            harmony_type=request.harmony_type,
            message=f"Successfully generated {harmony_type.value} harmony"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating harmony: {str(e)}"
        )


@app.post("/quick-harmony")
async def quick_harmony(pitch: str = "C4", harmony_type: str = "third"):
    """
    快速和声生成（单音符）
    用于快速测试和演示
    
    Args:
        pitch: 音高（例如: C4）
        harmony_type: 和声类型
        
    Returns:
        原始音符和和声音符
    """
    try:
        # 验证和声类型
        try:
            ht = HarmonyType(harmony_type)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid harmony type: {harmony_type}"
            )
        
        # 创建单音符旋律
        melody = [{'pitch': pitch, 'duration': 1.0, 'offset': 0.0}]
        
        # 生成和声
        harmony = harmony_generator.generate_harmony(melody, ht)
        
        return {
            "melody_note": melody[0]['pitch'],
            "harmony_note": harmony[0]['pitch'] if harmony else None,
            "harmony_type": harmony_type,
            "message": f"Generated {harmony_type} harmony for {pitch}"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    print("Starting Harmony Helper API Server...")
    print("API Documentation: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
