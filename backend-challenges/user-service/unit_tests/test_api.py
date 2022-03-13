import pytest
from app import create_app
from flask import json


@pytest.fixture()
def app():
    # this can be replaced with a different configuration file
    app = create_app('config.py')
    app.config.update({
        'TESTING': True,
        'DEBUG': True,
        'FLASK_ENV': "development"
    })
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


def test_user_get_1(client):
    """
    User that does not exist
    :param client: client object of Flask
    :return: None
    """
    response = client.get(
        '/user/54/'
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["msg"] == "User does not exist"


def test_user_add_1(client):
    """
    Provide incomplete information
    :param client: client object of Flask
    :return: None
    """
    response = client.post(
        '/user/add/',
        data=json.dumps({
                            "first_name": "John",
                            "last_name": "Doe"
                        }),
        content_type='application/json',
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["msg"] == "Please enter all the fields!"


def test_user_add_2(client):
    """
    Provide complete, valid data
    :param client: client object of Flask
    :return: None
    """
    response = client.post(
        '/user/add/',
        data=json.dumps({
                            "first_name": "John",
                            "last_name": "Doe",
                            "mail": "john.doe@gmail.com",
                            "phone": "9090872234"
                        }),
        content_type='application/json',
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["msg"] == "Successfully added user!"


def test_user_add_3(client):
    """
    Provide valid, complete information
    :param client: the client object of Flask
    :return: None
    """
    response = client.post(
        '/user/add/',
        data=json.dumps({
                            "first_name": "Daisy",
                            "last_name": "Doe",
                            "mail": "daisy.doe@gmail.com",
                            "phone": "6090872234"
                        }),
        content_type='application/json',
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["msg"] == "Successfully added user!"


def test_user_add_4(client):
    """
    Provide valid, complete data to generate 3rd user
    :param client: client object of Flask
    :return: None
    """
    response = client.post(
        '/user/add/',
        data=json.dumps({
                            "first_name": "Carey",
                            "last_name": "Carr",
                            "mail": "carey.carr@gmail.com",
                            "phone": "9090823300"
                        }),
        content_type='application/json',
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["msg"] == "Successfully added user!"


def test_user_get_2(client):
    """
    Get a user that exist
    :param client: client object of Flask
    :return: None
    """
    response = client.get(
        '/user/2/'
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["msg"] == "Success"
    assert data["data"] == {
                                "first_name": "daisy",
                                "id": 2,
                                "last_name": "doe",
                                "mail": [
                                    "daisy.doe@gmail.com"
                                ],
                                "phone": [
                                    "6090872234"
                                ]
                            }


def test_user_add_mail_1(client):
    """
    Add additional mail for user
    :param client: client object of Flask
    :return: None
    """
    response = client.post(
        '/user/add/mail/',
        data=json.dumps({
            "id": 2,
            "mail": "daisy.d@gmail.com"
        }),
        content_type='application/json',
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["msg"] == "Added new email to user successfully!"


def test_user_add_mail_2(client):
    """
    Try to add an existing email address for user
    :param client: client object of Flask
    :return: None
    """
    response = client.post(
        '/user/add/mail/',
        data=json.dumps({
            "id": 2,
            "mail": "daisy.d@gmail.com"
        }),
        content_type='application/json',
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["msg"] == "The specified email already exists for the user!"


def test_user_add_mail_3(client):
    """
    Add email for a user that does not exist in the db
    :param client: client object of Flask
    :return: None
    """
    response = client.post(
        '/user/add/mail/',
        data=json.dumps({
            "id": 55,
            "mail": "daisy.d@gmail.com"
        }),
        content_type='application/json',
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["msg"] == "The specified user does not exist!"


def test_user_add_mail_4(client):
    """
    Provide incomplete information
    :param client: client object of Flask
    :return: None
    """
    response = client.post(
        '/user/add/mail/',
        data=json.dumps({
            "id": 55
        }),
        content_type='application/json',
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["msg"] == "Please specify all the requested fields!"


def test_user_add_phone_1(client):
    """
    Add an additional phone number for user
    :param client: client object of Flask
    :return: None
    """
    response = client.post(
        '/user/add/phone/',
        data=json.dumps({
                            "id": 1,
                            "phone": "9001234992"
                        }),
        content_type='application/json',
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["msg"] == "Added new phone number for user successfully!"


def test_user_add_phone_2(client):
    """
    Add phone number for a user that does not exist
    :param client: client object of Flask
    :return: None
    """
    response = client.post(
        '/user/add/phone/',
        data=json.dumps({
                            "id": 56,
                            "phone": "9001234992"
                        }),
        content_type='application/json',
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["msg"] == "The specified user does not exist!"


def test_user_add_phone_3(client):
    """
    Add an already existing phone number for a user
    :param client: client object of Flask
    :return: None
    """
    response = client.post(
        '/user/add/phone/',
        data=json.dumps({
                            "id": 1,
                            "phone": "9001234992"
                        }),
        content_type='application/json',
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["msg"] == "The specified phone number already exists for the user!"


def test_user_add_phone_4(client):
    """
    Provide incomplete information
    :param client: client object of Flask
    :return: None
    """
    response = client.post(
        '/user/add/phone/',
        data=json.dumps({
                            "id": 1
                        }),
        content_type='application/json',
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["msg"] == "Please specify all the requested fields!"


def test_user_update_mail_1(client):
    """
    Update the existing email address of a user
    :param client: client object of Flask
    :return: None
    """
    response = client.put(
        '/user/update/mail/',
        data=json.dumps({
                            "id": 1,
                            "old_mail": "john.doe@gmail.com",
                            "new_mail": "j.doe1992@gmail.com"
                        }),
        content_type='application/json',
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["msg"] == "Updated user email successfully!"


def test_user_update_mail_2(client):
    """
    Try to update a mail that does not exist for the user
    :param client: client object of Flask
    :return: None
    """
    response = client.put(
        '/user/update/mail/',
        data=json.dumps({
                            "id": 1,
                            "old_mail": "john.doe@gmail.com",
                            "new_mail": "j.doe1992@gmail.com"
                        }),
        content_type='application/json',
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["msg"] == "The specified email does not exist!"


def test_user_update_mail_3(client):
    """
    Give same mails for old and new
    :param client: client object of Flask
    :return: None
    """
    response = client.put(
        '/user/update/mail/',
        data=json.dumps({
                            "id": 1,
                            "old_mail": "j.doe1992@gmail.com",
                            "new_mail": "j.doe1992@gmail.com"
                        }),
        content_type='application/json',
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["msg"] == "Old and new emails are the same!"


def test_user_update_mail_4(client):
    """
    Give incomplete information
    :param client: client object of Flask
    :return: None
    """
    response = client.put(
        '/user/update/mail/',
        data=json.dumps({
                            "id": 1,
                            "old_mail": "j.doe1992@gmail.com"
                        }),
        content_type='application/json',
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["msg"] == "Please specify all the requested fields."


def test_user_update_mail_5(client):
    """
    Update email for a user that does not exist
    :param client: client object of Flask
    :return: None
    """
    response = client.put(
        '/user/update/mail/',
        data=json.dumps({
                            "id": 67,
                            "old_mail": "j.doe1992@gmail.com",
                            "new_mail": "j.doe92@gmail.com"
                        }),
        content_type='application/json',
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["msg"] == "The specified user does not exist!"


def test_user_update_phone_1(client):
    """
    Update with correct values
    :param client: client object of Flask
    :return: None
    """
    response = client.put(
        '/user/update/phone/',
        data=json.dumps({
                            "id": 2,
                            "old_phone": "6090872234",
                            "new_phone": "9001234991"
                        }),
        content_type='application/json',
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["msg"] == "Updated user phone number successfully!"


def test_user_update_phone_2(client):
    """
    Update with number that does not exist
    :param client: client object of Flask
    :return: None
    """
    response = client.put(
        '/user/update/phone/',
        data=json.dumps({
                            "id": 2,
                            "old_phone": "6090872234",
                            "new_phone": "9001234991"
                        }),
        content_type='application/json',
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["msg"] == "The specified phone number does not exist!"


def test_user_update_phone_3(client):
    """
    Update with same old and new number
    :param client: client object of Flask
    :return: None
    """
    response = client.put(
        '/user/update/phone/',
        data=json.dumps({
                            "id": 2,
                            "old_phone": "9001234991",
                            "new_phone": "9001234991"
                        }),
        content_type='application/json',
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["msg"] == "The old and new phone numbers are the same!"


def test_user_update_phone_4(client):
    """
    Update phone number of a user that does not exist
    :param client: client object of Flask
    :return: None
    """
    response = client.put(
        '/user/update/phone/',
        data=json.dumps({
                            "id": 56,
                            "old_phone": "9001234991",
                            "new_phone": "9001234990"
                        }),
        content_type='application/json',
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["msg"] == "The specified user does not exist!"


def test_user_update_phone_5(client):
    """
    Provide incomplete information
    :param client: client object of Flask
    :return: None
    """
    response = client.put(
        '/user/update/phone/',
        data=json.dumps({
                            "id": 2,
                            "old_phone": "9001234991"
                        }),
        content_type='application/json',
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["msg"] == "Please specify all the requested fields."


def test_user_get_3(client):
    """
    Get the user information for user by first and last name
    :param client: client object of Flask
    :return: None
    """
    response = client.get(
        '/user?first_name=daisy&last_name=Doe'
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["msg"] == "Success"
    data_expected = [{
                        "first_name": "daisy",
                        "id": 2,
                        "last_name": "doe",
                        "mail": [
                            "daisy.doe@gmail.com",
                            "daisy.d@gmail.com"
                        ],
                        "phone": [
                            "9001234991"
                        ]
                    }]
    assert data["data"] == data_expected


def test_user_del_1(client):
    """
    Delete a user that exist
    :param client: client object of Flask
    :return: None
    """
    response = client.delete(
        '/user/del/',
        data=json.dumps({
            "id": 3
        }),
        content_type='application/json',
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["msg"] == "Deleted User"


def test_user_del_2(client):
    """
    Delete a user that does not exist
    :param client: client object of Flask
    :return: None
    """
    response = client.delete(
        '/user/del/',
        data=json.dumps({
            "id": 54
        }),
        content_type='application/json',
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["msg"] == "The specified user does not exist!"


def test_user_del_3(client):
    """
    Provide incomplete information while deleting a user
    :param client: client object of Flask
    :return: None
    """
    response = client.delete(
        '/user/del/',
        data=json.dumps({

        }),
        content_type='application/json',
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["msg"] == "Please specify the id!"
