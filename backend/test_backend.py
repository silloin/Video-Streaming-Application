import requests
import sys

BASE_URL = "http://localhost:5000"

def test_flow():
    print("Testing Backend Flow...")
    
    # 1. Signup
    email = "test@example.com"
    password = "password123"
    
    # Clean up potentially if needed, or just handle duplicate
    signup_payload = {"name": "Tester", "email": email, "password": password}
    try:
        r = requests.post(f"{BASE_URL}/auth/signup", json=signup_payload)
        if r.status_code == 201:
            print("[PASS] Signup Success")
            token = r.json()["token"]
        elif r.status_code == 400 and "already exists" in r.text:
            print("[INFO] User exists, logging in...")
            r = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
            if r.status_code == 200:
                print("[PASS] Login Success")
                token = r.json()["token"]
            else:
                print(f"[FAIL] Login failed: {r.text}")
                return
        else:
            print(f"[FAIL] Signup failed: {r.text}")
            return
    except requests.exceptions.ConnectionError:
        print("[FAIL] creating connection to backend. Is it running?")
        return

    # 2. Get Me
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    if r.status_code == 200:
        print("[PASS] Get Me Success")
    else:
        print(f"[FAIL] Get Me failed: {r.text}")

    # 3. Dashboard
    r = requests.get(f"{BASE_URL}/dashboard")
    if r.status_code == 200:
        videos = r.json()
        if len(videos) == 2:
            print("[PASS] Dashboard returned 2 videos")
            if "youtube_id" not in videos[0]:
                print("[PASS] YouTube ID is hidden")
            else:
                print("[FAIL] YouTube ID EXPOSED!")
        else:
            print(f"[FAIL] Dashboard returned {len(videos)} videos")
    else:
        print(f"[FAIL] Dashboard failed: {r.text}")

    # 4. Stream
    video_id = videos[0]["id"]
    r = requests.get(f"{BASE_URL}/video/{video_id}/stream", headers=headers)
    if r.status_code == 200:
        stream_url = r.json().get("stream_url")
        if "token=" in stream_url:
            print(f"[PASS] Stream URL generated: {stream_url}")
            
            # 5. Fetch Player Page
            # The URL might be http://localhost:5000/player...
            r_player = requests.get(stream_url)
            if r_player.status_code == 200 and "<iframe" in r_player.text:
                print("[PASS] Player page content verified")
            else:
                print(f"[FAIL] Player page failed: {r_player.status_code}")
        else:
            print("[FAIL] Stream URL missing token")
    else:
        print(f"[FAIL] Stream Endpoint failed: {r.text}")

if __name__ == "__main__":
    test_flow()
