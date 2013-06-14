def get_appid(plivo_api,app_name):
	for application in plivo_api.get_applications()[1]['objects']:
		if application['app_name'] == app_name:
			app_id=application['app_id']
	return app_id

def rent_number(plivo_api,app_name):
	app_id=get_appid(plivo_api,app_name)
	response=plivo_api.get_number_group({"country_iso":"US","region":"california"})
	group_id=response[1]["objects"][0]["group_id"]
	response=plivo_api.rent_from_number_group({"group_id":group_id,"app_id":app_id})
	number=response[1]["numbers"][0]["number"]
	return number



