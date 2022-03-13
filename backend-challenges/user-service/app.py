# module imports
import os
from flask import Flask, jsonify, request, flash
from flask_restful import Resource, Api
from models import Email, User, PhoneNumber, db
from sqlalchemy import func

# api instance for Flask-restful
api = Api()


def create_app(config_file):
    """
    The application factory to create multiple instances of Flask app

    :param config_file: the config file used for Flask
    :return: the application instance
    """
    # initialize the Flask app and get the configuration from file
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    # initialize the Api and db
    api.init_app(app)
    db.init_app(app)
    return app


class UserGetByID(Resource):
    """
    This Resource returns details of a user by providing user id
    """
    def get(self, id):
        """
        The GET request handler

        :param id: the user id
        :return: json object containing user info
        """
        # proceed with get request
        user_object = User.query.filter_by(id=id).first()
        if user_object is not None:
            # get the user's email and contact info
            email_objects = Email.query.filter_by(user_id=user_object.id).all()
            emails = [obj.mail for obj in email_objects]
            phone_objects = PhoneNumber.query.filter_by(user_id=user_object.id).all()
            phone_nums = [obj.phone for obj in phone_objects]
            data = {
                'id': user_object.id, 'last_name': user_object.last_name,
                'first_name': user_object.first_name, 'mail': emails,
                'phone': phone_nums
            }
            return jsonify({"msg": "Success", "data": data})
        msg = "User does not exist"
        flash(msg, 'error')
        return jsonify({"msg": msg})


class UserGetByName(Resource):
    """
    This Resource returns the user info by providing the user name (first name
    and last name). Note that there could be multiple users with same first and last name.
    """
    def get(self):
        """
        The GET request handler

        :return: list containing JSON object for each user
        """
        data = []
        # check if user specified an empty name
        first_name = request.args.get('first_name')
        last_name = request.args.get('last_name')
        if first_name is None or last_name is None:
            msg = "Please specify first and last names."
            flash(msg, 'error')
        else:
            # proceed with get request - use func.lower() function to remove case sensitivity
            user_objects = User.query.filter(func.lower(User.first_name) == func.lower(first_name),
                                             func.lower(User.last_name) == func.lower(last_name)).all()
            if user_objects is not None:
                for user_object in user_objects:
                    # get the user's email and contact info
                    email_objects = Email.query.filter_by(user_id=user_object.id).all()
                    emails = [obj.mail for obj in email_objects]
                    phone_objects = PhoneNumber.query.filter_by(user_id=user_object.id).all()
                    phone_nums = [obj.phone for obj in phone_objects]
                    user_info = {
                                'id': user_object.id, 'last_name': user_object.last_name,
                                'first_name': user_object.first_name, 'mail': emails,
                                'phone': phone_nums
                            }
                    data.append(user_info)
                return jsonify({"msg": "Success", "data": data})
            msg = "User does not exist"
            flash(msg, 'error')
        return jsonify({"msg": msg})


class UserAddPhone(Resource):
    """
    This Resource helps to add an additional phone number for user
    """
    def post(self):
        """
        The POST request handler for the resource

        :return: JSON containing status message of the operation
        """
        user_data = request.get_json()
        # check if user has specified all the fields
        if user_data is None or 'phone' not in user_data or 'id' not in user_data:
            msg = 'Please specify all the requested fields!'
            flash(msg, 'error')
        else:
            # check if phone number already exists
            user_object = User.query.filter_by(id=user_data['id']).first()
            if user_object is not None:
                phone_obj = PhoneNumber.query.filter_by(phone=user_data['phone'], user_id=user_object.id).first()
                if phone_obj is None:
                    # proceed with adding new phone number to the user
                    # create a new PhoneNumber record in db for the user
                    phone_number_object = PhoneNumber(user_data['phone'], user_object.id)
                    db.session.add(phone_number_object)
                    db.session.commit()
                    msg = 'Added new phone number for user successfully!'
                else:
                    msg = 'The specified phone number already exists for the user!'
            else:
                msg = 'The specified user does not exist!'

        return jsonify({"msg": msg})


class UserAddEmail(Resource):
    """
    This Resource helps to add an additional email ID for the user
    """
    def post(self):
        """
        The POST request handler for the resource

        :return: JSON object containing the status message of the operation
        """
        user_data = request.get_json()
        # check if user data contains email field and user id
        if user_data is None or 'mail' not in user_data or 'id' not in user_data:
            msg = 'Please specify all the requested fields!'
            flash(msg, 'error')
        else:
            # check if user already has the email
            user_object = User.query.filter_by(id=user_data['id']).first()
            if user_object is not None:
                mail_object = Email.query.filter_by(mail=user_data['mail'], user_id=user_object.id).first()
                if mail_object is None:
                    # proceed with adding new email for the user
                    # create a new email record in the Email table for the user
                    email_object = Email(user_data['mail'], user_object.id)
                    db.session.add(email_object)
                    db.session.commit()
                    msg = 'Added new email to user successfully!'
                else:
                    msg = 'The specified email already exists for the user!'
            else:
                msg = 'The specified user does not exist!'

        return jsonify({"msg": msg})


