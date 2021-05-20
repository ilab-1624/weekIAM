import json
from flask import Flask, request, g, render_template, jsonify, make_response, redirect, request, url_for, abort, session, flash
import requests
from module import MemberRegisterController, ConfigController, CognitoApi
from module import agentConfig, fidoServerConfig, securityConfig, awsConfig

from werkzeug.http import parse_authorization_header
import boto3

app = Flask(__name__, static_folder='static')


client = boto3.client('iam', region_name=awsConfig.regionName, aws_access_key_id=awsConfig.aws_access_key_id,
                      aws_secret_access_key=awsConfig.aws_secret_access_key)
# --------------------------------------------------authorization page--------------------------------------
global btnName
listPolicy = []


@app.route("/login/<btnName>/<agentName>", methods=['GET', 'POST'])
def login(btnName, agentName):
    if request.method == 'GET':
        return render_template('webauthn.html', status=True, btnName=btnName, agentName=agentName)
    if request.method == 'POST':
        auth = request.headers.get('Authorization')
        # -----------------------get user data ----------------------------
        accessToken = request.get_data()
        decodeToken = accessToken.decode('utf-8')
        convertToJson = json.loads(decodeToken)

        # ------判斷user 是否在此agent群組中--------------------------------------------
        getCognitoGroup = convertToJson['cognito:groups']
        clickAgentBehavior = agentName
        getUserName = convertToJson['username']
        name = getUserName
        # ------------------------------query user from IAM-------------------------------
        # ---------------------- -------get user group -----------------------------------
        response = client.list_groups_for_user(
            UserName=name,
            MaxItems=123
        )
        # print('----------------------get user group-------- -----------------------------')
        getGroup = response['Groups'][0]['GroupName']

        # ----------------------------get group policy-------------------------------------
        response = client.list_attached_group_policies(
            GroupName=getGroup,
            MaxItems=123
        )
        # print('---從群組連接--getGroup policy--------')
        for item in range(len(response['AttachedPolicies'])):
            getPolicyName = response['AttachedPolicies'][item]['PolicyName']
            listPolicy.append(getPolicyName)

        # ----------------------------get role policy---------------------------------------
       customerRole = securityConfig.customerRole
        staffRole = securityConfig.staffRole
        managerRole = securityConfig.managerRole
        
        if getGroup == 'customer':
            roleNameForPolicy = customerRole
        elif getGroup =='staff':
            roleNameForPolicy = staffRole
        else:
            roleNameForPolicy = managerRole
        print(roleNameForPolicy)
        response = client.list_attached_role_policies(
            RoleName=roleNameForPolicy+'_'+clickAgentBehavior,
            MaxItems=123
        )

        # -------------------------get role policy-------------------------------------------------

        for items in range(len(response['AttachedPolicies'])):
            getRolePolicy = response['AttachedPolicies'][items]['PolicyName']

            listPolicy.append(getRolePolicy)

        # ------------------------------ getUserPolicy-----------------------------------------------
        response = client.list_attached_user_policies(
            UserName=name,
            MaxItems=123
        )
        #'---直接連接---get user policy------'
        for policies in range(len(response['AttachedPolicies'])):
            getUserPolicy = response['AttachedPolicies'][policies]['PolicyName']
            listPolicy.append(getUserPolicy)

        # --------------------------------------get role policy---------------------------------------
        print('--------所有政策--------')
        print(listPolicy)
    # -----------authorization page-----判斷user policy有無在listpolicy中----------------------------
        userinfo = dict()

        getPersonalPolicy = btnName+'_'+clickAgentBehavior
        # '判斷此使用者行為btnName+此人選擇的agent'
        print(getPersonalPolicy)
        if getPersonalPolicy in listPolicy:
            loginStatus = 'success'
        else:
            loginStatus = 'fail'

    # ------------  get information compose to  dict---return response to client----------------------
        userinfo['auth'] = auth
        userinfo['name'] = name
        userinfo['policy'] = listPolicy
        userinfo['loginStatus'] = loginStatus
        userinfo['behavior'] = btnName
        userinfo['userAgent'] = getCognitoGroup[0]
        userinfo['agentBehavior'] = clickAgentBehavior

        print(userinfo)
        return jsonify(userinfo)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
