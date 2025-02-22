
from nanoid import generate
from .db import db
from datetime import datetime
userInfo_ref = db.collection("Agents").document("agentInfo")
userStat_ref = db.collection("Agents").document("agentStat")
payment_ref = db.collection("paymentReq")
session_ref = db.collection("session")
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
    userReferal = generate(size=10)
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
            newInfo = {**allInfo[ref],**allStat[ref],"date":currentDate,"id":ref,"curAmount":curAmount}
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

def addSession(tele_id,referal):
    ref = session_ref.document(tele_id)
    if ref.get().exists:
        return
    ref.set({"referal":referal})
    
def getSession(tele_id):
    ref = session_ref.document(tele_id).get()
    if ref.exists:
        return ref.get()["referal"]
    return ""
    
    
intro_text = """🎉Well Come to Victory Agent system

Victory official channel👇
https://t.me/VictoryTutor_7

ከተማሪዎቻችን የተሰጡ አስተያየቶች👇
https://t.me/victorystcom_7

የvictory team ለማናገር👇
@VICTORY_TUTOR_TEAMS

የትምህርቱን አሰጣት Sample ለማየት👇
https://t.me/VictorySample7


🌟የኤጀንት ሲስተም አሰራር እና የአከፋፈል ሁኔታ
✨አንድ የቪክትሪ ኤጀንት በመሆን መስራት የሚፈልግ ሰው በመጀመርያ ስለ ቪክትሪ እና ስለሚሰጣቸው አገልግሎቶች ጠንቅቆ ማወቅ ይኖርበታል።

✨በመሆኑም ለተማሪዎቻችን ስለምንሰጠው አገልግሎት የተቀመጠውን አጭር ዶክመንት አንብቦ መረዳት ይኖርብርታል።

✨አንድ ሰው ኤጀንት ሆኖ ከመመዝገቡ በፊት ስራውን ለመስራት የሚያስችል ብቃት ወይም ፍላጎት እና ብዛት ተማሪዎችን ማግኘት እንደሚችል እራሱን መለየት ይኖርበታል።

✨ይህንን ስራ በተሻለ ሁኔታ ለመስራት ተማሪ፣ መምህር በተለያዩ ማህበራዊ ገፆች ላይ እንቅስቃሴዎች የሚያደርግ ሲሆነ አልያም potential market-ኡን የሚያገኝ ሊሆን ይገባል።


  🌟የአሰራር ቅደም ተከተሎች
1️⃣አንድ ሰው የትምህርት አሰጣጡን ዶክመንት በደንብ ካነበበ በኋላ bot-ኡን በመጠቀም ስሙን እና አካውንቱን ጨምሮ ሙሉ የሚጠየቀውን መረጃዎች ያስመዘግባል።

✨ይህ ሙሉ መረጃ ወደ መረጃ ቋታችን (database) በመሄድ ይቀመጣል። በመቀጠልም የተመዘገበውን ኤጀንት ምን ያክል ተማሪ እንዳስመዘገበ ፣ በስሩ ምን ያህል ኤጀንት እንዳለ፣ ምን ያህል ብር እንዳለው እና ምን ያክል እንዳወጣ እያንዳንዱን ነገር በሰራነው ሲስተም ሙሉ የምንቆጣጠረው (track) የምናደርገው ይሆናል።

2️⃣ ይህንን ሂደት ካጠናቀቀ በኋላ “የ Referal link ለማግኘት ” የሚለውን በመንካት የራሱን link ይሰጠዋል። ይህንን link በመያዝ ተማሪዎችን እያናገረ በሱ ሊንክ ተማሪዎች እንዲገቡ ያደርጋል፤ በ social media የሚሰራም ከሆነ ደግሞ ማስታወቅያዎችን እየሰራ link-ኡን በማስቀመጥ ተማሪዎች እንዲመዘገቡ ያደርጋል።

✨ይሄ link  የሚመዘገቡ ተማሪዎችን ወደ ተማሪዎች መመዝገብያ Bot የሚወስዳቸው ሲሆን ተማሪዎቹ ልክ ተመዝግበው Approval እንዳገኙ ለኤጀንቱ ሲስተሙ ራሱ በሱ link የተመዘገበውን ተማሪ screensoot እና Approval የሚልክለት ሲሆን የተመዘገበው ተማሪ ስንተኛው እንደሆነ ይገልፅለታል።

✨ብር ለማውጣት ሲፈልግ “ብር ለማውጣት” የሚለውን በመንካት ይጠይቃል።እኛም ያስመዘገበውን ተማሪ ብዛት በመቶ በማባዛት ባስመዘገበው ባንክ አካውንት የምንልክለት ይሆናል።

3️⃣አንድ ኤጀንት በስሩ 2 ተማሪ ካስገባ በኋላ የኤጀንት Referral link የሚለውን በመንካት የኤጀንት refrral link ማግኘት ይችላል። የዚህ ዋነኛው ስራ ዋናው ኤጀንት በስሩ ሌሎች ኤጀንቶችን በመመልመል እነዛ ኤጀንቶች ተማሪዎችን ሲያስገቡ ዋናው ኤጀንት ከእያንዳንዱ ኤጀንት ባስገቡት የተማሪ ልክ በ25 ብር በማባዛት የሚያገኝ ሲሆን ።

✨በስሩ ያሉ ኤጀንቶች ግን ልክ እንደተለመደው የ 100 ብር ክፍያ ባስገቡት ተማሪ ተባዝቶ ክፍያውን ያገኛሉ።

✨አንድ ኤጀንት የኤጀንት link ቢያወጣ ተመራጭ የሚሆነው ብዙ ተማሪዎችን የሚያገኝበት የስራ ዘርፍ ውስጥ ካለ እና የት/ቤት ተማሪዎች ከርሱ ጋር ኤጀንት ሆነው ለመስራት ፍቃደኛ ከሆኑ ነው።

✨በኤጀንት ስር የሚገባ ኤጀንት ብዙ ተማሪዎች እንዲያስገባ በተቻለ መጠን የ 11 አልያም የ 12ኛ ክፍል የ social ወይም  Natural ተማሪ መሆን ይጠበቅበታል።

✨አንድ ኤጀንት ከሱ ስር ኤጀንት እንዲመዘገብ ሲፈልግ ሁለት ተማሪ ቅድሚያ ማስመዝገብ ይኖርበታል። በመቀጠል link-ኡን ካገኘ በኋላ በስሩ ለዛው ኤጀንት ሲልክለት አዲሱን ኤጀንት በቀጥታ ወደ መመዝገብያ Bot የሚወስደው ይሆናል።

✨አዲሱ ኤጀንት ከተመዘገበ በኋላ የራሱን referral link በመውሰድ ተማሪዎች እንዲመዘገቡ ሲያደርግ ለራሱም ለመጀመርያውም ኤጀንት የሚቆርጥለት ይሆናል።

ማሳሰብያ፦ ሁለተኛው ኤጀንት በስሩ ሶስተኛ ኤጀንት ቢያስገባ ሶስተኛው የሚያመጣው ተማሪ ለራሱ እና ለሁለተኛው ኤጀንት ብቻ ብር የሚያገኝ ይሆናል ።

✨በዚኛውም ሂደት የመጀመርያው ኤጀንት ምንም ብር የማይከፈለው መሆኑን ለመግለፅ እንወዳለን።

የኤጀንት ቦት ለኤጀንቱ ማየት የሚፈልጋቸውን ዝርዝሮች ያቀፈ በመሆኑ በየጊዜው እየገባ check ማድረግ ይችላል።"""