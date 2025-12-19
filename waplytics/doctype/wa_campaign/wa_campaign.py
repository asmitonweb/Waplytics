import frappe
from frappe.model.document import Document
from waplytics.waplytics.engine import dispatch_campaign_batch

class WaCampaign(Document):
	def on_submit(self):
		if self.status == "Draft":
			self.status = "In Progress"
			self.save()
			
			# Trigger Background Job
			frappe.enqueue(
				dispatch_campaign_batch,
				queue='long',
				campaign_name=self.name
			)
