from kenindus.utils.AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException
from django.conf import settings

gateway = AfricasTalkingGateway(settings.ATG_USERNAME, settings.ATG_API_KEY)


def send_text(to, msg):
	results = gateway.sendMessage(to, msg)
	return results
