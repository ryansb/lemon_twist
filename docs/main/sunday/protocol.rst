============================================
Welcome to the Sunday Protocol Documentation
============================================
.. _sunday:

Sunday Protocol
---------------

This is the official version of the
`Sunday <http://www.antiduh.com/drink/docs/sunday-protocol.html>`_
Protocol implemented by the ``lemon`` module.

Document Conventions
--------------------
* Lines sent from client to server shall begin with a :

* Lines sent from server to client shall begin with a >

* These symbols are not part of the protocol,
  and shall not be sent by any client or server
* Commands are not case-sensitive

* Data is case-sensitive

* Parameters in square brackets are ``[optional]``

* Parameters in angle brackets are ``<required>``

* All commands,
  unless stated otherwise,
  require a user to be logged in

* Commands requiring no authentication will be labeled,
  as will commands requiring administrative access

Background
----------
The Sunday Drink Protocol is a SMTP-like interface to the CSH Drink server software.
It was originally designed (quickly) by Joe Sunday in Fall 1999
when he rebuilt the drink hardware
and wrote his own server to drive his hardware.

While this new protocol was incompatible
(and less feature-rich)
than the existing protocol,
many clients were written that support this protocol.


When (yet-again) rebuilding and redesigning the drink hardware and software in fall of 2000,
the team decided to support both protocols for the most compatibility.
In the process of writing the ``SundayServer`` class,
there were some areas found where
the Sunday protocol could be enhanced.

(Note: There is not adequate documentation of the 'classic'
drink protocol, and currently only the Sunday protocol is supported)

When (yet another time) rebuilding the drink server,
this time in the ``lemon.twist`` implementation,
it was found that parts of the protocol were outdated.
These parts are not implemented,
and this document is the official version of the Sunday Protocol
supported by ``lemon.twist``.

Conventions
-----------
* Commands executed successfully shall return messages that
  begin with ``OK`` followed by any other information relevant
  to the command.

* Errors will begin with ``ERR`` and a unique error ID,
  then by a message describing the nature of the error

* The description for an error will have its first word capitalized,
  and will always end in a period

* If a user is not logged in and attempts a command that
  requires authentication,
  they will receive the error ``>ERR 204 You need to login.``

* If a user is logged in and attempts a command that
  requires adminstrative access,
  they will receive the error ``>ERR 200 Access denied.``

* The error ``>ERR 406 Invalid Parameters.`` will be thrown
  for any command where all the required parameters are not provided,
  or more parameters are provided than necessary.

* If a command is not implemented in the current version of the drink
  software, the command will return ``>ERR 451 Not implemented.``

* In the event that a parameter provided
  does not meet formatting specifications,
  an error specific to that parameter will be sent.
  If there are more than one violations,
  an error will be sent for only the first violation.

* If the command that was specified is not a recognized command,
  the error ``>ERR 452 Invalid command.`` will be issued.

Commands
-------------

USER
````
**USER <username>**

**Requires**

* Nothing

Specifies a username, beginning the login process. If a user was already logged in, it invalidates the current user. 

**Server Response:**

``>OK Password required.``
The command completed successfully; next, the 'PASS' command should be specified.

While you might expect to get an error if the username does not exist in the system, this could be a potential security hole (allowing a nefarious person to determine which usernames are valid). Therefore, this command can not be used to simply determine if the user is a valid user. The only way to determine this through the system is to log on as an administrator and issue the isvaliduser command.

see also PASS


PASS
````
**PASS <password>**

**Requires**

* USER command issued before PASS

Specifies a password, second phase of the login process.
The password is (unfortunately) transmitted in plain-text,
and the server response will indicate the user balance if successful. 

NOTE: If this command fails for any reason, the 'USER' command will have to be resent.

**Server Responses:**

``>OK Credits: <balance>``
Where <balance> is an integer representing the user's balance.
This response should be interpreted as a successful login.

``>ERR 201 USER command needs to be issued first.``
This response will be generated if the USER command was not issued before PASS was issued.

``>ERR 202 Invalid username or password.``
Indicates that either the username supplied during the USER command is invalid,
or the password supplied is invalid (insufficiently formatted),
or not correct.

see also USER

IBUTTON
```````
**IBUTTON <ibutton>**

**Requires**

* Nothing

**Server Responses:**

``>OK Credits: <balance>``
Where <balance> is an integer representing the user's balance.
This response should be interpreted as a successful login.

``>ERR 207 Invalid ibutton``
The specified IButton can't be found in LDAP. Sorry.


MACHINE
```````
**MACHINE <alias>**

**Requires**

* Machine online

**Machine aliases**

* d (big drink)
* ld (little drink)
* s (snack)

**Server Responses:**

``OK Welcome to <machine name>``
Returns the machine name as a string.
May contain spaces.

``>ERR 414 Invalid machine name - USAGE: MACHINE < d | ld | s >``
User entered a bad machine name.

