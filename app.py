from flask import Flask, render_template
from jobspy import scrape_jobs
import os

app = Flask(__name__)

@app.route("/")
def index():
    jobs = scrape_jobs(
        site_name=["indeed", "linkedin", "zip_recruiter", "glassdoor", "google", "bayt", "naukri"],
        search_term="software engineer",
        google_search_term="software engineer jobs near San Francisco, CA since yesterday",
        location="San Francisco, CA",
        results_wanted=20,
        hours_old=72,
        country_indeed='USA',
    )
    job_list = jobs.to_dict(orient='records')
    return render_template("index.html", jobs=job_list)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
