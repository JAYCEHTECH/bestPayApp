import requests

sms_message = "hi"

url = f"https://sms.arkesel.com/sms/api?action=send-sms&api_key=UmpEc1JzeFV4cERKTWxUWktqZEs&to=0275680647&from=BestPay&sms={sms_message}"


response = requests.request("GET", url)

print(response.text)
