def print_ads(url, token):
    ads = requests.get(
            url,
            headers={ "authorization": token }
        ).json()
    print(ads)
    for ad in ads["data"]:
        price = f"{ad['price']['value']:,}"
        print(
            f"┌{'─' * (len(ad['subject']) + 4)}┐\n" +
            colored(f"│ > {ad['subject']} │\n", attrs=['bold']) +

            #f"│ $ {price} {ad['price']['suffix']} ┌\
            #{'─' * (len(ad['subject']) + 4 - len(price)
            #- len(ad['price']['suffix']) - 6)}┘\n" +
            f"""│ $ {price} {ad['price']['suffix'] +
            ' ' * (len(ad['subject']) + 4 - len(price) -
            len(ad['price']['suffix']) - 4)}│\n""" +

            #f"└{'─' * (len(price) + len(ad['price']['suffix']) + 5)}\
            #┘\n" +
            f"└{'─' * (len(ad['subject']) + 4)}┘\n"
        )
        for line in ad['body'].split("\n"):
            print(f"┇ {line}")



def main():
    global requests
    import requests
    global colored
    from termcolor import colored
    query = input("Search: ")
    token = "Bearer " + requests.get(
        "https://www.blocket.se/api/adout-api-route/refresh-token-and-validate-session"
        ).json()["bearerToken"]

    categories_fetch = requests.get(
        f"https://api.blocket.se/classifieds/v2/ad_counters?include=all&q=\
        {query}&st=s",
        headers={ "authorization": token }
    )

    print(categories_fetch.json())

    category_names = []
    categories = {}
    for category in categories_fetch.json()["category_counters"]:
        category_names.append(category["label"])
        categories.update({category['label']: category['ad_counter']})

    print(
        f"{categories_fetch.json()['total_count']} resultat för '{query}':"
    )

    i = 1
    for category in category_names:
        print(f"{i}: " + category + ": " +
        " " * (len(max(category_names, key=len))-len(category)) + str(categories[category]))
        i += 1

    next_menu = input("Choose category (leave empty for all): ")

    if next_menu == "":
        print_ads(
            f"https://api.blocket.se/search_bff/v2/content?lim=40&\
            q={query}&st=s&status=active&gl=3&\
            include=extend_with_shipping", token
        )

    else:
        try:
            print_ads(
                f"""https://api.blocket.se{categories_fetch.json()
                ['category_counters'][int(next_menu) - 1]['api_query']}""",
                token
            )

        except ValueError:
            print(f"error: Must be a number")



if __name__ == "__main__": main()