from PySide6.QtCore import QCoreApplication


USE_MOCK_DATA = False
if USE_MOCK_DATA:
    print("Using mock data.")
__DOMAIN_NAME = "76.176.224.129"  # chuadevs.com
SERVICE_BASE_URL = f"http://{__DOMAIN_NAME}:1587/v1"
POSTER_WIDTH = 235
POSTER_HEIGHT = 350
QCoreApplication.setApplicationName("MovieFinder")
QCoreApplication.setOrganizationDomain("chuadevs.com")
QCoreApplication.setOrganizationName("chuadevs.com")
