import os
from src import app

# Checks if the run.py file has executed directly and not imported
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Default to port 10000 if PORT is not set
    app.run(debug=True, host='0.0.0.0', port=port)
