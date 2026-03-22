import os
import pickle

from django.conf import settings


def user_input(file):
    file_is = os.path.join(settings.MEDIA_ROOT, 'files', file)
    # Import Module
    import ftplib
    # Fill Required Information
    HOSTNAME = "ftp.drivehq.com"
    USERNAME = "dpHyd"
    PASSWORD = "lx160cm"
    # Connect FTP Server
    ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
    # force UTF-8 encoding
    ftp_server.encoding = "utf-8"
    # Enter File Name with Extension

    # Read file in binary mode
    with open(file_is, "rb") as file:
        # Command for Uploading the file "STOR filename"
        ftp_server.storbinary(f"STOR dph/{file_is}", file)



    # Close the Connection
    ftp_server.quit()


