import smtplib 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import imapclient
import pyzmail
class messageManager:
    """A simple class to handle sending and reading text messages via SMS Gateways.

    Dependencies:
        imapclient: https://github.com/mjs/imapclient
        pyzmail: https://github.com/aspineux/pyzmail

    Attributes:
        email: a string containing the email from which the texts will be sent.
        paswd: a string containing the password for the email above.
        stmp: (optional) a string containing the name of the stmp server.
        port: (optional) an int containing the port number to connect to smtp.
        SMS_Gateways_US: a dictionary containing the mobile carrier and their respective gateway

    """
    SMS_GATEWAYS_US = {
        'Alltel': 'sms.alltelwireless.com',
        'AT&T': 'txt.att.net',
        'Boost Mobile': 'sms.myboostmobile.com',
        'Cricket Wireless': 'mms.cricketwireless.net',
        'FirstNet': 'txt.att.net',
        'MetroPCS': 'mymetropcs.com',
        'Republic Wireless': 'text.republicwireless.com',
        'Sprint': 'messaging.sprintpcs.com',
        'T-Mobile': 'tmomail.net',
        'U.S. Cellular': 'email.uscc.net',
        'Verizon Wireless': 'vtext.com',
        'Virgin Mobile': 'vmobl.com',
        }
    
    def __init__(self, email, paswd, smtp="smtp.gmail.com", port=587):
        """Initialize self.

        Note:
            If not using gmail, the smtp and port must be specified.
        """
        self.email = email
        self.paswd = paswd
        self.smtp = smtp
        self.port = port

    def getGateways(self):
        """Returns all the US Mobile Carriers and respective SMS Gateways.

        Returns:
            Dictionary of US Mobile Carriers paired with their SMS Gateways.
        """
        return messageManager.SMS_GATEWAYS_US

    def getTextMessages(self,sms_address,returnUID=False):
        """Grabs all messages sent by the sms address.

        Retrieves all text messsages sent by the specified sms address.
        Only retrieves the body of the email.

        Args:
            sms_address: string containing the specified address.
            returnUID: Whether or not to return the UIDs

        Returns:
            Default:
                Python List containing the body of each message sent by sms_address
                as strings. example:

                ['hello world','foo']

            returnUID:
                Python Dictionary containing the UID and message as pairs.
                example:

                {123: 'foo',234: 'bar'}

        """
        #initialize the server
        server = imapclient.IMAPClient(self.smtp, ssl=True)
        server._MAXLINE = 10000000 #Allows the server to read large emails
        server.login(self.email,self.paswd)
        
        server.select_folder('INBOX',readonly=True)
        UIDs = server.search(['FROM',sms_address])

        rawMessages = server.fetch(UIDs, ['BODY[]'])
        server.logout()

        messages=[]
        for ID in UIDs:
            message = pyzmail.PyzMessage.factory(rawMessages[ID][b'BODY[]'])
            for mailpart in message.mailparts:
                if mailpart.type.startswith('text/plain'): #Grab only the plain text parts
                    payload, used_charset=pyzmail.decode_text(mailpart.get_payload(), mailpart.charset, None)
                    messages.append(payload)
        if returnUID:
            return dict(zip(UIDs,messages))
        else:
            return messages

    def sendTextMessage(self,message,sms_address,subject="I am a bot. Beep Boop."):
        """Sends text message to specified sms_address.

        Composes an email from the message and subject and sends it to the recipients.
        Example:
            I am a bot. Beep Boop./ Hello World.

        Args:
            sms_address: string or list containing the addresses to be sent
            message: Text message to be sent.
            subject: (optional) message to be used on subject line.

        Returns:
            String on success, Nothing otherwise.
        """
        # The server we use to send emails in our case it will be gmail but every email provider has a different smtp 
        # and port is also provided by the email provider.
        # This will start our email server
        server = smtplib.SMTP(self.smtp,self.port)
        # Quick Test
        server.ehlo()
        # Starting the server
        server.starttls()
        # Now we need to login
        server.login(self.email,self.paswd)
        if type(sms_address)==str: #needs to be a list
            sms_address = [sms_address]
        # Now we use the MIME module to structure our message.
        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = ', '.join(sms_address)
        # Make sure you add a new line in the subject
        msg['Subject'] = subject + "\n"
        # Make sure you also add new lines to your body
        body = message + "\n"
        # and then attach that body furthermore you can also send html content.
        msg.attach(MIMEText(body, 'plain'))
        sms = msg.as_string()
        success = server.sendmail(self.email,sms_address,sms)
        # lastly quit the server
        server.quit()
        
        if not bool(success): #checks for empty dictionary
            return("Message Sent Successfully to "+ " ".join(sms_address))
        

    def delMessagesByUID(self,UIDs):
        """Deletes all emails from UID list.

        Args:
            UIDs: Python list containing Unique IDs of the emails to be deleted
            
        Returns:
            String on success, Nothing otherwise
        """
        #initialize the server
        server = imapclient.IMAPClient(self.smtp, ssl=True)
        server.login(self.email,self.paswd)
        server.select_folder('INBOX',readonly=False)
        server.delete_messages(UIDs)
        success = server.expunge()
        server.logout()
        return success

    def delMessagesFromSMS(self,sms_address):
        """Deletes all emails from aspecified sms gateway.

        Args:
            sms_address: String containing the sms from which emails will be deleted
            
        Returns:
            String on success, Nothing otherwise
        """
        #initialize the server
        server = imapclient.IMAPClient(self.smtp, ssl=True)
        server.login(self.email,self.paswd)
        
        server.select_folder('INBOX',readonly=False)
        UIDs = server.search(['FROM',sms_address])
        server.delete_messages(UIDs)
        success = server.expunge()
        server.logout()
        return success

    def delMessagesBySelf(self,folder='[Gmail]/Sent Mail'):
        """Deletes all emails sent.
        
        Args:
            folder: (optional) Folder to be deleted from
            
        Returns:
            String on success, Nothing otherwise
        """
        #initialize the server
        server = imapclient.IMAPClient(self.smtp, ssl=True)
        server.login(self.email,self.paswd)
        print(server.list_folders())
        server.select_folder(folder,readonly=False)
        UIDs = server.search(['FROM',self.email])
        server.delete_messages(UIDs)
        success = server.expunge()
        server.logout()
        return success

    def delMessagesToSMS(self,sms_address,folder='[Gmail]/Sent Mail'):
        """Deletes all emails to specified sms gateway.

        Args:
            sms_address: String containing the sms to which emails will be deleted
            
        Returns:
            String on success, Nothing otherwise
        """
        #initialize the server
        server = imapclient.IMAPClient(self.smtp, ssl=True)
        server.login(self.email,self.paswd)
        server.select_folder(folder,readonly=False)
        UIDs = server.search(['TO',sms_address])
        server.delete_messages(UIDs)
        success = server.expunge()
        server.logout()
        return success
        
    def checkAccess(self):
        """Attempts to log into the email server
        
        Returns:
            String on success, Nothing otherwise
        """
        #initialize the server
        server = imapclient.IMAPClient(self.smtp, ssl=True)
        return server.login(self.email,self.paswd)






        
