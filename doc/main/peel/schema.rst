==========
Schema
==========

Database Interaction
--------------------

We interact with the database using
`twistar <http://findingscience.com/twistar/>`_
An asynchronous ActiveRecord implementation for
`Twisted <http://twistedmatrix.com/trac/>`_

lemon.peel.metadata
---------------
**status_id**
    * stat_id(primary)(smallint unsigned)
    * stat_name(varchar(512))

**drink_users**
    * drink_id(primary)(uuid) # on a cronjob, make sure uid and user_name are matching
    * user_name(varchar(255))
    * uid(int unsigned)

lemon.peel.machines
----------------
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

lemon.peel.logs
--------------
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

lemon.peel.apps
---------------
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

Bootstrapping the DB
--------------------

.. code-block:: sql

   DROP DATABASE IF EXISTS `drink`;
   CREATE DATABASE `drink`;
   
   CREATE TABLE `drink`.`drink_users` (
       `drink_id` INT UNSIGNED NOT NULL,
       `user_name` VARCHAR(255) NULL,
       `uid` INT UNSIGNED NULL,
       PRIMARY KEY (`drink_id`)
   );
   
   
   CREATE TABLE `drink`.`status_id` (
       `stat_id` SMALLINT UNSIGNED NOT NULL,
       `stat_name` VARCHAR(512) NULL,
       PRIMARY KEY (`stat_id`)
   );
   
   
   CREATE TABLE `drink`.`machine_id` (
       `mid` SMALLINT UNSIGNED NOT NULL,
       `name` VARCHAR(255) NULL,
       `deleted` BOOL NOT NULL DEFAULT 0,
       PRIMARY KEY (`mid`)
   );
   
   
   CREATE TABLE `drink`.`machine_ip` (
       `mid` SMALLINT UNSIGNED NOT NULL,
       `public_ip` VARCHAR(15) NULL,
       `machine_ip` VARCHAR(15) NULL,
       FOREIGN KEY (`mid`) REFERENCES machine_id(mid),
       PRIMARY KEY (`mid`)
   );
   
   
   CREATE TABLE `drink`.`machine_property` (
       `mid` SMALLINT UNSIGNED NOT NULL,
       `password` VARCHAR(255) NOT NULL,
       `available_sensor` BOOL NOT NULL DEFAULT 0,
       `allow_connect` BOOL NOT NULL DEFAULT 1,
       `admin_only` BOOL NOT NULL DEFAULT 0,
       `location` VARCHAR(255),
       FOREIGN KEY (`mid`) REFERENCES machine_id(mid),
       PRIMARY KEY (`mid`)
   );
   
   
   CREATE TABLE `drink`.`slot_property` (
       `mid` SMALLINT UNSIGNED NOT NULL,
       `slot_num` TINYINT UNSIGNED NOT NULL,
       `slot_name` VARCHAR(255),
       `price` INT UNSIGNED,
       `availability` SMALLINT UNSIGNED NOT NULL,
       `disabled` BOOL NOT NULL DEFAULT 0,
       FOREIGN KEY (`mid`) REFERENCES machine_id(mid),
       PRIMARY KEY (`mid`, `slot_num`)
   );
   
   
   CREATE TABLE `drink`.`temperature_log` (
       `mid` SMALLINT UNSIGNED NOT NULL,
       `time` DATETIME NOT NULL,
       `temp` FLOAT,
       FOREIGN KEY (`mid`) REFERENCES machine_id(mid),
       PRIMARY KEY (`mid`, `time`)
   );
   
   
   CREATE TABLE `drink`.`drop_log` (
       `mid` SMALLINT UNSIGNED NOT NULL,
       `time` DATETIME NOT NULL,
       `slot_name` VARCHAR(255),
       `drink_id` INT UNSIGNED NOT NULL,
       `stat_id` SMALLINT UNSIGNED,
       FOREIGN KEY (`mid`) REFERENCES machine_id(`mid`),
       FOREIGN KEY (`stat_id`) REFERENCES status_id(`stat_id`),
       FOREIGN KEY (`drink_id`) REFERENCES drink_users(`drink_id`)
   );
   
   
   CREATE TABLE `drink`.`money_log` (
       `time` DATETIME NOT NULL,
       `slot_name` VARCHAR(255),
       `drink_id` INT UNSIGNED NOT NULL,
       `admin_id` INT UNSIGNED NOT NULL,
       `amount` INT SIGNED NOT NULL,
       `reason` VARCHAR(255),
       FOREIGN KEY (`drink_id`) REFERENCES drink_users(`drink_id`),
       FOREIGN KEY (`admin_id`) REFERENCES drink_users(`drink_id`),
       PRIMARY KEY (`time`)
   );
   
   
   CREATE TABLE `drink`.`app_id` (
       `aid` SMALLINT UNSIGNED NOT NULL,
       `name` VARCHAR(255) NULL,
       PRIMARY KEY (`aid`)
   );
   
   
   CREATE TABLE `drink`.`app_info` (
       `aid` SMALLINT UNSIGNED NOT NULL,
       `owner` INT UNSIGNED NOT NULL,
       `description` varchar(255),
       FOREIGN KEY (`owner`) REFERENCES drink_users(`drink_id`),
       FOREIGN KEY (`aid`) REFERENCES app_id(`aid`),
       PRIMARY KEY (`aid`)
   );
   
   
   CREATE TABLE `drink`.`app_prop` (
       `aid` SMALLINT UNSIGNED NOT NULL,
       `public_key` varchar(4096),
       `owner_only` BOOL NOT NULL DEFAULT 0,
       FOREIGN KEY (`aid`) REFERENCES app_id(`aid`),
       PRIMARY KEY (`aid`)
   );
   
   
   CREATE TABLE `drink`.`app_users` (
       `aid` SMALLINT UNSIGNED NOT NULL,
       `drink_id` INT UNSIGNED NOT NULL,
       `date_granted` DATETIME NOT NULL,
       FOREIGN KEY (`drink_id`) REFERENCES drink_users(`drink_id`),
       FOREIGN KEY (`aid`) REFERENCES app_id(`aid`),
       PRIMARY KEY (`aid`)
   );
   
   
   CREATE TABLE `drink`.`app_used` (
       `aid` SMALLINT UNSIGNED NOT NULL,
       `drink_id` INT UNSIGNED NOT NULL,
       `date` DATETIME NOT NULL,
       FOREIGN KEY (`drink_id`) REFERENCES drink_users(`drink_id`),
       FOREIGN KEY (`aid`) REFERENCES app_id(`aid`),
       PRIMARY KEY (`aid`)
   );
