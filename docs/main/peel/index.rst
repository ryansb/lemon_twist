========================================
Welcome to the data model documentation!
========================================
.. _peel:

Data Models
-----------

This page contains a text summary for the SQL schema used by lemon,
and the docs for the SQLAlchemy objects.

Database Interaction
--------------------

We interact with the database using
`sqlalchemy <http://docs.sqlalchemy.org/en/rel_0_7>`_ version 0.7.8
An exceedingly fancy Python ORM.
We interact with it in a deferred manner
using twisted.internet.threads.deferToThread
so we don't block the reactor unnecessarily

Schema Summary
--------------

Machine Info Tables
```````````````````
**machine_id**
    * mid(primary)(smallint unsigned)
    * name(varchar(255))
    * deleted(secondary)(bool not null default 0)

**machine_ip**
    * mid(primary)(smallint unsigned)
    * public_ip(varchar(15)) # IP of Sunday protocol/web service
    * machine_ip(varchar(15)) # IP of the tini/pi

**machine_property**
    * mid(primary)(smallint unsigned)
    * password(varchar(255)) # currently ignored by drink server, just auto-accepts. Currently done by whitelisted IP
    * available_sensor(secondary)(bool not null default 0) # has a sensor to check if there's stuff left
    * allow_connect(secondary)(bool not null default 1) # if no, doesn't accept user connections (Sunday server off)
    * admin_only(secondary)(bool not null default 0) # only admins can perform actions
    * location(varchar(255)) # where the machine is, for Sunday command

**slot_property**
    * mid(primary)(smallint unsigned) #     \
    * slot_num(primary)(tinyint unsigned) # -> need both values to index anything
    * slot_name(varchar(255))
    * price(int unsigned)
    * availability(smallint unsigned not null) 
    * disabled(bool not null default 0)

Metadata Tables
```````````````
**status_id**
    * stat_id(primary)(smallint unsigned)
    * stat_name(varchar(512))

**drink_users**
    * drink_id(primary)(uuid) # on a cronjob, make sure uid and user_name are matching
    * user_name(varchar(255))
    * uid(int unsigned)

Log Tables
``````````
**temperature_log**
    * mid(primary)(smallint unsigned)
    * time(primary datetime) # need both to index
    * temp(float)

**drop_log**
    * mid(primary)(smallint unsigned)
    * time(primary)(time)
    * slot_name(varchar(255))
    * drink_id(varchar(255)) # think about storing users in another table with a drink id from drink table
    * stat_id(smallint unsigned) # wtf is this shit?

**money_log**
    * time(datetime)
    * drink_id(uuid)
    * admin_id(uuid) # Also a drink_id
    * amount(int signed)
    * reason(varchar(255))

App Tables
``````````
**app_id**
    * aid(smallint unsigned)
    * name(varchar(255))

**app_info**
    * aid(smallint unsigned)
    * owner(drink_id) # admin of project
    * description(varchar(255))

**app_prop**
    * aid(smallint unsigned)
    * public_key(varchar(4096)) # is that length enough?
    * owner_only(bool not null default 0) # show on public app list

**app_users**
    * aid(smallint unsigned)
    * drink_id
    * date_granted(datetime)

**app_used**
    * aid(smallint unsigned)
    * drink_id
    * date(datetime)

lemon.peel.machines
-------------------
Machine
```````
.. autoclass:: lemon.peel.machines.Machine
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance:

Slot
````
.. autoclass:: lemon.peel.machines.Slot
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance:


lemon.peel.logs
---------------
DropLog
```````
.. autoclass:: lemon.peel.logs.DropLog
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance:

TemperatureLog
``````````````
.. autoclass:: lemon.peel.logs.TemperatureLog
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance:

MoneyLog
````````
.. autoclass:: lemon.peel.logs.MoneyLog
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance:

lemon.peel.metadata
-------------------
StatusId
````````
.. autoclass:: lemon.peel.metadata.StatusId
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance:


lemon.peel.users
-------------------
User
````
.. autoclass:: lemon.peel.users.User
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance:

lemon.peel.apps
---------------

AppId
`````
.. autoclass:: lemon.peel.apps.AppId
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance:

AppInfo
```````
.. autoclass:: lemon.peel.apps.AppInfo
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance:

AppProp
```````
.. autoclass:: lemon.peel.apps.AppProp
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance:

AppUsers
````````
.. autoclass:: lemon.peel.apps.AppUsers
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance:

AppUsed
```````
.. autoclass:: lemon.peel.apps.AppUsed
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance:
