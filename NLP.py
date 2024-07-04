import tkinter as tk
from tkinter import filedialog, messagebox, Text, Scrollbar
import threading
from PyPDF2 import PdfReader
from rake_nltk import Rake
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import nltk

nltk.download('punkt')
nltk.download('stopwords')

def extract_keywords(query):
    r = Rake()
    r.extract_keywords_from_text(query)
    keywords = r.get_ranked_phrases()
    return keywords

def modsummarize_text(text):
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    words = [word.lower() for word in words if word.isalnum()]
    freq_dist = FreqDist(words)
    stop_words = set(stopwords.words("english"))
    top_tokens = [word for word in freq_dist if word not in stop_words]

    # Find sentences containing the top tokens
    relevant_sentences = []
    for sentence in sentences:
        sentence_words = word_tokenize(sentence.lower())
        if any(word in sentence_words for word in top_tokens):
            relevant_sentences.append(sentence)
    
    return relevant_sentences[:5]  


def extract_related_passages(query, texts):
    keywords = extract_keywords(query)
    
    relevant_sentences = []
    for text in texts:
        sentences = sent_tokenize(text)
        for sentence in sentences:
            sentence_lower = sentence.lower()
            for keyword in keywords:
                if keyword in sentence_lower and sentence not in relevant_sentences:
                    relevant_sentences.append(sentence)
    
    return relevant_sentences


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

        self.highlight_button = tk.Button(self.button_frame, text="Highlight Text", command=self.highlight_keywords)
        self.highlight_button.pack(fill='x', pady=5)

        self.keypoints_button = tk.Button(self.button_frame, text="Find Key Points", command=self.find_keypoints)
        self.keypoints_button.pack(fill='x', pady=5)

        self.back_button = tk.Button(self.button_frame, text="Back to Main Menu", command=self.back_to_main_menu)
        self.back_button.pack(fill='x', pady=5)

        # Frame for user input and clear buttons
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(pady=10, padx=10, fill='x')

        # Label and Text field box for keywords input
        self.bottom_label = tk.Label(self.bottom_frame, text="Enter keywords (comma-separated):")
        self.bottom_label.pack(side=tk.LEFT, padx=5)
        self.bottom_text_box = Text(self.bottom_frame, wrap='word', height=1)
        self.bottom_text_box.pack(side=tk.LEFT, padx=5)

        # Clear button for bottom_text_box
        self.clear_query_button = tk.Button(self.bottom_frame, text="Clear Query", command=self.clear_query)
        self.clear_query_button.pack(side=tk.LEFT, padx=5)

        # Clear button for text_box
        self.clear_text_button = tk.Button(self.bottom_frame, text="Clear Text", command=self.clear_text)
        self.clear_text_button.pack(side=tk.LEFT, padx=5)

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
            "- Find Key Points: Displays the most relevant keywords in the PDF based on the entered query."
        )
        messagebox.showinfo("Help", help_text)

    def upload_pdf(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if self.file_path:
            self.preview_text.delete(1.0, tk.END)
            threading.Thread(target=self.load_pdf).start()

    def load_pdf(self):
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
        threading.Thread(target=self.run_summarize_text).start()

    def run_summarize_text(self):
        text = self.extract_text()
        if text:
            summary = modsummarize_text(text)
            print(summary)
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, summary)
        else:
            print("No text extracted.")  # Debugging print statement
            messagebox.showerror("Error", "Failed to extract text from PDF.")

    def highlight_keywords(self):
        keywords_str = self.bottom_text_box.get("1.0", "end-1c").strip()
        if not keywords_str:
            messagebox.showerror("Error", "Please enter keywords to highlight.")
            return

        keywords = [keyword.strip() for keyword in keywords_str.split(',') if keyword.strip()]
        if not keywords:
            messagebox.showerror("Error", "Please enter valid keywords to highlight.")
            return

        found_keywords = []
        not_found_keywords = []

        # Check right text field first
        text = self.text_box.get("1.0", tk.END).strip()
        if text:
            found_in_summary = self.highlight_text_in_box(text, keywords, self.text_box, found_keywords)
            if not found_in_summary:
                not_found_keywords.extend([keyword for keyword in keywords if keyword not in found_keywords])

        # If not found in the right text field, check the left text field
        if not found_keywords:
            text = self.preview_text.get("1.0", tk.END).strip()
            if text:
                self.text_box.delete(1.0, tk.END)  # Clear right text field
                self.text_box.insert(tk.END, text)  # Insert left field text into right field
                found_in_preview = self.highlight_text_in_box(text, keywords, self.text_box, found_keywords)
                if not found_in_preview:
                    not_found_keywords.extend([keyword for keyword in keywords if keyword not in found_keywords])

        # If no keywords were found
        if not found_keywords:
            messagebox.showinfo("Not Found", f"The word(s) '{', '.join(not_found_keywords)}' do not exist.")

    def highlight_text_in_box(self, text, keywords, text_box, found_keywords):
        """
        Highlight the keywords in the given text box.

        Args:
        text (str): The text to search in.
        keywords (list of str): The keywords to highlight.
        text_box (tk.Text): The text box to apply highlights.
        found_keywords (list of str): List to collect found keywords.

        Returns:
        bool: True if at least one keyword is highlighted, False otherwise.
        """
        found = False
        for keyword in keywords:
            start_pos = "1.0"
            while True:
                start_pos = text_box.search(keyword, start_pos, stopindex=tk.END, nocase=1)
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(keyword)}c"
                text_box.tag_add(keyword, start_pos, end_pos)
                text_box.tag_config(keyword, background="yellow")
                start_pos = end_pos
                found = True
                found_keywords.append(keyword)
        return found

    def find_keypoints(self):
        threading.Thread(target=self.run_find_keypoints).start()

    def run_find_keypoints(self):
        try:
            query = self.bottom_text_box.get("1.0", "end-1c").strip()
            if not query:
                raise ValueError("Query is empty. Please enter a valid query.")

            text = [f"""{self.extract_text()}"""]
            keywords = extract_related_passages(query, text)
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, ', '.join(keywords))
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def clear_query(self):
        self.bottom_text_box.delete(1.0, tk.END)

    def clear_text(self):
        self.text_box.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFAnalyzer(root)
    root.mainloop()
