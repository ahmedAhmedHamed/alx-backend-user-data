#!/usr/bin/env python3
"""end to end integration test
"""
import requests

BASE_URL = 'http://127.0.0.1:5000/'


def register_user(email: str, password: str) -> None:
    """register user endpoint test"""
    response = requests.post(BASE_URL + 'users', data={'email': email,
                                                       'password': password})
    assert (response.json() ==
            {"email": email, "message": "user created"})


def log_in_wrong_password(email: str, password: str) -> None:
    """log in user with wrong password endpoint test"""
    response = requests.post(BASE_URL + 'sessions',
                             data={'email': email,
                                   'password': password})
    assert (response.status_code == 401)


def log_in(email: str, password: str) -> str:
    """ log in user with password endpoint test """
    response = requests.post(BASE_URL + 'sessions',
                             data={'email': email,
                                   'password': password})
    assert (response.status_code == 200)
    assert (isinstance(response.cookies.get('session_id'), str))
    return response.cookies.get('session_id')


def profile_logged(session_id: str) -> None:
    """ checks if user is logged in with a session id """
    response = requests.get(BASE_URL + 'profile',
                            cookies={'session_id': session_id})
    assert (response.status_code == 200)


def log_out(session_id: str) -> None:
    """ log out user with session id """
    response = requests.delete(BASE_URL + 'sessions',
                               cookies={'session_id': session_id})
    assert (response.status_code == 200)
    assert response.history


def profile_unlogged() -> None:
    """ checks if no user is logged in """
    response = requests.get(BASE_URL + 'profile')
    assert (response.status_code == 403)


def reset_password_token(email: str) -> str:
    """ reset password token """
    response = requests.post(BASE_URL + 'reset_password',
                             data={'email': email})
    assert (response.status_code == 200)
    resp_json = response.json()
    assert (resp_json.get('email') == email)
    assert (resp_json.get('reset_token'))
    return resp_json.get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ update user password """
    response = requests.put(BASE_URL + 'reset_password',
                            data={'email': email,
                                  'reset_token': reset_token,
                                  'new_password': new_password})
    resp_json = response.json()
    assert (resp_json == {"email": email, "message": "Password updated"})
    assert (response.status_code == 200)


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
