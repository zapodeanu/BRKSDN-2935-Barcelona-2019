#!/usr/bin/env python3


# developed by Gabi Zapodeanu, TSA, GPO, Cisco Systems


# this module includes common utilized functions to create applications using Spark APIs


import requests
import json
import urllib3

from requests_toolbelt import MultipartEncoder  # required to encode messages uploaded to Spark
from urllib3.exceptions import InsecureRequestWarning  # for insecure https warnings

from config import WEBEX_TEAMS_AUTH, WEBEX_TEAMS_URL


urllib3.disable_warnings(InsecureRequestWarning)  # Disable insecure https warnings


def create_team(team_name):
    """
    This function will create a Webex Teams team with the name {team_name}
    Call to Webex Teams - /teams
    :param team_name: new Webex Teams team name
    :return: the Webex Teams team id
    """

    payload = {'name': team_name}
    url = WEBEX_TEAMS_URL + '/teams'
    header = {'content-type': 'application/json', 'authorization': WEBEX_TEAMS_AUTH}
    team_response = requests.post(url, data=json.dumps(payload), headers=header, verify=False)
    team_json = team_response.json()
    team_id = team_json['id']
    print('\nCreated Spark Team with the name: ', team_name)
    return team_id


def get_team_id(team_name):
    """
    This function will find a Webex Teams team with the name {team_name}
    Call to Webex Teams - /teams
    :param team_name: Webex Teams team name
    :return: the Webex Teams team id
    """

    team_id = None
    url = WEBEX_TEAMS_URL + '/teams'
    header = {'content-type': 'application/json', 'authorization': WEBEX_TEAMS_AUTH}
    team_response = requests.get(url, headers=header, verify=False)
    team_json = team_response.json()
    team_list = team_json['items']
    for teams in team_list:
        if teams['name'] == team_name:
            team_id = teams['id']
    return team_id


def delete_team(team_name):
    """
    This function will delete the Webex Teams team with the {team_name}
    Calls to: it will call first the function get_team_id(team_name) to find out the team id.
              Webex Teams - /teams/ to find delete the team
    :param team_name: The Webex Teams team name
    :return:
    """

    team_id = get_team_id(team_name)
    url = WEBEX_TEAMS_URL + '/teams/' + team_id
    header = {'content-type': 'application/json', 'authorization': WEBEX_TEAMS_AUTH}
    requests.delete(url, headers=header, verify=False)


def create_space(space_name):
    """
    This function will create a Webex Teams space with the name {space_name}
    Calls to Webex Teams - /rooms
    :param space_name: Webex Teams space name
    :return: the Webex Teams space id
    """

    payload = {'title': space_name}
    url = WEBEX_TEAMS_URL + '/rooms'
    header = {'content-type': 'application/json', 'authorization': WEBEX_TEAMS_AUTH}
    space_response = requests.post(url, data=json.dumps(payload), headers=header, verify=False)
    space_json = space_response.json()
    space_id = space_json['id']
    return space_id


def get_space_id(space_name):
    """
    This function will find the Webex Teams space id based on the {space_name}
    Call to Webex Teams - /rooms
    :param space_name: The Webex Teams space name
    :return: the Webex Teams space Id
    """

    payload = {'title': space_name}
    space_number = None
    url = WEBEX_TEAMS_URL + '/rooms'
    header = {'content-type': 'application/json', 'authorization': WEBEX_TEAMS_AUTH}
    space_response = requests.get(url, data=json.dumps(payload), headers=header, verify=False)
    space_list_json = space_response.json()
    space_list = space_list_json['items']
    for spaces in space_list:
        if spaces['title'] == space_name:
            space_number = spaces['id']
    return space_number


def add_team_membership(space_name, email_invite):
    """
    This function will add membership to the Webex Teams space with the name {space_name}
    Calls to Webex Teams - /memberships to add membership
    :param space_name: The Webex Teams space name
    :param email_invite: Webex Teams user email to add to the team
    :return: status for adding the user, by returning the email address
    """

    space_id = get_space_id(space_name)
    payload = {'roomId': space_id, 'personEmail': email_invite, 'isModerator': 'true'}
    url = WEBEX_TEAMS_URL + '/memberships'
    header = {'content-type': 'application/json', 'authorization': WEBEX_TEAMS_AUTH}
    membership_response = requests.post(url, data=json.dumps(payload), headers=header, verify=False)
    membership_json = membership_response.json()
    try:
        membership = membership_json['personEmail']
    except:
        membership = None
    return membership


