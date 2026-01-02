from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import matplotlib.pyplot as plt
import re
import cv2
import numpy as np
from string import punctuation
import os

# Simple text cleaning without NLTK dependencies
def cleanPost(doc):
    """Clean and preprocess text without NLTK"""
    # Convert to lowercase
    doc = doc.lower()
    
    # Remove punctuation
    doc = ''.join([c if c not in punctuation else ' ' for c in doc])
    
    # Split into words
    tokens = doc.split()
    
    # Remove empty strings
    tokens = [w for w in tokens if w.strip()]
    
    # Remove single character words
    tokens = [word for word in tokens if len(word) > 1]
    
    # Simple stemming - just remove common suffixes
    tokens = [remove_suffix(word) for word in tokens]
    
    return ' '.join(tokens)

def remove_suffix(word):
    """Simple stemming by removing common suffixes"""
    suffixes = ['ing', 'ed', 'ly', 'er', 'est', 'ment', 'ness']
    for suffix in suffixes:
        if word.endswith(suffix) and len(word) > len(suffix) + 2:
            return word[:-len(suffix)]
    return word

def simple_tokenize(text):
    """Simple word tokenization without NLTK"""
    # Remove punctuation and split
    text = ''.join([c if c not in punctuation else ' ' for c in text])
    return text.split()

def LCS(l1, l2):
    """LCS method - Longest Common Subsequence"""
    s1 = simple_tokenize(l1)
    s2 = simple_tokenize(l2)
    
    if len(s1) == 0 or len(s2) == 0:
        return 0
    
    dp = [[0] * (len(s1) + 1) for _ in range(len(s2) + 1)]
    
    for i in range(1, len(s2) + 1):
        for j in range(1, len(s1) + 1):
            if s2[i-1] == s1[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[len(s2)][len(s1)]


text_files = []
text_data = []
image_files = []
image_data = []

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})

def Login(request):
    if request.method == 'GET':
       return render(request, 'Login.html', {})

def UploadSuspiciousFile(request):
    if request.method == 'GET':
        return render(request, 'UploadSuspiciousFile.html', {})


def UploadSuspiciousImage(request):
    if request.method == 'GET':
        return render(request, 'UploadSuspiciousImage.html', {})

def FMM(name):#five modules algorithm
    img = cv2.imread(name)
    img = cv2.resize(img,(50,50))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rows,cols = img.shape
    for i in range(rows):
        for j in range(cols):
            if img[i,j] < 120:
                img[i,j] = 210
    for i in range(rows):
        for j in range(cols):
            k = img[i,j]
            if (k % 5) == 4:
                img[i,j] = k + 1
            elif (k % 5) == 3:
                img[i,j] = k + 2
            elif (k % 5) == 2:
                img[i,j] = k - 2
            elif (k % 5) == 1:
                img[i,j] = k - 1
    for i in range(rows):
        for j in range(cols):
            k = img[i,j]
            k = k / 5
            img[i,j] = k
    temp = img.ravel()
    temp = np.min(img)
    for i in range(rows):
        for j in range(cols):
            if img[i,j] > 0:
                img[i,j] = img[i,j] - temp
        
    hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    return hist    


