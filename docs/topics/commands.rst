.. _topics-commands:

=================
Command line tool
=================

.. versionadded:: 0.10

pyrake is controlled through the ``pyrake`` command-line tool, to be referred
here as the "pyrake tool" to differentiate it from the sub-commands, which we
just call "commands" or "pyrake commands".

The pyrake tool provides several commands, for multiple purposes, and each one
accepts a different set of arguments and options.

.. _topics-project-structure:

Default structure of pyrake projects
====================================

Before delving into the command-line tool and its sub-commands, let's first
understand the directory structure of a pyrake project.

Though it can be modified, all pyrake projects have the same file
structure by default, similar to this::

   pyrake.cfg
   myproject/
       __init__.py
       items.py
       pipelines.py
       settings.py
       spiders/
           __init__.py
           spider1.py
           spider2.py
           ...

The directory where the ``pyrake.cfg`` file resides is known as the *project
root directory*. That file contains the name of the python module that defines
the project settings. Here is an example::

    [settings]
    default = myproject.settings

Using the ``pyrake`` tool
=========================

You can start by running the pyrake tool with no arguments and it will print
some usage help and the available commands::

    pyrake X.Y - no active project

    Usage:
      pyrake <command> [options] [args]

    Available commands:
      crawl         Run a spider
      fetch         Fetch a URL using the pyrake downloader
    [...]

The first line will print the currently active project, if you're inside a
pyrake project. In this, it was run from outside a project. If run from inside
a project it would have printed something like this::

    pyrake X.Y - project: myproject

    Usage:
      pyrake <command> [options] [args]

    [...]

Creating projects
-----------------

The first thing you typically do with the ``pyrake`` tool is create your pyrake
project::

    pyrake startproject myproject

That will create a pyrake project under the ``myproject`` directory.

Next, you go inside the new project directory::

    cd myproject

And you're ready to use the ``pyrake`` command to manage and control your
project from there.

Controlling projects
--------------------

You use the ``pyrake`` tool from inside your projects to control and manage
them.

For example, to create a new spider::

    pyrake genspider mydomain mydomain.com

Some pyrake commands (like :command:`crawl`) must be run from inside a pyrake
project. See the :ref:`commands reference <topics-commands-ref>` below for more
information on which commands must be run from inside projects, and which not.

Also keep in mind that some commands may have slightly different behaviours
when running them from inside projects. For example, the fetch command will use
spider-overridden behaviours (such as the ``user_agent`` attribute to override
the user-agent) if the url being fetched is associated with some specific
spider. This is intentional, as the ``fetch`` command is meant to be used to
check how spiders are downloading pages.

.. _topics-commands-ref:

Available tool commands
=======================

This section contains a list of the available built-in commands with a
description and some usage examples. Remember you can always get more info
about each command by running::

    pyrake <command> -h

And you can see all available commands with::

    pyrake -h

There are two kinds of commands, those that only work from inside a pyrake
project (Project-specific commands) and those that also work without an active
pyrake project (Global commands), though they may behave slightly different
when running from inside a project (as they would use the project overridden
settings).

Global commands:

* :command:`startproject`
* :command:`settings`
* :command:`runspider`
* :command:`shell`
* :command:`fetch`
* :command:`view`
* :command:`version`

Project-only commands:

* :command:`crawl`
* :command:`check`
* :command:`list`
* :command:`edit`
* :command:`parse`
* :command:`genspider`
* :command:`deploy`
* :command:`bench`

.. command:: startproject

startproject
------------

* Syntax: ``pyrake startproject <project_name>``
* Requires project: *no*

Creates a new pyrake project named ``project_name``, under the ``project_name``
directory.

Usage example::

    $ pyrake startproject myproject

.. command:: genspider

genspider
---------

* Syntax: ``pyrake genspider [-t template] <name> <domain>``
* Requires project: *yes*

Create a new spider in the current project.

This is just a convenient shortcut command for creating spiders based on
pre-defined templates, but certainly not the only way to create spiders. You
can just create the spider source code files yourself, instead of using this
command.

Usage example::

    $ pyrake genspider -l
    Available templates:
      basic
      crawl
      csvfeed
      xmlfeed

    $ pyrake genspider -d basic
    import pyrake

    class $classname(pyrake.Spider):
        name = "$name"
        allowed_domains = ["$domain"]
        start_urls = (
            'http://www.$domain/',
            )

        def parse(self, response):
            pass

    $ pyrake genspider -t basic example example.com
    Created spider 'example' using template 'basic' in module:
      mybot.spiders.example

.. command:: crawl

crawl
-----

* Syntax: ``pyrake crawl <spider>``
* Requires project: *yes*

Start crawling using a spider.

Usage examples::

    $ pyrake crawl myspider
    [ ... myspider starts crawling ... ]


.. command:: check

check
-----

* Syntax: ``pyrake check [-l] <spider>``
* Requires project: *yes*

Run contract checks.

Usage examples::

    $ pyrake check -l
    first_spider
      * parse
      * parse_item
    second_spider
      * parse
      * parse_item

    $ pyrake check
    [FAILED] first_spider:parse_item
    >>> 'RetailPricex' field is missing

    [FAILED] first_spider:parse
    >>> Returned 92 requests, expected 0..4

.. command:: list

list
----

* Syntax: ``pyrake list``
* Requires project: *yes*

List all available spiders in the current project. The output is one spider per
line.

Usage example::

    $ pyrake list
    spider1
    spider2

.. command:: edit

edit
----

* Syntax: ``pyrake edit <spider>``
* Requires project: *yes*

Edit the given spider using the editor defined in the :setting:`EDITOR`
setting.

