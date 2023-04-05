import os
from typing import List
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders

def main():

    # Auto detect the supported smtp servers from the email address
    def smtp_detector(address: str):
        if "@gmail." in address:
            return "smtp.gmail.com"
        elif "@hotmail." in address or "@outlook." in address:
            return "smtp.office365.com"
        elif "@yahoo." in address:
            return "smtp.mail.yahoo.com"
        else:
            smtp = input('unable to find the smtp server, you can input your smtp or type "exit" to cancel: ')
            return smtp


    def email_sender(From:str, To:str, Password:str, Subject="", Body="", html_body="",Attachements: List[str] = []):
        try:
            # SMTP server
            smtp_server = smtp_detector(From)
            if smtp_server.lower() == "exit":
                print("send canceled")
                return

            smtp_port = 587

            # connection to the SMTP server
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(From, Password)

            # email message
            msg = MIMEMultipart()
            msg['From'] = From
            msg['To'] = COMMASPACE.join([To])
            msg['Subject'] = Subject

            # plain text body
            body = Body
            msg.attach(MIMEText(body))

            # HTML text body
            if html_body != "":
                msg.attach(MIMEText(html_body, 'html'))


            # attachments of the email
            if Attachements:
                for file in Attachements:
                    try:
                        fileAdd  = file
                        filename = os.path.basename(fileAdd)

                        with open(fileAdd, "rb") as attachment:
                            part = MIMEBase("application", "octet-stream")
                            part.set_payload(attachment.read())
                            encoders.encode_base64(part)
                            part.add_header("Content-Disposition", f"attachment; filename={filename}")
                            msg.attach(part)
                    except Exception as e:
                        print("\n")
                        print(e)
                        while True:
                            inp = input("Do you want to continue sending the email ? [Y/n] ")
                            if not inp.lower() in ["y", "n"]:
                                print("bad input, try again")
                            else:
                                break

                        if not inp in ["Y", "y"]:
                            print("Send canceled")
                            return


            # send the email and close the connection
            server.sendmail(From, To, msg.as_string())
            server.quit()
            print("The email sent succefully")

        except Exception as e:
            if "Application-specific password required" in str(e):
                print("""Error in password: To send emails with the email provider Google "Gmail" you have to login with App-Password instead of the real password
                    > learn more at https://support.google.com/mail/?p=InvalidSecondFactor
                    """)
            else:
                print(e)


    sender = "sender_address@example.com"
    receiver = "receiver_address@example.com"
    password = "senders_application_password"
    subject= "Email sender test"
    body="""
        this is
        a plain text
        for body
        of the
        email.
    """

    html = """
        <html>
            <body>
                <center>
                    <h1>Hello world</h1>
                    <br>
                    <p>This is a test email with <b>HTML</b> content sent from Python.</p>
                </center>
            </body>
        </html>
    """
    files = [
        "example_file1.txt",
        "path/to/example_file2.txt",
    ]

    try:
        email_sender(From=sender, To=receiver, Password=password, Subject=subject, Body=body, html_body=html, Attachements=files)
    except Exception as e:
        if "Application-specific password required" in str(e):
            print("""Error in password: To send emails with the email provider Google "Gmail" you have to login with App-Password instead of the real password
            > learn more at https://support.google.com/mail/?p=InvalidSecondFactor
            """)
        else:
            print(e)


if __name__ == '__main__':
    main()