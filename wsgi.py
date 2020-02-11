import os

if __name__ == "__main__":
    port = int(os.environ.get('PORT', app.config['SERVER_PORT']))
    app.run(debug=app.config['DEBUG'], host=app.config['SERVER_IP'], port=port)
