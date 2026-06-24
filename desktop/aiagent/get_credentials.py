#!/usr/bin/env python3
"""
Script to get NeuralAgent credentials for desktop client
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def get_credentials(email, password, thread_title="Desktop Agent Thread"):
    """Get access token and create a thread"""
    
    try:
        # Step 1: Login to get access token
        print(f"🔐 Authenticating with {email}...")
        login_response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": email, "password": password}
        )
        
        if login_response.status_code != 200:
            print(f"❌ Login failed: {login_response.text}")
            return None, None
        
        login_data = login_response.json()
        access_token = login_data.get("access_token")
        print(f"✅ Login successful!")
        print(f"📌 Access Token: {access_token}")
        
        # Step 2: Create a thread
        print(f"\n📝 Creating thread: '{thread_title}'...")
        thread_response = requests.post(
            f"{BASE_URL}/threads",
            headers={"Authorization": f"Bearer {access_token}"},
            json={"title": thread_title}
        )
        
        if thread_response.status_code not in [200, 201]:
            print(f"❌ Thread creation failed: {thread_response.text}")
            return access_token, None
        
        thread_data = thread_response.json()
        thread_id = thread_data.get("id")
        print(f"✅ Thread created!")
        print(f"📌 Thread ID: {thread_id}")
        
        return access_token, thread_id
        
    except requests.exceptions.ConnectionError:
        print(f"❌ Could not connect to {BASE_URL}")
        print("   Make sure your backend server is running!")
        return None, None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None, None

if __name__ == "__main__":
    print("=" * 50)
    print("  NeuralAgent Desktop Credentials Helper")
    print("=" * 50)
    
    email = input("\n📧 Enter your email: ").strip()
    password = input("🔑 Enter your password: ").strip()
    
    access_token, thread_id = get_credentials(email, password)
    
    if access_token and thread_id:
        print("\n" + "=" * 50)
        print("✅ SUCCESS! Add these to your .env file:")
        print("=" * 50)
        print(f'NEURALAGENT_API_URL=http://localhost:8000')
        print(f'NEURALAGENT_THREAD_ID={thread_id}')
        print(f'NEURALAGENT_USER_ACCESS_TOKEN={access_token}')
        print("=" * 50)
    else:
        print("\n❌ Failed to get credentials. Please check:")
        print("   1. Backend server is running on http://localhost:8000")
        print("   2. Email and password are correct")
        sys.exit(1)
