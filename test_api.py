import urllib.request
import urllib.error
import urllib.parse
import json
import time

base_url = "https://web-production-31bbb.up.railway.app/api"
test_reg = "AGENT" + str(int(time.time()))

def post_json(url, data, headers=None):
    if headers is None:
        headers = {}
    headers['Content-Type'] = 'application/json'
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req) as response:
            return response.status, response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8')

print(f"Signing up {test_reg}...")
status, body = post_json(f"{base_url}/signup", {
    "name": "Test Agent",
    "regNo": test_reg,
    "password": "password"
})
print("Signup:", status, body[:200])

if status == 201:
    token = json.loads(body).get("token")
    print("\nCreating ticket...")
    try:
        status2, body2 = post_json(f"{base_url}/tickets/create", 
            {
                "name": "Test Agent", 
                "regNo": test_reg, 
                "query": "i want to change my hostel"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        print("Ticket creation status:", status2)
        print("Ticket creation response:", body2[:1000])
    except Exception as e:
        print("Error during ticket creation:", e)
else:
    print("Could not signup.")
