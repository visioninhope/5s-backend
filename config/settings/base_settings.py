from pathlib import Path
from decouple import config


BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config("SECRET_KEY", default="default_secret_key")

DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party application
    "django_filters",
    "rest_framework",
    "djoser",
    "corsheaders",
    "drf_yasg",
    "django_redis",
    "django_extensions",
    'django_crontab',
    # Main application
    "src.StaffControl.Employees.apps.EmployeesConfig",
    "src.StaffControl.Locations.apps.LocationsConfig",
    "src.StaffControl.History.apps.HistoryConfig",
    # Common application
    "src.Algorithms",
    "src.OrderView",
    "src.MsSqlConnector",
    "src.Cameras.apps.CamerasConfig",
    "src.CompanyLicense.apps.CompanyLicenseConfig",
    "src.Inventory.apps.InventoryConfig",
    # Collections reports
    "src.Reports.apps.ReportsConfig",
    "src.ImageReport.apps.ImageConfig",
    "src.Mailer.apps.MailerConfig",
    "src.Core.apps.CoreConfig",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
]


ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Etc/GMT"

USE_I18N = True

USE_TZ = True


STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static/"

MEDIA_URL = "/images/"
MEDIA_ROOT = BASE_DIR / "images/"

VIDEO_URL = "/videos/"
VIDEO_ROOT = BASE_DIR / "videos/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CRONJOBS = [    ('0 9 * * *', 'src.Mailer.check_low_stock_items.run', '>> /var/log/cron.log')]

