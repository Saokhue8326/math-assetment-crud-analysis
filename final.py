import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
import pandas as pd
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ================================
# Phần 1: Bé Hào
# ================================

FILE_NAME = r"D:\Code\Python\doan\dataset.csv"
du_lieu = pd.DataFrame()

danh_sach_cot = ["Student ID", "Student Country", "Question ID", "Type of Answer",
                 "Question Level", "Topic", "Sbtopic", "Keywords"]
# Đọc dữ liệu từ tệp tin CSV hoặc trả về DataFrame trống
def doc_du_lieu(file_name):
    if os.path.exists(file_name):
        try:
            return pd.read_csv(file_name, delimiter=";", encoding="utf-8")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đọc tệp: {e}")
            return pd.DataFrame(columns=danh_sach_cot)
    else:
        messagebox.showwarning("Cảnh báo", "Tệp không tồn tại. Sử dụng dữ liệu mặc định.")
        return pd.DataFrame(columns=danh_sach_cot)

# Hiển thị dữ liệu trong Treeview
def hien_thi_du_lieu():
    global du_lieu
    du_lieu = doc_du_lieu(FILE_NAME)
    tree.delete(*tree.get_children())  # Xóa toàn bộ dữ liệu trong Treeview
    for _, row in du_lieu.iterrows():
        tree.insert("", "end", values=list(row))

# Tự động đổ dữ liệu vào ô nhập liệu khi chọn dòng
def tu_dong_do_du_lieu(event):
    selected_items = tree.selection()
    if selected_items:
        item = selected_items[0]
        values = tree.item(item, "values")
        for i, value in enumerate(values):
            danh_sach_o_nhap[i].delete(0, tk.END)
            danh_sach_o_nhap[i].insert(0, value)

# Thêm dữ liệu mới vào CSV
def them_du_lieu():
    new_data = [entry.get() for entry in danh_sach_o_nhap]
    du_lieu.loc[len(du_lieu)] = new_data
    du_lieu.to_csv(FILE_NAME, sep=";", index=False, encoding="utf-8")
    hien_thi_du_lieu()

# Xóa dữ liệu được chọn
def xoa_du_lieu():
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("Cảnh báo", "Chọn mục để xóa.")
        return
    for item in selected_items:
        index = tree.index(item)
        du_lieu.drop(du_lieu.index[index], inplace=True)
    du_lieu.to_csv(FILE_NAME, sep=";", index=False, encoding="utf-8")
    hien_thi_du_lieu()


# ================================
# Phần 2: Bé Hào (Đồ thị)
# ================================

# Hàm hiển thị biểu đồ ở chế độ toàn màn hình
def hien_thi_full_screen(fig):
    full_screen = tk.Toplevel()
    full_screen.title("Xem biểu đồ toàn màn hình")
    full_screen.state("zoomed")
    canvas = FigureCanvasTkAgg(fig, master=full_screen)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    tk.Button(full_screen, text="Thoát", command=full_screen.destroy).pack(pady=10)

# Vẽ biểu đồ cột chồng
def ve_do_thi_cot():
    for widget in khung_4.winfo_children():
        widget.destroy()
    if 'Student Country' in du_lieu.columns and 'Type of Answer' in du_lieu.columns:
        grouped_data = du_lieu.groupby(['Student Country', 'Type of Answer']).size().unstack(fill_value=0)
        fig, ax = plt.subplots(figsize=(8, 5))
        grouped_data.plot(kind='bar', stacked=True, ax=ax, color=['red', 'green'])
        ax.set_title('Biểu đồ cột chồng thể hiện Student Country và Type of Answer')
        ax.set_xlabel('Student Country')
        ax.set_ylabel('Số lượng')
        ax.legend(title='Type of Answer', labels=['Sai (0)', 'Đúng (1)'])
        canvas = FigureCanvasTkAgg(fig, master=khung_4)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        tk.Button(khung_4, text="Phóng to", command=lambda: hien_thi_full_screen(fig)).pack(pady=10)

# Vẽ biểu đồ tròn
def ve_bieu_do_tron():
    for widget in khung_4.winfo_children():
        widget.destroy()
    if 'Question Level' in du_lieu.columns:
        data = du_lieu['Question Level'].value_counts()
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(data, labels=data.index, autopct='%1.1f%%', startangle=90)
        ax.set_title("Biểu đồ tròn thể hiện Question Level")
        canvas = FigureCanvasTkAgg(fig, master=khung_4)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        tk.Button(khung_4, text="Phóng to", command=lambda: hien_thi_full_screen(fig)).pack(pady=10)

# ================================
# Phần 3: Bé Duy (Biểu đồ miền)
# ================================

# Vẽ biểu đồ miền
def ve_bieu_do_mien():
    for widget in khung_4.winfo_children():
        widget.destroy()
    if 'Topic' in du_lieu.columns:
        data = du_lieu['Topic'].value_counts()
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.fill_between(data.index, data.values, color="skyblue", alpha=0.4)
        ax.plot(data.index, data.values, color="Slateblue", alpha=0.6, linewidth=2)
        ax.set_title("Biểu đồ miền topic")
        ax.set_xlabel("Topic")
        ax.set_ylabel("Số lượng")
        ax.tick_params(axis='x', rotation=45)
        canvas = FigureCanvasTkAgg(fig, master=khung_4)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        tk.Button(khung_4, text="Phóng to", command=lambda: hien_thi_full_screen(fig)).pack(pady=10)

# Cập nhật dữ liệu được chọn
def cap_nhat_du_lieu():
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("Cảnh báo", "Chọn mục để cập nhật.")
        return
    updated_data = [entry.get() for entry in danh_sach_o_nhap]
    for item in selected_items:
        index = tree.index(item)
        du_lieu.iloc[index] = updated_data
    du_lieu.to_csv(FILE_NAME, sep=";", index=False, encoding="utf-8")
    hien_thi_du_lieu()


