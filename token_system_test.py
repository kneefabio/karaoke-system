#!/usr/bin/env python3
"""
Comprehensive test of the secure token system for QR codes
Following the exact sequence specified in the review request
"""

import requests
import json
import sys
from datetime import datetime

class TokenSystemTester:
    def __init__(self, base_url="https://songqueue-pro.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.admin_token = None
        self.session_token = None
        self.serata_id = None
        self.test_results = []

    def log_result(self, step, success, details=""):
        """Log test step result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} Step {step}: {details}")
        self.test_results.append({
            "step": step,
            "success": success,
            "details": details
        })
        return success

    def test_step_1_admin_login(self):
        """Step 1: POST /api/admin/login - Login as admin to get JWT token"""
        try:
            login_data = {
                "username": "superadmin",
                "password": "superpassword123"
            }
            
            response = requests.post(f"{self.api_url}/admin/login", json=login_data, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'access_token' in data:
                    self.admin_token = data['access_token']
                    return self.log_result(1, True, "Admin login successful, JWT token obtained")
                else:
                    return self.log_result(1, False, "No access_token in response")
            else:
                return self.log_result(1, False, f"Login failed: {response.status_code} - {response.text}")
                
        except Exception as e:
            return self.log_result(1, False, f"Exception: {str(e)}")

    def test_step_2_generate_session_token(self):
        """Step 2: POST /api/admin/booking-session-token - Generate session token"""
        if not self.admin_token:
            return self.log_result(2, False, "No admin token available")
            
        try:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            response = requests.post(f"{self.api_url}/admin/booking-session-token", headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                expected_fields = ['success', 'token', 'admin_username']
                
                if all(field in data for field in expected_fields) and data.get('success') == True:
                    self.session_token = data['token']
                    admin_username = data['admin_username']
                    return self.log_result(2, True, f"Session token generated: {self.session_token[:8]}..., admin: {admin_username}")
                else:
                    return self.log_result(2, False, f"Invalid response format: {data}")
            else:
                return self.log_result(2, False, f"Request failed: {response.status_code} - {response.text}")
                
        except Exception as e:
            return self.log_result(2, False, f"Exception: {str(e)}")

    def test_step_3_validate_token(self):
        """Step 3: GET /api/booking-session/validate/{token} - Validate token"""
        if not self.session_token:
            return self.log_result(3, False, "No session token available")
            
        try:
            response = requests.get(f"{self.api_url}/booking-session/validate/{self.session_token}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                expected_fields = ['success', 'admin_username', 'token']
                
                if all(field in data for field in expected_fields) and data.get('success') == True:
                    admin_username = data['admin_username']
                    token = data['token']
                    return self.log_result(3, True, f"Token validation successful: admin={admin_username}, token={token[:8]}...")
                else:
                    return self.log_result(3, False, f"Invalid response format: {data}")
            else:
                return self.log_result(3, False, f"Validation failed: {response.status_code} - {response.text}")
                
        except Exception as e:
            return self.log_result(3, False, f"Exception: {str(e)}")

    def test_step_3b_validate_invalid_token(self):
        """Step 3b: Test invalid token returns 404"""
        try:
            invalid_token = "invalid-token-12345"
            response = requests.get(f"{self.api_url}/booking-session/validate/{invalid_token}", timeout=10)
            
            if response.status_code == 404:
                return self.log_result("3b", True, "Invalid token correctly rejected with 404")
            else:
                return self.log_result("3b", False, f"Expected 404, got {response.status_code}")
                
        except Exception as e:
            return self.log_result("3b", False, f"Exception: {str(e)}")

    def test_step_4_booking_with_token(self):
        """Step 4: POST /api/book - Test booking with session_token"""
        if not self.session_token:
            return self.log_result(4, False, "No session token available")
            
        try:
            booking_data = {
                "nome": "Mario Rossi",
                "canzone": "Volare",
                "tonalita": "Do",
                "session_token": self.session_token
            }
            
            response = requests.post(f"{self.api_url}/book", json=booking_data, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') == True and 'codice' in data:
                    codice = data['codice']
                    return self.log_result(4, True, f"Booking successful with session token, codice: {codice}")
                else:
                    return self.log_result(4, False, f"Invalid booking response: {data}")
            else:
                return self.log_result(4, False, f"Booking failed: {response.status_code} - {response.text}")
                
        except Exception as e:
            return self.log_result(4, False, f"Exception: {str(e)}")

    def test_step_5a_create_serata(self):
        """Step 5a: Create a serata for testing closure"""
        if not self.admin_token:
            return self.log_result("5a", False, "No admin token available")
            
        try:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            serata_data = {
                "nome": f"TestSerata_{datetime.now().strftime('%H%M%S')}",
                "display_time": 5
            }
            
            response = requests.post(f"{self.api_url}/admin/serata/create", json=serata_data, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') == True and 'serata_id' in data:
                    self.serata_id = data['serata_id']
                    return self.log_result("5a", True, f"Serata created: {data['nome']}")
                else:
                    return self.log_result("5a", False, f"Invalid serata response: {data}")
            else:
                return self.log_result("5a", False, f"Serata creation failed: {response.status_code} - {response.text}")
                
        except Exception as e:
            return self.log_result("5a", False, f"Exception: {str(e)}")

    def test_step_5_close_serata_and_invalidate_tokens(self):
        """Step 5: PUT /api/admin/serata/{serata_id}/close - Close serata and verify token invalidation"""
        if not self.admin_token or not self.serata_id:
            return self.log_result(5, False, "No admin token or serata_id available")
            
        try:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            
            # Close the serata
            response = requests.put(f"{self.api_url}/admin/serata/{self.serata_id}/close", headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') == True:
                    # Verify token is now invalidated
                    if self.session_token:
                        validate_response = requests.get(f"{self.api_url}/booking-session/validate/{self.session_token}", timeout=10)
                        token_invalidated = validate_response.status_code == 404
                        
                        if token_invalidated:
                            return self.log_result(5, True, f"Serata closed successfully and session token invalidated (active=false)")
                        else:
                            return self.log_result(5, False, f"Serata closed but token still valid (status: {validate_response.status_code})")
                    else:
                        return self.log_result(5, True, "Serata closed successfully (no token to validate)")
                else:
                    return self.log_result(5, False, f"Serata close failed: {data}")
            else:
                return self.log_result(5, False, f"Close request failed: {response.status_code} - {response.text}")
                
        except Exception as e:
            return self.log_result(5, False, f"Exception: {str(e)}")

    def test_compatibility_with_legacy_system(self):
        """Test that legacy admin_username system still works"""
        try:
            booking_data = {
                "nome": "Luigi Verdi",
                "canzone": "Nel blu dipinto di blu",
                "tonalita": "Re",
                "admin_username": "superadmin"  # Legacy system
            }
            
            response = requests.post(f"{self.api_url}/book", json=booking_data, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') == True and 'codice' in data:
                    return self.log_result("Legacy", True, f"Legacy admin_username system still works, codice: {data['codice']}")
                else:
                    return self.log_result("Legacy", False, f"Invalid legacy booking response: {data}")
            else:
                return self.log_result("Legacy", False, f"Legacy booking failed: {response.status_code} - {response.text}")
                
        except Exception as e:
            return self.log_result("Legacy", False, f"Exception: {str(e)}")

    def run_complete_test_sequence(self):
        """Run the complete test sequence as specified in the review request"""
        print("🔐 SECURE TOKEN SYSTEM - COMPREHENSIVE TEST")
        print("=" * 60)
        print("Testing sequence as specified in review request:")
        print("1. Admin login → 2. Generate token → 3. Validate token → 4. Book with token → 5. Close serata")
        print("=" * 60)
        
        # Execute test sequence
        success_count = 0
        total_tests = 0
        
        tests = [
            self.test_step_1_admin_login,
            self.test_step_2_generate_session_token,
            self.test_step_3_validate_token,
            self.test_step_3b_validate_invalid_token,
            self.test_step_4_booking_with_token,
            self.test_step_5a_create_serata,
            self.test_step_5_close_serata_and_invalidate_tokens,
            self.test_compatibility_with_legacy_system
        ]
        
        for test in tests:
            if test():
                success_count += 1
            total_tests += 1
        
        print("\n" + "=" * 60)
        print(f"📊 FINAL RESULTS: {success_count}/{total_tests} tests passed")
        print(f"Success Rate: {(success_count/total_tests)*100:.1f}%")
        
        # Detailed summary
        print("\n🔍 DETAILED SUMMARY:")
        for result in self.test_results:
            status = "✅" if result['success'] else "❌"
            print(f"{status} Step {result['step']}: {result['details']}")
        
        if success_count == total_tests:
            print("\n🎉 ALL TESTS PASSED! The secure token system is working correctly.")
            return True
        else:
            print(f"\n⚠️  {total_tests - success_count} test(s) failed. Review the issues above.")
            return False

def main():
    tester = TokenSystemTester()
    success = tester.run_complete_test_sequence()
    
    # Save results
    with open('/app/token_system_test_results.json', 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'success': success,
            'results': tester.test_results
        }, f, indent=2)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())