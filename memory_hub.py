import json
import os


class MemoryHub:
    def __init__(self, storage_path="memory.json"):
        self.storage_path = storage_path
        self.messages = []
        self._load()

    def _load(self):
        # 如果存储路径存在，则加载记忆到内存中，如果不存在，则创建一个空列表
        if os.path.exists(self.storage_path):
            with open(self.storage_path, "r", encoding="utf-8") as file:
                self.messages = json.load(file)
        else:
            self.messages = []

    def _save(self):
        # 保存记忆到文件
        # 使用 json 库将内存数据保存到文件中，w是写入模式
        with open(self.storage_path, "w", encoding="utf-8") as file:
            json.dump(self.messages, file, ensure_ascii=False, indent=2)

    def add_message(self, role, content):
        """添加一条消息（role: 'user' 或 'assistant'）"""
        self.messages.append({"role": role, "content": content})
        self._save()
        print(f"已添加消息: {role}: {content}")

    def find_messages(self, keyword):
        results = []
        for msg in self.messages:
            # 检查消息内容是否包含关键字（忽略大小写）
            if keyword.lower() in msg["content"].lower():
                # 将匹配的消息添加到结果列表中
                results.append(msg)
        return results


if __name__ == "__main__":
    hub = MemoryHub("test_memory.json")
    hub.add_message("user", "我喜欢晴天")
    hub.add_message("assistant", "那我们去海边吧")
    found = hub.find_messages("晴天")
    print("找到的消息:", found)
