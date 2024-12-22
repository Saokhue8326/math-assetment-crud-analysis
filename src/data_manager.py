import pandas as pd
import os
from tkinter import messagebox

COLUMN_NAMES = ["Student ID", "Student Country", "Question ID", "Type of Answer", "Question Level", "Topic", "Subtopic", "Keywords"]

class DataManager:
    def __init__(self, file_name="./dataset.csv"):
        self.file_name = file_name
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(self.file_name):
            try:
                return pd.read_csv(self.file_name, delimiter=";", encoding="utf-8")
            except Exception as e:
                messagebox.showerror("Error", f"Unable to read file: {e}")
                return pd.DataFrame(columns=COLUMN_NAMES)
        else:
            messagebox.showwarning("Warning", "File does not exist. Using default data.")
            return pd.DataFrame(columns=COLUMN_NAMES)

    def save_data(self):
        self.data.to_csv(self.file_name, sep=";", index=False, encoding="utf-8")

    def add_data(self, new_data):
        self.data.loc[len(self.data)] = new_data
        self.save_data()

    def delete_data(self, indices):
        self.data.drop(self.data.index[indices], inplace=True)
        self.save_data()

    def update_data(self, index, updated_data):
        self.data.iloc[index] = updated_data
        self.save_data()

    def search_data(self, search_values):
        filtered_data = self.data.copy()
        for i, value in enumerate(search_values):
            if value:
                filtered_data = filtered_data[filtered_data[COLUMN_NAMES[i]].astype(str).str.contains(value, case=False, na=False)]
        return filtered_data

    def sort_data(self, sort_by, ascending=True):
        if sort_by in self.data.columns:
            self.data.sort_values(by=sort_by, ascending=ascending, inplace=True)
        return self.data