# Plagiarism Detection System

## 🔍 Project Description
A comprehensive **Text and Image Plagiarism Detection System** designed to identify copied content with high accuracy. This application uses advanced algorithms (Longest Common Subsequence for text and Histogram Intersection for images) to compare uploaded files against a trusted corpus of source material. It provides detailed similarity scores and visual comparison reports.

## 🎯 Who It Is For
This tool is perfect for:
- **Educators & Teachers**: To verify the originality of student assignments.
- **Students & Researchers**: To self-check their work before submission.
- **Content Creators**: To ensure their visual and textual content is unique.
- **Developers**: Learning about Django and computer vision integration.

## 📱 Responsive Design
The website is fully responsive and optimized for all screen sizes. It works perfectly on:
- ✅ **Mobile Devices** (iPhone, Android)
- ✅ **Tablets** (iPad, Android Tablets)
- ✅ **Laptops**
- ✅ **Desktop Screens**

## 🛠️ Technologies Used

### Frontend
- **HTML5 & CSS3**: For structure and modern styling.
- **JavaScript**: For interactive UI elements and dynamic content.
- **Bootstrap**: For responsive grid layouts and components.

### Backend
- **Python 3**: Core programming language.
- **Django**: High-level Python web framework.

### Styling
- **Custom CSS**: Premium, glassmorphism-inspired UI.
- **FontAwesome**: For beautiful, scalable icons.

### Libraries & Tools
- **OpenCV & NumPy**: For image processing and comparison.
- **NLTK (Natural Language Toolkit)**: For text processing.
- **SQLite**: Lightweight database for storing user execution data.

## 📂 Project Structure

```text
Plagiarism/
├── PlagiarismApp/           # Main application logic
│   ├── migrations/          # Database migrations
│   ├── static/              # CSS, JS, and Images
│   │   ├── css/            # Custom stylesheets
│   │   └── images/         # Static assets
│   ├── templates/           # HTML files
│   │   ├── base.html       # Base layout
│   │   ├── index.html      # Landing page
│   │   └── ...             # Other page templates
│   ├── views.py             # Main logic (Text & Image detection)
│   ├── urls.py              # URL routing
│   └── models.py            # Database models
├── corpus-20090418/         # Source text documents for comparison
├── images/                  # Source images for comparison
├── manage.py                # Django CLI utility
├── run.py                   # ★ Auto-launcher script
└── requirements.txt         # List of dependencies
```

## 🗺️ File Navigation Guide
- **`run.py`**: The easiest way to start the project. It automatically sets up your environment, installs dependencies, migrates the database, and launches the server.
- **`manage.py`**: The standard Django command-line tool for administrative tasks.
- **`PlagiarismApp/views.py`**: Contains the core logic for plagiarism detection (LCS algorithm and Histogram comparison).
- **`templates/`**: Holds all the HTML files that users see in the browser.
- **`static/`**: Contains the styling (CSS) and code (JS) that makes the site look good and work interactively.

## 🚀 How to Run the Project (Step-by-Step)

Follow these simple steps to get the project running on your local machine.

### 1. Clone the Repository
Open your terminal or command prompt and run:
```bash
git clone <repository_url>
cd plagarism
```

### 2. Navigate to Source Directory
The source code is located deep in the folder structure. Navigate to the `Plagiarism` directory:
```bash
cd "11.TEXT and IMAGE Plagiarism Detection/11.TEXT and IMAGE Plagiarism Detection/SOURCE CODE/Plagiarism"
```

### 3. Run the Auto-Launcher
The project includes a `run.py` script that handles everything for you (venv creation, requirements, migration, and server start).

**Windows:**
```bash
python run.py
```

**macOS / Linux:**
```bash
python3 run.py
```

*The script will print the local URL (usually `http://127.0.0.1:8000`) which you can open in your browser.*

---

## 📦 Virtual Environment (venv) Setup
If you prefer to set it up manually, follows these steps:

### 1. Create Virtual Environment
```bash
python -m venv .venv
```

### 2. Activate Virtual Environment
- **Windows:**
  ```bash
  .venv\Scripts\activate
  ```
- **macOS / Linux:**
  ```bash
  source .venv/bin/activate
  ```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Server
```bash
python manage.py runserver
```

## ✅ Prerequisites
- **Python 3.7 or higher**: Make sure Python is installed on your system.
  - Check by running `python --version` in your terminal.
- **Git**: To clone the repository.

## 📝 Notes for New Users
- **First Run**: The first time you run the project, it might take a minute to download and install all the required libraries (like OpenCV and Django).
- **Admin**: The default setup creates pages for users. To manage the site, you can create a superuser via `python manage.py createsuperuser` if needed, though the main functionality is accessible via the user dashboard.
- **Stopping**: To stop the server, go to your terminal and press `CTRL + C`.
