                               User Management System(Python v3.6)
                              **************************************

@Author: Chahat Agarwal
Email ID: chahatagarwal@ymail.com

**********************************************************************************
Use case:
From the given problem statement given, I have implemented CRUD Operations for User Management System. 
I have also come up with two types of users: Admin & Agent. 
It also involves basic statistics like the number of active or inactive users in the system as a ROLE assigned to ONLY AGENT.
As an ADMIN, it can do CRUD operations with the data available in the system
Apart from this, I have considered gender neutrality while developing an application hence didn't consider as an seperate attribute.

**********************************************************************************
Process Flow:

ASSUME INITIALLY "1 ADMIN is approved in the system and can login"

1) When the new Admin/Agent wants to access the portal, they would need to register themselves on the portal. - CREATE
   1)a) After basic validation of email and password, the account is registered successfully but can't access until it is approved by the existing Admin. 
2) Admin who is already approved within the system, LOGIN and thus can see which all users requires approval to onboard after successful registeration in the front end. - READ
   2)a) Admin has rights to check list of USERS within the system - READ 
   2)b) Admin can approves/rejects the users waiting in queue to access the portal - UPDATE
   2)c) Admin also has rights to deactivate any Agent account from the system - UPDATE
   2)d) Admin also has rights to remove the user from the system only when user are deactivated in the system - DELETE
   2)d) Admin has rights to view all the logs - READ
3) Agent can also LOGIN after successful verification by ADMIN in the system
   3)a) Agent have ONLY access to find the number of active or deactivate users based on need. - READ
4) If AGENT/ADMIN wants to Logoff, then they could LOGOUT from the System and hence SESSION is CLOSED

NOTE:
1) The data visible on the front-end would be masked for email and phone number attributes. 
2) When the actor logs-in SESSION is created for the respective USER type and hence validation is made at every ROUTE

***********************************************************************************
Additional information:

1) user_phone -> Primary key
2) activated user in db as AGENT -> user_phone: 9876543210 & user_password: hello_world
3) activated user in db as ADMIN -> user_phone: 7200828674 & user_password: hello_world

***************************************************************************************
Download packages to run the FLASK application. They are as belows:
a)  SQLAlchemy with flask compatibility
    pip install --user flask sqlalchemy flask-sqlalchemy
b) flask
   pip install Flask

2) To run flask server
   python routes.py 

NOTE:
Running @Port-> 5000 & Address-> 0.0.0.0

************************************************************************************
User-defined functions created:
1) loging data when UPDATE or DELETE operations are made by ADMIN
   It collects IP Address of remote user, datetime, attribute actioned with old and new values.
2) Masking data
   mask email, phone number while sending the data to front end ADMIN panel
3) Validation(using Regular expression)
   a) Email
   b) Phone Number

****************************************************************************************
List of APIs implemented(8 nos):

1) API Purpose: Register Agent/Admin
   Route: "/registeruser"
   Method-type: POST 
   Content-Type: application/json
   Parmas: {user_fname, user_lname, user_email, user_password, user_role, user_phone}
   
   NOTE:
   1) If we need to make one user add manually into the system then pass "is_activated = 1" else no need.
   2) Validation check for email and phone number are made
   3) user_role: 0-> AGENT & 1-> ADMIN
   4) Need unique user_phone & user_email

2) API: LOGIN as Admin/Agent
   Route: "/userlogin"
   Method type: POST 
   Content-Type: application/json
   Parmas: {user_password, user_phone}

   NOTE:
   1) Create session for respective user while logging in.
   2) making sure if the user has access to the portal
   3) respective task is accessible based on user type.

3) API: Read all users ONLY by ADMIN
   Route: "/readusers"
   Method type: GET

   NOTE:
   1) It list all the users in the system

4) API: activate/deactivate user using UPDATE by ADMIN ONLY
   Route: "/userupdate"
   Method type: PUT
   Params: {user_phone, action_type}

   NOTE:
   1) Input type for "action_type" attribute: 
      1)a) "inactive" -> revoke access of portal for that user
                        OR
      1)b) "active" -> provide access to the portal for that user

5) API: DELETE inactive user from the system, ONLY by ADMIN
   Route: "/deleteuser"
   Method type: DELETE
   Params: {user_phone}

   NOTE:
   1) pre-requiste-> user should already be deactivated/revoked from accessing the portal

6) API: LOGS retrieval by ADMIN only
   Route: "/userlogs"
   Method type: GET

   NOTE:
   1) It stores Remote IP Address, datetime, attribute changed along with old and new values

7) API: Statistics - count for active or inactive users by AGENT ONLY
   Route: "/count/<count_action_type>"
   Method type: GET 

   NOTE:
   1) Input type for "count_action_type": 
      1)a) "inactive" -> returns count of inactive users present in the system
                     OR 
      1)b) "active" -> returns count of active users present in the system

8) API: LOGOUT ADMIN/AGENT
   Route: "/userlogout"
   Method type: POST 
   Content-Type: application/json
   Parmas: {user_phone}

   NOTE:
   1) Remove session for respective user logging off from the system

*****************************************************************************
