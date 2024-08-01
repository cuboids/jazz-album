import os
from flask import Flask, jsonify, render_template
from flask_cors import CORS
import ja

app = Flask(__name__)
CORS(app)  # Enable CORS for the Flask app

@app.route('/', methods=['GET'])
def get_jazz_album():
    jaotd = ja.main()
    return render_template(
        'index.html',
        youtube_url=jaotd['youtube_url'],
        album=jaotd['album'],
        artist=jaotd['artist']
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
