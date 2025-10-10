import requests
import time

# --- CONFIGURATION ---
BACKEND_URL = "https://cognidocbackend.onrender.com"
MAX_RETRIES = 15  # Increased retries for more patience
RETRY_DELAY_SECONDS = 15 # Increased delay between attempts

def wake_up_server_patiently():
    """
    Pings the server repeatedly, ignoring 502 errors which are common
    during a cold start on services like Render.
    """
    print(f"Attempting to wake up the backend at: {BACKEND_URL}")
    print("This may take several minutes. 502 errors are expected while the server starts.")

    start_time = time.time()

    for attempt in range(MAX_RETRIES):
        print(f"\n--- Attempt {attempt + 1} of {MAX_RETRIES} ---")
        try:
            response = requests.get(BACKEND_URL, timeout=30)

            # If we get a 502 error, treat it as "still starting" and continue the loop
            if response.status_code == 502:
                print("   Status: 502 Bad Gateway. Server is likely still starting up.")
                if attempt < MAX_RETRIES - 1:
                    print(f"   Retrying in {RETRY_DELAY_SECONDS} seconds...")
                    time.sleep(RETRY_DELAY_SECONDS)
                    continue
                else:
                    # Last attempt also resulted in 502
                    raise requests.exceptions.HTTPError("Server stuck in a 502 state.")

            # Any other error code (4xx, 5xx) will raise an exception
            response.raise_for_status()
            
            # If we get here, it means we got a 200 OK!
            end_time = time.time()
            total_duration = end_time - start_time
            print("\n✅ Success! The backend is awake and responding.")
            print(f"   Status Code: {response.status_code}")
            print(f"   Response: {response.json()}")
            print(f"   Total time to wake up: {total_duration:.2f} seconds.")
            return

        except requests.exceptions.RequestException as e:
            print(f"   Attempt failed with connection error: {e}")
            if attempt < MAX_RETRIES - 1:
                print(f"   Retrying in {RETRY_DELAY_SECONDS} seconds...")
                time.sleep(RETRY_DELAY_SECONDS)

    # This part is reached only if all retries fail
    end_time = time.time()
    total_duration = end_time - start_time
    print(f"\n❌ Failed to wake up the server after {MAX_RETRIES} attempts ({total_duration:.2f} seconds).")

if __name__ == "__main__":
    wake_up_server_patiently()
