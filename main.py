import smtplib
from google.cloud import firestore


db = firestore.Client()

def retrieveUserEmails():
    """
    This function retrieves the email addresses of all users from a "profile" collection in a database.
    :return: The function `retrieveUserEmails()` returns a list of email addresses of all the users in
    the "profile" collection in the database.
    """
    usersCollection = db.collection("profile").get()
    userEmails = [user.to_dict()["email"] for user in usersCollection]
    return userEmails


def trigger_emails(event, context):
    """
    This function triggers emails to be sent to a list of user emails when a new post is made on
    AshNetwork.
    
    :param event: An event object that contains information about the trigger that caused the function
    to run. It likely includes information about the new post that was made on AshNetwork
    :param context: The context parameter is a dictionary containing information about the current
    execution context, such as the cloud function name, version, and ARN. It also includes
    information about the invocation, such as the request ID and the deadline for the function to
    complete
    """
    authorEmail = event["value"]["fields"]["emailAuthor"]["stringValue"]
    authorName = db.collection('profile').where('email', '==', authorEmail).get()[0].to_dict()["name"]
    subject = "New Post on AshNetwork!"
    smtpServer = "smtp.gmail.com"
    port = 587
    senderEmail ="ychudah@gmail.com"
    senderPassword = "hvwpioupbgrcwjoa"
    server = smtplib.SMTP(smtpServer, port)
    server.starttls()
    server.login(senderEmail, senderPassword)
    emails = retrieveUserEmails()
    body = f'User {authorName} just made a Post'
    for email  in emails:
        message = f'Subject: {subject}\n{body}'
        server.sendmail(senderEmail, email, message)


    
