from flask import Blueprint, jsonify, session, request
from app.models import User, db, Spot

from flask_login import current_user, login_user, logout_user, login_required

spot_routes = Blueprint('spot', __name__)



@spot_routes.route('/')
def get_all_spots():
    spots_list = Spot.query.all()
    return_list = []
    default_img = "https://images.pexels.com/photos/186077/pexels-photo-186077.jpeg?cs=srgb&dl=pexels-binyamin-mellish-186077.jpg&fm=jpg"
    for spot in spots_list:
        #Turn spots into dictionaries
        spot_dict = spot.to_dict()
        #Initialize the rating
        rating = 0
        #Get all associated reviews and their rating
        spot_reviews = spot.reviews
        for review in spot_reviews:
            rating += review.stars
        #Setting the rating in the spot
        if len(spot_reviews):
            spot_dict['rating'] = rating / len(spot_reviews)
        else:
            spot_dict['rating'] = rating
        #Get all spot images
        spot_images = spot.spot_images
        #Iterate through the images if there is a preview image set the url
        if len(spot_images):
            for image in spot_images:
                if image.preview_image == True:
                    spot_dict['preview_image'] = image.url
        #If a preview image was not set upload a preview image
        if not len(spot_images):
            spot_dict['preview_image'] = default_img
        return_list.append(spot_dict)
    return return_list

@spot_routes.route('/<id>')
def get_selected_spot(id):
    selected_spot = Spot.query.get(id)
    #Turn spots into dictionaries
    spot_dict = selected_spot.to_dict()
    #Initialize the rating
    rating = 0
    #Get all associated reviews and their rating
    spot_reviews = selected_spot.reviews
    review_list = []
    review_image_list = []
    for review in spot_reviews:
        rating += review.stars
        review_image = review.review_images
        #Iterate through the review images
        for rev_image in review_image:
            review_image_list.append(rev_image.url)
        #turn the review into a dictionary
        final_review = review.to_dict()
        #add the image list
        final_review['images'] = review_image_list
        #append the reivews to the spot
        review_list.append(final_review)
    #Setting the rating in the spot
    if len(spot_reviews):
        spot_dict['rating'] = rating / len(spot_reviews)
    else:
        spot_dict['rating'] = rating
    #Get all Images on the spot
    spot_images = selected_spot.spot_images
    #Initialize the image list
    image_list = []
    #For each Image add the url to the image list
    for image in spot_images:
        image_list.append(image.url)
    spot_dict['reviews'] = review_list
    spot_dict['images'] = image_list
    return spot_dict
