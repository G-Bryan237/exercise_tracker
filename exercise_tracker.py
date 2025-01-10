import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os

class ExerciseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Exercise Tracking App")
        self.root.geometry("800x600")
        
        # Define exercise types and their default units
        self.exercise_types = {
            "Running": "km",
            "Cycling": "km",
            "Swimming": "km",
            "Push-ups": "rounds",
            "Pull-ups": "rounds",
            "Sit-ups": "rounds",
            "Squats": "rounds",
            "Custom": "rounds"
        }
        
        # Data storage
        self.exercise_records = []
        
        # Load data if the method exists
        self.load_data()
    
        # Create main container
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create frames
        self.create_input_frame()
        self.create_list_frame()
        self.create_action_buttons()
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(1, weight=1)

    def create_input_frame(self):
        # Input Frame
        input_frame = ttk.LabelFrame(self.main_frame, text="Add Exercise", padding="10")
        input_frame.grid(row=0, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        # Exercise Type Selection
        ttk.Label(input_frame, text="Exercise Type:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.exercise_type = ttk.Combobox(input_frame, values=list(self.exercise_types.keys()), width=20)
        self.exercise_type.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        self.exercise_type.bind('<<ComboboxSelected>>', self.on_exercise_type_change)
        
        # Custom Exercise Name Entry
        self.custom_name_label = ttk.Label(input_frame, text="Exercise Name:")
        self.custom_name_label.grid(row=0, column=2, padx=5, pady=5, sticky='w')
        self.custom_name = ttk.Entry(input_frame, width=20)
        self.custom_name.grid(row=0, column=3, padx=5, pady=5, sticky='w')
        
        # Initially hide custom name fields
        self.custom_name_label.grid_remove()
        self.custom_name.grid_remove()
        
        # Amount Entry
        self.amount_label = ttk.Label(input_frame, text="Amount:")
        self.amount_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.amount = ttk.Entry(input_frame, width=10)
        self.amount.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        
        # Unit Selection Frame
        unit_frame = ttk.LabelFrame(input_frame, text="Unit Selection", padding="5")
        unit_frame.grid(row=1, column=2, columnspan=2, padx=5, pady=5, sticky='w')
        
        self.unit_var = tk.StringVar(value="rounds")
        self.rounds_radio = ttk.Radiobutton(unit_frame, text="Rounds", variable=self.unit_var, value="rounds")
        self.rounds_radio.pack(side=tk.LEFT, padx=10)
        self.km_radio = ttk.Radiobutton(unit_frame, text="Kilometers", variable=self.unit_var, value="km")
        self.km_radio.pack(side=tk.LEFT, padx=10)
        
        # Duration Entry
        self.duration_label = ttk.Label(input_frame, text="Duration (minutes):")
        self.duration_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.duration = ttk.Entry(input_frame, width=10)
        self.duration.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        
        # Add Button
        self.add_button = ttk.Button(input_frame, text="Add Exercise", command=self.add_exercise)
        self.add_button.grid(row=3, column=0, columnspan=4, pady=10)

    def on_exercise_type_change(self, event=None):
        selected_type = self.exercise_type.get()
        
        # Show/hide custom name field
        if selected_type == "Custom":
            self.custom_name_label.grid()
            self.custom_name.grid()
        else:
            self.custom_name_label.grid_remove()
            self.custom_name.grid_remove()
            # Set the default unit for predefined exercises
            self.unit_var.set(self.exercise_types[selected_type])

    def add_exercise(self):
        try:
            # Get and validate exercise type
            exercise_type = self.exercise_type.get().strip()
            if not exercise_type:
                messagebox.showerror("Error", "Please select an exercise type")
                return

            # Get and validate amount
            amount_str = self.amount.get().strip()
            if not amount_str:
                messagebox.showerror("Error", "Please enter an amount")
                return
            amount = float(amount_str)

            # Get and validate duration (optional)
            duration_str = self.duration.get().strip()
            duration = float(duration_str) if duration_str else 0

            # Handle exercise name and unit
            if exercise_type == "Custom":
                exercise_name = self.custom_name.get().strip()
                if not exercise_name:
                    messagebox.showerror("Error", "Please enter a custom exercise name")
                    return
            else:
                exercise_name = exercise_type

            # Get the selected unit
            unit = self.unit_var.get()

            # Create record with consistent key names
            record = {
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Exercise Name": exercise_name,
                "Amount": amount,
                "Unit": unit,
                "Duration": duration
            }

            # Add record and update
            self.exercise_records.append(record)
            self.save_data()
            self.refresh_list()
            self.clear_inputs()

            # Show success message
            messagebox.showinfo("Success", "Exercise added successfully!")

        except ValueError as e:
            messagebox.showerror("Error", "Please enter valid numbers for amount and duration")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def create_list_frame(self):
        list_frame = ttk.LabelFrame(self.main_frame, text="Exercise Records", padding="10")
        list_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Treeview with consistent column names
        columns = ("Date", "Exercise Name", "Amount", "Unit", "Duration")  # Changed to match record keys
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Configure columns
        column_texts = {
            "Date": "Date",
            "Exercise Name": "Exercise Name",
            "Amount": "Amount",
            "Unit": "Unit",
            "Duration": "Duration (min)"
        }
        
        for col in columns:
            self.tree.heading(col, text=column_texts[col])
            self.tree.column(col, width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configure weights
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

    def create_action_buttons(self):
        actions_frame = ttk.Frame(self.main_frame, padding="10")
        actions_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        self.edit_button = ttk.Button(actions_frame, text="Edit Exercise", command=self.edit_exercise)
        self.edit_button.pack(side=tk.LEFT, padx=5)
        
        self.delete_button = ttk.Button(actions_frame, text="Delete Exercise", command=self.delete_exercise)
        self.delete_button.pack(side=tk.LEFT, padx=5)

    def edit_exercise(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an exercise to edit")
            return
            
        item = selected_item[0]
        index = self.tree.index(item)
        
        # Create edit dialog
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Exercise")
        edit_window.geometry("300x250")
        
        # Get current values
        current_values = self.exercise_records[index]
        
        # Create entry fields
        ttk.Label(edit_window, text="Exercise Name:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = ttk.Entry(edit_window)
        name_entry.insert(0, current_values["Exercise Name"])
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(edit_window, text="Amount:").grid(row=1, column=0, padx=5, pady=5)
        amount_entry = ttk.Entry(edit_window)
        amount_entry.insert(0, current_values["Amount"])
        amount_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(edit_window, text="Unit:").grid(row=2, column=0, padx=5, pady=5)
        unit_combobox = ttk.Combobox(edit_window, values=["rounds", "km"])
        unit_combobox.set(current_values["Unit"])
        unit_combobox.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(edit_window, text="Duration (minutes):").grid(row=3, column=0, padx=5, pady=5)
        duration_entry = ttk.Entry(edit_window)
        duration_entry.insert(0, current_values["Duration"])
        duration_entry.grid(row=3, column=1, padx=5, pady=5)
        
        def save_changes():
            try:
                new_name = name_entry.get().strip()
                new_amount = float(amount_entry.get().strip())
                new_unit = unit_combobox.get().strip()
                new_duration = float(duration_entry.get().strip())
                
                if not new_name:
                    messagebox.showerror("Error", "Please enter an exercise name")
                    return
                    
                self.exercise_records[index]["Exercise Name"] = new_name
                self.exercise_records[index]["Amount"] = new_amount
                self.exercise_records[index]["Unit"] = new_unit
                self.exercise_records[index]["Duration"] = new_duration
                self.save_data()
                self.refresh_list()
                edit_window.destroy()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for amount and duration")
        
        ttk.Button(edit_window, text="Save", command=save_changes).grid(row=4, column=0, columnspan=2, pady=20)

    def delete_exercise(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an exercise to delete")
            return
            
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this exercise?"):
            item = selected_item[0]
            index = self.tree.index(item)
            del self.exercise_records[index]
            self.save_data()
            self.refresh_list()

    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for record in self.exercise_records:
            # Use consistent key names when displaying records
            self.tree.insert("", tk.END, values=(
                record["Date"],
                record["Exercise Name"],  # Changed from "Exercise" to "Exercise Name"
                record["Amount"],
                record["Unit"],
                record["Duration"]
            ))

    def clear_inputs(self):
        self.exercise_type.set('')
        self.custom_name.delete(0, tk.END)
        self.amount.delete(0, tk.END)
        self.duration.delete(0, tk.END)
        self.unit_var.set("rounds")
        self.custom_name_label.grid_remove()
        self.custom_name.grid_remove()

    def load_data(self):
        try:
            if os.path.exists("exercise_data.json"):
                with open("exercise_data.json", "r") as file:
                    loaded_records = json.load(file)
                    # Convert old records to new format if necessary
                    self.exercise_records = []
                    for record in loaded_records:
                        if "Exercise" in record:  # Handle old format
                            record["Exercise Name"] = record.pop("Exercise")
                        self.exercise_records.append(record)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
            self.exercise_records = []

    def save_data(self):
        try:
            with open("exercise_data.json", "w") as file:
                json.dump(self.exercise_records, file)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")

def main():
    root = tk.Tk()
    app = ExerciseTracker(root)
    root.mainloop()

if __name__ == "__main__":
    main()
