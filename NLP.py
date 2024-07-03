import tkinter as tk
from tkinter import filedialog, Text, Scrollbar, messagebox
from PyPDF2 import PdfReader
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist

nltk.download('punkt')
nltk.download('stopwords')

def pdf_to_text(pdf_path):
    """
    Convert a PDF file to text.

    Args:
    pdf_path (str): The path to the PDF file to be converted.

    Returns:
    str: The extracted text from the PDF.
    """
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

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

        # Text field box for keywords input
        self.bottom_text_box = Text(self.bottom_frame, wrap='word', height=5)
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
        self.bottom_frame.pack_forget()
        self.clear_query_button.pack_forget()
        self.clear_text_button.pack_forget()
        self.main_menu.pack(pady=20, padx=20)
        self.root.title("KeyPoints Extractor")

    def show_help(self):
        help_text = (
            "PDF Text Analyzer Help:\n\n"
            "- Start Analyzer: Opens the PDF analyzer interface.\n"
            "- Upload PDF: Select a PDF file to analyze.\n"
            "- Delete PDF: Removes the uploaded PDF file.\n"
            "- Summarize Text: Provides a summary of the PDF content or entered text.\n"
            "- Highlight Text: Highlights important words in the PDF or entered text.\n"
            "- Find Key Points: Displays the most common words in the PDF or entered text."
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
        self.file_path = None
        self.preview_text.delete(1.0, tk.END)
        self.text_box.delete(1.0, tk.END)
        messagebox.showinfo("Success", "PDF file and input text deleted.")

    def extract_text(self):
        if self.file_path:
            return pdf_to_text(self.file_path)
        else:
            return self.preview_text.get("1.0", tk.END)

    def summarize_text(self):
        text = self.extract_text().strip()
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

    def highlight_keywords(self):
        keywords_str = self.bottom_text_box.get("1.0", "end-1c").strip()
        if not keywords_str:
            messagebox.showerror("Error", "Please enter keywords to highlight.")
            return

        keywords = [keyword.strip() for keyword in keywords_str.split(',') if keyword.strip()]
        if not keywords:
            messagebox.showerror("Error", "Please enter valid keywords to highlight.")
            return

        # Check right text field first
        text = self.text_box.get("1.0", tk.END).strip()
        if text:
            highlighted = self.highlight_text_in_box(text, keywords, self.text_box)
            if highlighted:
                return

        # If not found in the right text field, check the left text field
        text = self.preview_text.get("1.0", tk.END).strip()
        if text:
            self.text_box.delete(1.0, tk.END)  # Clear right text field
            self.text_box.insert(tk.END, text)  # Insert left field text into right field
            highlighted = self.highlight_text_in_box(text, keywords, self.text_box)
            if highlighted:
                return

        # If not found in either text field
        messagebox.showerror("Error", "The word(s) do not exist.")

    def highlight_text_in_box(self, text, keywords, text_box):
        """
        Highlight the keywords in the given text box.

        Args:
        text (str): The text to search in.
        keywords (list of str): The keywords to highlight.
        text_box (tk.Text): The text box to apply highlights.

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
        return found

    def find_keypoints(self):
        text = self.extract_text().strip()
        if text:
            words = nltk.word_tokenize(text.lower())
            words = [word for word in words if word.isalnum()]
            stop_words = set(stopwords.words('english'))
            words = [word for word in words if word not in stop_words]
            freq_dist = FreqDist(words)
            most_common_words = freq_dist.most_common(10)
            keypoints = ', '.join([word for word, _ in most_common_words])
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, keypoints)

    def clear_query(self):
        self.bottom_text_box.delete(1.0, tk.END)

    def clear_text(self):
        self.text_box.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFAnalyzer(root)
    root.mainloop()
