import json
from urllib import request
from time import sleep
user_api = '1c0be6bf-e4a8-4807-bc3d-83183356944a'
featured_url = 'https://na.api.pvp.net/observer-mode/rest/featured?api_key={}'.format(user_api)
champions_url = 'https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion?api_key={}'.format(user_api)
with open('meta_adcs.txt') as a:
	adc_list = a.read().splitlines()
a.close()
with open('meta_supports.txt') as s:
	support_list = s.read().splitlines()
s.close()


adc_dict = {}
support_dict = {}
data_file = open("bot_bot_data.txt", "r")
temp_data = data_file.read()
data_file.close()
data_dict = json.loads(temp_data)

game_id_list = []
champions_data = request.urlopen(champions_url)
json_string_champions = champions_data.read().decode('utf-8')
json_data_champions = json.loads(json_string_champions)

for adc in adc_list:
	adc_id = json_data_champions["data"][adc]["id"]
	adc_dict[adc_id] = adc

for support in support_list:
	support_id = json_data_champions["data"][support]["id"]
	support_dict[support_id] = support
while(True):	
	featured_data = request.urlopen(featured_url)
	json_string_featured = featured_data.read().decode('utf-8')
	json_data_featured = json.loads(json_string_featured)
	
	adc_flag, multi_adcs, support_flag, multi_supports = False, False, False, False
	adc_id, support_id, player_count = 0, 0, 0
	sleeptime = json_data_featured["clientRefreshInterval"]
	for game in json_data_featured["gameList"]:
		#if len(game_id_list) > 100:
		#	del game_id_list[:]
		if game["gameId"] in game_id_list:
			continue
		else:
			game_id_list.append(game["gameId"])
		for summoner in game["participants"]:
			player_count += 1
			if summoner["championId"] in adc_dict:
				#print(adc_dict[summoner["championId"]])
				if adc_flag == True:
					multi_adcs = True
				else:
					adc_id = summoner["championId"]		
					adc_flag = True
			elif summoner["championId"] in support_dict:
				#print(support_dict[summoner["championId"]])
				if support_flag == True:
					multi_supports = True
				else:
					support_id = summoner["championId"]
					support_flag = True
			if player_count == 5:
				#print("New Game")
				player_count = 0
				if multi_adcs == False and multi_supports == False and adc_flag == True and support_flag == True:
					if adc_dict[adc_id] in data_dict:
						if support_dict[support_id] in data_dict[adc_dict[adc_id]]:
							data_dict[adc_dict[adc_id]][support_dict[support_id]] += 1
						else:
							data_dict[adc_dict[adc_id]][support_dict[support_id]] = 1
					else:
						data_dict[adc_dict[adc_id]] = {}
						data_dict[adc_dict[adc_id]][support_dict[support_id]] = 1
				adc_flag, multi_adcs, support_flag, multi_supports = False, False, False, False	
	print(data_dict)
	json_obj = json.dumps(data_dict)
	data_file = open('bot_bot_data.txt', 'w')
	data_file.write(json_obj)
	data_file.close()
	#break
	sleep(300)
