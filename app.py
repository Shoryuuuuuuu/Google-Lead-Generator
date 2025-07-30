from flask import Flask, render_template, request, send_file
from scraper import scrape_google
import pandas as pd
import io

app = Flask(__name__)
scraped_data = []

@app.route('/', methods=['GET', 'POST'])
def index():
    global scraped_data
    scraped_data = []

    if request.method == 'POST':
        keyword = request.form['keyword']
        scraped_data = scrape_google(keyword, pages=2)
        scraped_data.sort(key=lambda x: x['Score'], reverse=True)  # Sort by Score descending

    return render_template('index.html', data=scraped_data)

@app.route('/download')
def download_csv():
    if not scraped_data:
        return "No data to download"

    df = pd.DataFrame(scraped_data)
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)

    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name='results.csv'
    )

if __name__ == '__main__':
    app.run(debug=True)