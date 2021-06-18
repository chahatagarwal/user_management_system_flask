# User Management System
From the problem statement given, I have implemented CRUD Operations for User Management System. I have come up with two types of users: Admin &amp; Agent. It also involves basic statistics like different active or inactive users in the system. Apart from this, I have considered gender neutrality while developing an application.

                               User Management System(Python v3.6)
                              **************************************
                              
@Author: Chahat Agarwal
Email ID: chahatagarwal@ymail.com

**********************************************************************************
Use case:
From the problem statement given, I have implemented CRUD Operations for User Management System. 
I have come up with two types of users: Admin & Agent. It also involves basic statistics like different active or inactive users in the system.
Apart from this, I have considered gender neutrality while developing an application.

**********************************************************************************
Flow:
1) Initally, when Admin/Agent wants to access the portal, they would need to register themselves on the portal.
   1)a) After basic validation of email and password, the account is registered successfully but can't be access until it is approved by the existing Admin. 
2) Admin who is already approved within the system, LOGS into the Portal and thus can see which all users needs approval to onboard after successful registeration.
   2)a) Admin has rights to check list of different USERS within the system 
   2)b) Admin then approves/rejects the users waiting in queue to access the portal
   2)c) Admin also has rights to deactivate any Agent account from the system
   2)d) Admin also has rights to remove the user from the system only when user are deactivated in the system
   2)d) Admin has rights to list the logs of all user
3) Agent can also LOGIN after successful verification by ADMIN in the system
   3)a) Agent have access to find the number of active or deactivate users.
4) If AGENT/ADMIN wants to Logoff, then I they could LOGOUT from the System

NOTE:
The data visible on the front-end would be masked for email and phone number attributes. 

***********************************************************************************
NOTE:
Running at Port-> 5000
Running at Address-> 0.0.0.0

************************************************************************************
List of APIs implemented:

1) API: Register for Agent/Admin
   Route: "/registeruser"
   Method type: POST 
   Content-Type: application/json
   Parmas: {user_fname,user_lname,user_email,user_password,user_role,user_phone}
   NOTE:
   If we need to make one user add manually into the system then pass "is_activated = 1" else no need. Follow general process for aproval by ADMIN
   
2) API: LOGIN for Admin/Agent
   Route: "/userlogin"
   Method type: POST 
   Content-Type: application/json
   Parmas: {user_password,user_phone}

3) API: Read all users only by ADMIN
   Route: "/readusers"
   Method type: GET

4) API: activate/deactivate user based on UPDATE by ADMIN only
   Route: "/userupdate"
   Method type: PUT
   Params: {user_phone, action_type}
   types of input for "action_type": inactive (or) active

5) API: DELETE inactive user from the system
   Route: "/deleteuser"
   Params: {user_phone}
   Method type: DELETE

6) API: LOGS retrieved by ADMIN only
   Route: "/userlogs"
   Method type: GET

7) API: Statistics - count for active or inactive users by AGENT as an user type
   Route: "/count/<count_action_type>"
   Method type: GET 
   types of input for "count_action_type": inactive (or) active

8) API: LOGOUT for both ADMIN/AGENT
   Route: "/userlogout"
   Method type: POST 
   Content-Type: application/json
   Parmas: {user_phone}
 
 NOTE: 
a) user_phone -> PK
b) activated user in db as AGENT -> user_phone: 7200828674 & user_password: hello_world
c) activated user in db as ADMIN -> user_phone: 9876543210 & user_password: hello_world

******************************************************************************
user-defined Functions created:
1) loging data
2) Masking data
3) Validation
   a) Email
   b) Phone Number

******************************************************************************
Download packages to run the API application. They are as belows:
a)  SQLAlchemy with flask compatibility
    pip install --user flask sqlalchemy flask-sqlalchemy
b) flask
   pip install Flask

2) for execution run flask server
python routes.py

*******************************************************************************
