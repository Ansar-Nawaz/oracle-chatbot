from app import app

if __name__ == "__main__":
    import os
    # Use the PORT from the environment or default to 5000 if not set.
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

