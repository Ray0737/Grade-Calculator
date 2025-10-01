import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

# --- Data Structure for Subjects and Scores ---
# A simple list of dictionaries to hold our subject data
subjects_data = []

# --- Core Calculation Function ---
def calculate_final_score(score_obtained, total_items):
    """
    Calculates the final exam score normalized to a 40% weight.
    Formula: (Score Obtained / Total Items) * 40
    """
    try:
        score = float(score_obtained)
        total = float(total_items)
        if total <= 0:
            return 0.0
        
        final_score_40 = (score / total) * 40
        return round(final_score_40, 2)
    except ValueError:
        return 0.0

# --- GUI Update & Interaction Functions ---

def update_treeview():
    """Clears and repopulates the subject score table."""
    for item in tree.get_children():
        tree.delete(item)

    for subj in subjects_data:
        # Calculate total weighted score
        total_score = subj['pre_score'] + subj['final_score_40']
        
        # Display Final Exam details as: Raw Score/Total Items (Weighted Score out of 40)
        final_display = f"{subj['final_score']}/{subj['final_total']} ({subj['final_score_40']:.2f})"
        
        tree.insert('', tk.END, values=(
            subj['name'],
            subj['credit'],
            f"{subj['pre_score']:.2f}", # Display Pre Score out of 60
            final_display,
            f"{total_score:.2f}" # Display Total Score out of 100
        ))

# --- NEW FUNCTION FOR EDITING INITIAL DATA ---
def open_initial_data_editor(subject_name, current_credit, current_pre_score):
    """
    Opens a pop-up window to edit the initial subject data (Name, Credit, Pre Score out of 60).
    """
    editor = tk.Toplevel(root)
    editor.title(f"Edit Subject: {subject_name}")
    editor.geometry("500x200")
    editor.transient(root) # Keep it on top of the main window
    editor.grab_set() # Makes it a modal window

    main_frame = ttk.Frame(editor, padding="10")
    main_frame.pack(fill='both', expand=True)

    # 1. Subject Name
    ttk.Label(main_frame, text="Subject Name:").grid(row=0, column=0, padx=5, pady=10, sticky='w')
    name_var = tk.StringVar(value=str(subject_name))
    name_entry = ttk.Entry(main_frame, textvariable=name_var, width=30)
    name_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

    # 2. Credit
    ttk.Label(main_frame, text="Credit:").grid(row=1, column=0, padx=5, pady=10, sticky='w')
    credit_var = tk.StringVar(value=str(current_credit))
    credit_entry = ttk.Entry(main_frame, textvariable=credit_var, width=15)
    credit_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

    # 3. Pre Score (60%)
    ttk.Label(main_frame, text="Pre Score (0-60):").grid(row=2, column=0, padx=5, pady=10, sticky='w')
    pre_score_var = tk.StringVar(value=str(current_pre_score))
    pre_score_entry = ttk.Entry(main_frame, textvariable=pre_score_var, width=15)
    pre_score_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

    def save_initial_data():
        new_name = name_var.get().strip()
        new_credit_str = credit_var.get().strip()
        new_pre_score_str = pre_score_var.get().strip()
        
        # Validation checks
        if not new_name:
            messagebox.showerror("Input Error", "Subject Name cannot be empty.")
            return

        try:
            new_credit = float(new_credit_str)
            new_pre_score = float(new_pre_score_str)

            if not (0 <= new_pre_score <= 60):
                messagebox.showerror("Input Error", "Pre Score must be between 0 and 60.")
                return
        except ValueError:
            messagebox.showerror("Input Error", "Credit and Pre Score must be valid numbers.")
            return
            
        # Check for duplicate name, but allow the current subject to keep its name if unchanged
        if new_name != subject_name and any(subj['name'] == new_name for subj in subjects_data):
            messagebox.showwarning("Duplicate", f"Subject '{new_name}' already exists.")
            return
            
        # Find the subject and update its data
        for subj in subjects_data:
            if subj['name'] == subject_name:
                subj['name'] = new_name
                subj['credit'] = new_credit
                subj['pre_score'] = new_pre_score
                break
        
        update_treeview()
        editor.destroy()
            
    # Save Button
    save_button = ttk.Button(main_frame, text="Save Changes", command=save_initial_data)
    save_button.grid(row=3, column=0, columnspan=2, pady=15)
    
    name_entry.focus_set()

def edit_initial_data_handler():
    """Handles the 'Edit Subject Data (60%)' button click."""
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showinfo("Selection", "Please select a subject to edit its initial data (Name, Credit, Pre Score).")
        return

    # Get values from the selected row
    item_values = tree.item(selected_item, 'values')
    subject_name = item_values[0] # Subject Name is the first column

    # Find the full subject data from our list
    selected_subj = next((subj for subj in subjects_data if subj['name'] == subject_name), None)

    if selected_subj:
        # Open the initial data editor
        open_initial_data_editor(
            selected_subj['name'],
            selected_subj.get('credit', 0),
            selected_subj.get('pre_score', 0.0)
        )
    else:
        messagebox.showerror("Error", "Subject data not found.")
