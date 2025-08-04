from flask import Flask, render_template, request, send_file
from scraper import scrape_google
import pandas as pd
import io
import math

app = Flask(__name__)
scraped_data = []

ITEMS_PER_PAGE = 10

@app.route('/', methods=['GET', 'POST'])
def index():
    global scraped_data
    page = int(request.args.get('page', 1))

    if request.method == 'POST':
        keyword = request.form['keyword']
        scraped_data = scrape_google(keyword, pages=2)
        scraped_data.sort(key=lambda x: x['Score'], reverse=True)

    total_items = len(scraped_data)
    total_pages = math.ceil(total_items / ITEMS_PER_PAGE)
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    page_data = scraped_data[start:end]

    return render_template('index.html', data=page_data, page=page, total_pages=total_pages)

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

@app.route('/download-selected', methods=['POST'])
def download_selected():
    selected_ids = request.form.getlist('selected_ids')
    if not scraped_data or not selected_ids:
        return "No data to download"

    selected_data = [scraped_data[int(i)] for i in selected_ids]
    df = pd.DataFrame(selected_data)
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)

    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name='selected_results.csv'
    )

if __name__ == '__main__':
    app.run(debug=True)