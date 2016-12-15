import requests
import pprint
from bs4 import BeautifulSoup


HOME_URL = "https://www.evaluabk.com/"
DEBUG = False

if DEBUG:
    pp = pprint.PrettyPrinter(indent=2)


# Recibe el objeto de `bs4` asociado al <form> que se debe enviar y construye
# payload que se debe enviar.
def form_to_empty_payload(form):
    payload = {}
    inputs = form.find_all("input") + form.find_all("select")
    for input_ in inputs:
        if input_.get("type") in ("hidden", "submit"):
            payload[input_.get("name")] = input_.get("value")
        else:
            payload[input_.get("name")] = None
    payload["JavaScriptEnabled"] = 1
    return payload


def main():
    session = requests.Session()
    current = session.get(HOME_URL)

    while not current.url.startswith(HOME_URL + "Finish.aspx"):
        soup = BeautifulSoup(current.content, "html.parser")
        form_object = soup.find(id="surveyEntryForm") or soup.find(id="surveyForm")
        next_url = HOME_URL + form_object.get("action")
        payload = form_to_empty_payload(form_object)

        if DEBUG:
            print("Posting to {}...".format(next_url))
            pp.pprint(payload)

        current = session.post(next_url, data=payload)

        if DEBUG:
            with open("last.html", "w") as last_dump:
                last_dump.write(current.text)

    soup = BeautifulSoup(current.content, "html.parser")
    print(soup.find(class_="ValCode").string)

if __name__ == "__main__":
    main()
