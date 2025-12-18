import frappe
import string
import random

def generate_short_code(length=6):
	"""Generates a random 6-character string."""
	chars = string.ascii_letters + string.digits
	return ''.join(random.choice(chars) for _ in range(length))

def shorten_url(original_url, campaign_name=None):
	"""
	Creates a WaLinkTracker entry and returns the short URL.
	"""
	short_code = generate_short_code()
	
	# Ensure uniqueness
	while frappe.db.exists("WaLinkTracker", {"short_code": short_code}):
		short_code = generate_short_code()
	
	doc = frappe.get_doc({
		"doctype": "WaLinkTracker",
		"short_code": short_code,
		"original_url": original_url,
		"campaign": campaign_name,
		"click_count": 0
	})
	doc.insert(ignore_permissions=True)
	
	return f"{frappe.utils.get_url()}/l/{short_code}"

@frappe.whitelist(allow_guest=True)
def handle_redirect(short_code):
	"""
	Handles the redirect when a user clicks the short link.
	"""
	if not short_code:
		return
		
	# Async update for speed
	link_doc = frappe.db.get_value("WaLinkTracker", {"short_code": short_code}, ["name", "original_url"], as_dict=True)
	
	if link_doc:
		frappe.db.sql("""UPDATE `tabWaLinkTracker` SET click_count = click_count + 1 WHERE name = %s""", (link_doc.name))
		frappe.db.commit()
		
		frappe.local.response["type"] = "redirect"
		frappe.local.response["location"] = link_doc.original_url
	else:
		frappe.local.response["type"] = "redirect"
		frappe.local.response["location"] = "/" 