class UserUpdateMail(Resource):
    """
    This Resource helps to update an existing email of the user
    """
    def put(self):
        """
        The PUT request handler for this resource. We are using HTTP PUT
        here since we only need to modify an existing data.

        :return: the JSON object containing the status message of the operation
        """
        user_data = request.get_json()
        # check if user has provided the required info
        if user_data is None or 'old_mail' not in user_data or 'new_mail' not in user_data or 'id' not in user_data:
            msg = "Please specify all the requested fields."
            flash(msg, 'error')
        elif user_data['old_mail'].lower() == user_data['new_mail'].lower():
            msg = "Old and new emails are the same!"
            flash(msg, 'error')
        else:
            # if all good, proceed with update
            user_object = User.query.filter_by(id=user_data['id']).first()
            if user_object is not None:
                # get the email_object for the user to be updated
                email_object = Email.query.filter_by(mail=user_data['old_mail'].lower(),
                                                     user_id=user_object.id).first()
                if email_object is not None:
                    email_object.mail = user_data['new_mail'].lower()
                    db.session.commit()
                    msg = 'Updated user email successfully!'
                else:
                    msg = 'The specified email does not exist!'
            else:
                msg = 'The specified user does not exist!'
        return jsonify({"msg": msg})


class UserUpdatePhone(Resource):
    """
    This Resource helps to update an existing phone number of the user
    """
    def put(self):
        """
        The PUT request handler for this resource.

        :return: the JSON object containing the status message for this operation
        """
        user_data = request.get_json()
        # check if user has provided the required info
        if user_data is None or 'old_phone' not in user_data or 'new_phone' not in user_data or 'id' not in user_data:
            msg = "Please specify all the requested fields."
            flash(msg, 'error')
        elif user_data['old_phone'] == user_data['new_phone']:
            msg = "The old and new phone numbers are the same!"
            flash(msg, 'error')
        else:
            # if all good, proceed with update
            user_object = User.query.filter_by(id=user_data['id']).first()
            if user_object is not None:
                # get the email_object for the user to be updated
                phone_object = PhoneNumber.query.filter_by(phone=user_data['old_phone'], user_id=user_object.id).first()
                if phone_object is not None:
                    phone_object.phone = user_data['new_phone']
                    db.session.commit()
                    msg = 'Updated user phone number successfully!'
                else:
                    msg = 'The specified phone number does not exist!'
            else:
                msg = 'The specified user does not exist!'

        return jsonify({"msg": msg})


class UserDelete(Resource):
    """
    This Resource helps to delete a user from the database.
    Please note that when a User is deleted, its associated Email and PhoneNumber objects
    also need to be deleted from the db.
    """
    def delete(self):
        """
        The DELETE request handler for this resource.

        :return: the JSON object containing the status message of the operation
        """
        user_data = request.get_json()
        # check if user has specified id of the user to be deleted
        if user_data is None or 'id' not in user_data:
            msg = 'Please specify the id!'
            flash(msg, 'error')
        else:
            # proceed with delete
            user_object = User.query.filter_by(id=user_data['id']).first()
            if user_object is not None:
                # delete the user object as well as all phone number and email objects
                # corresponding to the user
                email_objects = Email.query.filter_by(user_id=user_object.id).all()
                phone_objects = PhoneNumber.query.filter_by(user_id=user_object.id).all()

                db.session.delete(user_object)
                db.session.commit()
                for email_object in email_objects:
                    db.session.delete(email_object)
                    db.session.commit()
                for phone_object in phone_objects:
                    db.session.delete(phone_object)
                    db.session.commit()

                msg = "Deleted User"
            else:
                msg = "The specified user does not exist!"
        return jsonify({"msg": msg})


class UserAdd(Resource):
    """
    This Resource helps to add a new user to the database, including the user's
    first name, last name, email ID and phone number
    """
    def post(self):
        """
        The POST request handler for this resource.

        :return: the JSON object containing the status message of the operation
        """
        # get the json response for the post request
        user_data = request.get_json()
        # check if any field is not provided by user, if so flash error message
        if user_data is None or 'last_name' not in user_data or 'first_name' not in user_data \
                or 'mail' not in user_data or 'phone' not in user_data:
            msg = 'Please enter all the fields!'
            flash(msg, 'error')
        else:
            # all fields are present, check if user with same email already exists
            email = Email.query.filter_by(mail=user_data['mail']).first()
            if email is not None:
                msg = "A user with the same email already exists!"
                flash(msg, 'error')
            else:
                # if all good, proceed with adding a new user to db
                user_object = User(user_data['last_name'].lower(), user_data['first_name'].lower())
                db.session.add(user_object)
                db.session.commit()
                # create a Email and PhoneNumber object for the user's mail and number
                email_object = Email(user_data['mail'].lower(), user_object.id)
                db.session.add(email_object)
                db.session.commit()

                phone_object = PhoneNumber(user_data['phone'], user_object.id)
                db.session.add(phone_object)
                db.session.commit()
                msg = 'Successfully added user!'

        return jsonify({"msg": msg})


class Home(Resource):
    """
    This Resource serves as a welcome message if the user
    goes to the web server root
    """
    def get(self):
        """
        The GET request handler for this resource.

        :return: None
        """
        return jsonify({"msg": "Hello Perseus!"})


# the resource endpoints for the service
api.add_resource(Home, '/')
api.add_resource(UserGetByID, '/user/<int:id>/')
api.add_resource(UserGetByName, '/user')
api.add_resource(UserAddEmail, '/user/add/mail/')
api.add_resource(UserAddPhone, '/user/add/phone/')
api.add_resource(UserDelete, '/user/del/')
api.add_resource(UserAdd, '/user/add/')
api.add_resource(UserUpdateMail, '/user/update/mail/')
api.add_resource(UserUpdatePhone, '/user/update/phone/')


if __name__ == '__main__':
    # create all the db tables
    # db.create_all()
    # create the Flask app and run.
    app = create_app('config.py')
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
