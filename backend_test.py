import requests
import sys
import json
from datetime import datetime

class KaraokeAPITester:
    def __init__(self, base_url="https://songqueue-pro.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.token = None
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def log_test(self, name, success, details=""):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name} - PASSED")
        else:
            print(f"❌ {name} - FAILED: {details}")
        
        self.test_results.append({
            "test": name,
            "success": success,
            "details": details
        })

    def test_api_health(self):
        """Test basic API connectivity"""
        try:
            response = requests.get(f"{self.api_url}/", timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}, Response: {response.json() if success else response.text}"
            self.log_test("API Health Check", success, details)
            return success
        except Exception as e:
            self.log_test("API Health Check", False, str(e))
            return False

    def test_settings_endpoint(self):
        """Test settings endpoint"""
        try:
            response = requests.get(f"{self.api_url}/settings", timeout=10)
            success = response.status_code == 200
            if success:
                data = response.json()
                success = 'prenotazioni_aperte' in data
                details = f"Settings: {data}"
            else:
                details = f"Status: {response.status_code}"
            self.log_test("Settings Endpoint", success, details)
            return success, response.json() if success else {}
        except Exception as e:
            self.log_test("Settings Endpoint", False, str(e))
            return False, {}

    def test_booking_new_singer(self):
        """Test booking with new singer (no code)"""
        try:
            booking_data = {
                "nome": f"TestSinger_{datetime.now().strftime('%H%M%S')}",
                "canzone": "Test Song",
                "tonalita": "Do"
            }
            
            response = requests.post(f"{self.api_url}/book", json=booking_data, timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                success = (data.get('success') == True and 
                          'codice' in data and 
                          data.get('nuovo_cantante') == True)
                details = f"Response: {data}"
                return success, data.get('codice', ''), booking_data['nome']
            else:
                details = f"Status: {response.status_code}, Response: {response.text}"
                
            self.log_test("Booking New Singer", success, details)
            return success, "", ""
            
        except Exception as e:
            self.log_test("Booking New Singer", False, str(e))
            return False, "", ""

    def test_booking_existing_singer(self, codice, nome):
        """Test booking with existing singer code"""
        try:
            booking_data = {
                "nome": nome,
                "canzone": "Second Test Song",
                "tonalita": "Re",
                "codice": codice
            }
            
            response = requests.post(f"{self.api_url}/book", json=booking_data, timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                success = (data.get('success') == True and 
                          data.get('nuovo_cantante') == False)
                details = f"Response: {data}"
            else:
                details = f"Status: {response.status_code}, Response: {response.text}"
                
            self.log_test("Booking Existing Singer", success, details)
            return success
            
        except Exception as e:
            self.log_test("Booking Existing Singer", False, str(e))
            return False

    def test_booking_wrong_name_for_code(self, codice):
        """Test booking with wrong name for existing code"""
        try:
            booking_data = {
                "nome": "WrongName",
                "canzone": "Test Song",
                "tonalita": "Do",
                "codice": codice
            }
            
            response = requests.post(f"{self.api_url}/book", json=booking_data, timeout=10)
            success = response.status_code == 400  # Should fail with 400
            
            if success:
                data = response.json()
                success = 'nome non corrisponde' in data.get('detail', '').lower()
                details = f"Correctly rejected: {data}"
            else:
                details = f"Status: {response.status_code}, Expected 400"
                
            self.log_test("Booking Wrong Name for Code", success, details)
            return success
            
        except Exception as e:
            self.log_test("Booking Wrong Name for Code", False, str(e))
            return False

    def test_admin_login(self):
        """Test admin login"""
        try:
            login_data = {
                "username": "admin",
                "password": "admin123"
            }
            
            response = requests.post(f"{self.api_url}/admin/login", json=login_data, timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                success = 'access_token' in data
                if success:
                    self.token = data['access_token']
                details = f"Login successful, token received"
            else:
                details = f"Status: {response.status_code}, Response: {response.text}"
                
            self.log_test("Admin Login", success, details)
            return success
            
        except Exception as e:
            self.log_test("Admin Login", False, str(e))
            return False

    def test_admin_singers_list(self):
        """Test admin singers list"""
        if not self.token:
            self.log_test("Admin Singers List", False, "No token available")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(f"{self.api_url}/admin/singers", headers=headers, timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                success = isinstance(data, list)
                details = f"Found {len(data)} singers"
            else:
                details = f"Status: {response.status_code}, Response: {response.text}"
                
            self.log_test("Admin Singers List", success, details)
            return success, data if success else []
            
        except Exception as e:
            self.log_test("Admin Singers List", False, str(e))
            return False, []

    def test_admin_stats(self):
        """Test admin statistics"""
        if not self.token:
            self.log_test("Admin Stats", False, "No token available")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(f"{self.api_url}/admin/stats", headers=headers, timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                required_fields = ['totale_prenotazioni', 'canzoni_cantate', 'in_attesa', 'totale_cantanti']
                success = all(field in data for field in required_fields)
                details = f"Stats: {data}"
            else:
                details = f"Status: {response.status_code}, Response: {response.text}"
                
            self.log_test("Admin Stats", success, details)
            return success
            
        except Exception as e:
            self.log_test("Admin Stats", False, str(e))
            return False

    def test_toggle_bookings(self):
        """Test toggle bookings functionality"""
        if not self.token:
            self.log_test("Toggle Bookings", False, "No token available")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            
            # First close bookings
            response = requests.put(
                f"{self.api_url}/admin/settings", 
                json={"prenotazioni_aperte": False}, 
                headers=headers, 
                timeout=10
            )
            success = response.status_code == 200
            
            if success:
                # Test that booking is rejected when closed
                booking_data = {
                    "nome": "TestClosedBooking",
                    "canzone": "Test Song",
                    "tonalita": "Do"
                }
                
                booking_response = requests.post(f"{self.api_url}/book", json=booking_data, timeout=10)
                booking_rejected = booking_response.status_code == 400
                
                # Reopen bookings
                reopen_response = requests.put(
                    f"{self.api_url}/admin/settings", 
                    json={"prenotazioni_aperte": True}, 
                    headers=headers, 
                    timeout=10
                )
                
                success = booking_rejected and reopen_response.status_code == 200
                details = f"Bookings closed and rejected correctly, then reopened"
            else:
                details = f"Status: {response.status_code}, Response: {response.text}"
                
            self.log_test("Toggle Bookings", success, details)
            return success
            
        except Exception as e:
            self.log_test("Toggle Bookings", False, str(e))
            return False

    def run_all_tests(self):
        """Run all backend tests"""
        print("🎤 Starting Karaoke Backend API Tests...")
        print("=" * 50)
        
        # Basic connectivity
        if not self.test_api_health():
            print("❌ API not accessible, stopping tests")
            return False
            
        # Settings endpoint
        settings_success, settings_data = self.test_settings_endpoint()
        
        # Booking tests
        booking_success, codice, nome = self.test_booking_new_singer()
        if booking_success and codice:
            self.test_booking_existing_singer(codice, nome)
            self.test_booking_wrong_name_for_code(codice)
        
        # Admin tests
        if self.test_admin_login():
            self.test_admin_singers_list()
            self.test_admin_stats()
            self.test_toggle_bookings()
        
        # Print summary
        print("\n" + "=" * 50)
        print(f"📊 Test Results: {self.tests_passed}/{self.tests_run} passed")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        return self.tests_passed == self.tests_run

def main():
    tester = KaraokeAPITester()
    success = tester.run_all_tests()
    
    # Save detailed results
    with open('/app/backend_test_results.json', 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'total_tests': tester.tests_run,
            'passed_tests': tester.tests_passed,
            'success_rate': (tester.tests_passed/tester.tests_run)*100 if tester.tests_run > 0 else 0,
            'results': tester.test_results
        }, f, indent=2)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())