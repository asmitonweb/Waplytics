app_name = "waplytics"
app_title = "Waplytics"
app_publisher = "Asmit"
app_description = "The Ultimate Open-Source WhatsApp Analytics Engine"
app_email = "hello@asmitonweb.com"
app_license = "mit"

# Asset Configuration (Critical for Build)
app_include_css = ["/assets/waplytics/css/waplytics.bundle.css"]
app_include_js = ["/assets/waplytics/js/waplytics.bundle.js"]

# Document Events
doc_events = {
	"Wa Message Log": {
		"before_insert": "waplytics.waplytics.doctype.wa_link_tracker.utils.intercept_and_shorten"
	}
}

required_apps = ["frappe_whatsapp"]
