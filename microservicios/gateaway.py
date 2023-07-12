from flask import Flask
from flask import request, jsonify
import urllib.request, json
import concurrent.futures

app = Flask(__name__)

@app.route('/report')
def report_by_country():
    country_arg = request.args.get('country')

    with concurrent.futures.ThreadPoolExecutor() as executor:
        president_future = executor.submit(fetch_data, 'http://127.0.0.1:6103/', country_arg)
        pbi_future = executor.submit(fetch_data, 'http://127.0.0.1:6102/', country_arg)
        holiday_future = executor.submit(fetch_data, 'http://127.0.0.1:6101/', country_arg)

        president_response = president_future.result()
        pbi_response = pbi_future.result()
        holiday_response = holiday_future.result()

    list_presidentes = json.loads(president_response)
    list_pbi = json.loads(pbi_response)
    list_holiday = json.loads(holiday_response)

    report = Report(country_arg, list_pbi['pbi'], list_presidentes['president'], list_holiday)
    return jsonify(report.to_json())


def fetch_data(url, country_arg):
    full_url = f"{url}?country={country_arg}"
    with urllib.request.urlopen(full_url) as response:
        data = response.read()
    return data


class Report:
    def __init__(self, country, pbi, presidente, feriados):
        self.country = country
        self.pbi = pbi
        self.presidente = presidente
        self.feriados = feriados

    def to_json(self):
        return {
            "Country": self.country,
            "PBI": self.pbi,
            "Presidente": self.presidente,
            "Feriados" : self.feriados
        }


if __name__ == "__main__":
    app.run(debug=True, port=6105)
