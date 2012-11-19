================================================
Welcome to the LemonTwist protocol documentation
================================================
.. _twist:

LemonTwist daemon
-----------------

This page contains information about the twisted reactor
and the .tac file used to daemonize it.

The Daemon
----------

We use a Twisted AppliCation file to daemonize the server itself,
the .tac is located in ``bin/lemontwist.tac``.

By default the daemon reads its configuration from ``conf/lemon.cfg``
where it gets database credentials,
learns what port to run on,
and other settings.

To run the daemon in the foreground use the command
``twistd -noy bin/lemontwist.tac``
and to run in the background run
``twistd -y bin/lemontwist.tac``.

The .tac also contains helper classes to allow
the daemon to record logs and run in the background.

FormattedLogObserver
--------------------

Changes the log format from the default twistd log fomat
(which is absolutely unreadable)
to timestamped logs.

LemonTwistService
-----------------
Is the service that produces ``LemonFactory`` objects
that then produce ``LemonTwist`` protocol objects
that serve telnet requests.
In the future it will be possible to add
websocket and REST protocols
without significant changes to the .tac file.

Adding new protocols will only require adding more ``TCPServer`` objects
to serve the new protocols on different ports.
