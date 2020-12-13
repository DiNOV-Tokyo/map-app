from flask import Flask, redirect, render_template

from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import csv
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# URLの指定
html = urlopen("https://www.latlong.net/category/airports-236-19.html")
bsObj = BeautifulSoup(html, "html.parser")

# テーブルを指定
table = bsObj.findAll("table")[0]
rows = table.findAll("tr")
data = []

# Flaskインスタンス
app = Flask(__name__)

# URLのルーティング 
@app.route('/')
def index():

    with open("data.csv", "w", encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in rows:
            csvRow = []
            for cell in row.findAll(['td', 'th']):
                csvRow.append(cell.get_text())
            data.append(csvRow)
            writer.writerow(csvRow)


    json_list = []

    # CSV ファイルの読み込み
    with open('data.csv', 'r') as f:
        for row in csv.DictReader(f):
            json_list.append(row)

    # JSON ファイルへの書き込み
    with open('output.json', 'w') as f:
        json.dump(json_list, f)
    
    # JSONファイルのロード
    with open('output.json', 'r') as f:
        json_output = json.load(f)
    
    # htmlのレンダリング
    return render_template('osm_map.html', data = json_output)
    
    
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
