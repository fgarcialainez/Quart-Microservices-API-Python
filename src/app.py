import quart_injector
from quart import Quart
from quart_schema import QuartSchema

from conf import configure
from application.cli import drop_db, populate_db
from application.views.admin_views import AdminUpdateExperienceView
from application.views.customer_views import CustomerListExperiencesView, CustomerBookExperienceView
from application.views.partner_views import PartnerListExperiencesView, PartnerUpdateExperienceView, \
    PartnerGetExperienceView


# Create the Quart app
app = Quart(__name__)

# OpenAPI (Swagger) docs
QuartSchema(app)

# Define routes
app.add_url_rule(
    "/customer/book",
    view_func=CustomerBookExperienceView.as_view("book")
)
app.add_url_rule(
    "/customer/experiences",
    view_func=CustomerListExperiencesView.as_view("customer_experiences_list")
)
app.add_url_rule(
    "/admin/experiences/<experience_id>",
    view_func=AdminUpdateExperienceView.as_view("admin_experience_update")
)
app.add_url_rule(
    "/partner/experiences",
    view_func=PartnerListExperiencesView.as_view("partner_experiences_list")
)
app.add_url_rule(
    "/partner/experiences/<experience_id>",
    view_func=PartnerUpdateExperienceView.as_view("partner_experience_update")
)
app.add_url_rule(
    "/partner/experiences/<experience_id>",
    view_func=PartnerGetExperienceView.as_view("partner_experience_get")
)

# Setup commands
app.cli.add_command(populate_db, "populate-db")
app.cli.add_command(drop_db, "drop-db")

# Wire the app to the injector configuration
quart_injector.wire(app, configure)

if __name__ == "__main__":
    # Run the app
    app.run()
