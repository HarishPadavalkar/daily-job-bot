import requests, smtplib, datetime, os
from email.mime.text import MIMEText

GMAIL_USER = os.environ["GMAIL_USER"]
GMAIL_APP_PASS = os.environ["GMAIL_APP_PASS"]
TO_EMAIL = os.environ["TO_EMAIL"]

KEYWORDS = ["project","program","operations","manager","lead","head","director"]

def fetch_remotive():
    r = requests.get("https://remotive.com/api/remote-jobs")
    jobs=[]
    for j in r.json()["jobs"]:
        if any(k in j["title"].lower() for k in KEYWORDS):
            jobs.append(f'{j["title"]}\n{j["url"]}\n')
    return jobs

def fetch_adzuna():
    url="https://api.adzuna.com/v1/api/jobs/in/search/1?app_id=demo&app_key=demo&what=manager&content-type=application/json"
    r=requests.get(url)
    jobs=[]
    for j in r.json()["results"]:
        jobs.append(f'{j["title"]}\n{j["redirect_url"]}\n')
    return jobs

def send_email(jobs):
    body="\n".join(jobs[:30])
    msg=MIMEText(body)
    msg["Subject"]=f"Daily Manager Jobs – {datetime.date.today()}"
    msg["From"]=GMAIL_USER
    msg["To"]=TO_EMAIL
    s=smtplib.SMTP("smtp.gmail.com",587)
    s.starttls()
    s.login(GMAIL_USER,GMAIL_APP_PASS)
    s.send_message(msg)
    s.quit()

if __name__=="__main__":
    send_email(fetch_remotive()+fetch_adzuna())
