import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import pyttsx3
from PyPDF2 import PdfReader


def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    except Exception as e:
        messagebox.showerror("Error", f"Could not read PDF: {e}")
    return text


def browse_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        extracted_text = extract_text_from_pdf(file_path)
        text_display.delete('1.0', tk.END)
        text_display.insert(tk.END, extracted_text)
        app.extracted_text = extracted_text


def read_aloud():
    text = getattr(app, 'extracted_text', '')
    if not text.strip():
        messagebox.showwarning("Empty Text", "No text available to read.")
        return
    try:
        engine = pyttsx3.init()


        rate = rate_slider.get()
        engine.setProperty('rate', rate)

        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read aloud: {e}")


def close_app():
    app.destroy()


# GUI
app = tk.Tk()
app.title("PDF Text Reader")
app.geometry("1000x1000")

# PDF Upload
tk.Label(app, text="Select a PDF File:", font=("Futura", 20)).pack(pady=(10, 0))
tk.Button(app, text="Browse", command=browse_pdf, bg="#FF69B4").pack()

# Text Display
text_display = scrolledtext.ScrolledText(app, height=20, width=100, wrap=tk.WORD)
text_display.pack(pady=10)

# Speech Rate Control
tk.Label(app, text="Adjust Read Aloud Speed:", font=("Futura", 14)).pack()
rate_slider = tk.Scale(app, from_=100, to=300, orient=tk.HORIZONTAL)
rate_slider.set(150)  
rate_slider.pack(pady=5)

# Read Aloud Button
tk.Button(app, text="Read aloud", command=read_aloud, bg="#FF69B4").pack(pady=5)

# Close Button
tk.Button(app, text="Close", command=close_app, bg="#FF69B4").pack(pady=10)

# Handle window close (X button)
app.protocol("WM_DELETE_WINDOW", close_app)

app.mainloop()