
from mcp.server.fastmcp import FastMCP

# 初始化一個 MCP Server
# "My Math Server" 是服務名稱
mcp = FastMCP("My Math Server")

# 定義工具，使用 @mcp.tool() 裝飾器
# 這會自動將 Python 函數轉換為 MCP Tool 定義
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def query_sales_db(sql_query: str) -> str:
    """
    Execute a SQL query against the internal 'sales' database.
    Schema:
    - sales_data (id, product_name, amount, date)
    
    Example: "SELECT sum(amount) FROM sales_data WHERE date > '2023-01-01'"
    """
    # 模擬資料庫 (Mock DB using Pandas logic or simple list)
    # 在真實世界，這裡會連接 PostgreSQL/MySQL
    import sqlite3
    
    # 建立一個記憶體資料庫來模擬
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    # 塞入假資料
    cursor.execute("CREATE TABLE sales_data (id INTEGER, product_name TEXT, amount INTEGER, date TEXT)")
    cursor.executemany("INSERT INTO sales_data VALUES (?, ?, ?, ?)", [
        (1, "Laptop", 1200, "2023-01-15"),
        (2, "Mouse", 25, "2023-01-16"),
        (3, "Monitor", 300, "2023-02-01"),
        (4, "Laptop", 1200, "2023-02-10"),
    ])
    conn.commit()
    
    try:
        # 安全檢查 (簡單版)
        if "DROP" in sql_query.upper() or "DELETE" in sql_query.upper():
            return "Error: Destructive operations are not allowed."
            
        cursor.execute(sql_query)
        results = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        
        # 格式化輸出
        if not results:
            return "No results found."
            
        output = f"Columns: {column_names}\n"
        for row in results:
            output += str(row) + "\n"
            
        return output.strip()
        
    except Exception as e:
        return f"SQL Error: {e}"
    finally:
        conn.close()

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

if __name__ == "__main__":
    # 使用 STDIO 模式啟動 Server
    # 這是最常見的 MCP 溝通方式，不需要開 Port，直接透過 Pipe 傳輸
    mcp.run()
