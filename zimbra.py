import requests,json
# SOAP request URL
from config import HOST,PORT,USERNAME,PASSWORD
URL = f"https://{HOST}:{PORT}/service/admin/soap"

"""AUTHORIZATION TOKEN"""
# METHODS STARTS
def getToken():
    token_xml = f"""<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Header><context xmlns="urn:zimbra"><userAgent name="ZimbraWebClient - GC113 (Win)"/><session/><authTokenControl voidOnExpired="1"/><format type="js"/></context></soap:Header><soap:Body><AuthRequest xmlns="urn:zimbraAdmin"><name>{USERNAME}</name><password>{PASSWORD}</password><virtualHost>101.50.86.254</virtualHost><csrfTokenSecured>1</csrfTokenSecured></AuthRequest></soap:Body></soap:Envelope>"""

    # HEADERS
    headers = { 'Content-Type': 'application/soap+xml'}
    # POST REQUEST
    r = requests.post(URL, data=token_xml, headers=headers,verify=False)
    try:
        response = json.loads(r.text)

        response= {
            'authToken' : response['Body']['AuthResponse']['authToken'][0]['_content'],
            'csrfToken' : response['Body']['AuthResponse']['csrfToken']['_content']
        }
    except:
        response= {
            'authToken' : "",
            'csrfToken' : "",
        }
    
    return response
# METHOD ENDS

"""GET DOMAIN ID"""
# METHOD DEFINTION
def getDomainId(domainName):
    
    # AUTH
    token =getToken()
    authToken = token['authToken']
    csrfToken = token['csrfToken']

    # REQUEST BODY
    payload = f"""<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Header><context xmlns="urn:zimbra"><userAgent name="ZimbraWebClient - GC114 (Win)"/><session /><format type="js"/><authToken>{authToken}</authToken><csrfToken>{csrfToken}</csrfToken></context></soap:Header><soap:Body><GetDomainInfoRequest xmlns="urn:zimbraAdmin"><domain by="name">{domainName}</domain></GetDomainInfoRequest></soap:Body></soap:Envelope>"""

    # HEADERS
    headers = { 'Content-Type': 'application/soap+xml' }
    
    # POST REQUEST
    response = requests.post(URL, headers=headers, data=payload, verify=False)

    try:
      response = json.loads(response.text)  
      domainId = response['Body']['GetDomainInfoResponse']['domain'][0]['id']
      return domainId
    except:
        return 0
# METHOD ENDS


"""DOMAIN CREATION"""
# METHOD DEFINTION
def createDomain(domainName,defaultCOSid=""):

  # AUTH
  token =getToken()
  authToken = token['authToken']
  csrfToken = token['csrfToken']

  # REQUEST BODY
  payload = f"""<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Header><context xmlns="urn:zimbra"><userAgent name="ZimbraWebClient - GC114 (Win)"/><session /><format type="js"/><authToken>{authToken}</authToken><csrfToken>{csrfToken}</csrfToken></context></soap:Header><soap:Body><CreateDomainRequest xmlns="urn:zimbraAdmin"><name>{domainName}</name><a n="zimbraGalMode">zimbra</a><a n="zimbraGalMaxResults">1</a><a n="zimbraNotes"/><a n="description"/><a n="zimbraAuthMech">zimbra</a><a n="zimbraPublicServiceHostname">{domainName}</a>"""
  if defaultCOSid != "":
    payload+=f"""<a n = "zimbraDomainDefaultCOSId">{defaultCOSid}</a>"""
  
  payload+="""<a n="zimbraDomainStatus">active</a></CreateDomainRequest></soap:Body></soap:Envelope>"""

  # HEADERS
  headers = { 'Content-Type': 'application/soap+xml' }
  
  # POST REQUEST
  response = requests.post(URL, headers=headers, data=payload, verify=False)
  
  try:
      response = json.loads(response.text)  
      accountRes = response['Body']['CreateDomainResponse']['domain'][0]['name']
      if accountRes == domainName:
          print(f"Domain Registered - {accountRes}")
          return 1
  except:
      try:
          accountRes = response['Body']['Fault']['Reason']['Text']
          print(f"ERROR : {accountRes}")
          return 2
      except:
          print("System Error Occured")
          return 0

