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
plagarism/
├── README.md
└── plagarism-main/
   ├── IMG-TEXT-PLAG/
   │   └── SOURCE CODE/
   │       ├── views.py
   │       └── Plagiarism/                   # Main Django project
   │           ├── manage.py
   │           ├── run.py
   │           ├── requirements.txt
   │           ├── db.sqlite3
   │           ├── corpus-20090418/          # Source text corpus
   │           ├── images/                   # Source image corpus
   │           ├── Plagiarism/               # Project settings package
   │           ├── PlagiarismApp/            # App logic (views, urls, models)
   │           │   ├── migrations/
   │           │   ├── static/
   │           │   └── templates/
   │           └── staticfiles/
   └── SOURCE CODE/
      ├── run.py
      └── PlagiarismApp/
         └── templates/
            ├── base.html
            ├── UploadSource.html
            ├── UploadSourceImage.html
            ├── UploadSuspiciousFile.html
            ├── UploadSuspiciousImage.html
            ├── SuspiciousFileResult.html
            ├── SuspiciousImageResult.html
            └── UserScreen.html
```

## � How to Run the Project

### 🏁 Quick Start (Recommended)

1. **Clone the Repository**
   ```bash
   git clone <repository_url>
   cd "plagarism/plagarism-main/IMG-TEXT-PLAG/SOURCE CODE/Plagiarism"
   ```

2. **Run the Auto-Launcher**
   The project includes a `run.py` script that handles everything for you:
    - Creates a virtual environment (`.venv`).
    - Installs all required dependencies.
    - Applies database migrations.
    - Starts the development server.

   **On Windows:**
   ```cmd:
   run:
   cd "c:\Users\heman\OneDrive\Desktop\plagarism\plagarism-main\IMG-TEXT-PLAG\SOURCE CODE\Plagiarism"
   python run.py
   ```
   **On macOS / Linux:**
   ```bash
   python3 run.py
   ```

3. **Access the Application**
   - Once the server is running, open your web browser and go to:
   - **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

### 🛠️ Manual Setup (For Advanced Users)

If you prefer to set up the project manually:

1. **Create and Activate Virtual Environment**
   ```bash
   # Create venv
   python -m venv .venv
   
   # Activate on Windows
   .venv\Scripts\activate
   
   # Activate on macOS/Linux
   source .venv/bin/activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Apply Database Migrations**
   ```bash
   python manage.py migrate
   ```

4. **Run the Server**
   ```bash
   python manage.py runserver
   ```
   - To stop the server, press `CTRL + C` in the terminal.

---

## 💡 How It Works

This system detects plagiarism in two ways:

1.  **Text Analysis**: It uses the **Longest Common Subsequence (LCS)** algorithm to compare the word sequence of an uploaded text file against a corpus of source documents. The similarity score is based on the length of the longest matching sequence.
2.  **Image Analysis**: It uses **Histogram Intersection** to compare the color distribution of an uploaded image against a library of source images. A high intersection score suggests a potential visual match.

In both cases, a similarity score is calculated, and if it exceeds a predefined threshold (e.g., 60%), the content is flagged as potential plagiarism.

---

## ❓ FAQ

**Q: How do I add more source files?**
A: Place new `.txt` files in the `corpus-20090418/` directory and new images in the `images/` directory. The system will automatically pick them up.

**Q: How do I reset the database?**
A: Delete the `db.sqlite3` file and run the migration command again: `python manage.py migrate`.

**Q: Can I create an admin user?**
A: Yes. Run `python manage.py createsuperuser` and follow the prompts to create an administrator account.

---

## 🏆 Credits
Developed by B.Hemanth Reddy. For academic and demonstration use.
