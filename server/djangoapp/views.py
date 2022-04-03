from cgitb import text
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
from .restapis import get_dealers_from_cf, get_request, get_dealers_from_cf, get_dealer_by_id_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
# def login_request(request):
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/obentech%40gmail.com_dev/car-dealership/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        output = "";
        for dealer in dealerships:
            template = "<h3>Dealer Full Name:" + dealer.full_name + "</h3>" + \
                    "Dealer city:" + str(dealer.city) + "<br>" + \
                    "Dealer address:" + dealer.address + "<br>" + \
                    "Dealer id:" + str(dealer.id) + "<br>" + \
                    "Location lat:" + str(dealer.lat) + "<br>" + \
                    "Location long:" + str(dealer.long) + "<br>" + \
                    "Dealer short name:" + str(dealer.short_name) + "<br>" + \
                    "Dealer state:" + str(dealer.st) + "<br>" + \
                    "Dealer zip:" + str(dealer.zip) + "<br><hr>";
            output += template;
        
        #dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(output)



# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        context = {}
        dealer_url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/obentech%40gmail.com_dev/car-dealership/get-dealership"
        dealers = get_dealer_by_id_from_cf(dealer_url, id=dealer_id)
        
        context["dealerId"] = dealer_id
    
        review_url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/obentech%40gmail.com_dev/car-dealership/review"
        reviews = get_dealer_reviews_from_cf(review_url, id=dealer_id)
        context["reviews"] = reviews
        
        output = "";
        for review in reviews:
            template = "<h3>Name:" + review.name + "</h3>" + \
                    "Dealership:" + str(review.dealership) + "<br>" + \
                    "Name:" + review.name + "<br>" + \
                    "Purchase:" + str(review.purchase) + "<br>" + \
                    "Purchase Date:" + str(review.purchase_date) + "<br>" + \
                    "Car Make:" + str(review.car_make) + "<br>" + \
                    "Car Model:" + str(review.car_model) + "<br>" + \
                    "Car Year:" + str(review.car_year) + "<br>" + \
                    "Sentiment:" + review.sentiment + "<br>" + \
                    "Id:" + str(review.id) + "<br><hr>";
            output += template;
        
        #review_names = ' '.join([review.name for review in reviews])
        # Return a list of dealer short name
        return HttpResponse(output);
        
        #return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, id):
    context = {}
    dealer_url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/obentech%40gmail.com_dev/car-dealership/get-dealership"
    dealer = get_dealer_by_id_from_cf(dealer_url, id=id)
    context["dealer"] = dealer
    if request.method == 'GET':
        # Get cars for the dealer
        cars = CarModel.objects.filter(id=id)
        print(cars)
        context["cars"] = cars
        
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        if request.user.is_authenticated:
            username = request.user.username
            print(request.POST)
            review = dict()
            car_id = request.POST["car"]
            car = CarModel.objects.get(pk=car_id)
            review["time"] = datetime.utcnow().isoformat()
            review["name"] = username
            review["dealership"] = id
            review["id"] = id
            review["review"] = request.POST["content"]
            review["purchase"] = False
            if "purchasecheck" in request.POST:
                if request.POST["purchasecheck"] == 'on':
                    review["purchase"] = True
            review["purchase_date"] = request.POST["purchasedate"]
            review["car_make"] = car.make.name
            review["car_model"] = car.name
            review["car_year"] = int(car.year.strftime("%Y"))

            json_payload = {}
            json_payload["review"] = review
            review_post_url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/obentech%40gmail.com_dev/car-dealership/review"
            
            json_result = post_request(review_post_url, json_payload, dealerId=id)
            print('Add Review Result:', json_result)
        return redirect("djangoapp:dealer_details", id=id)

