from flask import Flask, render_template, request, jsonify, send_file
import os
from scraper import ECourtsScraper

app = Flask(__name__)
scraper = ECourtsScraper()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/states')
def get_states():
    return jsonify(scraper.get_states())

@app.route('/districts/<state_code>')
def get_districts(state_code):
    return jsonify(scraper.get_districts(state_code))

@app.route('/complexes/<state_code>/<district_code>')
def get_complexes(state_code, district_code):
    return jsonify(scraper.get_court_complexes(state_code, district_code))

@app.route('/courts/<state_code>/<district_code>/<complex_code>')
def get_courts(state_code, district_code, complex_code):
    return jsonify(scraper.get_courts(state_code, district_code, complex_code))

@app.route('/download', methods=['POST'])
def download_cause_list():
    data = request.json
    state_code = data['state_code']
    district_code = data['district_code']
    court_complex_code = data['court_complex_code']
    court_code = data.get('court_code', '')
    date = data['date']
    download_all = data.get('download_all', False)
    
    try:
        if download_all:
            files = scraper.download_all_cause_lists(state_code, district_code, court_complex_code, date)
            if files:
                return jsonify({
                    'success': True,
                    'message': f'Downloaded {len(files)} cause lists successfully!'
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'CAPTCHA protection prevented PDF download. The website has security measures that block automated scraping.'
                })
        else:
            if not court_code:
                return jsonify({
                    'success': False,
                    'message': 'Please select a specific court or choose "Download all courts"'
                })
            
            result = scraper.download_cause_list_pdf(state_code, district_code, court_complex_code, court_code, date)
            if result.get('success'):
                return jsonify({
                    'success': True,
                    'message': 'Cause list downloaded successfully!'
                })
            else:
                return jsonify({
                    'success': False,
                    'message': result.get('message', 'CAPTCHA protection prevented PDF download.')
                })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

if __name__ == "__main__":
    print("Starting eCourts Scraper Web Interface...")
    print("Open http://localhost:5000 in your browser")
    print("NOTE: PDF download is limited by CAPTCHA protection")
    app.run(debug=True, port=5000)