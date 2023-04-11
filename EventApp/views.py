from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
import geocoder, pycountry
from geopy.geocoders import Nominatim
import json

from .conditions import get_venue_by_address, get_top_attraction, get_event_list, get_classification_search_result

def getCity(request):
    if request.method == 'POST':
        lat = request.POST.get('lat', '')
        long = request.POST.get('long', '')
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.reverse(str(lat)+","+str(long))
        address = location.raw['address']
        try:
            response = json.dumps({
                'status' : 'success',
                'state' : address.get("state",''),
                'city' : address.get("city",''),
                'country' : address.get("country",''),
                'district' : address.get("state_district",''),
            }, default=str)
            print("in get city function ===", response)
            request.session['city'] = address.get("city",'')
            country = address.get("country",'')
            country_code = pycountry.countries.get(name=country).alpha_2
            request.session['country_code'] = country_code
            return HttpResponse(response)

        except Exception as e:
            print("Exception is --------> ",e)
            return HttpResponse('{"status":"failure"}')
        
class Search_Event(View):

    # Get event suggestions from TicketMaster
    def get(self, request):
        city = request.session.get('city','')
        country_code = request.session.get('country_code','')
        print("city and country === ", city, country_code)
        venue_response = get_venue_by_address(city, country_code)
        attraction_response = get_top_attraction()
        return render(request, 'home.html', {'venue_list':venue_response['venue_list'], 'attraction_list':attraction_response['attraction_list']})
        

    # Search events based on search term and city
    def post(self, request):
        search_word = request.POST.get("search_word")
        search_city = request.POST.get("search_city")
        print("search word from form ========", search_word, search_city)
        search_response = get_event_list(search_word, search_city)
        if "error_message" in search_response:
            print("error_message in search event")
            return render(request, 'result.html',{"error_message":"No record found !!!!"})
        else:
            return render(request, 'result.html', {"response_event_list":search_response})
        
# Display events based on category selected
def get_category_event(request):
    classification_id = request.GET.get('id')
    print("Classification id for category selected ==== ",classification_id)
    search_response = get_classification_search_result(classification_id)
    if "error_message" in search_response:
        print("error_message in category event")
        return render(request, 'category.html',{"error_message":"No record found !!!!"})
    else:
        return render(request, 'category.html', {"response_event_list":search_response})




