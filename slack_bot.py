import json, configparser, os
import requests





class SlackBot():

	# Base URL for all Slack API
	_URL = 'https://slack.com/api/'


	def __init__(self, bot_token, user_token):
		self._bot_token = bot_token
		self._user_token = user_token


	def __del__(self):
		pass


	# MESSAGING FUNCTIONS


	# Sends a message to given channel
	def send_msg(self, channel_id, msg, *blocks):

		endpoint = 'chat.postMessage'

		payload = {
			"text" : msg,
			"channel" : channel_id,
			"blocks" : blocks
		}


		return self._post_api(endpoint, payload)


	# Updates an existing message
	def update_msg(self, channel_id, timestamp, msg, blocks = None):

		endpoint = "chat.update"

		payload = {
			"text" : msg,
			"channel" : channel_id,
			"ts" : timestamp,
			"blocks" : blocks
		}

		return self._post_api(endpoint, payload)




	# MANAGEMENT FUNCTIONS


	# Create a new channel
	def create_channel(self, channel_name):

		endpoint = 'channels.create'

		payload = {
			"name" : channel_name,
			"validate" : True
		}

		return self._post_api(endpoint, payload, False)


	# Invite a user to a channel
	def invite_channel(self, channel_id, user_id):

		endpoint = 'channels.invite'

		payload = {
			"user" : user_id,
			"channel" : channel_id
		}

		return self._post_api(endpoint, payload, False)


	# Returns a user object for the given email
	def get_user(self, email):

		endpoint = 'users.lookupByEmail'

		params = {
			"email" : email
		}

		response = self._get_api(endpoint, params)

		return response['user']



	# Creates a channel and adds all the emails given
	# For Feras 😉
	def init_channel(self, channel_name, emails):
		response = self.create_channel(channel_name)
		channel_id = response['channel']['id']

		for email in emails:
			user = self.get_user(email)
			user_id = user['id']
			self.invite_channel(channel_id, user_id)



	# BLOCK KIT FUNCTIONS


	# Create's actions to include in messages
	def create_actions(self, *elements):

		block = {
			"type": "actions",
			"elements": elements
		}

		return block


	# Creates a button element for messages
	def create_button(self, text, value):

		block = {
			"type": "button",
			"text": {
				"type": "plain_text",
				"text": text,
				"emoji": True
			},
			"value": value
		}	

		return block




	# PRIVATE HELPER METHODS

	# Private method to create the header for any HTTP calls
	def _headers(self, use_bot_token):

		token = self._bot_token if use_bot_token else self._user_token

		headers = {
			"Content-type" : "application/json",
			"Authorization": "Bearer " + token
		}
		return headers


	# Private method to hit a Slack GET API
	def _get_api(self, endpoint, params = None, use_bot_token = True):
		headers = self._headers(use_bot_token)
		url = self._URL + endpoint
		response = requests.get(url = url, params = params, headers = headers)

		if response.status_code != 200:
			raise Exception('Slack BIG mad yo')

		return response.json()


	# Private method to hit a Slack POST API
	def _post_api(self, endpoint, payload, use_bot_token = True):
		headers = self._headers(use_bot_token)
		url = self._URL + endpoint
		response = requests.post(url = url, data = json.dumps(payload), headers = headers)

		if response.status_code != 200:
			raise Exception('Slack BIG mad yo')

		return response.json()





# Uses config parser to grab the bot's tokens and create it
def create_config_bot():

	# First check env variables, used in heroku deployments
	if 'slack_bot_token' in os.environ:
		bot_token = os.environ['slack_bot_token']
		user_token = os.environ['slack_user_token']

	# Else check config file
	else:
		config = configparser.ConfigParser()
		config.read('bot_config.cfg')

		bot_token = config['slack']['bot_token']
		user_token = config['slack']['user_token']

	bot = SlackBot(bot_token, user_token)
	return bot


def main():

	bot = create_config_bot()
	# Do stuff here



if __name__ == '__main__':
	main()



