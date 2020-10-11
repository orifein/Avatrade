
import os
import json
import requests
import random
import string
from base_logger import BaseLogger


def read_configuration_file(config_file):

    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))

    with open(os.path.join(__location__, config_file)) as f:
        config_file_data = json.loads(f.read())
        return config_file_data


def random_letters(numRange):

        return ''.join(random.choice(string.ascii_letters) for _ in range(numRange))


def generate_email():

    rand_prefix = random_letters(5)
    return rand_prefix+"@gmail.com"


def generate_password():
    return random_letters(8)


def create_post_api(user_id, jwt, starting_post_id):
    create_post_response_list = []
    url = create_post_url
    create_post_obj  = {
            "jwt" : jwt.decode("UTF-8"),
            "title" : "This title is About: " + random_letters(6),
            "post_id" : starting_post_id
    }
    create_post_json = json.dumps(create_post_obj)
    response = requests.post(url,data = create_post_json)
    create_post_response_list.append(json.loads(response.content))
    num_of_posts_per_user_dict[(user_id,jwt.decode("UTF-8"))] = number_of_posts_by_user
    return create_post_response_list


def create_signup_api(index_user_id):
    signup_jwt_list=[]


    email = generate_email()
    password = generate_password()
    url = signup_url
    signup_obj = {

        'user_id':index_user_id,
        "email" : email,
        "password" : password


    }

    signup_json = json.dumps(signup_obj)

    jwt_token = requests.post(url,data = signup_json)
    jwt_token_decoded = jwt_token.content.decode("UTF-8")
    if jwt_token_decoded == 'False':
        logger.debug("User Didnt Succeed Email Verifier - Not Signing,  Problematic Email: "+ email)
        return []
    num_of_likes_per_user_dict[(index_user_id,jwt_token_decoded)] = max_likes_per_user
    logger.debug("Signed User - Email: "+email+" User Id: "+str(index_user_id))
    signup_jwt_list.append((index_user_id,jwt_token.content))
    return signup_jwt_list


def create_like_post_api(user_tuple,num_of_posts):
      url = like_post_url
      logger.debug("Now Giving Like By User Id: "+str(user_tuple[0]))
      like_post_obj = {
            "jwt": user_tuple[1]
        }
      like_post_json = json.dumps(like_post_obj)
      response = requests.post(url,data = like_post_json)
      return response


if __name__ == "__main__":
    #region Global Variables Configuration
    logger = BaseLogger().create_logger("avatrade_bot")
    logger.debug("Reading Configuration File")
    config_info = read_configuration_file("config_file.json")
    logger.debug("Done Reading Configuration File")
    number_of_users = config_info["number_of_users"]
    max_posts_per_user = config_info["max_posts_per_user"]
    max_likes_per_user = config_info["max_likes_per_user"]
    signup_jwt_list = []
    create_post_response_list=[]
    num_of_likes_per_user_dict = dict()
    num_of_posts_per_user_dict = dict()    
    signup_url ='http://127.0.0.1:8000/bot/signup'
    create_post_url = 'http://127.0.0.1:8000/bot/create_post'
    like_post_url = 'http://127.0.0.1:8000/bot/like_post'
    clear_all_tables_url = 'http://127.0.0.1:8000/bot/clear_tables'
    #endregion 
    logger.debug("Clearing all tables before starting bot")
    requests.get(clear_all_tables_url)
    logger.debug("Finished Clearing all tables before starting bot")
    logger.debug("Signing Users to Our Social Media")  
    index_user_id=1
    for i in range(number_of_users):
        signup_user = create_signup_api(index_user_id)
        if signup_user:
            index_user_id+=1
            signup_jwt_list.extend(signup_user)
    
    starting_post_id= 1

    for user_id,jwt in signup_jwt_list:
        number_of_posts_by_user = random.randint(1,max_posts_per_user)
        for _ in range(number_of_posts_by_user):
            create_post_response_list.extend(create_post_api(user_id,jwt,starting_post_id))
            starting_post_id+=1
    

    all_posts_with_likes = False

    while (not all(value == 0 for value in num_of_likes_per_user_dict.values()) and not all_posts_with_likes ):

        sort_jwt_users_by_max_posts = sorted(num_of_posts_per_user_dict.items(), key=lambda x: x[1], reverse=True)

        for user_tuple,num_of_posts in sort_jwt_users_by_max_posts:

            while(num_of_likes_per_user_dict[user_tuple] > 0):

                response = create_like_post_api(user_tuple,num_of_posts)
                
                if response.status_code == 200:
                    num_of_likes_per_user_dict[user_tuple] -=1
                    logger.debug("Succesfully Gave Like - User Id: " + str(user_tuple[0]) + " Number Of likes he Still got:   " +str(num_of_likes_per_user_dict[user_tuple]))


                elif response.status_code == 201:
                    logger.debug("User Id: " + str(user_tuple[0]) + " Has No More Likes")
                    break #No More posts he can give likes, exiting 


                elif response.status_code == 202: #Custom status_code - all posts with likes
                    all_posts_with_likes = True
                    break      
            
            if all_posts_with_likes:
                break

    if all_posts_with_likes:
        logger.debug("Finished Automatic Bot Because All posts got likes - enjoy!")
    else:
        logger.debug("Finished Automatic Bot Because All users finished their likes")


