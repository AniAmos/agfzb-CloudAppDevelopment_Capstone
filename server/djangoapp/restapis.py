import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["docs"]
        # For each dealer object
        for dealer in dealers:
        # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)
    return results
        
# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    dealer_id = kwargs['dealer_id']
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealer_id)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result["docs"]
        # For each dealer object
        for review in reviews:            
            # Create a DealerReview object with values in `doc` object
            if review['purchase'] == True:
                review_obj = DealerReview(car_make=review["car_make"], car_model=review["car_model"],
                                    car_year=review["car_year"], dealership=review["dealership"],
                                    name=review["name"], purchase=review["purchase"],
                                    purchase_date=review["purchase_date"], review=review["review"],
                                    sentiment = analyze_review_sentiments(review["review"]))
                results.append(review_obj)
            else:
                review_obj = DealerReview(car_make='None', car_model='No car',
                                    car_year=0, dealership=review["dealership"],
                                    name=review["name"], purchase=review["purchase"],
                                    purchase_date='', review=review["review"],
                                    sentiment = analyze_review_sentiments(review["review"]))
                results.append(review_obj)
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealerreview):
    url = ''
    api_key = ''
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version = "2021-03-25", authenticator = authenticator)
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze(text = dealerreview, features = Features(sentiment = SentimentOptions()), language="en").get_result()
    sentiment_label = response["sentiment"]["document"]["label"]
    return sentiment_label