# --- END NEW FUNCTIONS ---

def open_final_exam_editor(subject_name, current_score, current_total):
    """
    Opens a pop-up window (sub-menu) to input raw final exam scores (score/total items) 
    and calculates the weighted 40% score.
    """
    editor = tk.Toplevel(root)
    editor.title(f"Edit Final Exam: {subject_name}")
    editor.geometry("500x200")
    editor.transient(root) # Keep it on top of the main window
    editor.grab_set() # Makes it a modal window

    main_frame = ttk.Frame(editor, padding="10")
    main_frame.pack(fill='both', expand=True)

    ttk.Label(main_frame, text=f"Subject: {subject_name}", font=('Arial', 11, 'bold')).grid(row=0, column=0,sticky='nw')
    ttk.Label(main_frame, text="40% Calculation Input", font=('Arial', 10, 'italic')).grid(row=1, column=0,sticky='nw')

    # Input for Score Obtained
    ttk.Label(main_frame, text="Score Obtained:").grid(row=2, column=0, padx=5, pady=20, sticky='nw')
    score_var = tk.StringVar(value=str(current_score))
    score_entry = ttk.Entry(main_frame, textvariable=score_var, width=15)
    score_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

    # Input for Total Items
    ttk.Label(main_frame, text="Total Items:").grid(row=4, column=0, padx=5, pady=10, sticky='nw')
    total_var = tk.StringVar(value=str(current_total))
    total_entry = ttk.Entry(main_frame, textvariable=total_var, width=15)
    total_entry.grid(row=4, column=1, padx=5, pady=5, sticky='w')

    def save_and_calculate():
        new_score_str = score_var.get()
        new_total_str = total_var.get()
        
        try:
            new_score = float(new_score_str)
            new_total = float(new_total_str)
            
            if new_score < 0 or new_total <= 0 or new_score > new_total:
                messagebox.showerror("Input Error", "Please ensure scores are valid: Score >= 0, Total > 0, Score <= Total.")
                return

            # Perform the calculation
            calculated_40 = calculate_final_score(new_score, new_total)

            # Find the subject and update its data
            for subj in subjects_data:
                if subj['name'] == subject_name:
                    subj['final_score'] = new_score
                    subj['final_total'] = new_total
                    subj['final_score_40'] = calculated_40
                    break
            
            update_treeview()
            editor.destroy()

        except ValueError:
            messagebox.showerror("Input Error", "Score and Total Items must be valid numbers.")
            
    # Calculate & Save Button
    save_button = ttk.Button(main_frame, text="Calculate & Save (Update 40%)", command=save_and_calculate)
    save_button.grid(row=5, column=0, columnspan=2, pady=10)
    
    score_entry.focus_set()

def add_subject():
    """Adds a new subject using the input fields."""
    name = subject_entry.get().strip()
    credit_str = credit_entry.get().strip()
    pre_score_str = pre_score_entry.get().strip()

    if not name or not credit_str or not pre_score_str:
        messagebox.showwarning("Missing Info", "Please enter Subject Name, Credit, and Pre Score (60%).")
        return

    try:
        credit = float(credit_str)
        pre_score = float(pre_score_str)

        if not (0 <= pre_score <= 60):
             messagebox.showwarning("Score Error", "Pre Score must be between 0 and 60.")
             return
             
    except ValueError:
        messagebox.showerror("Input Error", "Credit and Pre Score must be numbers.")
        return

    # Check for duplicate subject name
    if any(subj['name'] == name for subj in subjects_data):
        messagebox.showwarning("Duplicate", f"Subject '{name}' already exists.")
        return

    new_subject = {
        'name': name,
        'credit': credit,
        'pre_score': pre_score,  # Out of 60
        'final_score': 0,  # Raw score obtained (e.g., 13)
        'final_total': 0,  # Raw total items (e.g., 25)
        'final_score_40': 0.0  # Weighted score out of 40 (calculated)
    }
    
    subjects_data.append(new_subject)
    update_treeview()

    # Clear input fields
    subject_entry.delete(0, tk.END)
    credit_entry.delete(0, tk.END)
    pre_score_entry.delete(0, tk.END)

