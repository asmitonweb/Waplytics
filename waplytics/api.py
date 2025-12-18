import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def webhook():
	"""
	High-speed webhook receiver for WhatsApp Cloud API.
	Validates the token (GET) or accepts the payload (POST).
	"""
	if frappe.request.method == "GET":
		# Verification Request
		verify_token = frappe.conf.get("whatsapp_webhook_secret")
		mode = frappe.form_dict.get("hub.mode")
		token = frappe.form_dict.get("hub.verify_token")
		challenge = frappe.form_dict.get("hub.challenge")

		if mode and token:
			if mode == "subscribe" and token == verify_token:
				frappe.response.status_code = 200
				return int(challenge)
			else:
				frappe.response.status_code = 403
				return
	
	elif frappe.request.method == "POST":
		# Ingestion Request
		payload = frappe.request.json
		if not payload:
			return
		
		# Enqueue for background processing for maximum speed (Native Architecture)
		frappe.enqueue(
			'waplytics.waplytics.api.process_webhook',
			queue='short',
			payload=payload
		)
		
		# Respond immediately to Meta
		return "OK"

def process_webhook(payload):
	"""
	Background worker to process the raw JSON logs.
	"""
	try:
		# Extract relevant data from the standard WhatsApp JSON structure
		entry = payload.get("entry", [])[0]
		changes = entry.get("changes", [])[0]
		value = changes.get("value", {})
		
		# Check for different types of updates (Messages vs Statuses)
		if "messages" in value:
			for msg in value["messages"]:
				create_message_log(msg, value)
		
		elif "statuses" in value:
			for status in value["statuses"]:
				update_message_status(status)

	except Exception as e:
		frappe.log_error(f"Error processing webhook: {str(e)}", "Waplytics Webhook")

def create_message_log(msg_data, value_data):
	"""
	Creates a new WaMessageLog for incoming messages.
	"""
	sender = msg_data.get("from")
	msg_type = msg_data.get("type")
	msg_body = ""
	
	# Extract body based on type
	if msg_type == "text":
		msg_body = msg_data.get("text", {}).get("body")
	elif msg_type == "interactive":
		interactive = msg_data.get("interactive", {})
		if interactive.get("type") == "button_reply":
			msg_body = f"[Button] {interactive.get('button_reply', {}).get('title')}"
		elif interactive.get("type") == "list_reply":
			msg_body = f"[List] {interactive.get('list_reply', {}).get('title')}"
	
	doc = frappe.get_doc({
		"doctype": "WaMessageLog",
		"direction": "Inbound",
		"message_id": msg_data.get("id"),
		"timestamp": frappe.utils.now(),
		"to_phone": value_data.get("metadata", {}).get("display_phone_number"), # Receiver is us
		"from_phone": sender,
		"status": "Received",
		"content": msg_body
	})
	doc.insert(ignore_permissions=True)

def update_message_status(status_data):
	"""
	Updates the status of an existing WaMessageLog (Sent -> Delivered -> Read).
	"""
	message_id = status_data.get("id")
	new_status = status_data.get("status") # sent, delivered, read, failed
	
	# Map Meta status to our DocType options
	status_map = {
		"sent": "Sent",
		"delivered": "Delivered",
		"read": "Read",
		"failed": "Failed"
	}

	if frappe.db.exists("WaMessageLog", {"message_id": message_id}):
		doc = frappe.get_doc("WaMessageLog", {"message_id": message_id})
		doc.status = status_map.get(new_status, doc.status)
		
		# Update timestamp based on status for precise analytics
		if new_status == "delivered":
			doc.delivery_time = frappe.utils.now() 
		elif new_status == "read":
			doc.read_time = frappe.utils.now()
			
		doc.save(ignore_permissions=True)
