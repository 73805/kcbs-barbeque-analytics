import requests
import pickle

with open('pkls/contest_links.pkl', 'rb') as f:
    contest_links = pickle.load(f)

for i, link in enumerate(contest_links):
    res = requests.get(link)
    if res.status_code == requests.codes.ok:
        fn = link.split('/')
        fn = fn[-2] + "-" + fn[-1]
        fn = "contest_html/" + fn + ".html"
        with open(fn, 'wb') as fd:
            for chunk in res.iter_content(chunk_size=100000):
                fd.write(chunk)
        print "Done Writing:", i
    else:
        print "Request error!"
        print link
        break
