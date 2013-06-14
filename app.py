from flask import Flask,request,Response,make_response,url_for

import plivo



SIP="sip:abishek130613133829@phone.plivo.com"

MOBILE=919940728522

CALLLER_NAME="plivo"

CALLLER_ID=19512977322

BASE_URL="http://ancient-taiga-3101.herokuapp.com"

VOICEMAIL_NUMBER=13235960802

app = Flask(__name__)

app.debug=True

@app.route('/forward')

def forward():
	response=plivo.Response()
	response.addSpeak("Please wait while we are forwarding your call")
	response.addDial(callerName=CALLLER_NAME).addUser(SIP)
	response.addDial(callerId=CALLLER_ID).addNumber(MOBILE)
	response.addSpeak("The number you're trying is not reachable at the moment. Please leave a message after the beep")
	response.addDial(callerId=CALLLER_ID,
			action=BASE_URL+url_for('voice_mail')).addNumber(VOICEMAIL_NUMBER)
	response=make_response(response.to_xml())
	response.headers['Content-Type']='text/xml'
	
	return response


@app.route('/voice/mail')

def voice_mail():
	response=plivo.Response()
	response.addSpeak("Please leave your message after the beep")
	response.addRecord(action=BASE_URL+url_for('message'))
	response.addSpeak("Thank you, your message has been recorded")
	response.addHangup()
	response=make_response(response.to_xml())
	response.headers['Content-Type']='text/xml'
	
	return response


@app.route('/message')


def message():
	record_url=request.args.get('RecordUrl','')
	MESSAGE="Hey, we have received a voice message for you. You can access them at %s" %(record_url)
	response=plivo.Response()
	response.addMessage(src=CALLLER_ID,dst=MOBILE,body=MESSAGE)
	response=make_response(response.to_xml())

	response.headers['Content-Type']='text/xml'
	
	return response



if __name__ == '__main__':
       app.run(host='0.0.0.0')

