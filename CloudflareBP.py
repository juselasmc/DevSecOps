import requests, json, csv
from socket import *
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# api token, read only token should be enough
api_token = "PUT HER YOUR API TOKEN"
zone_id = "PUR HERE YOUR ZONE ID"

page_no =  1
total_pages = 1

url = 'https://api.cloudflare.com/client/v4/zones/' + zone_id + '/dns_records'
headers = json.loads('{"Authorization": "Bearer %s", "Content-Type": "application/json"}' % api_token)
jsondata = []

while (page_no <= total_pages) :
    params =  json.loads('{"page": '+ str(page_no) +', "per_page": 20, "type": "A", "order": "name", "direction": "desc"}')
    r = requests.get(url, params=params, headers=headers)
    resp = r.json()
    total_pages = resp["result_info"]["total_pages"]
    page_no = resp["result_info"]["page"] + 1
    for element in resp["result"]:
        s = socket(AF_INET, SOCK_STREAM)
        s.settimeout(2)
        conn = s.connect_ex((element["content"], 443))
        if (conn == 0) :
            element["DTO"] = {"TCP": "YES", "HTTP": "NO"}
            s.close()
            try:
                req = requests.get('https://%s/' %element["content"], headers={'Host': '%s' %element["name"]}, verify=False, allow_redirects=False, timeout=1)
                element["DTO"]["HTTP"] = req.status_code
            except requests.exceptions.RequestException as e:
                element["DTO"]["HTTP"] = "ConnectionResetError"
        else:
            element["DTO"] = {"TCP": "NO", "HTTP": "NO"}
            s.close()
    jsondata += resp["result"]

#print(jsondata)

fieldnames = []
for element in jsondata:
    for key in element:
        if key not in fieldnames:
            fieldnames.append(key)


data_file = open('RECORDS.csv', 'w', newline='')
csv_writer = csv.DictWriter(data_file, fieldnames=fieldnames)
csv_writer.writeheader()
for data in jsondata:
    csv_writer.writerow(data)
 
data_file.close()
