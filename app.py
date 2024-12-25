from tkinter import Tk, Frame, Canvas, LabelFrame, Label, Entry, Button, Scrollbar, Toplevel, messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
import pandas as pd
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

FILE_NAME = "./data/dataset.csv"
COLUMN_NAMES = ["Student ID", "Student Country", "Question ID", "Type of Answer", "Question Level", "Topic", "Subtopic", "Keywords"]

# Global variable to store the current figure
current_figure = None

# Load data from CSV or return an empty DataFrame
def load_data(file_name):
    if os.path.exists(file_name):
        try:
            return pd.read_csv(file_name, delimiter=";", encoding="utf-8")
        except Exception as e:
            messagebox.showerror("Error", f"Unable to read file: {e}")
            return pd.DataFrame(columns=COLUMN_NAMES)
    else:
        messagebox.showwarning("Warning", "File does not exist. Using default data.")
        return pd.DataFrame(columns=COLUMN_NAMES)

# Display data in the Treeview
def display_data(sort_by="Student ID", ascending=True):
    global data
    data = load_data(FILE_NAME)
    if sort_by in data.columns:
        data.sort_values(by=sort_by, ascending=ascending, inplace=True)
    tree.delete(*tree.get_children())
    for _, row in data.iterrows():
        tree.insert("", "end", values=list(row))
    for field in input_fields:
        field.delete(0, "end")

# Auto-fill input fields when selecting a row
def auto_fill_fields(events):
    selected_items = tree.selection()
    if selected_items:
        values = tree.item(selected_items[0], "values")
        for i, value in enumerate(values):
            input_fields[i].delete(0, "end")
            input_fields[i].insert(0, value)

# Add new data to CSV
def add_data():
    new_data = [entry.get() for entry in input_fields]
    data.loc[len(data)] = new_data
    data.to_csv(FILE_NAME, sep=";", index=False, encoding="utf-8")
    display_data()

# Delete selected data
def delete_data():
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("Warning", "Please select an item to delete.")
        return
    for item in selected_items:
        index = tree.index(item)
        data.drop(data.index[index], inplace=True)
    data.to_csv(FILE_NAME, sep=";", index=False, encoding="utf-8")
    display_data()

# Update selected data
def update_data():
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("Warning", "Please select an item to update.")
        return
    updated_data = [field.get() for field in input_fields]
    for item in selected_items:
        index = tree.index(item)
        data.iloc[index] = updated_data
    data.to_csv(FILE_NAME, sep=";", index=False, encoding="utf-8")
    display_data()


# Search data (modified to work with combined input fields)
def search_data():
    search_values = [field.get().strip() for field in input_fields] # Use input_fields for search
    if not any(search_values):
        messagebox.showwarning("Warning", "Please enter at least one value to search.")
        return
    filtered_data = data.copy()
    for i, value in enumerate(search_values):
        if value:
            filtered_data = filtered_data[filtered_data[COLUMN_NAMES[i]].astype(str).str.contains(value, case=False, na=False)]
    tree.delete(*tree.get_children())
    for _, row in filtered_data.iterrows():
        tree.insert("", "end", values=tuple(row))
    if filtered_data.empty:
        messagebox.showinfo("Result", "No matching results found.")

# Sort data in the Treeview
def sort_column(col):
    global ascending_order
    ascending_order[col] = not ascending_order.get(col, True)
    display_data(sort_by=col, ascending=ascending_order[col])

# Draw a stacked bar chart
def draw_stacked_bar_chart():
    clear_chart_area()
    if {'Student Country', 'Type of Answer'}.issubset(data.columns):
        grouped = data.groupby(['Student Country', 'Type of Answer']).size().unstack(fill_value=0)
        fig, ax = plt.subplots(figsize=(8, 4)) # Increased height for better visualization
        grouped.plot(kind='bar', stacked=True, ax=ax, color=['red', 'green'])
        ax.set_title("Stacked Bar Chart: Student Country vs. Type of Answer")
        ax.set_xlabel("Student Country")
        ax.set_ylabel("Count")
        ax.legend(title="Type of Answer", labels=['Incorrect (0)', 'Correct (1)'])
        render_chart(fig)
    else:
        messagebox.showwarning("Warning", "Required columns ('Student Country', 'Type of Answer') not found for stacked bar chart.")
        return

# Draw a pie chart
def draw_pie_chart():
    clear_chart_area()
    if 'Question Level' in data.columns:
        value_counts = data['Question Level'].value_counts()
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(value_counts, labels=value_counts.index, autopct='%1.1f%%', startangle=90)
        ax.set_title("Pie Chart: Question Levels")
        render_chart(fig)
    else:
        messagebox.showwarning("Warning", "Required column ('Question Level') not found for pie chart.")
        return

