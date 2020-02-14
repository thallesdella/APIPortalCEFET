from apicefet import create_app
from sys import argv
import os

if __name__ == "__main__":
    env = 'develop' if len(argv) == 1 else argv[1]
    app = create_app(env)

    port = int(os.environ.get('PORT', app.config['SERVER_PORT']))
    app.run(debug=app.config['DEBUG'], host=app.config['SERVER_IP'], port=port)
