import requests

r = requests.get("http://localhost:8081/job/TestJob/4/consoleText", auth=('admin', 'admin'))


print(r)
print(r.text)