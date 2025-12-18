import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime

class WaCampaign(Document):
	def validate(self):
		if self.status == "Scheduled" and not self.schedule_time:
			frappe.throw("Schedule Time is required for scheduled campaigns")

	def on_submit(self):
		self.status = "In Progress"
		self.save()
		
		# Trigger Background Job with correct module path
		frappe.enqueue(
			'waplytics.waplytics.engine.dispatch_campaign_batch',
			queue='long',
			campaign_name=self.name,
			timeout=1500
		)
		
		frappe.msgprint("Campaign Started! Messages are being queued.")
