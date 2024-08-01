from flask import Flask, jsonify, render_template
from flask_cors import CORS
import ja


app = Flask(__name__)
CORS(app)  # Enable CORS for the Flask app


@app.route('/', methods=['GET'])
def get_jazz_album():

    jaotd = jazz_album_of_the_day.main()

    return render_template(
        'index.html',
        youtube_url=jaotd['youtube_url'],
        album=jaotd['album'],
        artist=jaotd['artist'])


if __name__ == '__main__':
    app.run(debug=False)
