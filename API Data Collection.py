import time
from pathlib import Path
import requests

Ciks= {
    "intel": "0000050863",
    "amd": "0001045810",
    "nvidia": "0000002488"
}

base_dir=Path("data/raw")
start_yr=2021

HEADERS = {
    "User-Agent": "J Zhou jzhou34@vols.utk.edu",
    "Accept-Encoding": "gzip, deflate",
}

session = requests.Session()
session.headers.update(HEADERS)


def download_filings(company, cik):
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    response = session.get(url, timeout=30)
    response.raise_for_status()
    submissions = response.json()["filings"]["recent"]

    for i, form in enumerate(submissions["form"]):
        if form not in ("10-K", "10-Q"):
            continue

        filing_date = submissions["filingDate"][i]
        if int(filing_date[:4]) < start_yr:
            continue

        accession = submissions["accessionNumber"][i]
        document = submissions["primaryDocument"][i]
        accession_clean = accession.replace("-", "")

        filing_url = (
            f"https://www.sec.gov/Archives/edgar/data/"
            f"{int(cik)}/{accession_clean}/{document}"
        )

        folder = base_dir / company / form
        folder.mkdir(parents=True, exist_ok=True)

        filename = f"{filing_date}_{accession}_{document}"
        output = folder / filename

        if output.exists():
            continue

        try:
            result = session.get(filing_url, timeout=30)
            result.raise_for_status()
            output.write_bytes(result.content)
            print(f"Downloaded: {company} {form} {filing_date}")
        except requests.RequestException as error:
            print(f"Failed: {filing_url} | {error}")

        time.sleep(0.15)


for company, cik in Ciks.items():
    download_filings(company, cik)

print("Download Finished.")
