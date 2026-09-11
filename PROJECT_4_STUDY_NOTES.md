# Project 4 Study & Review Notes: Multimodal Image Content Analysis

---

## 1. Core AI & Web Concepts

### A. Data Modality & Multimodal AI
- **Data Modality**: A specific form or medium in which information is expressed (e.g., Text, Image, Audio, Video, Tabular).
- **Multimodal AI**: AI models (like Google Gemini 3.6 Flash / GPT-5 Vision) capable of processing multiple modalities simultaneously (e.g., receiving Image + Text prompt and generating Text/JSON output).

---

### B. Deep-Dive: Alt-Text & Its 3 Primary Purposes

#### 1. Screen Readers (Web Accessibility)
- **What it is**: A **screen reader** is assistive software (such as VoiceOver, NVDA, or JAWS) used by blind or visually impaired individuals. It reads aloud the text content of a web page.
- **Why Alt-Text is crucial**: Screen readers cannot "see" image pixels. Without alt-text, the screen reader unhelpfully reads aloud raw filenames like *"Image: 450599840_18439.jpg"*. With proper alt-text, it speaks out a clear description: *"A close-up of a silver digital stylus pen with a bright red clip."*

#### 2. Broken Image Fallbacks
- **What a "Fallback" is**: A fallback is an automatic backup plan when a system fails.
- **What a "Broken Image" is**: An image on a website becomes "broken" if it fails to load—due to a weak mobile connection, a server outage, a deleted file, or an incorrect image URL link.
- **How Alt-Text acts as a fallback**: If the image file fails to load, the web browser renders the **alt-text string directly inside the broken image box**, allowing the user to still understand what visual content was supposed to be shown there.

#### 3. SEO (Search Engine Optimization)
- **What SEO is**: **SEO** is the process of optimizing web content so search engines (like Google or Bing) can index, understand, and rank your website at the top of search results for relevant queries.
- **How Alt-Text boosts SEO**: Search engine bots ("crawlers") index web pages by reading text. They rely on image `alt` attributes to:
  1. Understand what your images depict so they appear in **Google Image Search** results.
  2. Understand the contextual relevance of your webpage, boosting your page's overall ranking when users search for related topics (e.g., *"foggy mountain highway photographs"*).

---

## 2. Project Architecture & File Breakdown

| File Name | Purpose & Function |
| :--- | :--- |
| **`.env`** | Stores private API keys (`GEMINI_API_KEY`) securely outside source code. |
| **`image_utils.py`** | Converts local images to Base64/PIL objects and generates test synthetic images. |
| **`api_client.py`** | Handles API connection to `gemini-3.6-flash` with automatic retries (503/429 errors) and fallback models. |
| **`use_cases.py`** | Contains the 3 core vision functions: **Q&A**, **Alt-Text**, and **JSON Object Detection**. |
| **`batch_analyzer.py`** | Scans your 911 Instagram photos, runs bulk analysis, and exports to CSV and JSON. |
| **`web_app.py`** | Graphical web browser application (Streamlit) with drag-and-drop, photo search, and CSV download buttons. |
| **`app.py`** | Interactive terminal CLI menu application. |
| **`README.md`** | Comprehensive project overview and step-by-step user guide. |

---

## 3. How to Operate the Visual Web Browser UI (`web_app.py`)

### 🚀 Launching the App
- **Fresh Start**: Run `python -m streamlit run web_app.py` in terminal.
- **Already Running**: Open your browser and go to `http://localhost:8501`.

---

### 📱 Web App Features Quick Reference

| Feature Area | Action / Function |
| :--- | :--- |
| **Sidebar (911 Photos)** | Jump by index (`1-911`), click **`🎲 Random`**, or type filename fragment (e.g. `629224241`). |
| **Sidebar (Upload)** | Drag-and-drop any custom image file directly from your computer. |
| **Tab 1: Q&A** | Click **Analyze Image** for a full breakdown, or type a custom question. |
| **Tab 2: Alt-Text** | Click **Generate Alt-Text** for a WCAG HTML tag & character counter. |
| **Tab 3: Object Detection** | Click **Detect Objects** for an interactive JSON tree. |
| **Tab 4: Batch Exporter** | Set photo count slider $\rightarrow$ Run Batch $\rightarrow$ Click **`📥 Download CSV Report`**! |

---

## 4. Key Developer Shortcuts & Tips

1. **Copy File Path in Windows**: Select file in File Explorer and press **`Ctrl + Shift + C`** (or right-click $\rightarrow$ *Copy as path*).
2. **Terminal Command History**: Press **`Up Arrow ↑`** in terminal to recall your last command without retyping.
3. **Numeric Filename Lookup**: Typing numbers like `629224241` in search automatically locates the photo and shows its index (#376).
