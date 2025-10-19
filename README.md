# eCourts Cause List Scraper

A Python web application to fetch court hierarchy and cause lists from eCourts website.

## 🚨 Important Notice: CAPTCHA Limitation

The eCourts website (`services.ecourts.gov.in`) has **CAPTCHA protection** which prevents automated scraping of cause lists. This is a security measure implemented by the website to protect against bots.

### What Works:
- ✅ **Full Hierarchy Scraping**: States → Districts → Court Complexes → Courts
- ✅ **Real-time Data**: All data fetched directly from eCourts website
- ✅ **Web Interface**: User-friendly interface with cascading dropdowns
- ✅ **Complete Scraping Logic**: Full implementation for cause list download

### What's Limited by CAPTCHA:
- ❌ **PDF Download**: Cannot download actual cause list PDFs due to CAPTCHA protection
- ❌ **Automated Form Submission**: CAPTCHA blocks form submissions

## Features Implemented

### Working Features:
1. **State Selection** - Fetch all Indian states from eCourts
2. **District Selection** - Get districts for selected state
3. **Court Complex Selection** - Get court complexes for selected district
4. **Court Selection** - Get individual courts for selected complex
5. **Date Selection** - Choose date for cause list
6. **Web Interface** - Complete Flask web application

### Technical Implementation:
- Real-time AJAX calls to eCourts APIs
- Proper session management and headers
- Error handling and rate limiting
- Responsive web design

## Installation

```bash
git clone <repository-url>
cd eCourts_Scraper
pip install -r requirements.txt

# eCourts Cause List Scraper

A Python Flask web application that scrapes cause lists from eCourts website in real-time and downloads them as PDF files.

## Features

- Real-time fetching of states, districts, court complexes, and courts
- Download cause lists for specific courts or all courts in a complex
- User-friendly web interface
- PDF download and management
- Responsive design

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd eCourts_scraper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to:

http://localhost:5000

# Usage
- Select State from the dropdown

- Select District (automatically populated based on state)

- Select Court Complex (automatically populated based on district)

- Optionally select a specific Court (leave empty to download all courts)

- Select the date for the cause list

- Check "Download all courts" if you want cause lists for all courts in the complex

- Click "Download Cause List"