``>ERR 416 Machine is offline or unreachable``
The machine is either inaccessible
or has been set to admin-only mode by a drinkadmin.


DROP
````
**DROP <slot index> [delay]**

**Requires**

* Auth
* Machine selected
* Machine online

Requests an actual drop from the machine.

* slot index - the index of the slot to drop from.
* delay - the number of seconds to wait before the drop occurs.
  Defaults to 0 if no argument is supplied.

**Server Responses:**

``>OK Credits remaining: <balance>``
Indicates that the drop was successful,
returns the user's balance after the drop,
then disconnects the user.

``>ERR 100 Slot empty.``
Indicates that the selected slot is empty.

``>ERR 101 Drop failed, contact an admin.``
Indicates that there was a failure in dropping the drink,
which is generally a bad thing.

``>ERR 150 Unable to initialize hardware for drop.``
There was a hardware problem. Uhoh...

``>ERR 103 Unknown Failure.``
We don't know what happened. Very bad.

``>ERR 203 User is poor.``
Indicates that the user's balance insufficient to purchase
the drink in the specified slot.

``>ERR 403 Invalid delay.``
The delay time provided was not a 32-bit integer.
This error is not generated if the delay is less than zero
or larger than the maximum allowed delay,
which is 300 seconds in this implementation.

``>ERR 409 Invalid slot.``
Indicates that the supplied slot number is not valid in the machine.


RAND
````
**RAND [delay]**

**Requires**

* Auth
* Machine selected
* Machine online

Requests a drop of a random drink
from one of the stocked, enabled slots
on the selected machine.

Only drinks that the user can afford are selected.

* delay - the number of seconds you wish to wait before the drop occurs (defaults to 0 if this argument is not given).

**Server Responses:**

``>OK Credits remaining: <n>``
Indicates the users new balance.
This should be interpreted as a successful drop.

``>ERR 101 Drop failed, contact an admin.``
Indicates that there was a failure in dropping the drink,
which is generally a bad thing

``>ERR 104 No slots available.``
Indicates there are no slots that 
the user can afford,
are stocked,
and are enabled.

``>ERR 403 Invalid delay.``
The delay time provided was not a 32-bit integer.
This error is not generated if the delay is less than zero
or larger than the maximum allowed delay,
which is 300 seconds in this implementation.


STAT
````
**STAT [index]**

**Requires**

* Machine selected
* Machine online

Requests the contents of the machines slot(s).
If the contents of only a single slot is desired,
that slot index can be specified.

* index - Optional.
  If unspecified,
  print all slots

**Server Responses:**

``:STAT``

``>OK 0 "Coke" 50 13 200 true``

``>OK 1 "Mountain Dew" 50 15 199 true``

``>OK 2 Slots retrieved.``


``:STAT 0``

``>OK 0 "Coke" 50 13 200 true``


Each line contains the stats for one slot. The fields are space-delimited, except for the drink name. Their contents are as follows:

``<Slot #> <Contents> <Cost> <# Available> <Total # Dropped> <bool enabled>``

NOTE: Contents is wrapped in quotes, and may contain spaces.

The final line from the server is a typical status message, and it is in the form:

``>OK <n> Slots retrieved.``

Where n is the number of slots retrieved.

NOTE: Clients should not assume that the slot numbers will be contiguous. The server may contains slots 0-4, but 3 may be disabled. The server may skip disabled/empty slots and simply subtract skipped slots from the 'OK' status message at the end of the output.


TEMP
````
Displays the current machine temperature.
Note that the temperature that is returned is in centigrade.

Big Drink is currently the only machine with hardware to check temperature.

**Server Responses:**

``>OK <temperature>``
The command was successful in retrieving the temperature.

``>ERR 351 Unable to determine temperature.``
There was a subsystem failure in retrieving the cabinete temperature.


GETBALANCE
``````````
**GETBALANCE [user]**

**Requires**