def UploadSuspiciousImageAction(request):
    if request.method == 'POST' and request.FILES['t1']:
        output = ''
        myfile = request.FILES['t1']
        fs = FileSystemStorage()
        # Save uploaded file and get absolute path
        upload_name = str(myfile)
        filename = fs.save(upload_name, myfile)
        filepath = fs.path(filename)
        hist = FMM(filepath)
        try:
            os.remove(filepath)
        except Exception:
            pass
        similarity = 0
        file = 'No Match Found'
        hist1 = 0
        # Ensure corpus images are loaded
        if len(image_files) == 0:
            images_dir = os.path.join(settings.BASE_DIR, 'images')
            for root, dirs, directory in os.walk(images_dir):
                for j in range(len(directory)):
                    img_path = os.path.join(root, directory[j])
                    hist_src = FMM(img_path)
                    image_data.append(hist_src)
                    image_files.append(directory[j])

        # Find best match using histogram intersection percentage
        best_metric = 0.0
        best_idx = -1
        for i in range(len(image_files)):
            try:
                metric_val = cv2.compareHist(hist, image_data[i], cv2.HISTCMP_INTERSECT)
                # Convert to percentage of smaller histogram total to normalize
                denom = min(np.sum(hist), np.sum(image_data[i]))
                metric_pct = (metric_val / denom) * 100.0 if denom > 0 else 0.0
            except Exception:
                metric_pct = 0.0
            if metric_pct > best_metric:
                best_metric = metric_pct
                best_idx = i

        output = '<table><tr><th>Source Original Image</th><th>Suspicious Image</th><th>Score (%)</th><th>Result</th></tr>'
        result = 'No Plagiarism Detected'
        # Debug print
        print(str(upload_name) + " best_pct=" + str(best_metric))

        # Use a percentage threshold (adjustable). 60% is a reasonable starting point.
        threshold_pct = 60.0
        if best_metric >= threshold_pct and best_idx >= 0:
            result = 'Plagiarism Detected'
            file = image_files[best_idx]
            hist1 = image_data[best_idx]

        output += '<tr><td>' + str(file) + '</td><td>' + upload_name + '</td>'
        output += '<td>' + f"{best_metric:.2f}" + '</td><td>' + result + '</td></tr>'
        context = {'data': output, 'result_status': result, 'score': f"{best_metric:.2f}"}
        # Do not call plt.show() on the server; if plots are needed, generate images to embed instead.
        return render(request, 'SuspiciousImageResult.html', context)
        

def UploadSuspiciousFileAction(request):
    if request.method == 'POST' and request.FILES.get('t1'):
        try:
            # Load corpus files if not already loaded
            if len(text_files) == 0:
                corpus_dir = os.path.join(settings.BASE_DIR, 'corpus-20090418')
                for root, dirs, directory in os.walk(corpus_dir):
                    for j in range(len(directory)):
                        try:
                            data = ''
                            filepath = os.path.join(root, directory[j])
                            with open(filepath, "r", encoding='iso-8859-1') as file:
                                for line in file:
                                    line = line.strip('\n')
                                    line = line.strip()
                                    if line:
                                        data += line + " "
                            data = cleanPost(data.strip().lower())
                            if data.strip():  # Only add non-empty data
                                text_files.append(directory[j])
                                text_data.append(data)
                        except Exception as e:
                            print(f"Error reading {directory[j]}: {str(e)}")
                            continue
            
            # Process uploaded file
            myfile = request.FILES['t1']
            fs = FileSystemStorage()
            name = str(myfile)
            filename = fs.save("test.txt", myfile)
            filepath = fs.path(filename)

            data = ''
            with open(filepath, "r", encoding='iso-8859-1') as file:
                for line in file:
                    line = line.strip('\n')
                    line = line.strip()
                    if line:
                        data += line + " "
            file.close()
            try:
                os.remove(filepath)
            except Exception:
                pass
            
            data = cleanPost(data.strip().lower())
            
            # Ensure we have data to compare
            if len(data.split()) == 0:
                output = '<table><tr><th>Source File</th><th>Suspicious File</th><th>Similarity</th><th>Result</th></tr>'
                output += '<tr><td>N/A</td><td>' + name + '</td>'
                output += '<td>0%</td><td>Error: File is empty or invalid</td></tr>'
                context = {'data': output}
                return render(request, 'SuspiciousFileResult.html', context)
            
            # Compare with all corpus files
            sim = 0
            ff = 'No Match Found'
            best_similarity_percent = 0
            data_tokens = len(simple_tokenize(data))
            
            if data_tokens == 0:
                output = '<table><tr><th>Source File</th><th>Suspicious File</th><th>Similarity</th><th>Result</th></tr>'
                output += '<tr><td>N/A</td><td>' + name + '</td>'
                output += '<td>0%</td><td>Error: No valid text in file</td></tr>'
                context = {'data': output}
                return render(request, 'SuspiciousFileResult.html', context)
            
            for i in range(len(text_data)):
                if len(text_data[i].split()) > 0:
                    similarity = LCS(text_data[i], data)
                    similarity_percent = similarity / data_tokens if data_tokens > 0 else 0
                    if similarity_percent > best_similarity_percent:
                        sim = similarity
                        best_similarity_percent = similarity_percent
                        ff = text_files[i]
            
            output = '<table><tr><th>Source File</th><th>Suspicious File</th><th>Similarity</th><th>Result</th></tr>'
            result = 'No Plagiarism Detected'
            
            if best_similarity_percent >= 0.60:
                result = 'Plagiarism Detected'
            
            similarity_display = f"{best_similarity_percent*100:.2f}%"
            output += '<tr><td>' + ff + '</td><td>' + name + '</td>'
            output += '<td>' + similarity_display + '</td><td>' + result + '</td></tr>'
            
            # Prepare structured context for the new UI
            suspicious_text = data
            source_text = ""
            if best_similarity_percent > 0 and ff != 'No Match Found':
                 # Find the source text content again for display
                 try:
                     # This is a bit inefficient (searching again), but consistent with the existing structure
                     # We need to find the content of 'ff' in text_data
                     idx = text_files.index(ff)
                     source_text = text_data[idx]
                 except:
                     source_text = "Error retrieving source text."

            context = {
                'data': output, # Kept for backward compatibility if needed, though we will likely replace usage
                'result_status': result,
                'score': f"{best_similarity_percent*100:.2f}",
                'suspicious_file': name,
                'best_match_file': ff,
                'suspicious_text': suspicious_text,
                'source_text': source_text,
                'similarity_score': best_similarity_percent * 100
            }
            return render(request, 'SuspiciousFileResult.html', context)
            
        except Exception as e:
            # Fallback error context
            context = {
                'data': '',
                'result_status': 'Error',
                'score': '0.00',
                'error_message': str(e),
                'suspicious_file': 'Error',
                'best_match_file': 'N/A',
                'similarity_score': 0
            }
            return render(request, 'SuspiciousFileResult.html', context)
    

