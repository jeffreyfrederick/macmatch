from flask import Flask, render_template, request
from collections import defaultdict
import csv

app = Flask(__name__)

def load_displays():
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
            entry['source'] = 'Display'
            data.append(entry)
    return data

def load_boards():
    data = []
    with open('boards.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = []
        for row in reader:
            if not row or row[0].startswith("!"):
                continue
            if not headers:
                headers = row
                continue
            entry = dict(zip(headers, row))
            entry['source'] = 'Board'
            data.append(entry)
    return data

@app.route('/', methods=['GET', 'POST'])
def index():
    query = request.form.get('query', '').lower()
    display_data = load_displays()
    board_data = load_boards()
    all_data = display_data + board_data

    grouped_results = defaultdict(list)

    if query:
        for row in all_data:
            # Search all fields that exist in the row
            if any(query in str(value).lower() for value in row.values()):
                grouped_results[row.get('color', row['source'])].append(row)

    return render_template('index.html', grouped_results=grouped_results, query=query)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
