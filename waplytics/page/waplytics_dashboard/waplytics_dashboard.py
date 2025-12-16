import frappe

@frappe.whitelist()
def get_dashboard_data():
	# Query WA Message Log from frappe_whatsapp
	# Assuming Table Name `tabWA Message Log` and field `status`
	
	stats = {
		"sent": 0,
		"delivered": 0,
		"read": 0,
		"failed": 0,
		"clicks": 0
	}
	
	try:
		# Message Stats
		data = frappe.db.sql("""
			SELECT status, count(*) as count
			FROM `tabWa Message Log`
			GROUP BY status
		""", as_dict=True)
		
		for d in data:
			s = d.status.lower()
			if s in stats:
				stats[s] = d.count
				
		# Click Stats
		clicks = frappe.db.count("Wa Link Click")
		stats["clicks"] = clicks
		
	except Exception:
		# Table might not exist yet if app not installed/migrated
		pass
		
	return stats
