import requests
token = requests.get("https://www.blocket.se/api/adout-api-route/refresh-token-and-validate-session").json()["bearerToken"]
token = "Bearer " + token
response = requests.get(
    "https://api.blocket.se/search_bff/v2/content?lim=0&q=ktm&st=s&status=active&include=extend_with_shipping",
    headers={ "authorization": token }
)

response2 = requests.get(
    "https://api.blocket.se/marketing/v1/inventory?q=ktm&st=s&view=list",
    headers={ "authorization": token }
)

opts = requests.options("https://api.blocket.se/marketing/v1/inventory?q=ktm&st=s&view=list")
categories_fetch = requests.get(
    "https://api.blocket.se/classifieds/v2/ad_counters?include=all&q=ktm&st=s",
    headers={ "authorization": token }
)

category_names = []
categories = {}
for category in categories_fetch.json()["category_counters"]:
    category_names.append(category["label"])
    categories.update({category['label']: category['ad_counter']})

print(f"{response.json()['total_count']} resultat för '{response.json()['inventory']['context']['afs']['query']}':")

max = len(max(category_names, key=len))
for category in category_names:
    print(category + ": " + " " * (max-len(category)) + str(categories[category]))


