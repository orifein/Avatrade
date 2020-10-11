from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from bot.models import User, Post,Like
import jwt
import json
import uuid
import random
import string
from django.db.models import Q
def index(request):
    return HttpResponse("Hello, world. You're at the bot index.")


def random_name(numRange):

        return ''.join(random.choice(string.ascii_letters) for _ in range(numRange))


@csrf_exempt 
def signup_user(request):
    

    request_dic = json.loads(request.body)

    fullname = ''
    user_email = request_dic["email"]

    response_from_hunter_api = mock_hunter_api_for_checking_email_verifier(user_email)

    if response_from_hunter_api != "deliverable":
        return HttpResponse(bool(False))

    response_from_enrichment_api = mock_enrichment_api_for_getting_additional_data(user_email)

    if response_from_enrichment_api['person'] is not None:
        fullname = response_from_enrichment_api['person']['name']['fullname']




    create_user = User(user_id = request_dic["user_id"],email = request_dic["email"],password = request_dic["password"],name = fullname)

    create_user.save()

    encoded_jwt = jwt.encode({'user_id': request_dic["user_id"]}, 'secret', algorithm='HS256').decode("UTF-8")


    return HttpResponse(encoded_jwt)



def mock_hunter_api_for_checking_email_verifier(email):
    #Here should be Hunter api for checking Email Verifier - will make mock of resopnse 
    mock_api_key = str(uuid.uuid4())

    return call_hunter_api_mock(email,mock_api_key)

def mock_enrichment_api_for_getting_additional_data(email):
    #Here should be enrichment api for getting additional data  - will make mock of resopnse 

    return call_enrichment_api_mock(email)






def call_hunter_api_mock(email,api_key):
    response_status_list = ["deliverable","deliverable","deliverable","deliverable"]

    return random.choice(response_status_list)


def call_enrichment_api_mock(email):
    response_dic = dict()
    response_dic['person'] = dict()
    response_dic['person']['name'] = dict()
    response_dic['person']['name']['fullname'] = random_name(5)


    return response_dic


@csrf_exempt 
def create_post(request):

    request_dic = json.loads(request.body)

    jwt_decoded = jwt.decode(request_dic["jwt"], 'secret', algorithm='HS256')

    create_post = Post(user_id = jwt_decoded["user_id"],post_id = request_dic["post_id"],title = request_dic["title"])    

    create_post.save()

    response_tuple = (jwt_decoded["user_id"],request_dic["post_id"])

    return HttpResponse(json.dumps(response_tuple))

@csrf_exempt 
def clear_tables(request):

    Post.objects.all().delete()
    User.objects.all().delete()
    Like.objects.all().delete()


@csrf_exempt 
def like_post(request):

    #Retrieve Like Table 
    post_id_to_return = ''

    like_table = Like.objects.all()
    post_table = Post.objects.all()

    all_posts_id = [post.post_id for post in post_table]
    all_likes_id = [like.post_id for like in like_table]

    if all(post in all_likes_id for post in all_posts_id):
        status_got = 202
        return HttpResponse(post_id_to_return,status= status_got)


    request_dic = json.loads(request.body)
    jwt_decoded = jwt.decode(request_dic["jwt"], 'secret', algorithm='HS256')
    user_id_decoded = jwt_decoded["user_id"]
    posts_from_other_user_id = Post.objects.filter(~Q(user_id=user_id_decoded))
    gave_like = False
    for post in posts_from_other_user_id:
        check_if_post_in_like_table = like_table.filter(post_id = post.post_id)
        check_if_got_already_like_from_user = check_if_post_in_like_table.filter(like_by_user_id=user_id_decoded)


        if check_if_got_already_like_from_user:
            continue

        like_obj = Like(post_id = post.post_id, like_by_user_id =user_id_decoded )
        like_obj.save()
        gave_like = True
        post_id_to_return = str(post.post_id)
        break


    if False: #Check that everything finished
        status_got = 202

    status_got = 200 if gave_like else 201

    return HttpResponse(post_id_to_return,status= status_got)



@csrf_exempt 
def unlike_post(request):

    print("lala")
    return HttpResponse("Hello, world. You're at the signup User Page index.")