# Memory Hub

一个轻量级的本地长期记忆中间件，用于存储和检索对话历史，可集成到 AI 聊天应用（如 SillyTavern）或作为通用记忆服务。

## 目标

- 解决大模型应用中的长期记忆遗忘问题
- 提供简单易用的 API 进行记忆的存储与检索
- 支持向量检索、自动总结等高级特性（规划中）

## 当前功能

- [x] 基于 JSON 文件持久化存储对话消息
- [x] 添加消息（角色 + 内容）并自动保存
- [x] 基础关键词检索（规划中）
- [ ] 向量检索
- [ ] 重要性判断
- [ ] REST API 服务
- [ ] 集成到 SillyTavern

## 快速开始

### 环境要求
- Python 3.8+
- 无需额外依赖（仅用标准库）

### 安装与运行

```bash
git clone https://github.com/你的用户名/Memory_Hub.git
cd Memory_Hub
python memory_hub.py
```

### 基本使用

```python

from memory_hub import MemoryHub

hub = MemoryHub("my_memory.json")
hub.add_message("user", "我喜欢晴天")
hub.add_message("assistant", "那我们去海边吧")
# 查找功能（待实现）
# results = hub.find_messages("晴天")
```

## 技术栈
- Python 3

- JSON 文件存储（后续将支持 SQLite / 向量库）

- Git 版本控制

## 项目结构

Memory_Hub/
├── memory_hub.py       # 核心类
├── README.md
├── .gitignore
└── docs/               # 个人学习笔记（仅供参考学习）

## 下一步计划

- [ ] 实现 `find_messages` 关键词检索
- [ ] 用 FastAPI 封装成 HTTP 服务
- [ ] 引入向量数据库（Chroma）支持语义搜索
- [ ] 开发酒馆扩展，与 Memory Hub 联动

## 许可
MIT License

