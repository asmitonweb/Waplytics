import frappe
import re

def log_click(link_id, ip_address, user_agent):
	"""Log a click to Wa Link Click and update stats."""
	try:
		# Create Log
		click = frappe.get_doc({
			"doctype": "Wa Link Click",
			"link_tracker": link_id,
			"ip_address": ip_address,
			"user_agent": user_agent
		})
		click.insert(ignore_permissions=True)
		
		# Update Counter
		frappe.db.sql("""
			UPDATE `tabWa Link Tracker`
			SET total_clicks = total_clicks + 1
			WHERE name = %s
		""", (link_id,))
		
	except Exception:
		frappe.log_error("Failed to log click")

def process_message_text(text, campaign=None):
	"""
	Scan text for URLs, shorten them, and return modified text.
	"""
	url_pattern = r'(https?://[^\s]+)'
	urls = re.findall(url_pattern, text)
	
	if not urls:
		return text
		
	for url in urls:
		# Don't shorten if already shortened (simple check)
		if "/l/" in url:
			continue
			
		# Create Tracker
		tracker = frappe.get_doc({
			"doctype": "Wa Link Tracker",
			"original_url": url,
			"campaign": campaign,
			# Default UTMs will be picked up from DocType defaults if not set here
		})
		tracker.insert(ignore_permissions=True)
		
		short_url = frappe.utils.get_url(f"/l/{tracker.short_code}")
		text = text.replace(url, short_url)
		
	return text

def intercept_and_shorten(doc, method):
	"""
	Hook to intercept WA Message Log before insert,
	scan content/message field, and shorten links.
	"""
	# Check possible field names for message content
	if hasattr(doc, 'message'):
		doc.message = process_message_text(doc.message, campaign=getattr(doc, 'campaign', None))
	elif hasattr(doc, 'content'):
		doc.content = process_message_text(doc.content, campaign=getattr(doc, 'campaign', None))

