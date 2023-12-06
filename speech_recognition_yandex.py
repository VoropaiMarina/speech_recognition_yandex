import requests
import json
import time


def send_speech_recognition_request(api_key, uri):
	"""
	Sends a speech recognition request and returns the operation ID and response data.

	:param api_key: API key for authorization.
	:param uri: URI of the audio file for recognition.
	:return: Dictionary with the operation ID and response data.
	"""
	url = 'https://transcribe.api.cloud.yandex.net/speech/stt/v2/longRunningRecognize'
	headers = {
		'Authorization': f'Api-Key {api_key}',
		'Content-Type': 'application/json'
	}
	data = {
		"config": {
			"specification": {
				"languageCode": "ru-RU",
				"model": "general",
				"profanityFilter": False,
				"audioEncoding": "OGG_OPUS",
				"sampleRateHertz": 48000,
				"audioChannelCount": 1,
				"rawResults": False
			}
		},
		"audio": {
			"uri": uri
		}
	}

	response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
	response_data = response.json()

	return {"operation_id": response_data.get("id"), "data": response_data}


def get_speech_recognition_results(api_key, operation_id, output_file_path):
	"""
	Retrieves speech recognition results and writes them to a file.

	:param api_key: API key for authorization.
	:param operation_id: Operation ID for speech recognition.
	:param output_file_path: Path to save the result to a file.
	"""
	url = f'https://operation.api.cloud.yandex.net/operations/{operation_id}'
	headers = {
		'Authorization': f'Api-Key {api_key}'
	}

	response = requests.get(url, headers=headers, verify=False)

	if response.status_code == 200:
		response_data = response.json()
		if response_data.get("done", False):
			full_text = ""

			for chunk in response_data.get("response", {}).get("chunks", []):
				for alternative in chunk.get("alternatives", []):
					full_text += alternative.get("text", "") + "\n"

			with open(output_file_path, "w", encoding="utf-8") as file:
				file.write(full_text)
		else:
			print("Operation is not yet completed.")
	else:
		print("Error during the request: ", response.status_code)

# Replace these values with your own data
api_key = 'your_api'
uri = 'your_audiob_in_.opus'


if __name__ == "__main__":
	operation_result = send_speech_recognition_request(api_key, uri)
	operation_id = operation_result.get("operation_id")

	if operation_id:
		print("Waiting for 5 minutes before retrieving the results...")
		time.sleep(300)  # Wait for 5 minutes (300 seconds)
		get_speech_recognition_results(api_key, operation_id, "output.txt")
