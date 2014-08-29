.. _topics-ubuntu:

===============
Ubuntu packages
===============

.. versionadded:: 0.10

`Scrapinghub`_ publishes apt-gettable packages which are generally fresher than
those in Ubuntu, and more stable too since they're continuously built from
`Github repo`_ (master & stable branches) and so they contain the latest bug
fixes.

To use the packages:

1. Import the GPG key used to sign pyrake packages into APT keyring::

    sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 627220E7

2. Create `/etc/apt/sources.list.d/pyrake.list` file using the following command::

    echo 'deb http://archive.pyrake.org/ubuntu pyrake main' | sudo tee /etc/apt/sources.list.d/pyrake.list

3. Update package lists and install the pyrake-|version| package:

   .. parsed-literal::

      sudo apt-get update && sudo apt-get install pyrake-|version|

.. note:: Repeat step 3 if you are trying to upgrade pyrake.

.. warning:: `python-pyrake` is a different package provided by official debian
   repositories, it's very outdated and it isn't supported by pyrake team.

.. _Scrapinghub: http://scrapinghub.com/
.. _Github repo: https://github.com/pyrake/pyrake
