import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

app = create_app()

# Add this line to handle trailing slashes consistently
app.url_map.strict_slashes = False

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)