def UploadSourceImage(request):
    if request.method == 'GET':
        if len(image_files) == 0:
            for root, dirs, directory in os.walk('images'):
                for j in range(len(directory)):
                    hist = FMM(root+"/"+directory[j])
                    image_data.append(hist)
                    image_files.append(directory[j])
        output = '<table><tr><th>Image Name</th><th>Histogram Score</th></tr>'
        for i in range(len(image_files)):
            output+='<tr><td>'+image_files[i]+'</td><td>'+str(int(image_data[i].sum()))+"</td></tr>"
        context= {'data':output}
        return render(request, 'UploadSourceImage.html', context)

def UploadSource(request):
    if request.method == 'GET':
        if len(text_files) == 0:
            corpus_dir = os.path.join(settings.BASE_DIR, 'corpus-20090418')
            for root, dirs, directory in os.walk(corpus_dir):
                for j in range(len(directory)):
                    data = ''
                    fp = os.path.join(root, directory[j])
                    with open(fp, "r", encoding='iso-8859-1') as file:
                        for line in file:
                            line = line.strip('\n')
                            line = line.strip()
                            data += line + " "
                    data = cleanPost(data.strip().lower())
                    text_files.append(directory[j])
                    text_data.append(data)
        output = '<table><tr><th>File Name</th><th>Word Count</th></tr>'
        for i in range(len(text_files)):
            length = len(text_data[i].split(" "))
            output+='<tr><td>'+text_files[i]+'</td><td>'+str(length)+"</td></tr>"
        context= {'data':output}
        return render(request, 'UploadSource.html', context)


def UserLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            # Redirect to the user screen so the browser navigates away from the login page
            return redirect('/UserScreen')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'Login.html', {'error': 'Invalid credentials'})
    return render(request, 'Login.html', {})

def Signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        email = request.POST.get('email', '')
        
        if password != password2:
            return render(request, 'Register.html', {'error': 'Passwords do not match'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'Register.html', {'error': 'Username already exists'})
        
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'Signup successful! Please log in.')
            return render(request, 'Register.html', {'success': 'Account created successfully! Please login.'})
        except Exception as e:
            return render(request, 'Register.html', {'error': f'Error: {str(e)}'})
    return render(request, 'Register.html', {})


def Logout(request):
    auth_logout(request)
    return redirect('/index.html')


@login_required(login_url='/Login.html')
def UserScreen(request):
    return render(request, 'UserScreen.html', {'username': request.user.username})


