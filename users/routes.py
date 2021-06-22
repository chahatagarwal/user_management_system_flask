#importing the required modules need to execute routes.py
from users.modules import app, db, request, User, make_response, session, jsonify, re, Log
from users.validations import phoneno_Valid, email_check
from users.masking_data import maskPII
from users.logs import logging

#1st API
#register as Agent/Admin
@app.route('/registeruser', methods=['POST'])
def register():
    # get the post data
    post_data = request.get_json()
    # check if user already exists
    user = User.query.filter_by(user_phone=post_data.get('user_phone')).first()
    #if user doesn't exist and also validating email and phone number
    if not user and email_check(post_data.get('user_email')) and phoneno_Valid(str(post_data.get('user_phone'))):
        user = User(
            user_fname=post_data.get('user_fname'),
            user_lname=post_data.get('user_lname'),
            user_email=post_data.get('user_email'),
            user_password=post_data.get('user_password'),
            user_phone=post_data.get('user_phone'),
            user_role=post_data.get('user_role'),
            is_activated=post_data.get('is_activated')
        )
        # insert the user
        db.session.add(user)
        db.session.commit()
        responseObject = {
            'Message': 'Registration successful. Waiting for approval!'
        }
        return make_response(jsonify(responseObject)), 200 
    else:
        responseObject = {
            'Message': 'User Already exist or Require valid fields',
        }
    return make_response(jsonify(responseObject)), 400

#2nd API
#login API for Admin/Agent
@app.route('/userlogin', methods=['POST'])
def login():
    # get the post data
    post_data = request.get_json()
    user = User.query.filter_by(
        user_phone=post_data.get('user_phone'),user_password=post_data.get('user_password')).first()
    if user:  
        #USER as an ADMIN with pre-requsite of account activated..
        if user.is_activated == True and user.is_deleted==False and user.user_role==1:
            #listing users who need approval to access the portal
            list_users_requested = User.query.filter_by(is_activated=False).all()
            if list_users_requested:
                #extract data from Python data objects into JSON form
                responseObject = [] 
                for i in range(0,len(list_users_requested)):
                    temp = {}
                    temp = list_users_requested[i].as_dict()
                    #poping user_password to maintain confidentiality of user 
                    temp.pop('user_password')
                    #masking email and phone for front end
                    temp['user_email'] = maskPII(temp['user_email'])
                    temp['user_phone'] = maskPII(str(temp['user_phone']))
                    responseObject.append(temp)
                #response to front end
                data_response ={
                    "data": responseObject
                }
                resp = make_response(jsonify(data_response))
            else:
                resp = make_response(jsonify({"Message":"No new Request from new users! But Logged in Successfully!"})) 
            #creating a session for the user when logged in
            session['user_phone'] = user.user_phone
            return resp, 200
        #LOGIN as an AGENT
        elif user.is_activated == True and user.is_deleted==False and user.user_role==0:
            responseObject = {
            'Message': 'Successfully logged in as an AGENT!'
        }
            resp = make_response(jsonify(responseObject))
            #creating session for the user
            session['user_phone'] = user.user_phone
            return resp, 200
        else:
            responseObject = {
                'Message': 'Waiting for approval!'
            }
            resp = make_response(jsonify(responseObject))
            return resp, 400
    else:
        responseObject = {
            'Message': 'Please send correct Phone number and Password'
        }
        resp = make_response(jsonify(responseObject))
        return resp, 400

#3rd API
#read all users from database
@app.route('/readusers', methods=['GET'])
def list_users():
    try:
        #to find active session for a user as an ADMIN
        user_type = User.query.get(session['user_phone'])
        if session['user_phone'] and user_type.user_role == 1:
            users = User.query.all()
            if users:
                #extract data from Python data objects into JSON form
                responseObject = []
                for i in range(0,len(users)):
                    temp = {}
                    temp = users[i].as_dict()
                    #don't display of a user who is accessing this feature
                    if temp['user_phone'] == session['user_phone']:
                        continue
                    temp.pop('user_password')
                    #MASKED DATA sent to Front end
                    temp['user_email'] = maskPII(temp['user_email'])
                    temp['user_phone'] = maskPII(str(temp['user_phone']))
                    responseObject.append(temp)
                data_response ={
                    "data":responseObject
                }
                return make_response(jsonify(data_response)), 200
            else:
                responseObject = {
                    'Message': 'Could not find any users'
                }
                return make_response(jsonify(responseObject)), 400
        else:
            responseObject = {
                    'Message': 'Not Authorized to access'
                }
            return make_response(jsonify(responseObject)), 400
    except:
        responseObject = {
                    'Message': 'Not Authorized to access. Please login'
                }
        return make_response(jsonify(responseObject)), 400

