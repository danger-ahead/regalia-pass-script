import os
import dotenv

dotenv.load_dotenv()

mailgun_key = os.getenv("MAILGUN_KEY")
token = os.getenv("TOKEN")
mailgun_domain = os.getenv("MAILGUN_DOMAIN")
create_pass_api = os.getenv("CREATE_PASS_API")
