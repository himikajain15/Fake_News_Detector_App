import tkinter as tk
from tkinter import messagebox
import sqlite3
import nltk
from transformers import pipeline
from preprocess_data import preprocess_text

# Ensure necessary NLTK data is downloaded
nltk.download("punkt")
nltk.download("stopwords")

# Load the BERT model
bert_classifier = pipeline("text-classification", model="s-nlp/roberta_fake_news")



# Connect to SQLite database
conn = sqlite3.connect("fake_news.db")
cursor = conn.cursor()

# Ensure the "news" table exists with correct columns
cursor.execute("""
    CREATE TABLE IF NOT EXISTS news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        url TEXT,
        prediction TEXT
    )
""")
conn.commit()

# Function to check news credibility
def check_news():
    title = title_entry.get()
    article_url = url_entry.get()
    content = news_text.get("1.0", tk.END).strip()

    if not content:
        messagebox.showerror("Error", "Please enter news content.")
        return

    # Preprocess text
    processed_text = preprocess_text(content)
    
    # 🔹 Limit text to first 512 characters for BERT compatibility
    processed_text = processed_text[:512]  

    # Predict using BERT
    try:
        prediction = bert_classifier(processed_text, truncation=True)[0]['label']
    except Exception as e:
        messagebox.showerror("Error", f"Prediction failed: {str(e)}")
        return

    # Insert into database
    cursor.execute("INSERT INTO news (title, url, prediction) VALUES (?, ?, ?)", 
                   (title, article_url, prediction))
    conn.commit()

    # Show result
    messagebox.showinfo("Result", f"Prediction: {prediction}")

# GUI Setup
root = tk.Tk()
root.title("Fake News Detector")

# Title input
tk.Label(root, text="Title:").pack()
title_entry = tk.Entry(root, width=50)
title_entry.pack()

# URL input
tk.Label(root, text="Article URL:").pack()
url_entry = tk.Entry(root, width=50)
url_entry.pack()

# News content input
tk.Label(root, text="Enter News Content:").pack()
news_text = tk.Text(root, height=10, width=60)
news_text.pack()

# Button to check news
check_button = tk.Button(root, text="Check News", command=check_news)
check_button.pack()

# Run GUI
root.mainloop()

# Close database connection when the app closes
conn.close()