def delete_space(space_name):
    """
    This function will delete the Webex Teams space with the {space_name}
    Calls to: Webex Teams - /rooms
    :param space_name: The Webex Teams space name
    :return:
    """

    space_id = get_space_id(space_name)
    url = WEBEX_TEAMS_URL + '/rooms/' + space_id
    header = {'content-type': 'application/json', 'authorization': WEBEX_TEAMS_AUTH}
    requests.delete(url, headers=header, verify=False)
    print('\nDeleted Spark Team :  ', space_name)


def last_user_message(space_name):
    """
    This function will find the last message from the Spark space with the {space_name}
    Call to function get_space_id(space_name) to find the space_id
    Followed by API call to /messages?roomId={room_id}
    :param space_name: the Spark space name
    :return: {last_message} - the text of the last message posted in the space
             {last_user_email} - the author of the last message in the space
    """

    space_id = get_space_id(space_name)
    url = WEBEX_TEAMS_URL + '/messages?roomId=' + space_id
    header = {'content-type': 'application/json', 'authorization': WEBEX_TEAMS_AUTH}
    response = requests.get(url, headers=header, verify=False)
    list_messages_json = response.json()
    list_messages = list_messages_json['items']
    last_message = list_messages[0]['text']
    last_user_email = list_messages[0]['personEmail']
    return last_message, last_user_email


def add_space_membership(space_name, email_invite):
    """
    This function will add membership to the Webex Teams space with the name {space_name}
    Calls to Webex Teams - /memberships to add membership
    :param space_name: The Webex Teams space name
    :param email_invite: Webex Teams user email to add to the team
    :return: status for adding the user, by returning the email address
    """

    space_id = get_space_id(space_name)
    payload = {'roomId': space_id, 'personEmail': email_invite, 'isModerator': 'true'}
    url = WEBEX_TEAMS_URL + '/memberships'
    header = {'content-type': 'application/json', 'authorization': WEBEX_TEAMS_AUTH}
    membership_response = requests.post(url, data=json.dumps(payload), headers=header, verify=False)
    membership_json = membership_response.json()
    try:
        membership = membership_json['personEmail']
    except:
        membership = None
    return membership


def post_space_message(space_name, message):
    """
    This function will post the {message} to the Webex Teams space with the {space_name}
    Call to function get_space_id(space_name) to find the space_id
    Followed by API call /messages
    :param space_name: the Webex Teams space name
    :param message: the text of the message to be posted in the space
    :return: none
    """

    space_id = get_space_id(space_name)
    payload = {'roomId': space_id, 'text': message}
    url = WEBEX_TEAMS_URL + '/messages'
    header = {'content-type': 'application/json', 'authorization': WEBEX_TEAMS_AUTH}
    requests.post(url, data=json.dumps(payload), headers=header, verify=False)


def post_space_file(space_name, file_name, file_type, file_path):
    """
    This function will post the file with the name {file_name}, type of file {file_type},
    from the local folder with the path {file_path}, to the Webex Teams space with the name {space_name}
    Call to function get_space_id(space_name) to find the space_id
    Followed by API call /messages
    :param space_name: Webex Teams space name
    :param file_name: File name to be uploaded
    :param file_type: File type (example: image/jpg for image files)
    :param file_path: File path local on the computer
    :return:
    """

    space_id = get_space_id(space_name)

    # get the file name without the extension
    file = file_name.split('.')[0]

    payload = {'roomId': space_id,
               'files': (file, open(file_path+file_name, 'rb'), file_type)
               }
    # encode the file info, example: https://developer.ciscospark.com/blog/blog-details-8129.html

    m = MultipartEncoder(fields=payload)
    url = WEBEX_TEAMS_URL + '/messages'
    header = {'content-type': m.content_type, 'authorization': WEBEX_TEAMS_AUTH}
    requests.post(url, data=m, headers=header, verify=False)

