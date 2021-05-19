from flask import Flask, request, g, render_template, jsonify, make_response, redirect, request, url_for, abort, session, flash

app = Flask(__name__, static_folder='static')


agent = agentConfig.agent
TommyAgent = agentConfig.TommyAgent
EdwareAgent = agentConfig.EdwareAgent
fidoServerUrl = fidoServerConfig.fidoServerUrl


global btnName
listPolicy = []


@app.route("/", methods=['GET', 'POST'])
def getMenu():
    if request.method == 'GET':
        return render_template('amsMenu.html', agent=agent)
    if request.method == 'POST':

        choosedAgentName = request.form.get('tvalue')

        EdwareAgentsecurityStatus = securityConfig.EdwareAgentsecurityStatus
        TommyAgentsecurityStatus = securityConfig.TommyAgentsecurityStatus
        MaxAgentsecurityStatus = securityConfig.MaxAgentsecurityStatus

        if choosedAgentName == 'EdwareAgent' and EdwareAgentsecurityStatus == 'enable':
            if request.form.get('成員註冊') == '成員註冊':
                btnValue = 'register'
                print("成員註冊")
                return redirect(url_for('memberRegister', _external=True, _scheme='https', btnName=btnValue, agentName=choosedAgentName))
            elif request.form.get('組態設定') == '組態設定':
                btnValue = 'config'
                print("組態設定")
                return redirect(url_for('login', _external=True, _scheme='https', btnName=btnValue, agentName=agent))
            elif request.form.get('人流預測') == '人流預測':
                btnValue = 'forecast'
                print("人流預測")
                return redirect(url_for('login', _external=True, _scheme='https', btnName=btnValue, agentName=choosedAgentName))

            elif request.form.get('報表查詢') == '報表查詢':
                btnValue = 'report'
                print("報表查詢")
                return redirect(url_for('login', _external=True, _scheme='https', btnName=btnValue, agentName=choosedAgentName))
            else:
                print('unknown')

        elif choosedAgentName == 'TommyAgent' and TommyAgentsecurityStatus == 'enable':
            if request.form.get('成員註冊') == '成員註冊':
                btnValue = 'register'
                print("成員註冊")
                return redirect(url_for('memberRegister', _external=True, _scheme='https', btnName=btnValue, agentName=choosedAgentName))
            elif request.form.get('組態設定') == '組態設定':
                btnValue = 'config'
                print("組態設定")
                return redirect(url_for('login', _external=True, _scheme='https', btnName=btnValue, agentName=choosedAgentName))
            elif request.form.get('人流預測') == '人流預測':
                btnValue = 'forecast'
                print("人流預測")
                return redirect(url_for('login', _external=True, _scheme='https', btnName=btnValue, agentName=choosedAgentName))

            elif request.form.get('報表查詢') == '報表查詢':
                btnValue = 'report'
                print("報表查詢")
                return redirect(url_for('login', _external=True, _scheme='https', btnName=btnValue, agentName=choosedAgentName))
            else:
                print('unknown')

        elif choosedAgentName == 'MaxAgent' and MaxAgentsecurityStatus == 'enable':
            if request.form.get('成員註冊') == '成員註冊':

                btnValue = 'register'
                print("成員註冊")
                return redirect(url_for('memberRegister', _external=True, _scheme='https', btnName=btnValue, agentName=choosedAgentName))
            elif request.form.get('組態設定') == '組態設定':
                btnValue = 'config'
                print("組態設定")
                return redirect(url_for('login', _external=True, _scheme='https', btnName=btnValue, agentName=choosedAgentName))
            elif request.form.get('人流預測') == '人流預測':
                btnValue = 'forecast'
                print("人流預測")
                return redirect(url_for('login', _external=True, _scheme='https', btnName=btnValue, agentName=choosedAgentName))

            elif request.form.get('報表查詢') == '報表查詢':
                btnValue = 'report'
                print("報表查詢")
                return redirect(url_for('login', _external=True, _scheme='https', btnName=btnValue, agentName=choosedAgentName))
            else:
                print('unknown')

        else:

            if request.form.get('成員註冊') == '成員註冊':
                btnValue = 'register'
                return redirect(url_for('memberRegister', _external=True, _scheme='https', btnName=btnValue, agentName=choosedAgentName))
            elif request.form.get('組態設定') == '組態設定':
                btnValue = 'config'
                print("組態設定")
                return redirect(url_for('config', _external=True, _scheme='https'))
            elif request.form.get('人流預測') == '人流預測':
                btnValue = 'forecast'
                print("人流預測")
                return redirect(url_for('forecastIndex', _external=True, _scheme='https'))

            elif request.form.get('報表查詢') == '報表查詢':
                btnValue = 'report'
                print("報表查詢")
                return redirect(url_for('report', _external=True, _scheme='https'))
            else:
                print('unknown')


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
