import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox

def draw_stacked_bar_chart(data, chart_display_frame):
    if {'Student Country', 'Type of Answer'}.issubset(data.columns):
        grouped = data.groupby(['Student Country', 'Type of Answer']).size().unstack(fill_value=0)
        fig, ax = plt.subplots(figsize=(8, 4))
        grouped.plot(kind='bar', stacked=True, ax=ax, color=['red', 'green'])
        ax.set_title("Stacked Bar Chart: Student Country vs. Type of Answer")
        ax.set_xlabel("Student Country")
        ax.set_ylabel("Count")
        ax.legend(title="Type of Answer", labels=['Incorrect (0)', 'Correct (1)'])
        render_chart(fig, chart_display_frame)
    else:
        messagebox.showwarning("Warning", "Required columns ('Student Country', 'Type of Answer') not found for stacked bar chart.")

def draw_pie_chart(data, chart_display_frame):
    if 'Question Level' in data.columns:
        value_counts = data['Question Level'].value_counts()
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(value_counts, labels=value_counts.index, autopct='%1.1f%%', startangle=90)
        ax.set_title("Pie Chart: Question Levels")
        render_chart(fig, chart_display_frame)
    else:
        messagebox.showwarning("Warning", "Required column ('Question Level') not found for pie chart.")

def draw_area_chart(data, chart_display_frame):
    if 'Topic' in data.columns:
        value_counts = data['Topic'].value_counts()
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.fill_between(value_counts.index, value_counts.values, color="skyblue", alpha=0.4)
        ax.plot(value_counts.index, value_counts.values, color="Slateblue", alpha=0.6, linewidth=2)
        ax.set_title("Area Chart: Topics")
        ax.set_xlabel("Topic")
        ax.set_ylabel("Count")
        ax.tick_params(axis='x', rotation=45)
        render_chart(fig, chart_display_frame)
    else:
        messagebox.showwarning("Warning", "Required column ('Topic') not found for area chart.")

def render_chart(fig, chart_display_frame):
    clear_chart_area(chart_display_frame)
    canvas = FigureCanvasTkAgg(fig, master=chart_display_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="y", expand=True)
    canvas.get_tk_widget().bind("<Destroy>", lambda event: plt.close(fig))

def clear_chart_area(chart_display_frame):
    for widget in chart_display_frame.winfo_children():
        widget.destroy()