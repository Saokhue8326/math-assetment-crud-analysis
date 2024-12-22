import pandas as pd
import os
from tkinter import messagebox

COLUMN_NAMES = ["Student ID", "Student Country", "Question ID", "Type of Answer", "Question Level", "Topic", "Subtopic", "Keywords"]

class DataManager:
    """
    Quản lý dữ liệu cho ứng dụng.

    Lớp này chịu trách nhiệm tải, lưu, thao tác và tìm kiếm dữ liệu. Dữ liệu được lưu trữ trong một file CSV.
    """

    def __init__(self, file_name="./data/dataset.csv"):
        """
        Khởi tạo đối tượng DataManager.

        Tham số:
            file_name (str, tùy chọn): Đường dẫn tới file CSV chứa dữ liệu. Mặc định là "./dataset.csv".
        """
        self.file_name = file_name
        self.data = self.load_data()

    def load_data(self):
        """
        Tải dữ liệu từ file CSV.

        Kiểm tra sự tồn tại của file và đọc dữ liệu bằng pandas.read_csv(). Trả về một DataFrame rỗng nếu gặp lỗi.
        """
        if os.path.exists(self.file_name):
            try:
                return pd.read_csv(self.file_name, delimiter=";", encoding="utf-8")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể đọc file: {e}")
                return pd.DataFrame(columns=COLUMN_NAMES)
        else:
            messagebox.showwarning("Cảnh báo", "File không tồn tại. Sử dụng dữ liệu mặc định.")
            return pd.DataFrame(columns=COLUMN_NAMES)

    def save_data(self):
        """
        Lưu dữ liệu vào file CSV.

        Sử dụng pandas.to_csv() để lưu nội dung của DataFrame `self.data` vào file được chỉ định bởi `self.file_name`.
        """
        self.data.to_csv(self.file_name, sep=";", index=False, encoding="utf-8")

    def add_data(self, new_data):
        """
        Thêm một hàng dữ liệu mới vào DataFrame.

        Tham số:
            new_data (list): Danh sách các giá trị tương ứng với các cột trong DataFrame.
        """
        self.data.loc[len(self.data)] = new_data
        self.save_data()

    def delete_data(self, indices):
        """
        Xóa các hàng dữ liệu được chọn.

        Tham số:
            indices (list): Danh sách các chỉ số của các hàng cần xóa.
        """
        self.data.drop(self.data.index[indices], inplace=True)
        self.save_data()

    def update_data(self, index, updated_data):
        """
        Cập nhật dữ liệu của một hàng cụ thể.

        Tham số:
            index (int): Chỉ số của hàng cần cập nhật.
            updated_data (list): Danh sách các giá trị mới cho hàng được cập nhật.
        """
        self.data.iloc[index] = updated_data
        self.save_data()

    def search_data(self, search_values):
        """
        Tìm kiếm dữ liệu dựa trên các giá trị tìm kiếm.

        Tìm kiếm theo từng cột tương ứng với danh sách `search_values`. Sử dụng phương thức `str.contains` để kiểm tra sự khớp mẫu không phân biệt chữ hoa chữ thường.

        Tham số:
            search_values (list): Danh sách các giá trị tìm kiếm, tương ứng với các cột trong DataFrame.

        Trả về:
            pandas.DataFrame: DataFrame chứa các hàng dữ liệu thỏa mãn điều kiện tìm kiếm.
        """
        filtered_data = self.data.copy()
        for i, value in enumerate(search_values):
            if value:
                filtered_data = filtered_data[filtered_data[COLUMN_NAMES[i]].astype(str).str.contains(value, case=False, na=False)]
        return filtered_data

    def sort_data(self, sort_by, ascending=True):
        """
        Sắp xếp dữ liệu theo một cột cụ thể.

        Sử dụng phương thức `sort_values` của DataFrame để sắp xếp dữ liệu theo cột `sort_by` với thứ tự tăng dần hoặc giảm dần tùy thuộc vào tham số `
        # data_manager.py (continued)
        """
        if sort_by in self.data.columns:
            self.data.sort_values(by=sort_by, ascending=ascending, inplace=True)
        return self.data