import os

def main():
    print("✅ Upload script started successfully.")
    secret = os.getenv("GOOGLE_CLIENT_SECRET")
    if secret:
        print("🔐 Found Google Client Secret in environment variables.")
    else:
        print("⚠️ No GOOGLE_CLIENT_SECRET found — please check repository secrets.")
    print("🚀 This is a test script. YouTube upload logic not yet implemented.")

if __name__ == "__main__":
    main()
