# SMS Messenger

A simple Python package for sending messages over SMS Gateways.

## Description

SMS Messenger is a simple Python package that enables the user to send and read text messages via [SMS Gateways.](https://en.wikipedia.org/wiki/SMS_gateway) This package handles all the sending and reading of emails to SMS addresses. Requires an email to setup.

## Dependencies

[imapclient](https://github.com/mjs/imapclient)  
[pyzmail](https://github.com/aspineux/pyzmail)  
An Email _Preferably Gmail_

## Features

- Simple to use for sending and reading messages
- easy installation
- Lightweight with minimal external dependencies
- Docstrings

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install sms-messenger.

```bash
pip install sms_messenger
```

## Usage

```python
import sms_messenger
email = "example@gmail.com"
paswd = "FooBar"
addresses = ['+12003004000@tmomail.net','+15006007000@txt.att.net'] #must specify gateway domain

server = sms_messenger.messageManager(email,paswd) #create a messageManager Object
print(server.getGateways()) #US SMS Gateways
server.sendTextMessage("Hello World!",addresses)

server.semdTextMessage("This is the Body",'tmpEmail@email.com','This is the subject') #works with emails too

messages = server.getTextMessages(addresses) #needs an address
print(messages)
```

## Help

__If using gmail, look under the [security tab](https://myaccount.google.com/security?gar=1) and turn ON Less secure app access.
![example](/img/example.png)  
It must be on for the package to work.__

## Docstring

```
Help on package sms_messenger:

NAME
    sms_messenger - Create a module object.

DESCRIPTION
    The name must be a string; the optional doc argument can have any type.

PACKAGE CONTENTS


CLASSES
    builtins.object
        messageManager
    
    class messageManager(builtins.object)
     |  messageManager(email, paswd, smtp='smtp.gmail.com', port=587)
     |  
     |  A simple class to handle sending and reading text messages via SMS Gateways.
     |  
     |  Dependencies:
     |      imapclient: https://github.com/mjs/imapclient
     |      pyzmail: https://github.com/aspineux/pyzmail
     |  
     |  Attributes:
     |      email: a string containing the email from which the texts will be sent.
     |      paswd: a string containing the password for the email above.
     |      stmp: (optional) a string containing the name of the stmp server.
     |      port: (optional) an int containing the port number to connect to smtp.
     |      SMS_Gateways_US: a dictionary containing the mobile carrier and their respective gateway
     |  
     |  Methods defined here:
     |  
     |  __init__(self, email, paswd, smtp='smtp.gmail.com', port=587)
     |      Initialize self.
     |      
     |      Note:
     |          If not using gmail, the smtp and port must be specified.
     |  
     |  checkAccess(self)
     |      Attempts to log into the email server
     |      
     |      Returns:
     |          String on success, Nothing otherwise
     |  
     |  delMessagesBySelf(self, folder='[Gmail]/Sent Mail')
     |      Deletes all emails sent.
     |      
     |      Args:
     |          folder: (optional) Folder to be deleted from
     |          
     |      Returns:
     |          String on success, Nothing otherwise
     |  
     |  delMessagesByUID(self, UIDs)
     |      Deletes all emails from UID list.
     |      
     |      Args:
     |          UIDs: Python list containing Unique IDs of the emails to be deleted
     |          
     |      Returns:
     |          String on success, Nothing otherwise
     |  
     |  delMessagesFromSMS(self, sms_address)
     |      Deletes all emails from aspecified sms gateway.
     |      
     |      Args:
     |          sms_address: String containing the sms from which emails will be deleted
     |          
     |      Returns:
     |          String on success, Nothing otherwise
     |  
     |  delMessagesToSMS(self, sms_address, folder='[Gmail]/Sent Mail')
     |      Deletes all emails to specified sms gateway.
     |      
     |      Args:
     |          sms_address: String containing the sms to which emails will be deleted
     |          
     |      Returns:
     |          String on success, Nothing otherwise
     |  
     |  getGateways(self)
     |      Returns all the US Mobile Carriers and respective SMS Gateways.
     |      
     |      Returns:
     |          Dictionary of US Mobile Carriers paired with their SMS Gateways.
     |  
     |  getTextMessages(self, sms_address, returnUID=False)
     |      Grabs all messages sent by the sms address.
     |      
     |      Retrieves all text messsages sent by the specified sms address.
     |      Only retrieves the body of the email.
     |      
     |      Args:
     |          sms_address: string containing the specified address.
     |          returnUID: Whether or not to return the UIDs
     |      
     |      Returns:
     |          Default:
     |              Python List containing the body of each message sent by sms_address
     |              as strings. example:
     |      
     |              ['hello world','foo']
     |      
     |          returnUID:
     |              Python Dictionary containing the UID and message as pairs.
     |              example:
     |      
     |              {123: 'foo',234: 'bar'}
     |  
     |  sendTextMessage(self, message, sms_address, subject='I am a bot. Beep Boop.')
     |      Sends text message to specified sms_address.
     |      
     |      Composes an email from the message and subject and sends it to the recipients.
     |      Example:
     |          I am a bot. Beep Boop./ Hello World.
     |      
     |      Args:
     |          sms_address: string or list containing the addresses to be sent
     |          message: Text message to be sent.
     |          subject: (optional) message to be used on subject line.
     |      
     |      Returns:
     |          String on success, Nothing otherwise.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |  
     |  SMS_GATEWAYS_US = {'AT&T': 'txt.att.net', 'Alltel': 'sms.alltelwireles...
```

## License
[MIT](https://choosealicense.com/licenses/mit/)