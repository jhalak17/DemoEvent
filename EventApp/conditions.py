import requests, json

def get_venue_by_address(city, country_code):
    try:
        print("Country code ========",country_code, type(country_code))
        url = "https://app.ticketmaster.com/discovery/v2/venues?apikey=7elxdku9GGG5k8j0Xm8KWdANDgecHMV0&locale=*&countryCode=" + country_code
        response = requests.request("GET", url)
        response_body = response.json()
        if "page" in response_body.keys():
            if response_body["page"]["totalElements"] == 0:
                print("### No record found ###")
                url = "https://app.ticketmaster.com/discovery/v2/venues?apikey=7elxdku9GGG5k8j0Xm8KWdANDgecHMV0&locale=*"
                response = requests.request("GET", url)
                response_body = response.json()
                response_list = response_body["_embedded"]["venues"]
                venue_list = []
                for venue in response_list:
                    try:
                        venue_name = venue['name']
                        venue_id = venue['id']
                        venue_image = venue['images']['url'] if 'images' in venue.keys() else ""
                        venue_upcoming_events = venue['upcomingEvents']['_total']
                        venue_list.append(dict(venue_name=venue_name, venue_id=venue_id, venue_image=venue_image, venue_upcoming_events=venue_upcoming_events))
                    except Exception as e:
                        print("Exception 1 ----->", e)
                        continue
                return {'error_message':'No record found','venue_list':venue_list}
        response_list = response_body["_embedded"]["venues"]
        venue_list = []
        for venue in response_list:
            try:
                venue_name = venue['name']
                venue_id = venue['id']
                venue_image = venue['images']['url'] if 'images' in venue.keys() else ""
                venue_upcoming_events = venue['upcomingEvents']['_total']
                venue_list.append(dict(venue_name=venue_name, venue_id=venue_id, venue_image=venue_image, venue_upcoming_events=venue_upcoming_events))
            except Exception as e:
                print("Exception 2 ----->", e)
                continue
        print(len(venue_list))
        return {'venue_list':venue_list}
    except Exception as e:
        print("Exception 3 --------> ",e)
        return {'error_message':'Exception'}
    
def get_top_attraction():
    try:
        url = "https://app.ticketmaster.com/discovery/v2/attractions?apikey=7elxdku9GGG5k8j0Xm8KWdANDgecHMV0&locale=*&sort=relevance,desc"
        response = requests.request("GET", url)
        response_body = response.json()
        if "page" in response_body.keys():
            if response_body["page"]["totalElements"] == 0:
                return {'error_message':'No record found'}
        response_list = response_body["_embedded"]["attractions"]
        attraction_list = []
        for attraction in response_list:
            attr_name = attraction['name']
            attr_id = attraction['id']
            attr_image = attraction['images'][0]['url'] if 'images' in attraction.keys() else ''
            attr_upcoming_events = attraction['upcomingEvents']['_total']
            attraction_list.append(dict(attr_name=attr_name, attr_id=attr_id, attr_image=attr_image, attr_upcoming_events=attr_upcoming_events))
        print("Length of attraction list ==", len(attraction_list))
        return {'attraction_list':attraction_list}
    except Exception as e:
        print("Exception 4 --------> ",e)
        return {'error_message':'Exception'}
    
def get_event_list(searchword, search_address):
    if not search_address:
        url = "https://app.ticketmaster.com/discovery/v2/events?apikey=7elxdku9GGG5k8j0Xm8KWdANDgecHMV0&locale=*&sort=date,asc&keyword="+searchword
        print(url)
        response = requests.request("GET", url)
        response_body = response.json()
    else:
        search_city = search_address.split(", ")[0]
        url = "https://app.ticketmaster.com/discovery/v2/events?apikey=7elxdku9GGG5k8j0Xm8KWdANDgecHMV0&locale=*&sort=date,asc&keyword="+searchword+"&city="+search_city
        print(url)
        response = requests.request("GET", url)
        response_body = response.json()
        if "page" in response_body.keys():
            if response_body["page"]["totalElements"] == 0:
                url = "https://app.ticketmaster.com/discovery/v2/events?apikey=7elxdku9GGG5k8j0Xm8KWdANDgecHMV0&locale=*&sort=date,asc&keyword="+searchword
                print(url)
                response = requests.request("GET", url)
                response_body = response.json()
                if "page" in response_body.keys():
                    if response_body["page"]["totalElements"] == 0:
                        return {"error_message":"No record found"}
    event_list = response_body["_embedded"]["events"]
    event_response_list = []
    for event in event_list:
        try:
            ticket_company = "Ticket Master"
            event_id = event["id"]
            event_name = event["name"]
            event_image = event["images"][1]["url"]
            event_date = event["dates"]["start"]["localDate"]
            event_url = event["url"]
            event_timezone = event["dates"]["timezone"] if "timezone" in event["dates"].keys() else "-"
            if "priceRanges" in event.keys():
                price_range = event["priceRanges"]
                min_price = price_range[0]["min"] 
                currency = price_range[0]["currency"] 
            else:
                min_price = "-"
                currency = "-"
            event_venue = event["_embedded"]["venues"] if "venues" in event["_embedded"].keys() else None
            venue_name = event_venue[0]["name"] if event_venue else "-"
            event_attraction = event["_embedded"]["attractions"] if "attractions" in event["_embedded"].keys() else None
            performer_name = event_attraction[0]["name"] if event_attraction else "-"
            event_response_list.append(dict(ticket_company=ticket_company,searchword=searchword, event_id=event_id, event_url=event_url, event_name=event_name, event_image=event_image, event_date=event_date, event_timezone=event_timezone, min_price=min_price, currency=currency, venue_name=venue_name, performer_name=performer_name))
        except:
            print("******** Exception 5 Occured ***************")
            continue

    return event_response_list

def get_classification_search_result(id):
    url = "https://app.ticketmaster.com/discovery/v2/events?apikey=7elxdku9GGG5k8j0Xm8KWdANDgecHMV0&locale=*&classificationId="+id
    response = requests.request("GET", url)
    response_body = response.json()
    if "page" in response_body.keys():
        if response_body["page"]["totalElements"] == 0:
            return {"error_message":"No record found !!!!"}
    event_list = response_body["_embedded"]["events"]
    event_response_list = []
    for event in event_list:
        try:
            ticket_company = "Ticket Master"
            event_id = event["id"]
            event_name = event["name"]
            event_image = event["images"][1]["url"]
            event_date = event["dates"]["start"]["localDate"]
            event_url = event["url"]
            event_timezone = event["dates"]["timezone"] if "timezone" in event["dates"].keys() else "-"
            if "priceRanges" in event.keys():
                price_range = event["priceRanges"]
                min_price = price_range[0]["min"] if 'min' in price_range[0].keys() else "-"
                currency = price_range[0]["currency"] if 'min' in price_range[0].keys() else "-"
            else:
                min_price = "-"
                currency = "-"
            event_venue = event["_embedded"]["venues"] if "venues" in event["_embedded"].keys() else None
            venue_name = event_venue[0]["name"] if event_venue else "-"
            event_attraction = event["_embedded"]["attractions"] if "attractions" in event["_embedded"].keys() else None
            performer_name = event_attraction[0]["name"] if event_attraction else "-"
            event_response_list.append(dict(ticket_company=ticket_company, event_id=event_id, event_url=event_url, event_name=event_name, event_image=event_image, event_date=event_date, event_timezone=event_timezone, min_price=min_price, currency=currency, venue_name=venue_name, performer_name=performer_name))
        except Exception as e:
            print("Exception 6 ----->", e)
            continue

    return event_response_list

