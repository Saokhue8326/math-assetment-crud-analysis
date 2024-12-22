from tkinter import Tk, Frame, Canvas, LabelFrame, Label, Entry, Button, Scrollbar, Toplevel, messagebox
from tkinter import ttk
from data_manager import COLUMN_NAMES, DataManager
from chart_utils import draw_stacked_bar_chart, draw_pie_chart, draw_area_chart, clear_chart_area
import matplotlib.pyplot as plt

class App:
    def __init__(self, master):
        self.master = master
        master.title("Data Management and Visualization")
        master.state("zoomed")

        self.data_manager = DataManager()
        self.ascending_order = {}
        self.create_widgets()
        self.display_data()

    def create_widgets(self):
        # Main frame
        self.main_frame = Frame(self.master)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # CRUD frame
        self.crud_frame = LabelFrame(self.main_frame, text="CRUD", padx=10, pady=10)
        self.crud_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Chart frame
        self.chart_frame = LabelFrame(self.main_frame, text="Charts", padx=10, pady=10)
        self.chart_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Table frame
        self.tree_frame = LabelFrame(self.main_frame, text="Table", padx=10, pady=10)
        self.tree_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        # Configure row and column weights
        self.main_frame.grid_rowconfigure(0, weight=10)
        self.main_frame.grid_rowconfigure(1, weight=0)
        self.main_frame.grid_columnconfigure(0, weight=0)
        self.main_frame.grid_columnconfigure(1, weight=10)

        # Input fields
        self.input_fields = []
        for _, column in enumerate(COLUMN_NAMES):
            field_frame = Frame(self.crud_frame)
            field_frame.pack(fill="x", pady=5)
            Label(field_frame, text=column).pack(side="left", padx=5)
            entry = Entry(field_frame, width=30)
            entry.pack(side="right", padx=5)
            self.input_fields.append(entry)

        # Control buttons (CRUD and Search)
        crud_input_frame = Frame(self.crud_frame)
        crud_input_frame.pack(fill="x", pady=10)
        Button(crud_input_frame, text="Search", command=self.search_data).pack(side="left", padx=5)
        Button(crud_input_frame, text="Add", command=self.add_data).pack(side="left", padx=5)
        Button(crud_input_frame, text="Update", command=self.update_data).pack(side="left", padx=5)
        Button(crud_input_frame, text="Delete", command=self.delete_data).pack(side="left", padx=5)
        Button(crud_input_frame, text="Refresh", command=self.display_data).pack(side="left", padx=5)

        # Chart buttons (Vertical layout, left alignment)
        chart_button_frame = Frame(self.chart_frame)
        chart_button_frame.pack(side="left", fill="y", padx=(0, 10))
        Button(chart_button_frame, text="Stacked Bar Chart", command=self.draw_stacked_bar_chart).pack(fill="x", pady=5)
        Button(chart_button_frame, text="Pie Chart", command=self.draw_pie_chart).pack(fill="x", pady=5)
        Button(chart_button_frame, text="Area Chart", command=self.draw_area_chart).pack(fill="x", pady=5)

        # Chart display area
        self.chart_display_frame = Frame(self.chart_frame)
        self.chart_display_frame.pack(side="right", fill="both", expand=True)

        # Treeview for data display
        self.tree = ttk.Treeview(self.tree_frame, columns=COLUMN_NAMES, show="headings", height=15)
        for column in COLUMN_NAMES:
            self.tree.heading(column, text=column, command=lambda c=column: self.sort_column(c))
            self.tree.column(column, anchor="w", width=120)
        self.tree.pack(side="left", fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.auto_fill_fields)

        # Scrollbars
        vertical_scrollbar = Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        vertical_scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=vertical_scrollbar.set)

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def display_data(self, sort_by="Student ID", ascending=True):
        self.data_manager.sort_data(sort_by, ascending)
        self.tree.delete(*self.tree.get_children())
        for _, row in self.data_manager.data.iterrows():
            self.tree.insert("", "end", values=list(row))
        for field in self.input_fields:
            field.delete(0, "end")

    def auto_fill_fields(self, events):
        selected_items = self.tree.selection()
        if selected_items:
            values = self.tree.item(selected_items[0], "values")
            for i, value in enumerate(values):
                self.input_fields[i].delete(0, "end")
                self.input_fields[i].insert(0, value)

    def add_data(self):
        new_data = [entry.get() for entry in self.input_fields]
        self.data_manager.add_data(new_data)
        self.display_data()

    def delete_data(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "Please select an item to delete.")
            return
        indices = [self.tree.index(item) for item in selected_items]
        self.data_manager.delete_data(indices)
        self.display_data()

    def update_data(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "Please select an item to update.")
            return
        updated_data = [field.get() for field in self.input_fields]
        for item in selected_items:
            index = self.tree.index(item)
            self.data_manager.update_data(index, updated_data)
        self.display_data()

    def search_data(self):
        search_values = [field.get().strip() for field in self.input_fields]
        if not any(search_values):
            messagebox.showwarning("Warning", "Please enter at least one value to search.")
            return
        filtered_data = self.data_manager.search_data(search_values)
        self.tree.delete(*self.tree.get_children())
        for _, row in filtered_data.iterrows():
            self.tree.insert("", "end", values=tuple(row))
        if filtered_data.empty:
            messagebox.showinfo("Result", "No matching results found.")

    def sort_column(self, col):
        self.ascending_order[col] = not self.ascending_order.get(col, True)
        self.display_data(sort_by=col, ascending=self.ascending_order[col])

    def draw_stacked_bar_chart(self):
        draw_stacked_bar_chart(self.data_manager.data, self.chart_display_frame)

    def draw_pie_chart(self):
        draw_pie_chart(self.data_manager.data, self.chart_display_frame)

    def draw_area_chart(self):
        draw_area_chart(self.data_manager.data, self.chart_display_frame)

    def on_closing(self):
        clear_chart_area(self.chart_display_frame)
        self.master.destroy()

if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()