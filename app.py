from flask import Flask, render_template, request
from collections import defaultdict
import csv

app = Flask(__name__)

def load_data():
    data = []
    with open('displays.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = []
        for row in reader:
            if not row or row[0].startswith("!"):
                continue
            if not headers:
                headers = row
                continue
            entry = dict(zip(headers, row))
            data.append(entry)
    return data

@app.route('/', methods=['GET', 'POST'])
def index():
    query = request.form.get('query', '').lower()
    data = load_data()
    grouped_results = defaultdict(list)

    if query:
        for row in data:
            if (
                query in row['code#'][:5].lower() or
                query in row['part#'].lower() or
                query in row['release'].lower() or
                query in row['model#'].lower() or
                query in row['cpu'].lower() or
                query in row['emc'].lower() or
                query in row['size'].lower() or
                query in row['color'].lower()
            ):
                grouped_results[row['color']].append(row)

    return render_template('index.html', grouped_results=grouped_results, query=query)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
