from phrase_book import app

if __name__ == '__main__':

    # Start the web server
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=False
    )
