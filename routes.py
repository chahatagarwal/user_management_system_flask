import os
from flask import Flask, request, jsonify, make_response, session
from init import app, db
from flask_sqlalchemy import SQLAlchemy
import json
from models import User, Log
import datetime
import regex as re
#from werkzeug.security import generate_password_hash, check_password_hash

#verifying email type
def email_check(email):
    #regular expression
    email_regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    # pass the regular expression
    # and the string in search() method
    if(re.search(email_regex, email)):
        return 1
    else:
        return 0

#verifying phone number
def phoneno_Valid(phone_no):
    phoneno_Pattern = re.compile("[1-9][0-9]{9}")
    if phoneno_Pattern.match(phone_no):
        return 1
    else:
        return 0

#masking of data when sending to front end based on email or phone number
def maskPII(S):
    #email id
    if S.count('@')>0:
        s1=S.strip().split('@')[0]
        s2=S.strip().split('@')[1]
        ns1=s1[0] + '*****'+s1[-1]
        return (ns1.lower()+'@'+s2.lower())
    #phone number
    else:
        ns=re.sub('\D', '', S)
        return (["", "+*", "+**", "+***"][len(ns) - 10] + "******" + str(ns[-4:]))

#logging function
def logging(phone_no,remote_address,attribute,old_value,new_value):
    log = Log(log_user_phone=phone_no,log_ip_address=remote_address,log_attribute=attribute,log_old_value=old_value,log_new_value=new_value)
    db.session.add(log)
    db.session.commit()

#registering as Agent/Admin
@app.route('/registeruser', methods=['POST'])
def register():
    # get the post data
    post_data = request.get_json()
    # check if user already exists
    user = User.query.filter_by(user_phone=post_data.get('user_phone')).first()
    if not user:
        if email_check(post_data.get('user_email')) and phoneno_Valid(str(post_data.get('user_phone'))):
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
            'Message': 'Check the fields entered'
        }   
    else:
        responseObject = {
            'Message': 'User Already exist',
        }
    return make_response(jsonify(responseObject)), 400

#login API for Admin
@app.route('/userlogin', methods=['POST'])
def login():
    # get the post data
    post_data = request.get_json()
    user = User.query.filter_by(
        user_phone=post_data.get('user_phone'),user_password=post_data.get('user_password')).first()
    if user:  
        #ADMIN as a USER
        if user.is_activated == True and user.is_deleted==False and user.user_role==1:
            list_users_requested = User.query.filter_by(is_activated=False).all()
            if list_users_requested:
                responseObject = [] 
                for i in range(0,len(list_users_requested)):
                    temp = {}
                    temp = list_users_requested[i].as_dict()
                    temp.pop('user_password')
                    temp['user_email'] = maskPII(temp['user_email'])
                    temp['user_phone'] = maskPII(str(temp['user_phone']))
                    responseObject.append(temp)
                data_response ={
                    "data": responseObject
                }
                resp = make_response(jsonify(data_response))
            else:
                resp = make_response(jsonify({"Message":"No Request from new users"})) 
            session['user_phone'] = user.user_phone
            return resp, 200
        #LOGIN as an AGENT
        elif user.is_activated == True and user.is_deleted==False and user.user_role==0:
            responseObject = {
            'Message': 'Successfully logged in as an AGENT!'
        }
            resp = make_response(jsonify(responseObject))
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
            'Message': 'Please send Phone number and Password correctly'
        }
        resp = make_response(jsonify(responseObject))
        return resp, 400

