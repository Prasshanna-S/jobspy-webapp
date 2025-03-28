from flask import Flask, render_template, request
from jobspy import scrape_jobs
import threading
import webbrowser
import time

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    jobs = []
    if request.method == "POST":
        search_term = request.form.get("search_term")
        location = request.form.get("location")
        hours_old = int(request.form.get("hours_old", 72))
        results_wanted = int(request.form.get("results_wanted", 20))
        site_name = request.form.getlist("site_name")

        google_search_term = None
        if "google" in site_name:
            google_search_term = f"{search_term} jobs near {location} since yesterday"

        try:
            jobs_df = scrape_jobs(
                site_name=site_name,
                search_term=search_term,
                google_search_term=google_search_term,
                location=location,
                results_wanted=results_wanted,
                hours_old=hours_old,
                country_indeed='USA',
            )
            jobs = jobs_df.to_dict(orient="records")
        except Exception as e:
            print("Scraping error:", e)

    return render_template("index.html", jobs=jobs)

def run_server():
    app.run(host="127.0.0.1", port=8080, debug=False)

if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    time.sleep(1.5)  # Allow server to spin up
    webbrowser.open("http://127.0.0.1:8080")
    while True:
        pass  # Keep the app alive (or replace with app loop logic)
