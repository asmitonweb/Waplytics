frappe.pages['waplytics-dashboard'].on_page_load = function (wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Waplytics Dashboard',
        single_column: true
    });

    // Create Structure
    $(wrapper).find('.layout-main-section').append(`
		<div class="row">
			<div class="col-md-6">
				<div class="frappe-card">
					<div class="card-head"><h4>Message Status</h4></div>
					<div class="card-body" id="chart-status"></div>
				</div>
			</div>
			<div class="col-md-6">
				<div class="frappe-card">
					<div class="card-head"><h4>Click Performance</h4></div>
					<div class="card-body" id="chart-clicks"></div>
				</div>
			</div>
		</div>
	`);

    // Fetch Data
    frappe.call({
        method: "waplytics.waplytics.page.waplytics_dashboard.waplytics_dashboard.get_dashboard_data",
        callback: function (r) {
            if (r.message) {
                render_charts(r.message);
            }
        }
    });

    function render_charts(data) {
        // Status Chart
        new frappe.Chart("#chart-status", {
            data: {
                labels: ["Sent", "Delivered", "Read", "Failed"],
                datasets: [
                    {
                        name: "Count",
                        values: [data.sent, data.delivered, data.read, data.failed]
                    }
                ]
            },
            title: "Message Status (Last 30 Days)",
            type: 'bar',
            height: 250,
            colors: ['#7cd6fd', '#743ee2', '#2196f3', '#ff5858']
        });

        // Click Funnel / CTR
        new frappe.Chart("#chart-clicks", {
            data: {
                labels: ["Read", "Clicked"],
                datasets: [
                    {
                        name: "Users",
                        values: [data.read, data.clicks]
                    }
                ]
            },
            title: "Engagement (Read to Click)",
            type: 'percentage',
            height: 250,
            colors: ['#2196f3', '#48c4ae']
        });
    }
}
