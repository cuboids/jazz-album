from flask import Blueprint, jsonify, render_template

import app.ja as ja

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET'])
def get_jazz_album():
    jaotd = ja.main()
    return render_template(
        'index.html',
        youtube_url=jaotd['youtube_url'],
        album=jaotd['album'],
        artist=jaotd['artist']
    )
