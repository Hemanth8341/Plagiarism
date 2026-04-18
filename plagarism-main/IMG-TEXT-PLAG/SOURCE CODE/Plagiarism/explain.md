# Text and Image Plagiarism Detection - Full Project Explanation

## 1. Project Overview
This project is a web-based plagiarism detection system built using Django. It supports two major checks:
1. Text plagiarism detection by comparing uploaded text against a source corpus.
2. Image plagiarism detection by comparing uploaded images with stored source images.

The system gives a similarity score and a final decision like `Plagiarism Detected` or `No Plagiarism Detected`.

## 2. Technologies Used
- Backend: Python, Django
- Frontend: HTML, CSS, Bootstrap, JavaScript
- Image Processing: OpenCV (`cv2`), NumPy
- Database: SQLite (`db.sqlite3`)
- Auth: Django built-in authentication (`django.contrib.auth`)
- File Handling: Django `FileSystemStorage`

## 3. Algorithms Used

### 3.1 Text Plagiarism Algorithm
Text matching is based on **LCS (Longest Common Subsequence)** at word level.

Pipeline used in code:
1. Clean text (`cleanPost`): lowercase, remove punctuation, remove single-letter words, simple suffix stripping.
2. Tokenize text (`simple_tokenize`).
3. Compute LCS dynamic programming matrix (`LCS` function).
4. Convert score to percentage:
	- `similarity_percent = LCS_length / number_of_words_in_uploaded_text`
5. Decision threshold:
	- If percentage >= `60%`, result = `Plagiarism Detected`
	- Else, `No Plagiarism Detected`

Why LCS: It captures sequence-level overlap, not just random common words.

### 3.2 Image Plagiarism Algorithm
Image matching uses histogram-based similarity with preprocessing (`FMM`).

Pipeline used in code:
1. Read image and resize to `50x50`.
2. Convert to grayscale.
3. Pixel normalization/quantization steps (FMM logic).
4. Build histogram using `cv2.calcHist`.
5. Compare with source image histograms using `cv2.compareHist(..., HISTCMP_INTERSECT)`.
6. Normalize to percentage score.
7. Decision threshold:
	- If score >= `60%`, result = `Plagiarism Detected`
	- Else, `No Plagiarism Detected`

Why histogram intersection: fast, simple, and robust to small image-level changes.

## 4. Database Details
Main database in current Django app:
- Engine: `sqlite3`
- File: `db.sqlite3`
- Configured in `settings.py`

What is stored:
- User accounts and auth/session data (Django default tables)
- Project metadata if models are added

What is file-based (not DB tables):
- Text corpus files in `corpus-20090418/`
- Source images in `images/`
- Uploaded files are saved temporarily, processed, then removed.

## 5. Existing System vs Proposed System

### Existing System (General/Traditional)
- Manual checking or simple copy-match tools.
- Usually text-only checking.
- Less automation for image similarity.
- Slower and less scalable for large datasets.

### Proposed System (This Project)
- Unified platform for both text and image plagiarism.
- Automated scoring and result generation.
- Uses algorithmic methods:
  - LCS for text
  - Histogram intersection for images
- Threshold-based final decision.
- User login flow and dashboard support.
- Faster and consistent compared to manual process.

## 6. How the Project Works (Detailed Flow)
1. User opens home page, logs in, and chooses Text or Image analysis.
2. User uploads suspicious file/image.
3. Backend receives upload via Django view action.
4. Source dataset is loaded once (text corpus or source images).
5. Uploaded data is preprocessed:
	- Text: clean and tokenize
	- Image: resize, grayscale, histogram extraction
6. Similarity is computed against all source entries.
7. Best match is selected with highest score.
8. Score is converted to percentage.
9. Threshold logic marks plagiarism status.
10. Result page shows source file/image, uploaded file/image, score, and decision.

## 7. How Code Works in 10 Lines (As Requested)
1. `UploadSuspiciousFileAction` / `UploadSuspiciousImageAction` receives uploaded file.
2. File is saved temporarily using `FileSystemStorage`.
3. For text, `cleanPost()` preprocesses and `LCS()` computes match length.
4. For image, `FMM()` creates histogram features.
5. Source corpus/images are loaded from local folders.
6. Each source item is compared with uploaded input.
7. Highest similarity score and source match are tracked.
8. Score is converted to percentage and compared with 60% threshold.
9. Result string is formed: `Plagiarism Detected` or `No Plagiarism Detected`.
10. Django renders result template with score, best match, and status.

## 8. Viva Questions and Answers

### Q1. Why did you choose LCS for text plagiarism?
LCS measures ordered overlap of words and captures structural similarity better than simple word counting.

### Q2. What is the time complexity of LCS?
For two token sequences of lengths `m` and `n`, DP LCS complexity is `O(m*n)` in time and `O(m*n)` in space.

### Q3. Why is preprocessing needed before LCS?
Without preprocessing, punctuation/case/suffix variations create false mismatches. Cleaning improves matching quality.

### Q4. Why use histogram comparison for images?
Histogram-based comparison is efficient and works well for detecting similarity in intensity/color distributions.

### Q5. What does your image threshold mean?
If normalized histogram similarity >= 60%, it is classified as plagiarism. Threshold can be tuned for strictness.

### Q6. What are limitations of histogram-based image plagiarism?
It may fail for heavily transformed images (rotation, crop, strong edits) where distribution changes significantly.

### Q7. Why did you use SQLite?
It is simple, lightweight, and ideal for local development and small-to-medium academic projects.

### Q8. How are users managed in your system?
Using Django authentication (`authenticate`, `login`, `logout`) and built-in user/session tables.

### Q9. What happens if uploaded text is empty?
The backend returns a safe result with error messaging and 0% similarity.

### Q10. How can this project be improved?
Use TF-IDF/BERT for text, ORB/SIFT/CNN for image features, store history in DB, and add report export.

## 9. Advantages
- Supports both text and image plagiarism in one app.
- Gives explainable score with final status.
- Simple architecture, easy to demonstrate in viva.
- Uses standard Python libraries and Django flow.

## 10. Future Scope
- Add PDF/DOCX parser support.
- Add sentence-level highlighted plagiarism report.
- Add deep-learning-based semantic plagiarism detection.
- Add robust image feature matching for transformed images.
- Add admin analytics and downloadable reports.

## 11. Final One-Minute Summary (For Viva)
This is a Django-based plagiarism detection system that checks both text and images. For text, it cleans input and uses LCS to compute sequence similarity against a corpus. For images, it preprocesses images, creates histograms, and uses histogram intersection to find best matches. A 60% threshold is used to classify plagiarism. Results are displayed in a structured report with score, best matched source, and final status. The system uses SQLite for user/auth data and file-based datasets for source documents and images.
