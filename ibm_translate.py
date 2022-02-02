from ibm_watson import LanguageTranslatorV3, SpeechToTextV1, TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json

import os

lan_tr_TOKEN = os.environ["lan_tr_TOKEN"]
lan_tr_URL = os.environ["lan_tr_URL"]

sp_text_TOKEN = os.environ["sp_text_TOKEN"]
sp_text_URL = os.environ["sp_text_URL"]

text_sp_TOKEN = os.environ["text_sp_TOKEN"]
text_sp_URL = os.environ["text_sp_URL"]

language_translator_auth = IAMAuthenticator(lan_tr_TOKEN)
language_translator = LanguageTranslatorV3(
    version='2018-05-01',
    authenticator=language_translator_auth)
language_translator.set_service_url(lan_tr_URL)

speech_to_text_auth = IAMAuthenticator(sp_text_TOKEN)
speech_to_text = SpeechToTextV1(
    authenticator=speech_to_text_auth
)
speech_to_text.set_service_url(sp_text_URL)

text_to_speech_auth = IAMAuthenticator(text_sp_TOKEN)
text_to_speech = TextToSpeechV1(
    authenticator=text_to_speech_auth
)
text_to_speech.set_service_url(text_sp_URL)


voices = {
    'fr-FR': 'fr-FR_NicolasV3Voice',
    'en-US': 'en-US_MichaelV2Voice',
    'de-DE': 'de-DE_ErikaV3Voice',
    'it-IT': 'it-IT_FrancescaV3Voice',
    'ja-JP': 'ja-JP_EmiV3Voice',
    'pt-BR': 'pt-BR_IsabelaVoice',
    'es-US': 'es-US_SofiaV3Voice',
}


def select_voice(text, language):
    for i, j in voices.items():
        if language == i[:2]:
            audio = text_to_speech.synthesize(text=text, accept='audio/ogg;codecs=opus', voice=j).get_result()
            return audio.content


def language_identification(list_of_languages, identify_language):
    for i in identify_language:
        for j, k in list_of_languages.items():
            if i["language"] == j:
                return [j, k]
    return 0


def find_name(list_of_languages, language_code):
    for i, j in list_of_languages.items():
        if i == language_code:
            return j


def response_to_list(response):
    languages_list = json.dumps(response, indent=1)
    languages_list = json.loads(languages_list)
    return languages_list["languages"]
