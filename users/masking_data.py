from users.modules import re

#masking data when sending the data to front end for email or phone number
def maskPII(S):
    #email id mask
    if S.count('@')>0:
        s1=S.strip().split('@')[0]
        s2=S.strip().split('@')[1]
        ns1=s1[0] + '*****'+s1[-1]
        return (ns1.lower()+'@'+s2.lower())
    #phone number mask
    else:
        ns=re.sub('\D', '', S)
        return (["", "+*", "+**", "+***"][len(ns) - 10] + "******" + str(ns[-4:]))
