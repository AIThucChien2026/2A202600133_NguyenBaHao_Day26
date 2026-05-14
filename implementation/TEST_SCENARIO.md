# Kịch bản Test MCP Server (Demo Script)

Tài liệu này hướng dẫn các bước test và các điểm cần chụp ảnh để hoàn thiện bài nộp Lab 26.

## 1. Chuẩn bị (Setup)
- Đảm bảo đã chạy `python init_db.py`.
- Chạy lệnh: `npx @modelcontextprotocol/inspector python implementation/mcp_server.py`.
- Truy cập `localhost:3000` và nhấn nút **Connect**.

---

## 2. Các bước Test & Ảnh cần chụp

### 📸 Ảnh 1: Giao diện Kết nối thành công
- **Thao tác:** Sau khi nhấn Connect, dấu chấm chuyển sang màu xanh lá.
- **Yêu cầu:** Chụp toàn màn hình thấy rõ các tab `List Tools` và `List Resources`.

![Kết nối thành công](./images/1.GiaoDien.png)

### 📸 Ảnh 2: Khám phá Tài nguyên (Schema Resource)
- **Thao tác:** 
  - Chọn tab **Resources**.
  - Tìm `schema://database`, nhấn **Read Resource**.
- **Yêu cầu:** Chụp màn hình khung kết quả hiện ra cấu hình JSON của toàn bộ Database.

![Schema Resource](./images/2.Schema%20Resource.png)

### 📸 Ảnh 2b: Khám phá Tài nguyên bảng cụ thể (Single Table Schema)
- **Thao tác:** 
  - Chọn tab **Resources**.
  - Tìm `schema://table/students` (hoặc tự nhập URI này), nhấn **Read Resource**.
- **Yêu cầu:** Chụp màn hình khung kết quả hiện ra thông tin cấu trúc cột (id, name, cohort, email) của riêng bảng `students`.

![Single Table Schema Resource](./images/2b.TableSchema.png)

### 📸 Ảnh 3: Truy vấn dữ liệu (Search Tool)
- **Thao tác:**
  - Chọn tab **Tools**, chọn tool `search`.
  - Nhập Arguments:
    - `table`: `"students"`
    - `filters`: `{"cohort": "A1"}`
  - Nhấn **Run Tool**.
- **Yêu cầu:** Chụp kết quả trả về danh sách sinh viên Alice và Bob.

![Search Tool Success](./images/3.ToolSearch.png)

### 📸 Ảnh 4: Tính toán dữ liệu (Aggregate Tool)
- **Thao tác:**
  - Chọn tool `aggregate`.
  - Nhập Arguments:
    - `table`: `"enrollments"`
    - `metric`: `"AVG"`
    - `column`: `"grade"`
  - Nhấn **Run Tool**.
- **Yêu cầu:** Chụp kết quả hiện ra điểm trung bình (xấp xỉ 3.65).

![Aggregate Tool Success](./images/4.ToolAggregate.png)

### 📸 Ảnh 4b: Thêm dữ liệu (Insert Tool)
- **Thao tác:**
  - Chọn tab **Tools**, chọn tool `insert`.
  - Nhập Arguments:
    - `table`: `"students"`
    - `values`: `{"name": "Frank Castle", "cohort": "C3", "email": "frank@example.com"}`
  - Nhấn **Run Tool**.
- **Yêu cầu:** Chụp kết quả trả về: `"message": "Record inserted successfully"` kèm theo thông tin sinh viên vừa được thêm.

![Insert Tool Success](./images/4b.ToolInsert.png)

### 📸 Ảnh 5: Xử lý lỗi (Validation - Unknown Table)
- **Thao tác:**
  - Chọn tool `search`.
  - Nhập `table`: `"id_teacher"`.
  - Nhấn **Run Tool**.
- **Yêu cầu:** Chụp thông báo lỗi màu đỏ hiện ra: `"Error: Table 'id_teacher' does not exist."`

![Error Unknown Table](./images/5.ErrorTable.png)

### 📸 Ảnh 6: Xử lý lỗi (Validation - Unknown Column)
- **Thao tác:**
  - Chọn tool `search`.
  - Nhập `table`: `"students"`.
  - Nhập `filters`: `{"age": 20}`.
  - Nhấn **Run Tool**.
- **Yêu cầu:** Chụp thông báo lỗi: `"Error: Invalid filter column: age"`

![Error Unknown Column](./images/6.ErrorColumns.png)

### 📸 Ảnh 7: Xử lý lỗi (Validation - Empty Insert)
- **Thao tác:**
  - Chọn tab **Tools**, chọn tool `insert`.
  - Nhập `table`: `"courses"`.
  - Nhập `values`: `{}`.
  - Nhấn **Run Tool**.
- **Yêu cầu:** Chụp thông báo lỗi màu đỏ: `"Error: Insert values cannot be empty."`

![Error Empty Insert](./images/7.ErrorEmptyInsert.png)

### 📸 Ảnh 8: Tích hợp với Client (Gemini CLI)
- **Thao tác:**
  - Mở Terminal mới.
  - Chạy lệnh thêm server vào Gemini CLI (chú ý sửa đường dẫn tuyệt đối cho đúng thư mục máy bạn, lệnh bên dưới là ví dụ):
    ```bash
    gemini mcp add sqlite-lab python "b:\VInuni_lab\lab_26\Day26-Track3-MCP-tool-integration\implementation\mcp_server.py"
    ```
  - Chạy lệnh test nghiệm thu để Gemini dùng tool tìm học sinh:
    ```bash
    gemini --allowed-mcp-server-names sqlite-lab --skip-trust -p "Use mcp_sqlite-lab_search with table='students' and filters={'cohort': 'A1'}"
    ```
- **Yêu cầu:** Chụp toàn bộ màn hình Terminal cho thấy lệnh đã chạy, Gemini có gọi tool `search` và liệt kê ra được Alice và Bob.

![Gemini CLI Integration](./images/8.GeminiCLI.png)

---
