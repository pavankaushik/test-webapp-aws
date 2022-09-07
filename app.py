from flask import Flask, render_template, request
from get_data_feed import get_feed_from_inshorts
import json
app = Flask(__name__)
@app.route('/', methods=["GET", "POST"])
def home():
    category = ""
    response_dict = {}
    if request.method == "POST":
        category = request.form.get('name')
        response_dict = get_feed_from_inshorts(category)
        return render_template('home.html',
                            data=json.dumps(response_dict['feed_date']) + " At " + json.dumps(response_dict['feed_time']),
                            author=response_dict['feed_author'],
                            title = response_dict['feed_title'],
                            description=response_dict['feed_content'],
                            url=response_dict['feed_url'],
                )
    else:
        response_dict = get_feed_from_inshorts()
        return render_template('home.html',
                            data=json.dumps(response_dict['feed_date']) + " At " + json.dumps(response_dict['feed_time']),
                            author=response_dict['feed_author'],
                            title = response_dict['feed_title'],
                            description=response_dict['feed_content'],
                            url=response_dict['feed_url'],
                )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)