def draw_area_chart():
    clear_chart_area()
    if 'Topic' in data.columns:
        value_counts = data['Topic'].value_counts()
        fig, ax = plt.subplots(figsize=(8, 4)) # Increased height for better visualization
        ax.fill_between(value_counts.index, value_counts.values, color="skyblue", alpha=0.4)
        ax.plot(value_counts.index, value_counts.values, color="Slateblue", alpha=0.6, linewidth=2)
        ax.set_title("Area Chart: Topics")
        ax.set_xlabel("Topic")
        ax.set_ylabel("Count")
        ax.tick_params(axis='x', rotation=45) # Rotate x-axis labels if needed
        render_chart(fig)
    else:
        messagebox.showwarning("Warning", "Required column ('Topic') not found for area chart.")
        return

# Modified render_chart to store the figure globally
def render_chart(fig):
    global current_figure
    clear_chart_area()
    current_figure = fig  # Store the figure
    canvas = FigureCanvasTkAgg(fig, master=chart_display_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="y", expand=True)
    canvas.get_tk_widget().bind("<Destroy>", lambda event: plt.close(fig)) # Key change

# Modified clear_chart_area to use the dedicated display frame
def clear_chart_area():
    global current_figure
    for widget in chart_display_frame.winfo_children():
        widget.destroy()
    if current_figure:
        plt.close(current_figure) # Close the figure when clearing
        current_figure = None



# Function to handle window closing
def on_closing():
    global current_figure
    if current_figure:
        plt.close(current_figure) # Close the figure before exiting
        current_figure = None
    app.destroy() # Important: Use app.destroy()

# Create the application interface
app = Tk()
app.title("Data Management and Visualization")
app.state("zoomed")

# Main frames
main_frame = Frame(app)
main_frame.grid(row=0, column=0, sticky="nsew")
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

crud_frame = LabelFrame(main_frame, text="CRUD", padx=10, pady=10)
crud_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

chart_frame = LabelFrame(main_frame, text="Charts", padx=10, pady=10)
chart_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

tree_frame = LabelFrame(main_frame, text="Table", padx=10, pady=10)
tree_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

# Configure row and column weights
main_frame.grid_rowconfigure(0, weight=10)
main_frame.grid_rowconfigure(1, weight=0)
main_frame.grid_columnconfigure(0, weight=0)
main_frame.grid_columnconfigure(1, weight=10)

# Input fields (now used for both CRUD and Search)
input_fields = []
for i, column in enumerate(COLUMN_NAMES):
    field_frame = Frame(crud_frame)
    field_frame.pack(fill="x", pady=5)
    Label(field_frame, text=column).pack(side="left", padx=5)
    entry = Entry(field_frame, width=30)
    entry.pack(side="right", padx=5)
    input_fields.append(entry)

# Control buttons (CRUD and Search in the same frame)
crud_input_frame = Frame(crud_frame)
crud_input_frame.pack(fill="x", pady=10)
Button(crud_input_frame, text="Search", command=search_data).pack(side="left", padx=5) #Search Button
Button(crud_input_frame, text="Add", command=add_data).pack(side="left", padx=5)
Button(crud_input_frame, text="Update", command=update_data).pack(side="left", padx=5)
Button(crud_input_frame, text="Delete", command=delete_data).pack(side="left", padx=5)
Button(crud_input_frame, text="Refresh", command=display_data).pack(side="left", padx=5) #Refresh Button

# Chart buttons (Vertical layout, left alignment)
chart_button_frame = Frame(chart_frame)
chart_button_frame.pack(side="left", fill="y", padx=(0,10)) # Stick to left, fill vertically, Add padding right
Button(chart_button_frame, text="Stacked Bar Chart", command=draw_stacked_bar_chart).pack(fill="x", pady=5)
Button(chart_button_frame, text="Pie Chart", command=draw_pie_chart).pack(fill="x", pady=5)
Button(chart_button_frame, text="Area Chart", command=draw_area_chart).pack(fill="x", pady=5)

# Chart display area (separate from buttons)
chart_display_frame = Frame(chart_frame)
chart_display_frame.pack(side="right", fill="both", expand=True) # Display chart to the right, expand to fill


# Treeview for data display
tree = ttk.Treeview(tree_frame, columns=COLUMN_NAMES, show="headings", height=15)
ascending_order = {}
for column in COLUMN_NAMES:
    tree.heading(column, text=column, command=lambda c=column: sort_column(c))
    tree.column(column, anchor="w", width=120)
tree.pack(side="left", fill="both", expand=True)
tree.bind("<<TreeviewSelect>>", auto_fill_fields)

# Scrollbars
vertical_scrollbar = Scrollbar(tree_frame, orient="vertical", command=tree.yview)
vertical_scrollbar.pack(side="right", fill="y")
tree.configure(yscrollcommand=vertical_scrollbar.set)



# Protocol handler for window closing
app.protocol("WM_DELETE_WINDOW", on_closing) # Key change

# Initialize data
data = pd.DataFrame()
display_data()

# Run the application
app.mainloop()
