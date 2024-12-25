# Quản lý và Hiển thị Dữ liệu

Ứng dụng Python này cho phép người dùng quản lý và trực quan hóa dữ liệu được lưu trữ trong tệp CSV. Nó cung cấp các chức năng CRUD (Tạo, Đọc, Cập nhật, Xóa), tìm kiếm, sắp xếp và biểu đồ dữ liệu.

## Tính năng

*   **CRUD:** Thêm, sửa, xóa dữ liệu một cách dễ dàng.
*   **Tìm kiếm:** Tìm kiếm dữ liệu dựa trên nhiều tiêu chí.
*   **Sắp xếp:** Sắp xếp dữ liệu theo bất kỳ cột nào.
*   **Hiển thị dạng bảng:** Hiển thị dữ liệu trong bảng tương tác (Treeview).
*   **Biểu đồ:** Trực quan hóa dữ liệu bằng các loại biểu đồ:
    *   Biểu đồ cột xếp chồng (Stacked Bar Chart): So sánh số lượng câu trả lời đúng/sai theo quốc gia.
    *   Biểu đồ tròn (Pie Chart): Thể hiện tỷ lệ số lượng câu hỏi theo từng cấp độ.
    *   Biểu đồ diện tích (Area Chart): Thể hiện số lượng câu hỏi theo từng chủ đề.
*   **Giao diện người dùng:** Giao diện đồ họa thân thiện sử dụng Tkinter.
*   **Lưu trữ dữ liệu:** Dữ liệu được lưu trữ trong tệp CSV.

## Công nghệ sử dụng

*   Python
*   Tkinter (Giao diện người dùng)
*   Pandas (Xử lý dữ liệu)
*   Matplotlib (Vẽ biểu đồ)

## Cài đặt

1.  **Clone repository:**

    ```bash
    git clone https://github.com/Saokhue8326/math-assetment-crud-analysis.git
    ```

2.  **Di chuyển vào thư mục dự án:**

    ```bash
    cd math-assetment-crud-analysis
    ```

3.  **Tạo môi trường ảo (khuyến nghị):**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # Trên Linux/macOS
    .venv\Scripts\activate  # Trên Windows
    ```

4.  **Cài đặt các gói phụ thuộc:**

    ```bash
    pip install -r requirements.txt
    ```

## Cách sử dụng

1.  **Chạy ứng dụng:**

    ```bash
    python ./src/main.py
    ```

2.  **Giao diện chính:** Giao diện sẽ hiển thị bảng dữ liệu, các trường nhập liệu và các nút chức năng.

3.  **Thao tác với dữ liệu:**
    *   **Thêm:** Nhập dữ liệu vào các trường và nhấn nút "Add".
    *   **Sửa:** Chọn một hàng trong bảng, chỉnh sửa dữ liệu trong các trường và nhấn nút "Update".
    *   **Xóa:** Chọn một hoặc nhiều hàng trong bảng và nhấn nút "Delete".
    *   **Tìm kiếm:** Nhập giá trị tìm kiếm vào các trường và nhấn nút "Search".
    *   **Sắp xếp:** Nhấp vào tiêu đề cột trong bảng để sắp xếp.

4.  **Hiển thị biểu đồ:** Nhấn vào các nút "Stacked Bar Chart", "Pie Chart" hoặc "Area Chart" để hiển thị biểu đồ tương ứng.

## Cấu trúc thư mục

*   `math-assetment-crud-analysis`
    *   `data`
        *   `dataset.csv`: File dữ liệu mẫu (hoặc file dữ liệu của bạn)
    *   `src`
        *   `data_manager.py`: Quản lý dữ liệu (đọc/ghi file CSV, thao tác dữ liệu)
        *   `chart_utils.py`: Các hàm tiện ích để vẽ biểu đồ
        *   `main.py`: Code chính của ứng dụng

## Đóng góp

Chúng tôi xin cảm ơn sự đóng góp từ các thành viên:
- **Hồ Phạm Sao Khuê** (24154056)
- **Phan Khánh Duy** (24154020)
- **Ngô Trung Hoàng Đức** (24154028)
- **Nguyễn Duy Hào** (24154032)
- **Nguyễn Duy Hảo** (24154034)

Mọi đóng góp đều được hoan nghênh. Vui lòng tạo pull request hoặc mở issue nếu bạn tìm thấy lỗi hoặc có ý tưởng cải tiến.

## Liên hệ

Mọi thắc mắc, góp ý xin vui lòng liên hệ qua email: **khuehophamsao@gmail.com**