def edit_subject_handler():
    """Handles the 'Edit Final Exam' button click or double-click on the table."""
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showinfo("Selection", "Please select a subject to edit its Final Exam score.")
        return

    # Get values from the selected row
    item_values = tree.item(selected_item, 'values')
    subject_name = item_values[0] # Subject Name is the first column

    # Find the full subject data from our list
    selected_subj = next((subj for subj in subjects_data if subj['name'] == subject_name), None)

    if selected_subj:
        # Open the specific final exam editor for this subject
        open_final_exam_editor(
            selected_subj['name'],
            selected_subj.get('final_score', 0),
            selected_subj.get('final_total', 0)
        )
    else:
        messagebox.showerror("Error", "Subject data not found.")

def delete_subject():
    """Deletes the selected subject."""
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showinfo("Selection", "Please select a subject to remove.")
        return
    
    subject_name = tree.item(selected_item, 'values')[0]
    
    if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{subject_name}' and all its scores?"):
        global subjects_data
        # Filter out the subject to be deleted
        subjects_data = [subj for subj in subjects_data if subj['name'] != subject_name]
        update_treeview()

# --- Main Application Setup (Dashboard) ---

def dashboard():
    global root, tree, subject_entry, credit_entry, pre_score_entry

    root = tk.Tk()
    root.title("Minimal Grade 4 Planner 📚")
    # Increased width to accommodate the new button
    root.geometry("1050x650") 

    # Menu (Minimal)
    myMenu = tk.Menu(root)
    root.config(menu=myMenu)
    file_menu = tk.Menu(myMenu, tearoff=0)
    myMenu.add_cascade(label="📁 File", menu=file_menu)
    # Note: Save functionality is omitted for simplicity but can be added here
    file_menu.add_command(label="✂️ Exit", command=root.destroy)
    
    # --- Input Frame for Adding Subjects (Replaced the complex original input_frame) ---
    input_frame = ttk.LabelFrame(root, text="New Subject Input", padding="10 10")
    input_frame.pack(fill="x", padx=20, pady=10)
    
    # Input Widgets
    ttk.Label(input_frame, text="Subject Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    subject_entry = ttk.Entry(input_frame, width=25)
    subject_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
    
    ttk.Label(input_frame, text="Credit:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
    credit_entry = ttk.Entry(input_frame, width=10)
    credit_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")
    
    ttk.Label(input_frame, text="Pre Score (out of 60):").grid(row=0, column=4, padx=5, pady=5, sticky="e")
    pre_score_entry = ttk.Entry(input_frame, width=10)
    pre_score_entry.grid(row=0, column=5, padx=5, pady=5, sticky="w")
    
    # Action Buttons (UPDATED TO INCLUDE NEW EDIT BUTTON)
    add_button = ttk.Button(input_frame, text="➕ Add Subject", command=add_subject)
    add_button.grid(row=1, column=0, columnspan=1, padx=5, pady=10, sticky="ew")

    # NEW EDIT INITIAL DATA BUTTON
    edit_data_button = ttk.Button(input_frame, text="📝 Edit Subject Data (60%)", command=edit_initial_data_handler)
    edit_data_button.grid(row=1, column=1, columnspan=1, padx=5, pady=10, sticky="ew")

    edit_final_button = ttk.Button(input_frame, text="✏️ Edit Final Exam (40%)", command=edit_subject_handler)
    edit_final_button.grid(row=1, column=2, columnspan=1, padx=5, pady=10, sticky="ew")
    
    delete_button = ttk.Button(input_frame, text="➖ Remove Subject", command=delete_subject)
    delete_button.grid(row=1, column=3, columnspan=1, padx=5, pady=10, sticky="ew")
    
    # --- Subject/Score Table (Treeview) ---
    table_frame = ttk.LabelFrame(root, text="Subject Scores (60% Pre + 40% Final)", padding="10 10")
    table_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    # Define columns
    columns = ("Subject", "Credit", "PreScore_60", "FinalScore_40", "TotalScore")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")
    
    # Configure headings for clarity
    tree.heading("Subject", text="Subject")
    tree.heading("Credit", text="Credit")
    tree.heading("PreScore_60", text="Pre Score (60%)")
    tree.heading("FinalScore_40", text="Final Exam (40% Details)")
    tree.heading("TotalScore", text="Total Score (100%)")

    # Configure column widths and alignment
    tree.column("Subject", width=200, anchor=tk.W)
    tree.column("Credit", width=80, anchor=tk.CENTER)
    tree.column("PreScore_60", width=120, anchor=tk.CENTER)
    tree.column("FinalScore_40", width=250, anchor=tk.CENTER) # Wider to show raw score/total + weighted score
    tree.column("TotalScore", width=120, anchor=tk.CENTER)

    # Scrollbar
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    # Pack Treeview and Scrollbar
    scrollbar.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)
    
    # Bind double-click to quickly edit the final exam score (unchanged)
    tree.bind('<Double-1>', lambda e: edit_subject_handler())

    update_treeview()
    
    root.mainloop()

if __name__ == '__main__':
    dashboard()