from flask import Flask, render_template, request
from collections import defaultdict
import csv

app = Flask(__name__)

def load_data():
    data = []

    # Load displays
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
            entry['tag'] = 'MacBook Display'
            data.append(entry)

    # Load macminis
    with open('macminis.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = []
        for row in reader:
            if not row or row[0].startswith("!"):
                continue
            if not headers:
                headers = row
                continue
            entry = dict(zip(headers, row))
            entry['tag'] = 'Mac Mini'
            # Optionally set a 'color' to prevent key errors
            if 'color' not in entry:
                entry['color'] = 'Unknown'
            data.append(entry)

    return data

@app.route('/', methods=['GET', 'POST'])
def index():
    query = ' '.join(request.form.get('query', '').strip().lower().split())
    data = load_data()
    grouped_results = defaultdict(list)

    if query:
        for row in data:
            searchable_values = [row.get(key, '').lower() for key in row]
            if any(query in value for value in searchable_values):
            # Group by tag first, then color
                group_key = (row['tag'], row.get('color', 'Unknown'))
                grouped_results[group_key].append(row)

    return render_template('index.html', grouped_results=grouped_results, query=query)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)