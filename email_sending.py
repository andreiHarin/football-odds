import smtplib


def connect_to_outlook():
    smtp = smtplib.SMTP('smtp-mail.outlook.com', '587')
    smtp.ehlo()  # say hello to the server
    smtp.starttls()  # we will communicate using TLS encryption
    smtp.login('andrei.harin@outlook.com', 'password')  # login to outlook server, using generic email and password
    return smtp


def send_outlook_message(outlook_connection, email_receiver, message):
    print('message sent to ', email_receiver)
    return outlook_connection.sendmail('andrei.harin@outlook.com', email_receiver, message)
