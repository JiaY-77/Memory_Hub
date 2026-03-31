import sqlite3


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
        """查找包含指定关键字的消息（不区分大小写），按时间倒序返回"""
        # 1. 获取数据库游标，用于执行 SQL 语句
        cursor = self.conn.cursor()

        # 2. 执行查询：使用 LOWER() 函数实现不区分大小写匹配
        #    % 是通配符，表示任意字符；keyword 被 % 包围，实现包含匹配
        cursor.execute(
            """
            SELECT id, role, content, timestamp
            FROM messages
            WHERE LOWER(content) LIKE LOWER(?)
            ORDER BY timestamp DESC
            """,
            ("%" + keyword + "%",),  # 参数化查询，防止 SQL 注入
        )

        # 3. 获取所有匹配的行（元组列表）
        rows = cursor.fetchall()

        # 4. 将每个元组转换成字典，方便调用者通过字段名访问数据
        results = []
        for row in rows:
            results.append(
                {
                    "id": row[0],  # 消息 ID
                    "role": row[1],  # 角色（user/assistant）
                    "content": row[2],  # 消息内容
                    "timestamp": row[3],  # 时间戳（自动生成）
                }
            )

        # 5. 返回字典列表（如果没有匹配，返回空列表）
        return results

    def delete_message(self, message_id):
        """根据消息 ID 删除一条记录，返回被删除的消息内容（字典），如果 ID 不存在则返回 None"""
        # 1. 获取数据库游标（用于执行 SQL）
        cursor = self.conn.cursor()

        # 2. 先查询消息是否存在（避免删除不存在的 ID 后无法返回内容）
        cursor.execute(
            "SELECT id, role, content, timestamp FROM messages WHERE id = ?",
            (message_id,),
        )
        row = cursor.fetchone()  # 取第一条（应该只有一条）

        # 3. 如果查询结果为空，说明没有这个 ID，直接返回 None
        if row is None:
            return None

        # 4. 执行删除操作（参数化查询，安全）
        cursor.execute("DELETE FROM messages WHERE id = ?", (message_id,))
        self.conn.commit()  # 提交事务，使删除生效

        # 5. 把查询到的行转换成字典，返回给调用者（方便知道删了什么）
        deleted_message = {
            "id": row[0],
            "role": row[1],
            "content": row[2],
            "timestamp": row[3],
        }
        return deleted_message

    def add_message(self, role, content):
        """向数据库中添加一条消息记录，返回新记录的ID"""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO messages (role, content) VALUES (?, ?)", (role, content)
        )
        self.conn.commit()  # 提交事务
        return cursor.lastrowid  # 返回自增ID


if __name__ == "__main__":
    hub = MemoryHub()

    # 添加几条测试消息
    id1 = hub.add_message("user", "我喜欢晴天")
    print(f"添加消息 ID: {id1}")
    id2 = hub.add_message("assistant", "那我们去海边吧")
    print(f"添加消息 ID: {id2}")

    # 查找包含“晴天”的消息
    found = hub.find_messages("晴天")
    print("找到的消息:", found)

    # 删除刚才添加的第一条消息（假设 id1 是 1）
    deleted = hub.delete_message(id1)
    if deleted:
        print("已删除消息:", deleted)
    else:
        print("消息不存在")

    # 再次查找，验证已删除
    found_again = hub.find_messages("晴天")
    print("删除后再次查找:", found_again)
