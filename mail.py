from re import T
import requests
import env_config
# from bs4 import BeautifulSoup as bs


def send_mail(mail):
    html_obj = open('templates/pass.html')
    # soup = bs(html_obj, 'html.parser')
    t = requests.post(
        "https://api.eu.mailgun.net/v3/" + env_config.mailgun_domain + "/messages",
        auth=("api", env_config.mailgun_key),
        data={"from": "Excited User <mailgun@" + env_config.mailgun_domain + ">",
                "to": [mail],
                "subject": "Hi",
                "text": "Hi",
                "html": html_obj})

    print(t.reason)
    print(t.status_code)