# METHOD ENDS HERE

"""DOMAIN LOCKING"""
# METHOD DEFINTION
def lockDomain(domainName):
    # AUTH
    token =getToken()
    authToken = token['authToken']
    csrfToken = token['csrfToken']

    domainId = getDomainId(domainName)
    if domainId == 0:
        print("No Domain ID Found")
        return 0

    # REQUEST BODY
    payload = f"""<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Header><context xmlns="urn:zimbra"><userAgent name="ZimbraWebClient - GC113 (Win)"/><session/><format type="js"/><authToken>{authToken}</authToken><csrfToken>{csrfToken}</csrfToken></context></soap:Header><soap:Body><BatchRequest xmlns="urn:zimbra" onerror="stop"><ModifyDomainRequest xmlns="urn:zimbraAdmin"><id>{domainId}</id><a n="zimbraDomainStatus">locked</a></ModifyDomainRequest></BatchRequest></soap:Body></soap:Envelope>"""

    # HEADERS
    headers = { 'Content-Type': 'application/soap+xml' }
    
    # POST REQUEST
    response = requests.post(URL, headers=headers, data=payload, verify=False)

    try:
      response = json.loads(response.text)  
      domainRes = response['Body']['BatchResponse']['ModifyDomainResponse']

      if domainName in str(domainRes):
          print(f"Domain Locked - {domainName}")
          return 1
    except:
        try:
            domainRes = response['Body']['Fault']['Reason']['Text']
            print(f"ERROR : {domainRes}")
            return 2
        except:
            print("System Error Occured")
            return 0

"""DOMAIN ACTIVATION"""
# METHOD DEFINTION
def activateDomain(domainName):
    # AUTH
    token =getToken()
    authToken = token['authToken']
    csrfToken = token['csrfToken']

    domainId = getDomainId(domainName)
    if domainId == 0:
        print("No Domain ID Found")
        return 0

    # REQUEST BODY
    payload = f"""<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Header><context xmlns="urn:zimbra"><userAgent name="ZimbraWebClient - GC113 (Win)"/><session/><format type="js"/><authToken>{authToken}</authToken><csrfToken>{csrfToken}</csrfToken></context></soap:Header><soap:Body><BatchRequest xmlns="urn:zimbra" onerror="stop"><ModifyDomainRequest xmlns="urn:zimbraAdmin"><id>{domainId}</id><a n="zimbraDomainStatus">active</a></ModifyDomainRequest></BatchRequest></soap:Body></soap:Envelope>"""

    # HEADERS
    headers = { 'Content-Type': 'application/soap+xml' }
    
    # POST REQUEST
    response = requests.post(URL, headers=headers, data=payload, verify=False)

    try:
      response = json.loads(response.text)  
      domainRes = response['Body']['BatchResponse']['ModifyDomainResponse']

      if domainName in str(domainRes):
          print(f"Domain Locked - {domainName}")
          return 1
    except:
        try:
            domainRes = response['Body']['Fault']['Reason']['Text']
            print(f"ERROR : {domainRes}")
            return 2
        except:
            print("System Error Occured")
            return 0
        