#read all users from database
@app.route('/readusers', methods=['GET'])
def list_users():
    try:
        user_type = User.query.get(session['user_phone'])
        if session['user_phone'] and user_type.user_role == 1:
            users = User.query.all()
            if users:
                responseObject = []
                for i in range(0,len(users)):
                    temp = {}
                    temp = users[i].as_dict()
                    if temp['user_phone'] == session['user_phone']:
                        continue
                    temp.pop('user_password')
                    #MASKED DATA sent to Front end
                    temp['user_email'] = maskPII(temp['user_email'])
                    print(temp['user_phone'])
                    temp['user_phone'] = maskPII(str(temp['user_phone']))
                    responseObject.append(temp)
                data_response ={
                    "data":responseObject
                }
                return make_response(jsonify(data_response)), 200
            else:
                responseObject = {
                    'Message': 'Could not find any authorized users'
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

#update acivate/deactivate based on action
@app.route('/userupdate', methods=['PUT'])
def update():
    try:
        # get the post data
        post_data = request.get_json()
        user_type = User.query.get(session['user_phone'])
        if session['user_phone'] and user_type.user_role == 1:
            # check if user already exists
            stmt = User.query.get(post_data.get('user_phone'))
            if stmt:
                if post_data.get('action_type') == "active" and stmt.is_activated == 0:
                    stmt.is_activated = 1
                    db.session.commit()
                    responseObject = {
                        'Message': 'User access provided successfully'
                    }
                    #Logging information
                    logging(post_data.get('user_phone'),request.remote_addr,"is_activated",0,1)
                    return make_response(jsonify(responseObject)), 200
                elif post_data.get('action_type') == "active" and stmt.is_activated == 1:
                    responseObject = {
                        'Message': 'User already provided access'
                    }
                    return make_response(jsonify(responseObject)), 200
                elif post_data.get('action_type') == "inactive" and stmt.is_deleted == 0:
                    stmt.is_deleted = 1
                    stmt.is_activated = 0
                    db.session.commit()
                    responseObject = {
                        'Message': 'User deactivated succesfully!'
                    }
                    #Logging information
                    logging(post_data.get('user_phone'),request.remote_addr,"is_deleted",0,1)
                    return make_response(jsonify(responseObject)), 200
                elif post_data.get('action_type') == "active" and stmt.is_deleted == 1:
                    stmt.is_deleted = 0
                    db.session.commit()
                    responseObject = {
                        'Message': 'User ready for reuse of Account in Portal'
                    }
                    #Logging information
                    logging(post_data.get('user_phone'),request.remote_addr,"is_deleted",1,0)
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

#API to delete the inactive user
@app.route('/deleteuser', methods=['DELETE'])
def delete():
    try:
        #to check privilges of user taking an action
        user_type = User.query.get(session['user_phone'])
        post_data = request.get_json()
        # check if user already exists
        stmt = User.query.filter_by(user_phone=post_data.get("user_phone"),is_deleted=True)
        if session['user_phone'] and user_type.user_role == 1 and stmt:
            #delete the record and commit
            stmt.delete()
            db.session.commit()
            responseObject = {
                'Message': 'Successfully deleted in-active user from the system'
            }
            #Logging information
            logging(session['user_phone'],request.remote_addr,"record removed",post_data.get('user_phone'),"N/A")
            return make_response(jsonify(responseObject)),204
        else:
            responseObject = {
                'Message': 'Check your phone number or user is not deactivated!'
            }
        return make_response(jsonify(responseObject)), 400
    except:
        responseObject = {
                'Message': 'Not authorised to access!'
            }
        return make_response(jsonify(responseObject)), 400

#read all logs from database
@app.route('/userlogs', methods=['GET'])
def userlogs():
    try:
        user_type = User.query.get(session['user_phone'])
        if session['user_phone'] and user_type.user_role == 1:
            logs = Log.query.all()
            if logs:
                responseObject = []
                #retriving all logs
                for i in range(0,len(logs)):
                    temp = {}
                    temp = logs[i].as_dict()
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

#Statistics for AGENT as an USER -> Count inactive/active users
@app.route('/count/<count_action_type>', methods=['GET'])
def count_statistics(count_action_type):
    try:
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
                    'Message': 'Not authorised to access'
                }
            return make_response(jsonify(responseObject)), 400
    except:
        responseObject = {
                    'Message': 'Not authorised to access. Please login'
                }
        return make_response(jsonify(responseObject)), 400        

#logout API for Admin
@app.route('/userlogout', methods=['POST'])
def logout():
    # get the post data
    post_data = request.get_json()
    # fetch the user data
    user = User.query.filter_by(
            user_phone=post_data.get('user_phone')).first()
    if user:
        if session['user_phone'] == post_data.get('user_phone'):
            #remove the session
            session.pop('user_phone', None)
            responseObject = {
                'Message': 'Logout successful'
            }
            resp = make_response(jsonify(responseObject))
            return resp, 200
        else:
            responseObject = {
                'Message': 'Already logged out'
            }
            resp = make_response(jsonify(responseObject))
            return resp, 400
    else:
        responseObject = {
                'Message': 'Enter correct phone number'
            }
        resp = make_response(jsonify(responseObject))
        return resp, 400

#main function of flask
if __name__ == "__main__":
    #create a db file
    db.create_all()
    app.run(host='0.0.0.0', debug=True)