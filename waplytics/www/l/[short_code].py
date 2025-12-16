import frappe
from frappe import _

def get_context(context):
	# The route will be /l/<short_code>
	# Frappe web routing handles passing the last part as variable if configured or we can access via frappe.form_dict
	
	try:
		# We need to parse the path to get the short code
		path = frappe.request.path
		short_code = path.split('/')[-1]

		link_doc = frappe.db.get_value("Wa Link Tracker", {"short_code": short_code}, ["name", "original_url", "utm_source", "utm_medium", "utm_campaign"], as_dict=True)

		if not link_doc:
			frappe.local.flags.redirect_location = "/404"
			raise frappe.Redirect

		# Async Logging (to avoid blocking redirect) - using enqueue
		frappe.enqueue("waplytics.waplytics.doctype.wa_link_tracker.utils.log_click", 
			link_id=link_doc.name, 
			ip_address=frappe.local.request.remote_addr,
			user_agent=frappe.local.request.headers.get('User-Agent')
		)

		final_url = link_doc.original_url
		
		# UTM appending logic (if not already in URL)
		# We must ensure we don't double append or break existing query params
		if link_doc.utm_source or link_doc.utm_medium or link_doc.utm_campaign:
			import urllib.parse
			
			parsed_url = urllib.parse.urlparse(final_url)
			query_params = urllib.parse.parse_qs(parsed_url.query)
			
			if link_doc.utm_source:
				query_params['utm_source'] = [link_doc.utm_source]
			if link_doc.utm_medium:
				query_params['utm_medium'] = [link_doc.utm_medium]
			if link_doc.utm_campaign:
				query_params['utm_campaign'] = [link_doc.utm_campaign]
				
			new_query = urllib.parse.urlencode(query_params, doseq=True)
			final_url = urllib.parse.urlunparse(parsed_url._replace(query=new_query))

		frappe.local.flags.redirect_location = final_url
		raise frappe.Redirect

	except Exception as e:
		if not frappe.local.flags.redirect_location:
			frappe.log_error("Link Redirect Error")
			frappe.local.flags.redirect_location = "/404"
			raise frappe.Redirect