"""GET ACCOUNT ID"""
# METHOD DEFINTION
def getAccountId(emailAddress):
    
    # AUTH
    token =getToken()
    authToken = token['authToken']
    csrfToken = token['csrfToken']

    # REQUEST BODY
    payload = f"""<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Header><context xmlns="urn:zimbra"><userAgent name="ZimbraWebClient - GC114 (Win)"/><session /><format type="js"/><authToken>{authToken}</authToken><csrfToken>{csrfToken}</csrfToken></context></soap:Header><soap:Body><GetAccountInfoRequest xmlns="urn:zimbraAdmin"><account by="name">{emailAddress}</account></GetAccountInfoRequest></soap:Body></soap:Envelope>"""

    # HEADERS
    headers = { 'Content-Type': 'application/soap+xml' }
    
    # POST REQUEST
    response = requests.post(URL, headers=headers, data=payload, verify=False)

    try:
        response = json.loads(response.text)  
        accountId = response['Body']['GetAccountInfoResponse']['a'][0]['_content']
        return accountId
    except:
        return 0
# METHOD ENDS       

"""ACCOUNT CREATION"""
# METHOD DEFINITION
def createAccount(emailAddress,displayName,password):

    # AUTH
    token =getToken()
    authToken = token['authToken']
    csrfToken = token['csrfToken']

    # REQUEST BODY
    payload = f"""<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Header><context xmlns="urn:zimbra"><userAgent name="ZimbraWebClient - GC114 (Win)"/><session/><format type="js"/><authToken>{authToken}</authToken><csrfToken>{csrfToken}</csrfToken></context></soap:Header><soap:Body><CreateAccountRequest xmlns="urn:zimbraAdmin"><name>{emailAddress}</name><password>{password}</password><a n="zimbraAccountStatus">active</a><a n="displayName">{displayName}</a></CreateAccountRequest></soap:Body></soap:Envelope>"""

    # HEADERS
    headers = { 'Content-Type': 'application/soap+xml' }

    # POST REQUEST
    response = requests.request("POST", URL, headers=headers, data=payload, verify=False)
    
    try:
        response = json.loads(response.text)
        accountRes = response['Body']['CreateAccountResponse']['account'][0]['name']
        if accountRes == emailAddress:
            print(f"Account Created - {accountRes}")
            return 1
    except:
        try:
            accountRes = response['Body']['Fault']['Reason']['Text']
            print(f"ERROR : {accountRes}")
            return 2
        except:
            print("System Error Occured")
            return 0
# METHOD ENDS HERE


"""GET ACTIVATION"""
# METHOD DEFINTION
def activateAccount(emailAddress):

    # AUTH
    token =getToken()
    authToken = token['authToken']
    csrfToken = token['csrfToken']

    accountId = getAccountId(emailAddress)
    payload = f"""<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Header><context xmlns="urn:zimbra"><userAgent name="ZimbraWebClient - GC114 (Win)"/><session id="38"/><format type="js"/><authToken>{authToken}</authToken><csrfToken>{csrfToken}</csrfToken></context></soap:Header><soap:Body><ModifyAccountRequest xmlns="urn:zimbraAdmin"><id>{accountId}</id><a n="zimbraAccountStatus">active</a></ModifyAccountRequest></soap:Body></soap:Envelope>"""

    # HEADERS
    headers = { 'Content-Type': 'application/soap+xml' }
    # POST REQUEST
    response = requests.post(URL, headers=headers, data=payload, verify=False)

    try:
        response = json.loads(response.text)  
        accountResponse = response['Body']['ModifyAccountResponse']['account']
        if emailAddress in str(accountResponse):
            return 1
        else:
            return 0
    except:
        return 0
 # METHOD ENDS HERE   

"""GET DEACTIVATION"""
# METHOD DEFINTION
def deactivateAccount(emailAddress):
    # AUTH
    token =getToken()
    authToken = token['authToken']
    csrfToken = token['csrfToken']

    accountId = getAccountId(emailAddress)
    payload = f"""<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Header><context xmlns="urn:zimbra"><userAgent name="ZimbraWebClient - GC114 (Win)"/><session id="38"/><format type="js"/><authToken>{authToken}</authToken><csrfToken>{csrfToken}</csrfToken></context></soap:Header><soap:Body><ModifyAccountRequest xmlns="urn:zimbraAdmin"><id>{accountId}</id><a n="zimbraAccountStatus">locked</a></ModifyAccountRequest></soap:Body></soap:Envelope>"""

    # HEADERS
    headers = { 'Content-Type': 'application/soap+xml' }
    # POST REQUEST
    response = requests.post(URL, headers=headers, data=payload, verify=False)

    try:
        response = json.loads(response.text)  
        accountResponse = response['Body']['ModifyAccountResponse']['account']
        if emailAddress in str(accountResponse):
            return 1
        else:
            return 0
    except:
        return 0