#4th API
#update active/inactive based on action type sent by ADMIN
@app.route('/userupdate', methods=['PUT'])
def update():
    try:
        # get the post data
        post_data = request.get_json()
        #extracting a session to vaild as an ADMIN
        user_type = User.query.get(session['user_phone'])
        if session['user_phone'] and user_type.user_role == 1:
            # check if user already exists
            stmt = User.query.get(post_data.get('user_phone'))
            if stmt:
                #active -> action_type when is_activated=0
                if post_data.get('action_type') == "active" and stmt.is_activated == 0:
                    stmt.is_activated = 1
                    db.session.commit()
                    responseObject = {
                        'Message': 'User access provided successfully'
                    }
                    #Logging information
                    logging(post_data.get('user_phone'),request.remote_addr,"is_activated",0,1)
                    return make_response(jsonify(responseObject)), 200
                #active -> action_type when is_activated=1
                elif post_data.get('action_type') == "active" and stmt.is_activated == 1:
                    responseObject = {
                        'Message': 'User already provided access'
                    }
                    return make_response(jsonify(responseObject)), 200
                #inactive -> action_type when is_deleted=0
                elif post_data.get('action_type') == "inactive" and stmt.is_deleted == 0:
                    stmt.is_activated = 0
                    stmt.is_deleted = 1
                    db.session.commit()
                    responseObject = {
                        'Message': 'User deactivated succesfully!'
                    }
                    #Logging information
                    logging(post_data.get('user_phone'),request.remote_addr,"is_deleted",0,1)
                    return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {
                    'Message': 'Incorrect Phone number/does not exist'
                }
            return make_response(jsonify(responseObject)), 400
        else:
            responseObject = {
                    'Message': 'Not authorised to access'
                }
            return make_response(jsonify(responseObject)), 400
    except:
        responseObject = {
                    'Message': 'Not authorised to access. Please login'
                }
        return make_response(jsonify(responseObject)), 400

#5th API
#API to delete the inactive user from the system by ADMIN ONLY
@app.route('/deleteuser', methods=['DELETE'])
def delete():
    try:
        #to check privilges of user taking an action (ADMIN ONLY)
        user_type = User.query.get(session['user_phone'])
        post_data = request.get_json()
        # check if user already exists
        stmt = User.query.filter_by(user_phone=post_data.get("user_phone"),is_deleted=True)
        #if user exists which needs to be removed and also if the ADMIN session is valid to take an action
        if session['user_phone'] and user_type.user_role == 1 and stmt:
            #delete the record and commit
            stmt.delete()
            db.session.commit()
            responseObject = {
                'Message': 'Successfully deleted in-active user from the system'
            }
            #Logging information
            logging(session['user_phone'],request.remote_addr,"record removed",post_data.get('user_phone'),"N/A")
            return make_response(jsonify(responseObject)),200
        else:
            responseObject = {
                'Message': 'Check your phone number or user is not deactivated!'
            }
        return make_response(jsonify(responseObject)), 404
    except:
        responseObject = {
                'Message': 'Not authorised to access!'
            }
        return make_response(jsonify(responseObject)), 400

#6th API
#read all logs from database by ADMIN ONLY
@app.route('/userlogs', methods=['GET'])
def userlogs():
    try:
        #validating user as an ADMIN
        user_type = User.query.get(session['user_phone'])
        if session['user_phone'] and user_type.user_role == 1:
            #get all the logs
            logs = Log.query.all()
            if logs:
                responseObject = []
                #retriving all logs in JSON form from Python data object
                for i in range(0,len(logs)):
                    temp = {}
                    temp = logs[i].as_dict()
                    #masking user_phone number for front-end
                    temp['log_user_phone'] = maskPII(str(temp['log_user_phone']))
                    responseObject.append(temp)
                data_response ={
                    "data":responseObject
                }
                return make_response(jsonify(data_response)), 200
            else:
                responseObject = {
                    'Message': 'Could not find any logs'
                }
                return make_response(jsonify(responseObject)), 400
        else:
            responseObject = {
                    'Message': 'Not Authorized to access'
                }
            return make_response(jsonify(responseObject)), 400
    except:
        responseObject = {
                    'Message': 'Not Authorized to access. Please login'
                }
        return make_response(jsonify(responseObject)), 400

#7th API
#Statistics for AGENT as an USER -> Count inactive/active users
@app.route('/count/<count_action_type>', methods=['GET'])
def count_statistics(count_action_type):
    try:
        #validate AGENT's Session
        user_type = User.query.get(session['user_phone'])
        if session['user_phone'] and user_type.user_role == 0:
            #number of inactive users in the portal waiting for access
            if count_action_type == "inactive":
                stmt = User.query.filter_by(is_activated=0).all()
                if stmt:
                    responseObject = {
                        'is_inactive': len(stmt)
                    }
                    return make_response(jsonify(responseObject)), 200
                else:
                    responseObject = {
                        'is_inactive': 0
                    }
                    return make_response(jsonify(responseObject)), 200
            #number of active users in the portal, got the access
            elif count_action_type == "active":
                stmt = User.query.filter_by(is_activated=1).all()
                if stmt:
                    responseObject = {
                        'is_activated': len(stmt)
                    }
                    return make_response(jsonify(responseObject)), 200
                else:
                    responseObject = {
                        'is_activated': 0
                    }
                    return make_response(jsonify(responseObject)), 200
        else:
            responseObject = {
                    'Message': 'Not authorised to access'
                }
            return make_response(jsonify(responseObject)), 400
    except:
        responseObject = {
                    'Message': 'Not authorised to access. Please login'
                }
        return make_response(jsonify(responseObject)), 400        

#8th API
#logout API for Admin
@app.route('/userlogout', methods=['POST'])
def logout():
    # get the post data
    post_data = request.get_json()
    # fetch the user data
    user = User.query.filter_by(
            user_phone=post_data.get('user_phone')).first()
    if user:
        session.pop('user_phone', None)
        responseObject = {
            'Message': 'Logout successfully'
        }
        resp = make_response(jsonify(responseObject))
        return resp, 200
    else:
        responseObject = {
                'Message': 'Enter correct phone number or Already logged out!'
            }
        resp = make_response(jsonify(responseObject))
        return resp, 400