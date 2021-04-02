# from django.shortcuts import render
# from django.contrib.auth.models import Group
# from django.http import HttpResponse, JsonResponse
# from django.views.decorators.http import require_http_methods, require_GET, require_POST
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.decorators import api_view

# import json
# import secrets

# from .models import User, ApiKey, UserToken
# from .decorators import token_expire_checked


# def create_group(group_name):
#     # input group name
#     # output group, created
#     # group, created = Group.objects.get_or_create(
#     #     name=group_name)

#     return Group.objects.get_or_create(name=group_name)


# def delete_group(group_name):
#     return Group.objects.filter(name=group_name).delete()


# def create_user(creator_is_superuser, new_user_group, new_user_name, new_user_email=None, new_user_password=None):
#     # create user and add to group
#     # input:
#     #     1. creator_is_superuser
#     #     2. new_user - {
#     #           new_user_group,
#     #           new_user_name,
#     #           new_user_email=None,
#     #           new_user_password=None
#     #
#     #       }
#     # output:
#     #     1. User object
#     #     2. User already exist or not

#     # check username exist or not
#     user = User.objects.filter(username=new_user_name)
#     if len(user) > 0:
#         return user, False, None

#     # if password is None then generate a random password
#     if not new_user_password:
#         new_user_password = secrets.token_urlsafe()
#         print("new_user_password: ", new_user_password)

#     if creator_is_superuser:
#         new_user = User.objects.create_superuser(
#             username=new_user_name, email=new_user_email, password=new_user_password)
#         pass
#     else:
#         new_user = User.objects.create_user(
#             username=new_user_name, email=new_user_email, password=new_user_password)
#         pass

#     # set is_staff, need to modify
#     if new_user_name == new_user_group.name+'.manager' or new_user_name == new_user_group.name+'.app':
#         new_user.is_staff = True
#         new_user.save()

#     # set group
#     new_user.groups.add(new_user_group)

#     return new_user, True, new_user_password


# def delete_user(user_name):
#     return User.objects.filter(username=user_name).delete()


# def activate_user(user):
#     # input user object
#     user.is_active = 1
#     user.save()


# def deactivate_user(user):
#     # input user object
#     user.is_active = 0
#     user.save()


# def create_api_key(group):
#     # input group object
#     # output api_key, created

#     # while True:
#     #     key = secrets.token_urlsafe()
#     #     api_key, created = Api_Key.objects.get_or_create(
#     #         key=key, group=group_id)
#     #     print(api_key, created)
#     #     if created:
#     #         break
#     return ApiKey.objects.get_or_create(group=group)


# def delete_api_key(key):
#     # by key or group?
#     return ApiKey.objects.filter(key=key).delete()


# def create_user_token(user, expire_time_dict={'weeks': 0, 'days': 0, 'hours': 0}):
#     # input user object
#     # output user_token, created
#     token, created = UserToken.objects.get_or_create(user=user)
#     expire_time = (((expire_time_dict['weeks'] * 7) +
#                     expire_time_dict['days']) * 24) + expire_time_dict['hours']
#     if expire_time > 0:
#         token.refresh_expires(duration=expire_time)
#         token.save()
#     return token, created


# def delete_user_token():
#     pass


# @csrf_exempt
# # @api_view(['POST'])
# @require_POST
# # @login_required
# # @token_expire_checked
# def create(request):
#     post_data = request.POST

#     data = {}

#     # check parameters
#     if 'group_name' not in post_data:
#         return HttpResponse(status=304)
#     group_name = post_data.get('group_name')
#     data['group_name'] = group_name

#     if 'group_email' not in post_data:
#         group_email = None
#     else:
#         group_email = post_data.get('group_email')
#     data['group_email'] = group_email

#     # create group
#     group_obj, group_created = create_group(group_name)
#     if not group_created:
#         # return group already exist
#         data['responseCode'] = '999'
#         data['responseMsg'] = 'Create group fail, group already exist'
#         return JsonResponse(data)

#     # create api_key
#     api_key_obj, api_key_created = create_api_key(group_obj)
#     # if not api_key_created:
#     #     # return api_key already exist
#     #     return HttpResponse(status=400)

#     # create account {group}.manager
#     data['result'] = {}
#     manager, manager_created, manager_password = create_user(
#         False, group_obj, "{0}.manager".format(group_obj.name), group_email)
#     # manager_token, manager_token_created = create_user_token(manager)

#     # create account {group}.app and permanent token
#     app, app_created, app_password = create_user(
#         False, group_obj, "{0}.app".format(group_obj.name), group_email)
#     app_token, app_token_created = create_user_token(
#         app, {'weeks': 0, 'days': 365, 'hours': 0})

#     if manager_created and app_created:
#         data['responseCode'] = '200'
#         data['responseMsg'] = 'create group success'
#         data['result']['manager_account'] = manager.username
#         data['result']['manager_password'] = manager_password
#         data['result']['app_account'] = app.username
#         data['result']['app_password'] = app_password
#     else:
#         data['responseCode'] = '999'
#         data['responseMsg'] = 'create accounts fail, accounts already exist'

#     return JsonResponse(data)


# @csrf_exempt
# # @api_view(['POST'])
# @require_POST
# # @login_required
# # @token_expire_checked
# def delete(request):
#     if not request.META.get('HTTP_X_HTTP_METHOD_OVERRIDE'):
#         return HttpResponse(status=400)

#     if not request.META.get('HTTP_X_HTTP_METHOD_OVERRIDE') == 'DELETE':
#         return HttpResponse(status=400)

#     post_data = request.POST
#     print(post_data.get('group_name'))

#     data = {}

#     if 'group_name' not in post_data:
#         return HttpResponse(status=304)
#     group_name = post_data.get('group_name')
#     data['group_name'] = group_name

#     # check the group name is root or not
#     # the root group cannot be removed
#     # is_superuser

#     # get user object and set is_active = 0
#     users = User.objects.filter(groups__name=group_name)
#     for user in users:
#         deactivate_user(user)

#     (num, result_dict) = delete_group(group_name)
#     data['result'] = result_dict

#     if num > 0:
#         data['responseCode'] = '200'
#         data['responseMsg'] = 'delete success'
#     else:
#         data['responseCode'] = '999'
#         data['responseMsg'] = 'delete fail, group not exist'

#     return JsonResponse(data)