# METHOD ENDS HERE

"""ACCOUNT DELETION"""
# METHOD DEFINTION
def deleteAccount(emailAddress):
    # AUTH
    token =getToken()
    authToken = token['authToken']
    csrfToken = token['csrfToken']

    accountId = getAccountId(emailAddress)
    payload = f"""<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Header><context xmlns="urn:zimbra"><userAgent name="ZimbraWebClient - GC114 (Win)"/><session id="38"/><format type="js"/><authToken>{authToken}</authToken><csrfToken>{csrfToken}</csrfToken></context></soap:Header><soap:Body><DeleteAccountRequest xmlns="urn:zimbraAdmin"><id>{accountId}</id></DeleteAccountRequest></soap:Body></soap:Envelope>"""

    # HEADERS
    headers = { 'Content-Type': 'application/soap+xml' }
    
    # POST REQUEST
    response = requests.post(URL, headers=headers, data=payload, verify=False)

    try:
        response = json.loads(response.text)  
        if "DeleteAccountResponse" in response['Body']['DeleteAccountResponse']:
            return 1
        elif "Fault" in response['Body']:
            print(response['Body']['Fault']['Reason']['Text'])
            return 2
        else:
            return 0
    except:
        return 0
# METHOD ENDS HERE

"""RESET ACCOUNT PASSWORD"""
# METHOD DEFINTION
def resetPassword(emailAddress,password):

    # AUTH
    token =getToken()
    authToken = token['authToken']
    csrfToken = token['csrfToken']

    accountId = getAccountId(emailAddress)
    if accountId == 0:
        print("No Account ID Found")
        return 0

    # REQUEST BODY
    payload = f"""<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Header><context xmlns="urn:zimbra"><userAgent name="ZimbraWebClient - GC114 (Win)"/><session id="38"/><format type="js"/><authToken>{authToken}</authToken><csrfToken>{csrfToken}</csrfToken></context></soap:Header><soap:Body><SetPasswordRequest xmlns="urn:zimbraAdmin"><id>{accountId}</id><newPassword>{password}</newPassword></SetPasswordRequest></soap:Body></soap:Envelope>"""
    
    # HEADERS
    headers = { 'Content-Type': 'application/soap+xml' }
    
    # POST REQUEST
    response = requests.post(URL, headers=headers, data=payload, verify=False)

    try:
        response = json.loads(response.text) 
        if "SetPasswordResponse" in response['Body']:
            print("Password Updated")
            return 1
        else:
            try:
                print("Error : ",response['Body']['Fault']['Reason']['Text'])
            except:
                print("Error : Reason Unknown")
            return 0
    except:
        return 0
# METHOD ENDS

