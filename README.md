# 📚 Capstone Chatbot Data Management System

## 🌟 Overview 

Sistem manajemen data chatbot yang komprehensif untuk mengumpulkan, memproses, dan mengelola kutipan dari tokoh-tokoh bersejarah Indonesia (Soekarno dan Hatta). Sistem ini mencakup web scraping, pemrosesan data, dan operasi CRUD melalui REST API.


1. 📄 Data Files
- content_author_quotes.json            :Kutipan berdasarkan author
- content_by_author_and_tags.json       :Data terstruktur per author & tag
- content.json                          :Data utama untuk chatbot
- quotes_hatta.csv                      :Raw quotes Hatta
- quotes_soekarno.csv                   :Raw quotes Soekarno

2. 🐍 Python Scripts
- send_to_postman.py                    :Main API management tool
- form-add-line.py                      :Data editing & validation tool

3. 📓 Jupyter Notebooks
- hatta_scraping.ipynb                  :Scraping quotes Hatta
- notebook_scraping copy.ipynb          :Comprehensive data processing
- send_to_postman.ipynb                 :API testing notebook

4. 🎵 Audio Files
- audio_bcIk9n6nRUo_20250523_215906.mp3
-  audio_bcIk9n6nRUo_20250523_220126.mp3

5. video_transcript.txt                 :Transcript dari audio/video


## Core Components

1. send_to_postman.py - Main API Management Tool 🚀
Comprehensive chatbot data management system dengan REST API integration.

✨ Key Features:
📤 Push Operations: Upload data ke API (all, by author, specific tag)
🗑️ Delete Operations: Hapus tag, author, atau input/response tertentu
✏️ Edit Operations: Edit granular untuk input/response individual
🔧 Utilities: Debug tools, connectivity check, data preview
📊 Progress Tracking: Real-time feedback dan success rate

📤 PUSH DATA:
1. Push All Data (Semua author & tag)
2. Push by Author (Pilih author tertentu)
3. Push Specific Tag (Pilih tag tertentu)

🔧 UTILITIES:
4. Preview Data (Lihat data yang akan dikirim)
5. Test Single Request (Debug)
6. Check Endpoint Connectivity
7. View All Tags in API

🗑️ DELETE/EDIT DATA:
8. Delete Specific Tag
9. Delete All Tags by Author
10. Delete/Edit Inputs & Responses

API Integration:
- Base URL: https://capstone-five-dusky.vercel.app/chatbot/tags
- Methods: GET, POST, PUT, DELETE
- Format: JSON payload dengan struktur:

2. form-add-line.py - Data Editing & Validation Tool ✏️
Advanced tool untuk editing dan validasi data chatbot.

- 🎯 Main Functions:
- 📏 Response Length Audit: Deteksi response > 150 karakter
- ✂️ Text Editing: Edit partial atau rewrite complete
- 📊 Global Analysis: Audit semua author & tag sekaligus
- 🔍 Filtering: Filter by author, tag, atau length range
- 💾 Auto-save: Automatic data persistence

🛠️ Editing Options:
1. Edit response tertentu
2. Edit semua response panjang
3. Edit by author atau tag
4. Bulk editing operations
5. Input/response management

3. Jupyter Notebooks 📓
**hatta_scraping.ipynb**
- Web scraping quotes Mohammad Hatta dari Goodreads
- Data cleaning dan formatting
- CSV export untuk further processing

**notebook_scraping.ipynb**
- -Comprehensive data processing pipeline
- Multiple source integration
- JSON structure creation untuk chatbot
- API testing dan validation

## Installation & Setup

Prerequisites:

pip install requests beautifulsoup4 pandas jupyter

Environment Setup:

# Required libraries
import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
import time 

💻 Usage Examples
1. Web Scrapping:

jupyter notebook hatta_scraping.ipynb

jupyter notebook notebook_scraping.ipynb


2. Data Editing 
python form-add-line.py

3. Basic API Operation
python send_to_postman.py

🎯 Key Features

**🔥 Advanced Capabilities:**
- Multi-endpoint Support: Try berbagai API endpoints automatically
- Error Handling: Comprehensive error detection dan recovery
- Batch Operations: Process multiple items efficiently
- Safety Features: Confirmation prompts untuk prevent accidents
- Progress Tracking: Real-time monitoring dengan success rates
- Debug Tools: Extensive debugging dan testing utilities
**📈 Data Management:**
- CRUD Operations: Complete Create, Read, Update, Delete
- Granular Editing: Edit individual inputs/responses
- Bulk Operations: Process multiple items sekaligus
- Data Validation: Automatic validation dan cleaning
- Format Conversion: CSV ↔ JSON transformation
**🌐 API Integration:**
REST API Support: Full HTTP methods support
Multiple Endpoints: Try different API paths
Response Handling: Parse berbagai response formats
Timeout Management: Handle network issues gracefully
