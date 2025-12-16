import frappe
from frappe.model.document import Document
import string
import random

class WaLinkTracker(Document):
	def before_insert(self):
		if not self.short_code:
			self.short_code = self.generate_short_code()
			
	def generate_short_code(self, length=6):
		"""Generate a random short code."""
		chars = string.ascii_letters + string.digits
		while True:
			code = ''.join(random.choices(chars, k=length))
			if not frappe.db.exists("Wa Link Tracker", {"short_code": code}):
				return code

	def validate(self):
		# Ensure unique constraint if manually set
		if self.short_code:
			existing = frappe.db.exists("Wa Link Tracker", {"short_code": self.short_code})
			if existing and existing != self.name:
				frappe.throw("Short Code already exists.")