"""ADMIN DELEGATION RIGHTS"""
# METHOD DEFINTION
def createAdmin(emailAddress,domainName):
    # AUTH
    token =getToken()
    authToken = token['authToken']
    csrfToken = token['csrfToken']
    # REQUEST BODY
    payload = f"""<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Header><context xmlns="urn:zimbra"><userAgent name="ZimbraWebClient - GC113 (Win)"/><session/><format type="js"/><authToken>{authToken}</authToken><csrfToken>{csrfToken}</csrfToken></context></soap:Header><soap:Body><zextras xmlns="urn:zimbraAdmin"><module>ZxAdmin</module><action>doEditDelegationSettings</action><targetServers>{HOST}</targetServers><account>{emailAddress}</account><domain>{domainName}</domain><adminQuota>-1</adminQuota><editFeatures/><viewMail/><mode>ZxDoAddDelegationSettings</mode></zextras></soap:Body></soap:Envelope>"""

    # HEADERS
    headers = { 'Content-Type': 'application/soap+xml' }
    
    # POST REQUEST
    response = requests.post(URL, headers=headers, data=payload, verify=False)

    try:
        response = json.loads(response.text)
        response =  response['Body']['response']
        check = HOST in str(response)
        if check:
            print(f"Admin Delegation Created - {domainName}")
            return 1
        else:
            return 0
    except:
        try:
            resServer = response['Body']['Fault']['Reason']['Text']
            print(f"ERROR : {resServer}")
            return 2
        except:
            print("System Error Occured")
            return 0
# METHOD ENDS HERE


"""GET COS IDs"""
# METHOD DEFINTION
def getCOSId(cosName):
    # AUTH
    token =getToken()
    authToken = token['authToken']
    csrfToken = token['csrfToken']
    
    # REQUEST BODY
    payload = f"""<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Header><context xmlns="urn:zimbra"><userAgent name="ZimbraWebClient - GC114 (Win)"/><session /><format type="js"/><authToken>{authToken}</authToken><csrfToken>{csrfToken}</csrfToken></context></soap:Header><soap:Body><GetCosRequest xmlns="urn:zimbraAdmin"><cos by="name">{cosName}</cos></GetCosRequest></soap:Body></soap:Envelope>"""

    # HEADERS
    headers = { 'Content-Type': 'application/soap+xml' }
    
    # POST REQUEST
    response = requests.post(URL, headers=headers, data=payload, verify=False)
    try:
        response = json.loads(response.text)
        return response['Body']['GetCosResponse']['cos'][0]['id']

    except:
        return 0

"""ASSGIN MAIL BOX QUOTAS"""
# METHOD DEFINTION
def setMailBoxesLimit(domainName,cosLimitDetails):
    # AUTH
    token =getToken()
    authToken = token['authToken']
    csrfToken = token['csrfToken']

    #
    totalMailBoxCount = 0
    cosLimitsStr = ""
    for key in cosLimitDetails:
        cosLimitsStr +=f"{key}:{cosLimitDetails[key]},"
        totalMailBoxCount +=int(cosLimitDetails[key])
    #
    # REQUEST BODY
    payload = f"""<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Header><context xmlns="urn:zimbra"><userAgent name="ZimbraWebClient - GC113 (Win)"/><session/><format type="js"/><authToken>{authToken}</authToken><csrfToken>{csrfToken}</csrfToken></context></soap:Header><soap:Body><zextras xmlns="urn:zimbraAdmin"><module>ZxAdmin</module><action>setDomainSettings</action><targetServers>{HOST}</targetServers><accountLimit>{totalMailBoxCount}</accountLimit><resetCosLimits>{cosLimitsStr}</resetCosLimits><isBase64Encoded>false</isBase64Encoded><domain>{domainName}</domain><domainAccountQuota>0</domainAccountQuota></zextras></soap:Body></soap:Envelope>"""

    # HEADERS
    headers = { 'Content-Type': 'application/soap+xml' }
    
    # POST REQUEST
    response = requests.post(URL, headers=headers, data=payload, verify=False)
    try:
        
        response = json.loads(response.text)
        print("\n\n",response,'\n\n')
        response =  response['Body']['response']
        check = HOST in str(response)
        if check:
            print(f"Mail box Settings of {domainName} updated")
            return 1
        else:
            return 0
    except:
        try:
            resServer = response['Body']['Fault']['Reason']['Text']
            print(f"ERROR : {resServer}")
            return 2
        except:
            print("System Error Occured")
            return 0
# METHOD ENDS HERE

