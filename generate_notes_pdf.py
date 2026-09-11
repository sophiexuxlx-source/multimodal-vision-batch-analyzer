import os
from fpdf import FPDF

class PDFNotes(FPDF):
    def header(self):
        self.set_font("helvetica", "B", 14)
        self.set_text_color(44, 62, 80)
        self.cell(0, 10, "Project 4: Multimodal Image Content Analysis - Study Notes", border=False, new_x="LMARGIN", new_y="NEXT", align="C")
        self.set_draw_color(52, 152, 219)
        self.set_line_width(0.8)
        self.line(10, 18, 200, 18)
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 9)
        self.set_text_color(127, 140, 141)
        self.cell(0, 10, f"Page {self.page_no()} / {{nb}}", align="C")

def create_pdf(output_pdf_path: str = "PROJECT_4_STUDY_NOTES.pdf"):
    pdf = PDFNotes()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Section 1: Core AI & Web Concepts
    pdf.set_font("helvetica", "B", 13)
    pdf.set_text_color(41, 128, 185)
    pdf.cell(0, 8, "1. Core AI & Web Concepts", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    # Sub: Data Modality & Multimodal AI
    pdf.set_font("helvetica", "B", 11)
    pdf.set_text_color(52, 73, 94)
    pdf.cell(0, 6, "A. Data Modality & Multimodal AI", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("helvetica", "", 10)
    pdf.set_text_color(44, 62, 80)
    pdf.multi_cell(0, 5.5, (
        "- Data Modality: A specific form or medium in which data is expressed (Text, Image, Audio, Video, Tabular).\n"
        "- Multimodal AI: AI models (e.g. Google Gemini 3.6 Flash / GPT-5 Vision) capable of processing multiple modalities simultaneously (e.g., Image + Text prompt -> Text/JSON output)."
    ))
    pdf.ln(3)

    # Sub: Deep Dive Alt-Text
    pdf.set_font("helvetica", "B", 11)
    pdf.set_text_color(52, 73, 94)
    pdf.cell(0, 6, "B. Alt-Text & Its 3 Primary Purposes", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("helvetica", "B", 10)
    pdf.cell(0, 5.5, "1. Screen Readers (Web Accessibility):", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 10)
    pdf.multi_cell(0, 5.5, (
        "   Screen readers (NVDA, VoiceOver) are assistive software used by blind or visually impaired individuals. "
        "They cannot 'see' image pixels. Without alt-text, they read raw filenames like 'Image: 450599840.jpg'. "
        "With alt-text, they speak a descriptive text: 'A close-up of a silver digital stylus pen with a bright red clip.'"
    ))
    pdf.ln(2)

    pdf.set_font("helvetica", "B", 10)
    pdf.cell(0, 5.5, "2. Broken Image Fallbacks:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 10)
    pdf.multi_cell(0, 5.5, (
        "   A fallback is an automatic backup plan. If an image fails to load due to a weak signal, server outage, "
        "or broken URL link, the browser renders the alt-text string directly inside the broken image box so users still understand what was supposed to be shown."
    ))
    pdf.ln(2)

    pdf.set_font("helvetica", "B", 10)
    pdf.cell(0, 5.5, "3. SEO (Search Engine Optimization):", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 10)
    pdf.multi_cell(0, 5.5, (
        "   SEO is the practice of optimizing web content so search engines (Google, Bing) rank your site higher. "
        "Search engine crawlers read alt-text to index pictures in Google Image Search and understand your page's context to boost overall search rankings."
    ))
    pdf.ln(4)

    # Section 2: Project Architecture
    pdf.set_font("helvetica", "B", 13)
    pdf.set_text_color(41, 128, 185)
    pdf.cell(0, 8, "2. Project Architecture & File Breakdown", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    files_info = [
        (".env", "Stores private API keys (GEMINI_API_KEY) securely outside source code."),
        ("image_utils.py", "Encodes images to Base64/PIL objects and generates test images."),
        ("api_client.py", "Connects to gemini-3.6-flash with 503 retries & fallback models."),
        ("use_cases.py", "Contains core functions: Image Q&A, Alt-Text, and JSON Object Detection."),
        ("batch_analyzer.py", "Scans 911 Instagram photos, runs bulk analysis, exports to CSV & JSON."),
        ("app.py", "Interactive terminal menu app for image analysis & dataset navigation.")
    ]

    pdf.set_font("helvetica", "B", 10)
    pdf.set_fill_color(236, 240, 241)
    pdf.cell(40, 7, "File Name", border=1, fill=True)
    pdf.cell(150, 7, "Description & Purpose", border=1, fill=True, new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("helvetica", "", 9.5)
    for f_name, f_desc in files_info:
        pdf.cell(40, 6.5, f_name, border=1)
        pdf.cell(150, 6.5, f_desc, border=1, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    # Section 3: App Usage Guide
    pdf.set_font("helvetica", "B", 13)
    pdf.set_text_color(41, 128, 185)
    pdf.cell(0, 8, "3. Interactive Application (app.py) Options", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    options_info = [
        ("Option 1", "Describe / Q&A", "Press Enter for full description, or type a custom question."),
        ("Option 2", "Generate Alt-Text", "Outputs WCAG-compliant HTML tag under 125 characters."),
        ("Option 3", "Detect Objects", "Outputs structured JSON object breakdown (items, colors)."),
        ("Option 4", "Random Photo", "Swaps active image to a random photo from your 911 collection."),
        ("Option 5", "Search Photo", "Type an index (1-911) OR a filename fragment (e.g. 629224241)."),
        ("Option 6", "Batch Analysis", "Bulk-analyzes N photos and exports to batch_analysis_results.csv."),
        ("Option 7", "Custom Path", "Paste any custom image path (quotes are stripped automatically)."),
        ("Option 8", "Exit App", "Exits the application.")
    ]

    pdf.set_font("helvetica", "B", 10)
    pdf.set_fill_color(236, 240, 241)
    pdf.cell(25, 7, "Option", border=1, fill=True)
    pdf.cell(45, 7, "Action", border=1, fill=True)
    pdf.cell(120, 7, "Description", border=1, fill=True, new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("helvetica", "", 9.5)
    for opt, act, desc in options_info:
        pdf.cell(25, 6, opt, border=1)
        pdf.cell(45, 6, act, border=1)
        pdf.cell(120, 6, desc, border=1, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    # Section 4: Pro-Tips & Shortcuts
    pdf.set_font("helvetica", "B", 13)
    pdf.set_text_color(41, 128, 185)
    pdf.cell(0, 8, "4. Key Developer Shortcuts", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    pdf.set_font("helvetica", "", 10)
    pdf.multi_cell(0, 5.5, (
        "- Terminal History Recall: Click terminal and press Up Arrow ^ + Enter to re-run python app.py.\n"
        "- Copy Windows File Path: Select photo in File Explorer and press Ctrl + Shift + C.\n"
        "- Filename Lookup: Type numbers like 629224241 in Option 5 to find photo & its index (#376)."
    ))

    pdf.output(output_pdf_path)
    print(f"PDF successfully compiled at: {output_pdf_path}")
    return output_pdf_path

if __name__ == "__main__":
    create_pdf()
