from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "user.login"
login_manager.refresh_view = "user.login"
login_manager.needs_refresh_message = (
	"To protect your account, please reauthenticate to access this page."
)
login_manager.needs_refresh_message_category = "info"


from app.admin.views import MyAdminIndexView

flask_admin = Admin(
	name="ecomm", template_mode="bootstrap4", index_view=MyAdminIndexView()
)
