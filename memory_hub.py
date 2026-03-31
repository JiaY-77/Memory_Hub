import json
import os

"""
import json：Python 内置的 JSON 模块，用来把数据（列表、字典）保存成文件，或者从文件读取回来。因为我们要把聊天记录存成 JSON 文件，所以需要它。

import os：Python 内置的操作系统模块，里面有一个 os.path.exists 函数，可以判断文件是否存在。后面加载记忆时会用到。

"""

class MemoryHub:
    def __init__(self, storage_path = "memory.json"):
        self.storage_path = storage_path
        self.messages = []
        self._load()
        
        
    def _load(self):
        if os.path.exists(self.storage_path):
            with open(self.storage_path, "r", encoding = "utf-8") as file:
                self.messages = json.load(file)
        else:
            self.messages = []
 
    def _save(self):
        # 保存记忆到文件
        with open(self.storage_path, "w", encoding = "utf-8") as file:
            json.dump(self.messages, file, ensure_ascii = False, indent=2)
            
