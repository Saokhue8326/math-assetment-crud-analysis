import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox

def draw_stacked_bar_chart(data, chart_display_frame):
    """
    Vẽ biểu đồ hình cột xếp chồng thể hiện số câu trả lời đúng/sai theo quốc gia của học sinh.

    Tham số:
        data (pandas.DataFrame): Dữ liệu chứa các thông tin như Quốc gia học sinh, Loại câu trả lời.
        chart_display_frame (tkinter.Frame): Khung giao diện để hiển thị biểu đồ.

    Điều kiện:
        - Dữ liệu phải có các cột "Student Country" và "Type of Answer".

    Hiển thị thông báo cảnh báo nếu các cột cần thiết không được tìm thấy.
    """
    if {'Student Country', 'Type of Answer'}.issubset(data.columns):
        grouped = data.groupby(['Student Country', 'Type of Answer']).size().unstack(fill_value=0)
        fig, ax = plt.subplots(figsize=(8, 4))
        grouped.plot(kind='bar', stacked=True, ax=ax, color=['red', 'green'])
        ax.set_title("Biểu đồ hình cột xếp chồng: Quốc gia học sinh vs. Loại câu trả lời")
        ax.set_xlabel("Quốc gia học sinh")
        ax.set_ylabel("Số lượng")
        ax.legend(title="Loại câu trả lời", labels=['Sai (0)', 'Đúng (1)'])
        render_chart(fig, chart_display_frame)
    else:
        messagebox.showwarning("Cảnh báo", "Không tìm thấy các cột cần thiết ('Student Country', 'Type of Answer') để vẽ biểu đồ hình cột xếp chồng.")

def draw_pie_chart(data, chart_display_frame):
    """
    Vẽ biểu đồ hình tròn thể hiện số lượng câu hỏi theo cấp độ.

    Tham số:
        data (pandas.DataFrame): Dữ liệu chứa các thông tin như Cấp độ câu hỏi.
        chart_display_frame (tkinter.Frame): Khung giao diện để hiển thị biểu đồ.

    Điều kiện:
        - Dữ liệu phải có cột "Question Level".

    Hiển thị thông báo cảnh báo nếu cột cần thiết không được tìm thấy.
    """
    if 'Question Level' in data.columns:
        value_counts = data['Question Level'].value_counts()
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(value_counts, labels=value_counts.index, autopct='%1.1f%%', startangle=90)
        ax.set_title("Biểu đồ hình tròn: Cấp độ câu hỏi")
        render_chart(fig, chart_display_frame)
    else:
        messagebox.showwarning("Cảnh báo", "Không tìm thấy cột cần thiết ('Question Level') để vẽ biểu đồ hình tròn.")

def draw_area_chart(data, chart_display_frame):
    """
    Vẽ biểu đồ diện tích thể hiện số lượng câu hỏi theo chủ đề.

    Tham số:
        data (pandas.DataFrame): Dữ liệu chứa các thông tin như Chủ đề.
        chart_display_frame (tkinter.Frame): Khung giao diện để hiển thị biểu đồ.

    Điều kiện:
        - Dữ liệu phải có cột "Topic".

    Hiển thị thông báo cảnh báo nếu cột cần thiết không được tìm thấy.
    """
    if 'Topic' in data.columns:
        value_counts = data['Topic'].value_counts()
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.fill_between(value_counts.index, value_counts.values, color="skyblue", alpha=0.4)
        ax.plot(value_counts.index, value_counts.values, color="Slateblue", alpha=0.6, linewidth=2)
        ax.set_title("Biểu đồ diện tích: Chủ đề câu hỏi")
        ax.set_xlabel("Chủ đề")
        ax.set_ylabel("Số lượng")
        ax.tick_params(axis='x', rotation=45)
        render_chart(fig, chart_display_frame)
    else:
        messagebox.showwarning("Cảnh báo", "Không tìm thấy cột cần thiết ('Topic') để vẽ biểu đồ diện tích.")

def render_chart(fig, chart_display_frame):
    """
    Hiển thị biểu đồ matplotlib trong khung giao diện Tkinter.

    Xóa nội dung hiện có trong khung hiển thị biểu đồ trước khi vẽ biểu đồ mới.

    Tham số:
        fig (matplotlib.figure.Figure): Đối tượng biểu đồ matplotlib cần hiển thị.
        chart_display_frame (tkinter.Frame): Khung giao diện để hiển thị biểu đồ.
    """
    clear_chart_area(chart_display_frame)
    canvas = FigureCanvasTkAgg(fig, master=chart_display_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="y", expand=True)
    canvas.get_tk_widget().bind("<Destroy>", lambda event: plt.close(fig))

def clear_chart_area(chart_display_frame):
    """
    Xóa tất cả các widget con khỏi khung hiển thị biểu đồ.

    Sử dụng để làm sạch khung trước khi vẽ biểu đồ mới, tránh chồng chéo.

    Tham số:
        chart_display_frame (tkinter.Frame): Khung giao diện cần được làm sạch.
    """
    for widget in chart_display_frame.winfo_children():
        widget.destroy()