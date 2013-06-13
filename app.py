from flask import Flask,request,Response,make_response

import plivo



SIP="sip:abishek130613133829@phone.plivo.com"

MOBILE=919940728522

CALLLER_NAME="plivo"

CALLLER_ID=19512977322


app = Flask(__name__)

app.debug=True

@app.route('/forward')

def forward():
	response=plivo.Response()
	response.addDial(callerName=CALLLER_NAME).addUser(SIP)
	response.addDial(callerId=CALLLER_ID).addNumber(MOBILE)
	response=make_response(response.to_xml())
	response.headers['Content-Type']='text/xml'
	
	return response



if __name__ == '__main__':
       app.run(host='0.0.0.0')

