import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd

# Function to read the dataset and preprocess it
def load_dataset(file_path):
    try:
        # Read the dataset
        data = pd.read_csv(file_path)

        # Ensure required columns are present
        if 'listed_in' not in data.columns or 'title' not in data.columns:
            raise ValueError("Dataset must contain 'listed_in' and 'title' columns.")

        # Explode the 'listed_in' column into separate genres for easier filtering
        data['listed_in'] = data['listed_in'].str.split(', ')
        data = data.explode('listed_in')

        return data
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load dataset: {e}")
        return None

# Function to filter and display movies based on genre
def recommend_movies():
    genre = genre_var.get()
    if not genre:
        messagebox.showwarning("Input Required", "Please enter a genre.")
        return

    filtered_movies = movie_data[movie_data['listed_in'].str.contains(genre, case=False, na=False)]
    if filtered_movies.empty:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "No movies found for the selected genre.")
    else:
        sorted_movies = filtered_movies['title'].sort_values().tolist()
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "\n".join(sorted_movies))

# Function to select dataset file
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        global movie_data
        movie_data = load_dataset(file_path)
        if movie_data is not None:
            messagebox.showinfo("Success", "Dataset loaded successfully!")

# Create the GUI window
root = tk.Tk()
root.title("Movie Recommendation System")
root.geometry("600x400")

# Variables
genre_var = tk.StringVar()
movie_data = None

# GUI Layout
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky="NSEW")

# File selection button
file_button = ttk.Button(frame, text="Select Dataset", command=select_file)
file_button.grid(row=0, column=0, pady=10, sticky="W")

# Input field for genre
genre_label = ttk.Label(frame, text="Enter Genre:")
genre_label.grid(row=1, column=0, pady=10, sticky="W")

genre_entry = ttk.Entry(frame, textvariable=genre_var, width=30)
genre_entry.grid(row=1, column=1, pady=10, sticky="W")

# Recommend button
recommend_button = ttk.Button(frame, text="Recommend Movies", command=recommend_movies)
recommend_button.grid(row=2, column=0, columnspan=2, pady=10)

# Scrollable results display
result_frame = ttk.Frame(frame)
result_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky="NSEW")

result_text = tk.Text(result_frame, wrap=tk.WORD, height=15, width=50)
result_text.grid(row=0, column=0, sticky="NSEW")

scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=result_text.yview)
scrollbar.grid(row=0, column=1, sticky="NS")

result_text.config(yscrollcommand=scrollbar.set)

# Run the GUI main loop
root.mainloop()