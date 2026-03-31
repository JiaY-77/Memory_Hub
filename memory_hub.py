import json
import os

"""
import json：Python 内置的 JSON 模块，用来把数据（列表、字典）保存成文件，或者从文件读取回来。因为我们要把聊天记录存成 JSON 文件，所以需要它。

import os：Python 内置的操作系统模块，里面有一个 os.path.exists 函数，可以判断文件是否存在。后面加载记忆时会用到。

"""


class MemoryHub:
    def __init__(self, storage_path="memory.json"):
        self.storage_path = storage_path
        self.messages = []
        self._load()

    def _load(self):
        if os.path.exists(self.storage_path):
            with open(self.storage_path, "r", encoding="utf-8") as file:
                self.messages = json.load(file)
        else:
            self.messages = []

    def _save(self):
        # 保存记忆到文件
        with open(self.storage_path, "w", encoding="utf-8") as file:
            json.dump(self.messages, file, ensure_ascii=False, indent=2)

    def find_messages(self, keyword):
        results = []
        for msg in self.messages:
            if keyword.lower() in msg["content"].lower():
                results.append(msg)
        return results

    def add_message(self, role, content):
        """添加一条消息（role: 'user' 或 'assistant'）"""
        self.messages.append({"role": role, "content": content})
        self._save()
        print(f"已添加消息: {role}: {content}")


if __name__ == "__main__":
    hub = MemoryHub("test_memory.json")
    hub.add_message("user", "我喜欢晴天")
    hub.add_message("assistant", "那我们去海边吧")
    found = hub.find_messages("晴天")
    print("找到的消息:", found)