# Tạo giao diện ứng dụng
ung_dung = tk.Tk()
ung_dung.title("Quản lý dữ liệu với Đồ thị")
ung_dung.state('zoomed')

# Các khung giao diện
khung_1 = tk.Frame(ung_dung)
khung_1.grid(row=0, column=0, columnspan=3, sticky="nsew", pady=10)
khung_2 = tk.LabelFrame(ung_dung, text="Nhập dữ liệu", padx=10, pady=10)
khung_2.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
khung_4 = tk.LabelFrame(ung_dung, text="Đồ thị", padx=10, pady=10)
khung_4.grid(row=1, column=1, columnspan=2, sticky="nsew", padx=5, pady=5)
khung_3 = tk.Frame(ung_dung)
khung_3.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)



# ================================
# Phần 4: Bé Đức
# ================================



# Thêm khung tìm kiếm
khung_tim_kiem = tk.LabelFrame(ung_dung, text="Tìm kiếm dữ liệu", padx=10, pady=10)
# Thay vì dùng pack() dùng grid() như các khung khác
khung_tim_kiem.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

def tim_kiem_du_lieu_day_du():

    gia_tri_tim_kiem = [o_tim.get().strip() for o_tim in danh_sach_o_tim_kiem]

    # Kiểm tra nếu không nhập giá trị tìm kiếm nào
    if not any(gia_tri_tim_kiem):
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập ít nhất một giá trị để tìm kiếm!")
        return
    # Đọc dữ liệu từ CSV
    du_lieu = doc_du_lieu(FILE_NAME)

    # Lọc dữ liệu theo các giá trị tìm kiếm
    for i, gia_tri in enumerate(gia_tri_tim_kiem):
        if gia_tri:
            du_lieu = du_lieu[du_lieu[danh_sach_cot[i]].astype(str).str.contains(gia_tri, case=False, na=False)]

    # Xóa hết dữ liệu hiện tại trong Treeview
    for dong in tree.get_children():
        tree.delete(dong)

    # Thêm kết quả tìm kiếm vào Treeview
    for _, dong in du_lieu.iterrows():
        tree.insert("", "end", values=tuple(dong))

    # Nếu không có kết quả, hiển thị thông báo
    if du_lieu.empty:
        messagebox.showinfo("Kết quả", "Không tìm thấy kết quả nào phù hợp!")


# Khung tìm kiếm
khung_tim_kiem = tk.LabelFrame(ung_dung, text="Tìm kiếm dữ liệu", padx=10, pady=10)
khung_tim_kiem.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

danh_sach_o_tim_kiem = []
for i, cot in enumerate(danh_sach_cot):
    tk.Label(khung_tim_kiem, text=cot).grid(row=0, column=i, padx=5, pady=5)
    o_tim = tk.Entry(khung_tim_kiem, width=20)
    o_tim.grid(row=1, column=i, padx=5, pady=5)
    danh_sach_o_tim_kiem.append(o_tim)

tk.Button(khung_tim_kiem, text="Tìm kiếm", command=tim_kiem_du_lieu_day_du).grid(row=2, column=len(danh_sach_cot) - 1, padx=10)

# Nút điều khiển cho các chức năng
tk.Button(khung_1, text="Thêm", command=them_du_lieu).pack(side=tk.LEFT, padx=10)
tk.Button(khung_1, text="Cập nhật", command=cap_nhat_du_lieu).pack(side=tk.LEFT, padx=10)
tk.Button(khung_1, text="Xóa", command=xoa_du_lieu).pack(side=tk.LEFT, padx=10)

tk.Button(khung_1, text="Biểu đồ cột chồng", command=ve_do_thi_cot).pack(side=tk.LEFT, padx=10)
tk.Button(khung_1, text="Biểu đồ tròn", command=ve_bieu_do_tron).pack(side=tk.LEFT, padx=10)
tk.Button(khung_1, text="Biểu đồ miền", command=ve_bieu_do_mien).pack(side=tk.LEFT, padx=10)

# Các ô nhập liệu
danh_sach_o_nhap = []
for i, cot in enumerate(danh_sach_cot):
    tk.Label(khung_2, text=cot).grid(row=i, column=0, sticky=tk.W, pady=5)
    o_nhap = tk.Entry(khung_2, width=30)
    o_nhap.grid(row=i, column=1, pady=5, padx=5)
    danh_sach_o_nhap.append(o_nhap)

# Treeview để hiển thị dữ liệu
tree = ttk.Treeview(khung_3, columns=danh_sach_cot, show="headings", height=15)
for cot in danh_sach_cot:
    tree.heading(cot, text=cot)
    tree.column(cot, anchor=tk.W, width=120)
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
tree.bind("<<TreeviewSelect>>", tu_dong_do_du_lieu)

# Thanh cuộn ngang và dọc cho Treeview
thanh_cuon_d = tk.Scrollbar(khung_3, orient=tk.VERTICAL, command=tree.yview)
thanh_cuon_d.pack(side=tk.RIGHT, fill=tk.Y)
tree.configure(yscrollcommand=thanh_cuon_d.set)
thanh_cuon_ngang = tk.Scrollbar(khung_3, orient=tk.HORIZONTAL, command=tree.xview)
thanh_cuon_ngang.pack(side=tk.BOTTOM, fill=tk.X)
tree.configure(xscrollcommand=thanh_cuon_ngang.set)

# Khởi tạo dữ liệu ban đầu và hiển thị
hien_thi_du_lieu()

# Chạy ứng dụng
ung_dung.mainloop()
