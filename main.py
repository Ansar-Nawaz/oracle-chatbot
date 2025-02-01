from app import app
import os

if __name__ == "__main__":
    # Retrieve the PORT environment variable set by Railway; default to 5000 if not set
    port = int(os.environ.get("PORT", 5000))
    # Run the app, listening on all network interfaces (0.0.0.0) on the specified port
    app.run(host="0.0.0.0", port=port)

