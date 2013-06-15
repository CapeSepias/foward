
call forward
==========

This application is a jab at trying to showcase a wide variety of Plivo's API like Direct Dialing, Call Recording, Text Messaging,Renting number, Application API to build an app which provides user with a plivo number and a voice mail number which when called to would forward the incoming to call to the specified SIP Endpoint or Mobile Phone. If the call is not answered the call is automatically transferred to the Voice Mail, wherein the caller can record his message. A link to the voice message would be texted to the user at his mobile number

__Installation___


Clone the repo:

```bash
    git clone git@github.com:abishekk92/forward.git
```

Install the Python dependencies:

```bash
    pip install -r requirements.txt
```
Note: 

  - You would need pip to be installed. Instructions on how to install pip for variety of operating systems can be found [here](http://www.pip-installer.org/en/latest/installing.html)

  - The app uses MongoDB as the datastore, you can install it following the instruction found [here](http://docs.mongodb.org/manual/installation/)
  
  - The app heavily uses Plivo's API, please make sure to get a [free developer account](http://plivo.com/)
  
  - Update the AUTH_ID and AUTH_TOKEN in the app.config as follows 
  
    ```python
        AUTH_ID="YOUR-AUTH-ID"
        AUTH_TOKEN="YOUR-AUTH-TOKEN"
        BASE_URL="APP-BASE-URL"
    ```
    
  - Update the MongoDB host in models.py with your values as follows
     
     ```python
        connect('forward',host="YOUR-MONGODB_HOST")
     ```
     
  - To run the app
    
    ```bash
        foreman start
    ```
  - Please follow the instructions here to [deploy on heroku]( https://devcenter.heroku.com/articles/python)

__Workflow__ : 
   
   - The apps allows one to create conference on a subject and invite people to the conference by adding their mobile numbers.

   !["Call Forward"](https://raw.github.com/abishekk92/forward/master/screenshots/Screenshot%20from%202013-06-15%2023:12:23.png)
 
   

   - Once the conference is created, the members are notified with the conference number and pin. The number is provisioned on the fly using Plivo's rent number endpoint. The code would look like
     
    ```python
            def rent_number(plivo_api,app_name="Conference Call"):
                app_id=get_appid(plivo_api,app_name)
	            response=plivo_api.get_number_group({"country_iso":"US","region":"california"})
	            group_id=response[1]["objects"][0]["group_id"]
	            response=plivo_api.rent_from_number_group({"group_id":group_id,"app_id":app_id})
	            number=response[1]["numbers"][0]["number"]
	            return number
     ```

   - Once the conference is over and if the moderator has opted in for the conference to be recorded, A message containing the record url is messaged
      
      ```python
                response.addConference(body='plivo',
    			       action= BASE_URL+url_for('submit_recording'),
				       method='GET',
				       record=record_value)
      ```
      The message is sent out using the Plivo API as follows

     ```python 
                def notify(message,mobile):
                    response=plivo_api.send_message({'src':CALLER_ID,
				                                    'dst':mobile,
				                                    'text':message,
				                                    'type':'sms'
			    	                                })
	                return response
     ```
