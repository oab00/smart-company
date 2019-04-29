from app import create_app
app = create_app()

import logging
log = logging.getLogger('werkzeug')
log.disabled = True
#print("Root Handlers:", log.hasHandlers())


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, use_reloader=True)
	