This command is provided only as a convenient shortcut for the most common
case, the developer is of course free to choose any tool or IDE to write and
debug his spiders.

Usage example::

    $ pyrake edit spider1

.. command:: fetch

fetch
-----

* Syntax: ``pyrake fetch <url>``
* Requires project: *no*

Downloads the given URL using the pyrake downloader and writes the contents to
standard output.

The interesting thing about this command is that it fetches the page how the
spider would download it. For example, if the spider has an ``USER_AGENT``
attribute which overrides the User Agent, it will use that one.

So this command can be used to "see" how your spider would fetch a certain page.

If used outside a project, no particular per-spider behaviour would be applied
and it will just use the default pyrake downloader settings.

Usage examples::

    $ pyrake fetch --nolog http://www.example.com/some/page.html
    [ ... html content here ... ]

    $ pyrake fetch --nolog --headers http://www.example.com/
    {'Accept-Ranges': ['bytes'],
     'Age': ['1263   '],
     'Connection': ['close     '],
     'Content-Length': ['596'],
     'Content-Type': ['text/html; charset=UTF-8'],
     'Date': ['Wed, 18 Aug 2010 23:59:46 GMT'],
     'Etag': ['"573c1-254-48c9c87349680"'],
     'Last-Modified': ['Fri, 30 Jul 2010 15:30:18 GMT'],
     'Server': ['Apache/2.2.3 (CentOS)']}

.. command:: view

view
----

* Syntax: ``pyrake view <url>``
* Requires project: *no*

Opens the given URL in a browser, as your pyrake spider would "see" it.
Sometimes spiders see pages differently from regular users, so this can be used
to check what the spider "sees" and confirm it's what you expect.

Usage example::

    $ pyrake view http://www.example.com/some/page.html
    [ ... browser starts ... ]

.. command:: shell

shell
-----

* Syntax: ``pyrake shell [url]``
* Requires project: *no*

Starts the pyrake shell for the given URL (if given) or empty if no URL is
given. See :ref:`topics-shell` for more info.

Usage example::

    $ pyrake shell http://www.example.com/some/page.html
    [ ... pyrake shell starts ... ]

.. command:: parse

parse
-----

* Syntax: ``pyrake parse <url> [options]``
* Requires project: *yes*

Fetches the given URL and parses it with the spider that handles it, using the
method passed with the ``--callback`` option, or ``parse`` if not given.

Supported options:

* ``--spider=SPIDER``: bypass spider autodetection and force use of specific spider

* ``--a NAME=VALUE``: set spider argument (may be repeated)

* ``--callback`` or ``-c``: spider method to use as callback for parsing the
  response

* ``--pipelines``: process items through pipelines

* ``--rules`` or ``-r``: use :class:`~pyrake.contrib.spiders.CrawlSpider`
  rules to discover the callback (i.e. spider method) to use for parsing the
  response

* ``--noitems``: don't show scraped items

* ``--nolinks``: don't show extracted links

* ``--nocolour``: avoid using pygments to colorize the output

* ``--depth`` or ``-d``: depth level for which the requests should be followed
  recursively (default: 1)

* ``--verbose`` or ``-v``: display information for each depth level

Usage example::

    $ pyrake parse http://www.example.com/ -c parse_item
    [ ... pyrake log lines crawling example.com spider ... ]

    >>> STATUS DEPTH LEVEL 1 <<<
    # Scraped Items  ------------------------------------------------------------
    [{'name': u'Example item',
     'category': u'Furniture',
     'length': u'12 cm'}]

    # Requests  -----------------------------------------------------------------
    []


.. command:: settings

settings
--------

* Syntax: ``pyrake settings [options]``
* Requires project: *no*

Get the value of a pyrake setting.

If used inside a project it'll show the project setting value, otherwise it'll
show the default pyrake value for that setting.

Example usage::

    $ pyrake settings --get BOT_NAME
    pyrakebot
    $ pyrake settings --get DOWNLOAD_DELAY
    0

.. command:: runspider

runspider
---------

* Syntax: ``pyrake runspider <spider_file.py>``
* Requires project: *no*

Run a spider self-contained in a Python file, without having to create a
project.

Example usage::

    $ pyrake runspider myspider.py
    [ ... spider starts crawling ... ]

.. command:: version

version
-------

* Syntax: ``pyrake version [-v]``
* Requires project: *no*

Prints the pyrake version. If used with ``-v`` it also prints Python, Twisted
and Platform info, which is useful for bug reports.

.. command:: deploy

deploy
------

.. versionadded:: 0.11

* Syntax: ``pyrake deploy [ <target:project> | -l <target> | -L ]``
* Requires project: *yes*

Deploy the project into a pyraked server. See `Deploying your project`_.

.. command:: bench

bench
-----

.. versionadded:: 0.17

* Syntax: ``pyrake bench``
* Requires project: *no*

Run a quick benchmark test. :ref:`benchmarking`.

Custom project commands
=======================

You can also add your custom project commands by using the
:setting:`COMMANDS_MODULE` setting. See the pyrake commands in
`pyrake/commands`_ for examples on how to implement your commands.

.. _pyrake/commands: https://github.com/pyrake/pyrake/blob/master/pyrake/commands
.. setting:: COMMANDS_MODULE

COMMANDS_MODULE
---------------

Default: ``''`` (empty string)

A module to use for looking up custom pyrake commands. This is used to add custom
commands for your pyrake project.

Example::

    COMMANDS_MODULE = 'mybot.commands'

.. _Deploying your project: http://pyraked.readthedocs.org/en/latest/deploy.html
