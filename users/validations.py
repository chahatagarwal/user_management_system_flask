from users.modules import re

#verifying email type
def email_check(email):
    #regular expression for email
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