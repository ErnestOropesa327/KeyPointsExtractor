import tkinter as tk
from tkinter import filedialog, messagebox, Text, Scrollbar
import fitz  # PyMuPDF
from PyPDF2 import PdfReader
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import os

nltk.download('punkt')
nltk.download('stopwords')

class PDFAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("KeyPoints Extractor")

        # Main menu
        self.main_menu = tk.Frame(root)
        self.main_menu.pack(pady=20, padx=20)

        # Header title
        self.header_label = tk.Label(self.main_menu, text="KeyPoints Extractor", font=("Arial", 16, "bold"))
        self.header_label.pack(pady=10)

        # Button frame for alignment
        self.button_frame = tk.Frame(self.main_menu)
        self.button_frame.pack()

        self.start_button = tk.Button(self.button_frame, text="Start Analyzer", command=self.start_analyzer, width=20)
        self.start_button.pack(pady=5)

        self.help_button = tk.Button(self.button_frame, text="Help", command=self.show_help, width=20)
        self.help_button.pack(pady=5)

        self.close_button = tk.Button(self.button_frame, text="Close Program", command=root.quit, width=20)
        self.close_button.pack(pady=5)

    def start_analyzer(self):
        self.main_menu.pack_forget()
        self.root.title("KeyPoints Extractor - Analyzer")

        # Frame for PDF preview and controls
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10, padx=10, fill='both', expand=True)

        # PDF preview on the left
        self.preview_text = Text(self.frame, wrap='word', height=20, width=40)
        self.preview_text.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        # Scrollbar for the preview
        self.scrollbar = Scrollbar(self.frame, command=self.preview_text.yview)
        self.scrollbar.grid(row=0, column=1, sticky='ns')
        self.preview_text.config(yscrollcommand=self.scrollbar.set)

        # Text box for output in the center
        self.text_box = Text(self.frame, wrap='word', height=20, width=60)
        self.text_box.grid(row=0, column=2, padx=5, pady=5, sticky='nsew')

        # Frame for buttons on the right
        self.button_frame = tk.Frame(self.frame)
        self.button_frame.grid(row=0, column=3, padx=5, pady=5, sticky='ns')

        # Buttons for functionalities
        self.upload_button = tk.Button(self.button_frame, text="Upload PDF", command=self.upload_pdf)
        self.upload_button.pack(fill='x', pady=5)

        self.delete_button = tk.Button(self.button_frame, text="Delete PDF", command=self.delete_pdf)
        self.delete_button.pack(fill='x', pady=5)

        self.summarize_button = tk.Button(self.button_frame, text="Summarize Text", command=self.summarize_text)
        self.summarize_button.pack(fill='x', pady=5)

        self.highlight_button = tk.Button(self.button_frame, text="Highlight Text", command=self.highlight_text)
        self.highlight_button.pack(fill='x', pady=5)

        self.keypoints_button = tk.Button(self.button_frame, text="Find Key Points", command=self.find_keypoints)
        self.keypoints_button.pack(fill='x', pady=5)

        self.back_button = tk.Button(self.button_frame, text="Back to Main Menu", command=self.back_to_main_menu)
        self.back_button.pack(fill='x', pady=5)

        # Text field box at the bottom
        self.bottom_text_box = Text(self.root, wrap='word', height=5)
        self.bottom_text_box.pack(pady=10, padx=10, fill='x')

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)

        self.file_path = None

    def back_to_main_menu(self):
        self.frame.pack_forget()
        self.bottom_text_box.pack_forget()
        self.main_menu.pack(pady=20, padx=20)
        self.root.title("KeyPoints Extractor")

    def show_help(self):
        help_text = (
            "PDF Text Analyzer Help:\n\n"
            "- Start Analyzer: Opens the PDF analyzer interface.\n"
            "- Upload PDF: Select a PDF file to analyze.\n"
            "- Delete PDF: Removes the uploaded PDF file from the GUI.\n"
            "- Summarize Text: Provides a summary of the PDF content.\n"
            "- Highlight Text: Highlights important words in the PDF.\n"
            "- Find Key Points: Displays the most common words in the PDF."
        )
        messagebox.showinfo("Help", help_text)

    def upload_pdf(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if self.file_path:
            self.preview_text.delete(1.0, tk.END)
            text = self.extract_text()
            if text:
                self.preview_text.insert(tk.END, text)

    def delete_pdf(self):
        if self.file_path:
            self.file_path = None
            self.preview_text.delete(1.0, tk.END)
            self.text_box.delete(1.0, tk.END)
            messagebox.showinfo("Success", "PDF file deleted.")
        else:
            print("No file to clear.")
            messagebox.showerror("Error", "No PDF file to delete.")

    def extract_text(self):
        if not self.file_path:
            messagebox.showerror("Error", "Please upload a PDF file first.")
            return None
        reader = PdfReader(self.file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

    def summarize_text(self):
        text = self.extract_text()
        if text:
            sentences = sent_tokenize(text)
            word_frequencies = FreqDist(nltk.word_tokenize(text.lower()))
            stop_words = set(stopwords.words('english'))
            sentence_scores = {}

            for sentence in sentences:
                for word in nltk.word_tokenize(sentence.lower()):
                    if word in word_frequencies and word not in stop_words:
                        if len(sentence.split(' ')) < 30:
                            if sentence not in sentence_scores:
                                sentence_scores[sentence] = word_frequencies[word]
                            else:
                                sentence_scores[sentence] += word_frequencies[word]

            summary_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:5]
            summary = ' '.join(summary_sentences)
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, summary)

    def highlight_text(self):
        text = self.extract_text()
        if text:
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, text)
            for word in set(nltk.word_tokenize(text.lower())):
                if word in stopwords.words('english'):
                    continue
                start_index = '1.0'
                while True:
                    start_index = self.text_box.search(word, start_index, stopindex=tk.END)
                    if not start_index:
                        break
                    end_index = f"{start_index}+{len(word)}c"
                    self.text_box.tag_add("highlight", start_index, end_index)
                    self.text_box.tag_config("highlight", background="yellow")
                    start_index = end_index

    def find_keypoints(self):
        text = self.extract_text()
        if text:
            words = nltk.word_tokenize(text.lower())
            filtered_words = [word for word in words if word.isalnum()]
            fdist = FreqDist(filtered_words)
            keypoints = fdist.most_common(10)
            self.text_box.delete(1.0, tk.END)
            for point in keypoints:
                self.text_box.insert(tk.END, f"{point[0]}: {point[1]}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFAnalyzer(root)
    root.mainloop()
