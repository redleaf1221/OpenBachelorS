from src.app import app

if __name__ == "__main__":
    app.run(
        host="192.168.1.10",
        port=8443,
        debug=True,
    )
