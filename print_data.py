import json
data_file = open("bot_bot_data.txt", "r")
temp_data = data_file.read()
data_file.close()
data_dict = json.loads(temp_data)

for adc in data_dict:
	print("{}:".format(adc))
	for support in data_dict[adc]:
		print ("	{}: {}".format(support, data_dict[adc][support]))
