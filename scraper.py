import requests
from bs4 import BeautifulSoup
import json
import os
from urllib.parse import urljoin
import time

class ECourtsScraper:
    def __init__(self):
        self.base_url = "https://services.ecourts.gov.in/ecourtindia_v6/"
        self.cause_list_url = "https://services.ecourts.gov.in/ecourtindia_v6/?p=cause_list/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def get_app_token(self):
        """Fetch fresh app_token from homepage"""
        url = "https://services.ecourts.gov.in/ecourtindia_v6/"
        response = self.session.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        token_input = soup.find("input", {"id": "app_token"})
        if not token_input:
            raise Exception("app_token not found")
        return token_input.get("value")

    def get_states(self):
        """Fetch all states from eCourts website"""
        try:
            url = f"{self.cause_list_url}"
            response = self.session.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            states = []
            state_select = soup.find('select', {'id': 'sess_state_code'})
            if state_select:
                for option in state_select.find_all('option')[1:]:
                    states.append({
                        'code': option.get('value'),
                        'name': option.text.strip()
                    })
            return states
        except Exception as e:
            print(f"Error fetching states: {e}")
            return []

    def get_districts(self, state_code):
        """Fetch districts for a given state"""
        try:
            app_token = self.get_app_token()
            url = "https://services.ecourts.gov.in/ecourtindia_v6/?p=casestatus/fillDistrict"
            payload = {
                "state_code": state_code,
                "ajax_req": "true",
                "app_token": app_token
            }
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-Requested-With": "XMLHttpRequest"
            }

            response = self.session.post(url, data=payload, headers=headers)
            data = response.json()
            
            html_content = data.get("dist_list", "")
            soup = BeautifulSoup(html_content, "html.parser")
            
            districts = []
            for option in soup.find_all("option"):
                value = option.get("value")
                text = option.text.strip()
                if value and value != "" and text and text != "Select District":
                    districts.append({
                        "code": value,
                        "name": text
                    })
            
            return districts
            
        except Exception as e:
            print(f"Error fetching districts: {e}")
            return []

    def get_court_complexes(self, state_code, district_code):
        """Fetch court complexes for a given district"""
        try:
            app_token = self.get_app_token()
            url = "https://services.ecourts.gov.in/ecourtindia_v6/?p=casestatus/fillComplex"
            payload = {
                "state_code": state_code,
                "dist_code": district_code,
                "ajax_req": "true",
                "app_token": app_token
            }
            headers = {
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest"
            }

            response = self.session.post(url, data=payload, headers=headers)
            data = response.json()
            
            html_content = data.get("complex_list", "")
            soup = BeautifulSoup(html_content, "html.parser")
            
            complexes = []
            for option in soup.find_all("option"):
                value = option.get("value")
                text = option.text.strip()
                if value and value != "" and text and text != "Select Court Complex":
                    complexes.append({
                        "code": value,
                        "name": text
                    })
            
            return complexes
            
        except Exception as e:
            print(f"Error fetching court complexes: {e}")
            return []

    def get_courts(self, state_code, district_code, court_complex_code):
        """Fetch courts for a given court complex"""
        try:
            app_token = self.get_app_token()
            url = "https://services.ecourts.gov.in/ecourtindia_v6/?p=casestatus/fillComplex"
            payload = {
                "state_code": state_code,
                "dist_code": district_code,
                "court_complex_code": court_complex_code,
                "ajax_req": "true",
                "app_token": app_token
            }
            headers = {
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest"
            }

            response = self.session.post(url, data=payload, headers=headers)
            data = response.json()
            
            html_content = data.get("complex_list", "")
            soup = BeautifulSoup(html_content, "html.parser")
            
            courts = []
            for option in soup.find_all("option"):
                value = option.get("value")
                text = option.text.strip()
                if value and value != "" and text and text != "Select Court Establishment":
                    courts.append({
                        "code": value,
                        "name": text
                    })
            
            return courts
            
        except Exception as e:
            print(f"Error fetching courts: {e}")
            return []

    def download_cause_list_pdf(self, state_code, district_code, court_complex_code, court_code, date, download_folder="downloads"):
        """⚠️ CAPTCHA LIMITED: Download cause list PDF for a specific court"""
        try:
            if not os.path.exists(download_folder):
                os.makedirs(download_folder)
                
            url = f"{self.cause_list_url}"
            data = {
                'sess_state_code': state_code,
                'sess_dist_code': district_code,
                'court_complex_code': court_complex_code,
                'court_code': court_code,
                'from_date': date,
                'to_date': date,
                'search1': 'Search'
            }
            
            response = self.session.post(url, data=data)
            
            # 🚨 CAPTCHA LIMITATION: The website returns CAPTCHA page instead of PDF
            # This is where the automation breaks due to security measures
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Check if we got CAPTCHA page
            if soup.find('input', {'name': 'cause_list_captcha_code'}) or 'captcha' in response.text.lower():
                return {
                    'success': False,
                    'error': 'CAPTCHA_PROTECTION',
                    'message': 'Website has CAPTCHA protection. Cannot download PDF automatically.'
                }
            
            pdf_link = soup.find('a', href=lambda x: x and '.pdf' in x)
            
            if pdf_link:
                pdf_url = urljoin(self.base_url, pdf_link['href'])
                pdf_response = self.session.get(pdf_url, stream=True)
                
                filename = f"cause_list_{state_code}_{district_code}_{court_complex_code}_{court_code}_{date}.pdf"
                filepath = os.path.join(download_folder, filename)
                
                with open(filepath, 'wb') as f:
                    for chunk in pdf_response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                
                return {
                    'success': True,
                    'filepath': filepath,
                    'filename': filename
                }
            else:
                return {
                    'success': False,
                    'error': 'NO_PDF_FOUND',
                    'message': 'No PDF found for the selected criteria'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': 'EXCEPTION',
                'message': f'Error: {str(e)}'
            }

    def download_all_cause_lists(self, state_code, district_code, court_complex_code, date, download_folder="downloads"):
        """⚠️ CAPTCHA LIMITED: Download cause lists for all courts in a complex"""
        courts = self.get_courts(state_code, district_code, court_complex_code)
        
        if not courts:
            return []
        
        downloaded_files = []
        for court in courts:
            result = self.download_cause_list_pdf(
                state_code,
                district_code,
                court_complex_code,
                court['code'],
                date,
                download_folder
            )
            if result.get('success'):
                downloaded_files.append(result)
            time.sleep(1)
        
        return downloaded_files