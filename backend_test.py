import requests
import sys
import json
from datetime import datetime

class KaraokeAPITester:
    def __init__(self, base_url="https://songqueue-pro.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.token = None
        self.session_token = None
        self.serata_id = None
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

    def test_create_admin_if_needed(self):
        """Create testadmin if it doesn't exist"""
        if not self.token:
            self.log_test("Create Admin", False, "No super admin token available")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            admin_data = {
                "username": "testadmin",
                "password": "testpassword",
                "role": "admin"
            }
            
            response = requests.post(f"{self.api_url}/super-admin/create-admin", json=admin_data, headers=headers, timeout=10)
            
            # Success if created (201) or already exists (400)
            success = response.status_code in [200, 400]
            
            if response.status_code == 200:
                details = "testadmin created successfully"
            elif response.status_code == 400:
                details = "testadmin already exists"
            else:
                details = f"Status: {response.status_code}, Response: {response.text}"
                
            self.log_test("Create Test Admin", success, details)
            return success
            
        except Exception as e:
            self.log_test("Create Test Admin", False, str(e))
            return False

    def test_generate_booking_session_token(self):
        """Test POST /api/admin/booking-session-token"""
        if not self.token:
            self.log_test("Generate Session Token", False, "No admin token available")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.post(f"{self.api_url}/admin/booking-session-token", headers=headers, timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                required_fields = ['success', 'token', 'admin_username']
                success = (data.get('success') == True and 
                          all(field in data for field in required_fields))
                if success:
                    self.session_token = data['token']
                details = f"Session token generated: {data}"
            else:
                details = f"Status: {response.status_code}, Response: {response.text}"
                
            self.log_test("Generate Session Token", success, details)
            return success
            
        except Exception as e:
            self.log_test("Generate Session Token", False, str(e))
            return False

    def test_validate_booking_session_token(self):
        """Test GET /api/booking-session/validate/{token}"""
        if not self.session_token:
            self.log_test("Validate Session Token", False, "No session token available")
            return False
            
        try:
            response = requests.get(f"{self.api_url}/booking-session/validate/{self.session_token}", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                required_fields = ['success', 'admin_username', 'token']
                success = (data.get('success') == True and 
                          all(field in data for field in required_fields))
                details = f"Token validation successful: {data}"
            else:
                details = f"Status: {response.status_code}, Response: {response.text}"
                
            self.log_test("Validate Session Token", success, details)
            return success
            
        except Exception as e:
            self.log_test("Validate Session Token", False, str(e))
            return False

    def test_validate_invalid_token(self):
        """Test validation with invalid token"""
        try:
            invalid_token = "invalid-token-12345"
            response = requests.get(f"{self.api_url}/booking-session/validate/{invalid_token}", timeout=10)
            success = response.status_code == 404  # Should return 404 for invalid token
            
            if success:
                details = "Invalid token correctly rejected with 404"
            else:
                details = f"Status: {response.status_code}, Expected 404"
                
            self.log_test("Validate Invalid Token", success, details)
            return success
            
        except Exception as e:
            self.log_test("Validate Invalid Token", False, str(e))
            return False

    def test_booking_with_session_token(self):
        """Test POST /api/book with session_token"""
        if not self.session_token:
            self.log_test("Booking with Session Token", False, "No session token available")
            return False
            
        try:
            booking_data = {
                "nome": "Mario Rossi",
                "canzone": "Volare",
                "tonalita": "Do",
                "session_token": self.session_token
            }
            
            response = requests.post(f"{self.api_url}/book", json=booking_data, timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                success = (data.get('success') == True and 
                          'codice' in data)
                details = f"Booking with session token successful: {data}"
            else:
                details = f"Status: {response.status_code}, Response: {response.text}"
                
            self.log_test("Booking with Session Token", success, details)
            return success
            
        except Exception as e:
            self.log_test("Booking with Session Token", False, str(e))
            return False

    def test_create_serata(self):
        """Create a test serata for closing test"""
        if not self.token:
            self.log_test("Create Serata", False, "No admin token available")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            serata_data = {
                "nome": f"TestSerata_{datetime.now().strftime('%H%M%S')}",
                "display_time": 5
            }
            
            response = requests.post(f"{self.api_url}/admin/serata/create", json=serata_data, headers=headers, timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                success = data.get('success') == True and 'serata_id' in data
                if success:
                    self.serata_id = data['serata_id']
                details = f"Serata created: {data}"
            else:
                details = f"Status: {response.status_code}, Response: {response.text}"
                
            self.log_test("Create Serata", success, details)
            return success
            
        except Exception as e:
            self.log_test("Create Serata", False, str(e))
            return False

    def test_close_serata_and_invalidate_tokens(self):
        """Test PUT /api/admin/serata/{serata_id}/close and verify token invalidation"""
        if not self.token or not self.serata_id:
            self.log_test("Close Serata & Invalidate Tokens", False, "No admin token or serata_id available")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            
            # Close the serata
            response = requests.put(f"{self.api_url}/admin/serata/{self.serata_id}/close", headers=headers, timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                success = data.get('success') == True
                
                # Now verify that the session token is invalidated
                if success and self.session_token:
                    validate_response = requests.get(f"{self.api_url}/booking-session/validate/{self.session_token}", timeout=10)
                    token_invalidated = validate_response.status_code == 404
                    success = success and token_invalidated
                    
                details = f"Serata closed: {data}, Token invalidated: {token_invalidated if 'token_invalidated' in locals() else 'N/A'}"
            else:
                details = f"Status: {response.status_code}, Response: {response.text}"
                
            self.log_test("Close Serata & Invalidate Tokens", success, details)
            return success
            
        except Exception as e:
            self.log_test("Close Serata & Invalidate Tokens", False, str(e))
            return False

    def test_admin_login(self, username="superadmin", password="superpassword123"):
        """Test admin login with specified credentials"""
        try:
            login_data = {
                "username": username,
                "password": password
            }
            
            response = requests.post(f"{self.api_url}/admin/login", json=login_data, timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                success = 'access_token' in data
                if success:
                    self.token = data['access_token']
                details = f"Login successful for {username}, token received"
            else:
                details = f"Status: {response.status_code}, Response: {response.text}"
                
            self.log_test(f"Admin Login ({username})", success, details)
            return success
            
        except Exception as e:
            self.log_test(f"Admin Login ({username})", False, str(e))
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
        """Run all backend tests including secure token system"""
        print("🎤 Starting Karaoke Backend API Tests...")
        print("🔐 Testing Secure Token System for QR Codes")
        print("=" * 60)
        
        # Basic connectivity
        if not self.test_api_health():
            print("❌ API not accessible, stopping tests")
            return False
            
        # Settings endpoint
        settings_success, settings_data = self.test_settings_endpoint()
        
        # SECURE TOKEN SYSTEM TESTS (Main Focus)
        print("\n🔐 SECURE TOKEN SYSTEM TESTS")
        print("-" * 40)
        
        # 1. Admin login (super admin)
        if not self.test_admin_login("superadmin", "superadmin123"):
            print("❌ Super admin login failed, trying with testadmin")
            if not self.test_admin_login("testadmin", "testpassword"):
                print("❌ Both admin logins failed, stopping token tests")
                return False
        
        # Create testadmin if needed (only if we're logged in as super admin)
        self.test_create_admin_if_needed()
        
        # 2. Generate booking session token
        if not self.test_generate_booking_session_token():
            print("❌ Token generation failed, stopping token tests")
            return False
        
        # 3. Validate the generated token
        if not self.test_validate_booking_session_token():
            print("❌ Token validation failed")
        
        # 4. Test invalid token validation
        self.test_validate_invalid_token()
        
        # 5. Test booking with session token
        if not self.test_booking_with_session_token():
            print("❌ Booking with session token failed")
        
        # 6. Create serata for closing test
        if self.test_create_serata():
            # 7. Close serata and verify token invalidation
            self.test_close_serata_and_invalidate_tokens()
        
        # LEGACY BOOKING TESTS
        print("\n📝 LEGACY BOOKING SYSTEM TESTS")
        print("-" * 40)
        
        # Booking tests (legacy system with admin_username)
        booking_success, codice, nome = self.test_booking_new_singer()
        if booking_success and codice:
            self.test_booking_existing_singer(codice, nome)
            self.test_booking_wrong_name_for_code(codice)
        
        # ADMIN FUNCTIONALITY TESTS
        print("\n👤 ADMIN FUNCTIONALITY TESTS")
        print("-" * 40)
        
        # Admin tests (if we have a token)
        if self.token:
            self.test_admin_singers_list()
            self.test_admin_stats()
            self.test_toggle_bookings()
        
        # Print summary
        print("\n" + "=" * 60)
        print(f"📊 Test Results: {self.tests_passed}/{self.tests_run} passed")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        # Highlight critical token system results
        token_tests = [r for r in self.test_results if any(keyword in r['test'].lower() 
                      for keyword in ['session token', 'validate', 'booking with', 'close serata'])]
        
        print(f"\n🔐 Token System Tests: {len([t for t in token_tests if t['success']])}/{len(token_tests)} passed")
        
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