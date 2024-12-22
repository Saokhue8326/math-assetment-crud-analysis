from tkinter import Tk, Frame, Canvas, LabelFrame, Label, Entry, Button, Scrollbar, Toplevel, messagebox
from tkinter import ttk
from data_manager import COLUMN_NAMES, DataManager
from chart_utils import draw_stacked_bar_chart, draw_pie_chart, draw_area_chart, clear_chart_area
import matplotlib.pyplot as plt

class App:
    """
    Ứng dụng quản lý và hiển thị dữ liệu.

    Ứng dụng này cho phép người dùng:
        - Thêm, sửa, xóa dữ liệu.
        - Tìm kiếm dữ liệu dựa trên các trường.
        - Sắp xếp dữ liệu theo các cột.
        - Hiển thị dữ liệu dưới dạng bảng.
        - Biểu đồ dữ liệu theo các kiểu: Hình cột xếp chồng, Hình tròn, Diện tích.

    Lưu ý: Dữ liệu được lưu trữ trong file CSV.
    """

    def __init__(self, master):
        """
        Khởi tạo cửa sổ chính của ứng dụng.

        Tham số:
            master (tkinter.Tk): Đối tượng Tk() của cửa sổ chính.
        """
        self.master = master
        self.master.title("Quản lý và Hiển thị Dữ liệu")
        self.master.state("zoomed")

        self.data_manager = DataManager()
        self.ascending_order = {}  # Lưu trữ thứ tự sắp xếp cho từng cột
        self.create_widgets()
        self.display_data()

    def create_widgets(self):
        """
        Tạo các thành phần giao diện của ứng dụng.

        - Khung chính (main_frame) chứa các khung con khác.
        - Khung CRUD (crud_frame) chứa các nút chức năng thêm, sửa, xóa, tìm kiếm và làm mới dữ liệu.
        - Khung Biểu đồ (chart_frame) chứa các nút chức năng vẽ các loại biểu đồ.
        - Khung Bảng (tree_frame) chứa Treeview hiển thị dữ liệu.
        - Các trường nhập liệu (input_fields) tương ứng với các cột dữ liệu.
        """
        self.main_frame = Frame(self.master)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.crud_frame = LabelFrame(self.main_frame, text="CRUD", padx=10, pady=10)
        self.crud_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.chart_frame = LabelFrame(self.main_frame, text="Charts", padx=10, pady=10)
        self.chart_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.tree_frame = LabelFrame(self.main_frame, text="Table", padx=10, pady=10)
        self.tree_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        self.main_frame.grid_rowconfigure(0, weight=10)
        self.main_frame.grid_rowconfigure(1, weight=0)
        self.main_frame.grid_columnconfigure(0, weight=0)
        self.main_frame.grid_columnconfigure(1, weight=10)

        self.input_fields = []
        for _, column in enumerate(COLUMN_NAMES):
            field_frame = Frame(self.crud_frame)
            field_frame.pack(fill="x", pady=5)
            Label(field_frame, text=column).pack(side="left", padx=5)
            entry = Entry(field_frame, width=30)
            entry.pack(side="right", padx=5)
            self.input_fields.append(entry)

        crud_input_frame = Frame(self.crud_frame)
        crud_input_frame.pack(fill="x", pady=10)
        Button(crud_input_frame, text="Search", command=self.search_data).pack(side="left", padx=5)
        Button(crud_input_frame, text="Add", command=self.add_data).pack(side="left", padx=5)
        Button(crud_input_frame, text="Update", command=self.update_data).pack(side="left", padx=5)
        Button(crud_input_frame, text="Delete", command=self.delete_data).pack(side="left", padx=5)
        Button(crud_input_frame, text="Refresh", command=self.display_data).pack(side="left", padx=5)

        chart_button_frame = Frame(self.chart_frame)
        chart_button_frame.pack(side="left", fill="y", padx=(0, 10))
        Button(chart_button_frame, text="Stacked Bar Chart", command=self.draw_stacked_bar_chart).pack(fill="x", pady=5)
        Button(chart_button_frame, text="Pie Chart", command=self.draw_pie_chart).pack(fill="x", pady=5)
        Button(chart_button_frame, text="Area Chart", command=self.draw_area_chart).pack(fill="x", pady=5)

        self.chart_display_frame = Frame(self.chart_frame)
        self.chart_display_frame.pack(side="right", fill="both", expand=True)

        self.tree = ttk.Treeview(self.tree_frame, columns=COLUMN_NAMES, show="headings", height=15)
        for column in COLUMN_NAMES:
            self.tree.heading(column, text=column, command=lambda c=column: self.sort_column(c))
            self.tree.column(column, anchor="w", width=120)
        self.tree.pack(side="left", fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.auto_fill_fields)

        vertical_scrollbar = Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        vertical_scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=vertical_scrollbar.set)

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def display_data(self, sort_by="Student ID", ascending=True):
        """
        Hiển thị dữ liệu trong Treeview.

        Xóa dữ liệu cũ, sắp xếp dữ liệu theo cột và thứ tự được chọn,
        và sau đó hiển thị từng hàng dữ liệu trong Treeview.

        Tham số:
            sort_by (str, tùy chọn): Cột để sắp xếp dữ liệu. Mặc định là "Student ID".
            ascending (bool, tùy chọn): Thứ tự sắp xếp (True: tăng dần, False: giảm dần). Mặc định là True.
        """
        self.data_manager.sort_data(sort_by, ascending)
        self.tree.delete(*self.tree.get_children())
        for _, row in self.data_manager.data.iterrows():
            self.tree.insert("", "end", values=list(row))
        for field in self.input_fields:
            field.delete(0, "end")

    def auto_fill_fields(self, events):
        """
        Tự động điền các trường nhập liệu khi chọn một hàng trong Treeview.

        Xác định hàng được chọn và điền giá trị của các cột tương ứng vào các trường nhập liệu.
        """
        selected_items = self.tree.selection()
        if selected_items:
            values = self.tree.item(selected_items[0], "values")
            for i, value in enumerate(values):
                self.input_fields[i].delete(0, "end")
                self.input_fields[i].insert(0, value)

    def add_data(self):
        """
        Thêm một hàng dữ liệu mới.

        Lấy giá trị từ các trường nhập liệu, tạo thành một danh sách,
        gọi phương thức `add_data` của `data_manager` để thêm dữ liệu mới,
        cuối cùng cập nhật hiển thị dữ liệu trong Treeview.
        """
        new_data = [entry.get() for entry in self.input_fields]
        self.data_manager.add_data(new_data)
        self.display_data()

    def delete_data(self):
        # main.py (continued)
        """
        Xóa các hàng dữ liệu được chọn.

        Kiểm tra xem có hàng nào được chọn, nếu không hiển thị thông báo cảnh báo.
        Nếu có, lấy chỉ số của các hàng được chọn và gọi phương thức `delete_data`
        của `data_manager` để xóa dữ liệu, cuối cùng cập nhật hiển thị dữ liệu trong Treeview.
        """
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một mục để xóa.")
            return
        indices = [self.tree.index(item) for item in selected_items]
        self.data_manager.delete_data(indices)
        self.display_data()

    def update_data(self):
        """
        Cập nhật dữ liệu của các hàng được chọn.

        Kiểm tra xem có hàng nào được chọn, nếu không hiển thị thông báo cảnh báo.
        Nếu có, lấy giá trị từ các trường nhập liệu, gọi phương thức `update_data`
        của `data_manager` để cập nhật dữ liệu, cuối cùng cập nhật hiển thị dữ liệu trong Treeview.
        """
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một mục để cập nhật.")
            return
        updated_data = [field.get() for field in self.input_fields]
        for item in selected_items:
            index = self.tree.index(item)
            self.data_manager.update_data(index, updated_data)
        self.display_data()

    def search_data(self):
        """
        Tìm kiếm dữ liệu.

        Lấy giá trị tìm kiếm từ các trường nhập liệu, gọi phương thức `search_data`
        của `data_manager` để thực hiện tìm kiếm, sau đó hiển thị kết quả trong Treeview.
        Nếu không tìm thấy kết quả, hiển thị thông báo.
        """
        search_values = [field.get().strip() for field in self.input_fields]
        if not any(search_values):
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập ít nhất một giá trị để tìm kiếm.")
            return
        filtered_data = self.data_manager.search_data(search_values)
        self.tree.delete(*self.tree.get_children())
        for _, row in filtered_data.iterrows():
            self.tree.insert("", "end", values=tuple(row))
        if filtered_data.empty:
            messagebox.showinfo("Kết quả", "Không tìm thấy kết quả phù hợp.")

    def sort_column(self, col):
        """
        Sắp xếp dữ liệu theo một cột khi người dùng nhấp vào tiêu đề cột trong Treeview.

        Đảo ngược thứ tự sắp xếp hiện tại (tăng dần/giảm dần) và gọi `display_data` để cập nhật hiển thị.

        Tham số:
            col (str): Tên cột cần sắp xếp.
        """
        self.ascending_order[col] = not self.ascending_order.get(col, True)
        self.display_data(sort_by=col, ascending=self.ascending_order[col])

    def draw_stacked_bar_chart(self):
        """
        Vẽ biểu đồ hình cột xếp chồng.

        Gọi hàm `draw_stacked_bar_chart` từ `chart_utils` để vẽ biểu đồ.
        """
        draw_stacked_bar_chart(self.data_manager.data, self.chart_display_frame)

    def draw_pie_chart(self):
        """
        Vẽ biểu đồ hình tròn.

        Gọi hàm `draw_pie_chart` từ `chart_utils` để vẽ biểu đồ.
        """
        draw_pie_chart(self.data_manager.data, self.chart_display_frame)

    def draw_area_chart(self):
        """
        Vẽ biểu đồ diện tích.

        Gọi hàm `draw_area_chart` từ `chart_utils` để vẽ biểu đồ.
        """
        draw_area_chart(self.data_manager.data, self.chart_display_frame)

    def on_closing(self):
        """
        Xử lý sự kiện đóng cửa sổ ứng dụng.

        Xóa các biểu đồ đang hiển thị và đóng cửa sổ ứng dụng.
        """
        clear_chart_area(self.chart_display_frame)
        self.master.destroy()

if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()