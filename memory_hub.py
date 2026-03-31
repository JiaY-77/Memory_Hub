import sqlite3  # 导入 SQLite3 库用于存储记忆到数据库中


class MemoryHub:
    def __init__(self, db_path="memory.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self._create_table()
        print("已连接到数据库：", db_path)

    def _create_table(self):
        """创建 messages 表（如果不存在）"""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        self.conn.commit()
        print("已创建表：messages")

    def find_messages(self, keyword):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT id, role, content, timestamp
            FROM messages
            WHERE LOWER(content) LIKE LOWER(?)
            ORDER BY timestamp DESC
        """,
            ("%" + keyword + "%",),
        )
        rows = cursor.fetchall()
        results = []
        for row in rows:
            results.append(
                {"id": row[0], "role": row[1], "content": row[2], "timestamp": row[3]}
            )
        return results

    # def add_message(self, role, content):
    #     """添加一条消息（role: 'user' 或 'assistant'）"""
    #     self.messages.append({"role": role, "content": content})
    #     self._save()
    #     print(f"已添加消息: {role}: {content}")

    # def find_messages(self, keyword):
    #     results = []
    #     for msg in self.messages:
    #         # 检查消息内容是否包含关键字（忽略大小写）
    #         if keyword.lower() in msg["content"].lower():
    #             # 将匹配的消息添加到结果列表中
    #             results.append(msg)
    #     return results


if __name__ == "__main__":
    hub = MemoryHub()