* Auth
* Admin (to get another user's balance)

Returns the credit balance of the specified user.
Only administrators may retrieve the balance of other users.

* user - The user to retrieve the balance of. If this argument is not supplied, the current user is assumed.

**Server Responses:**

``>OK Credits: <credits>``
Indicates the command was successful, and displays the requested users credit balance.

``>ERR 200 Access denied.``
The current user (who is not an administrator) tried to access another user's credit balance.
 
``>ERR 410 Invalid user.``
The specified user was not found in the account database.


ADDCREDITS
``````````
**ADDCREDITS <username> <credits>**

**Requires**

* Auth
* Admin

Adds credits to the supplied users account. Both parameters are required.

* username - the username to add credits to.
* credits - the number of credits to add to the users current balance.
  This value may be negative to subtract credits.

**Server Responses:**

``>OK Added credits.``
Indicates that the operation was successfully performed.

``>ERR 209 Error during credit transfer.``
Something unknown went wrong while we were transferring your credits.

``>ERR 410 Invalid user.``
The specified username is unknown to the drink accounting system.

``>ERR 402 Invalid credits.``
The value given for the credits parameter was not a number. The only characters allowed are numbers and a single leading dash '-' to signify a negative integer.


SENDCREDITS
``````````
**SENDCREDITS <credits> <username>**

Synonym for ADDCREDITS,
with inverted syntax to maintain compatibility with the
`Drink-JS <http://github.com/ComputerScienceHouse/Drink-JS>`_.
version of the Sunday protocol.

See ADDCREDITS


EDITSLOT
````````
**EDITSLOT <slotnum> <name> <cost> <quantity> <num_dropped> <enabled>**

**Requires**

* Auth
* Admin

Edits all values for a single slot. All arguments are required.

* slotnum - The number (0-N) of the slot you wish to edit
* name - The name of the slot, e.g. "Coke". It must be wrapped in double quotes even if it does not contain spaces.
* cost - The cost in credits of the drink in this slot.
* quantity - The number of drinks contained in this slot
* num_dropped - Change the "Total Dropped" accumulator for this slot.
* enabled - "true" if the slot is enabled, "false" if not

Example:

``:editslot 0 "Mountain Dew" 50 43 307 true``

``>OK Changes saved.``

**Server Responses:**

``>OK Changes saved.``
The requested change has been saved into the user database

``>ERR 409 Invalid slot.``
The user tried to edit a non-existent slot.

``>ERR 401 Invalid cost.``
The specified cost was not a number.

``>ERR 408 Invalid quantity.``
The specified quantity was not a number.

``>ERR 405 Invalid num_dropped.``
The specified number of cans that had already been served was not a number.

``>ERR 404 Invalid enable flag.``
The specified enabled/disabled flag was not either 'true' or 'false'.


ISVALIDUSER
``````````````````
**ISVALIDUSER <user>**

**Requires**

* Auth
* Admin

Determines whether or not the specified username is known to the accounting system. 

* username - The username to check validity of.

**Server Responses:**

``>OK true User is known.``

Indicates that the supplied user is known to the accounting system.

``>OK false User is not known.``

Indicates that the supplied user is not known to the accounting system.


QUERYADMIN
``````````
**QUERYADMIN <user>**

**Requires**

* Auth
* Admin

Displays whether or not the specified user is an administrator.

* username - the name of the user whose administrator status is to be displayed.

**Server Responses:**

``>OK true User is an administrator.``
Indicates that the user is an administrator

``>OK false User is not an administrator.``
Indicates that the user is not an administrator.

``>ERR 410 Invalid user.``
The specified username is not known to the drink accounting system.


LOG
```
**LOG [message]**

**Requires**
* Auth
* Admin

Adds a message to the drink logfile.
The message may contain any characters.
Everything that comes after the ``LOG`` command is printed to the logfile.
The file is time stamped with the issuing users username. 

* message - the message to leave in the log file.

If there is no message, then a simple timestamp with the users name is left.

**Server Responses:**

``>OK Message added to log file.``


LOCATION
````````
**Requires**

* Nothing

Displays the machines (stored) physical location, such as "NRH (North)". The format of this field is completely arbitrary at the moment. The current locations in use are "NRH (North)" for Big Drink and "NRH ( South)" for Little Drink. These two location specifications mean that the machines are on the 3rd floor of the Nathaniel Rochester Hall building in Rochester, NY.

Note that the response is not in quotes, and that everything after the 'OK ' is to be interpreted as the actual location.

Does not require the user to be logged in. Does not require any parameters.

**Server Responses:**

``>OK NRH (North).``


VERSION
```````
**Requires**

* Nothing

Shows what version of ``lemon`` the drink server is running.

**Server Response:**

``>OK Lemon <version-hash>``

Where ``version`` is the dotted official version and ``hash`` is six digits of the git commit hash.

A revision id will look like this: ``0.1-017ec4``


CODE
````
**CODE <slot> <button indices>**

**UNIMPLEMENTED**

**Requires**

* Auth
* Admin

Sets the drink server to drop the specified drink when the specified sequence of buttons is pressed on the front of the machine.
This feature will only work on big drink.


UPTIME
``````
**Requires**

* Nothing

**Server Responses:**

``OK Up since: Wed, 22 Feb 2012 00:07:37 EST``


QUIT
````
**Requires**

* Nothing

Tells the server the session is over and to close the connection.

**Server Response:**

``>OK Disconnecting.``


SHUTDOWN
````````
**SHUTDOWN [-r]**

**Requires**

* Auth
* Admin

Tells the server to close all active connections, cleanup and then exit. 
If the -r option is specified, the Operating System the software is running on is to be rebooted. This does not imply that the software is to be brought back up with the OS. That can be achieved by placing the correct commands in the appropriate startup scripts. 

**Server Responses:**

``:shutdown``

``>OK Shutting down server.``

The connection will then be dropped.

``:shutdown -r``

``>OK Rebooting.``

The connection will then be dropped while the server reboots.

``>ERR 411 Invalid reboot flag.``

The single parameter specified was not '-r'. 
