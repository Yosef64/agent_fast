from uuid import uuid4
from db import db
from datetime import datetime
userInfo_ref = db.collection("Agents").document("agentInfo")
userStat_ref = db.collection("Agents").document("agentStat")
payment_ref = db.collection("paymentReq")
def getUserInfo():
    users = userInfo_ref.get().to_dict()
    return users
def getUserStat():
    users = userStat_ref.get().to_dict()
    return users
def getUserStatById(userId):
    userRef = getUserById(userId)
    users = getUserStat()
    return [users[userRef],userRef] if userRef else [False,userRef]
def updateUserStat(referal):
    users = getUserStat()
    curUser = users[referal]["ownStud"] + 1
    userInfo_ref.update({referal:curUser})
    curParent , ind = users[referal]["parent"] , 0
    while ind < 2 and curParent:
        curUser = users[curParent]["agentStud"] + 1
        userInfo_ref.update({curParent:curUser})
        curParent , ind = users[curParent]["parent"] , ind + 1
def registerAgent(userInfo,referal):
    agentStat = {"ownStud":0,"agentStud":0,"parent":str(referal),"timestamp":[],"totalAmount":0}
    userReferal = str(uuid4()).replace("-", "")
    userInfo_ref.update({userReferal:userInfo})
    userStat_ref.update({userReferal:agentStat})
def getUserById(userId):
    users = userInfo_ref.get().to_dict()
    for ref in users:
        if users[ref]["teleid"] == userId:
            return ref
    return ""
def askPayment(userId):
    ref = getUserById(userId)
    currentDate = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    if ref:
        doc_ref = payment_ref.document(ref).get()
        if doc_ref.exists:
            return [True,False,False]
        else:
            allStat , allInfo = getUserStat(),getUserInfo()
            stat , _ =  getUserStatById(userId)
            curAmount = stat["totalAmount"]
            if curAmount < 100:
                return [True,False,True]
            newInfo = {**allInfo[ref],**allStat[ref],"date":currentDate,"id":ref}
            payment_ref.document(ref).set(newInfo)
            return [True,True,False]
    return [False,False,False]

def getOwnAgent(ref):
    agentsStat = userStat_ref.get().to_dict()
    count = 0
    for refs in agentsStat:
        if agentsStat[refs]["parent"] == ref:
            count += 1
            
    return count