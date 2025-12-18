import frappe
import requests
from waplytics.waplytics.utils import shorten_url 

class WhatsAppEngine:
	"""
	Lightweight wrapper for WhatsApp Cloud API.
	"""
	def __init__(self):
		self.base_url = "https://graph.facebook.com"
		self.api_version = "v19.0"
		self.access_token = frappe.conf.get("whatsapp_access_token")
		self.phone_number_id = frappe.conf.get("whatsapp_phone_id")
		
		if not self.access_token or not self.phone_number_id:
			frappe.log_error("Missing WhatsApp Config in site_config.json", "Waplytics Engine")

	def send_template(self, to_phone, template_name, language="en_US", variables=None, link_tracking=False, campaign_name=None):
		url = f"{self.base_url}/{self.api_version}/{self.phone_number_id}/messages"
		
		headers = {
			"Authorization": f"Bearer {self.access_token}",
			"Content-Type": "application/json"
		}
		
		components = []
		if variables:
			body_params = []
			for var in variables:
				if link_tracking and (str(var).startswith("http://") or str(var).startswith("https://")):
					var = shorten_url(var, campaign_name)
				
				body_params.append({"type": "text", "text": str(var)})
			
			if body_params:
				components.append({
					"type": "body",
					"parameters": body_params
				})

		payload = {
			"messaging_product": "whatsapp",
			"to": to_phone,
			"type": "template",
			"template": {
				"name": template_name,
				"language": {"code": language},
				"components": components
			}
		}

		try:
			response = requests.post(url, headers=headers, json=payload, timeout=10)
			response.raise_for_status()
			return response.json()
		except requests.exceptions.RequestException as e:
			frappe.log_error(f"WhatsApp API Error: {str(e)}", "Waplytics Send")
			return {"error": str(e)}

def dispatch_campaign_batch(campaign_name, batch_size=50):
	campaign = frappe.get_doc("WaCampaign", campaign_name)
	if campaign.status != "In Progress":
		return

	# Implementation placeholder for batch processing
	pass
