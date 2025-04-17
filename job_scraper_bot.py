import requests
from bs4 import BeautifulSoup
import pandas as pd
import smtplib
from email.message import EmailMessage

# ========== PART 1: SCRAPE JOBS ==========

print("🔍 Scraping jobs...")

url = "https://remoteok.com/remote-dev-jobs"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

jobs = []
for job_elem in soup.find_all("tr", class_="job"):
    title = job_elem.find("h2", {"itemprop": "title"})
    company = job_elem.find("h3", {"itemprop": "name"})
    location = job_elem.find("div", class_="location")
    link = job_elem.get("data-href")

    if title and company:
        jobs.append({
            "Title": title.text.strip(),
            "Company": company.text.strip(),
            "Location": location.text.strip() if location else "Remote",
            "Link": f"https://remoteok.com{link}"
        })

df = pd.DataFrame(jobs)
df.to_csv("jobs.csv", index=False)

print(f"✅ Scraped {len(jobs)} jobs and saved to jobs.csv")


# ========== PART 2: EMAIL THE CSV ==========

print("📧 Sending email...")

EMAIL_ADDRESS = "hc96877@gmail.com"
EMAIL_PASSWORD = "ehcs rofm spvt hjyx"  # Use your generated App Password
TO_EMAIL = "patil.ankit1494@gmail.com"    # Set your destination email here

msg = EmailMessage()
msg["Subject"] = "Latest Job Listings"
msg["From"] = EMAIL_ADDRESS
msg["To"] = TO_EMAIL
msg.set_content("Attached is the latest job listing CSV file.")

# Attach CSV
with open("jobs.csv", "rb") as f:
    msg.add_attachment(f.read(), maintype="application", subtype="octet-stream", filename="jobs.csv")

# Send Email
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)

print("✅ Email sent successfully!")
