pyprofilehelper
===============

:Version: 0.1

pyprofilehelper is a collection of scripts to analyze Python cProfile .prof
files.

These scripts have been tested with python 2.7 and python 3.3

.. image:: https://api.travis-ci.org/bartdag/pyprofilehelper.png


Installation
------------

``pip install pyprofilehelper``


Quick Start
-----------

To print the 100 most time-consuming functions in a .prof file, just call:

``python cprofread.py path/to/file.prof 100``

To print the time spent in each parent package and their direct children:

``python cprofscan.py --print-children path/to/file.prof``

To only print the time spent in parent packages xyz and abc and their direct
children:

``python cprofscan.py --filters xyz,abc --print-children path/to/file.prof``


Example of output
-----------------

::

  $ python cprofscan.py --filters django --print-children path/to/file.prof

  Report for Sat Nov 23 11:26:50 2013  /Users/auser/projects/testdjango/fr.010806ms.1385224010.prof

  3879190 total calls in 10.797 seconds

  3819759 total calls in 10.797 seconds recorded in Tree

  Stats for django
    556650 total calls in 0.996 seconds
      utils: 381767 total calls in 0.467 seconds
      db: 65923 total calls in 0.226 seconds
      template: 70178 total calls in 0.205 seconds
      core: 10812 total calls in 0.058 seconds
      dispatch: 26588 total calls in 0.030 seconds
      templatetags: 477 total calls in 0.005 seconds
      forms: 566 total calls in 0.003 seconds
      contrib: 23 total calls in 0.002 seconds
      conf: 223 total calls in 0.001 seconds
      http: 83 total calls in 0.000 seconds
      middleware: 9 total calls in 0.000 seconds
      shortcuts: 1 total calls in 0.000 seconds


Notes on cprofscan
------------------

PYTHONPATH
~~~~~~~~~~

cprofscan will use the PYTHONPATH variable to determine the name of the
packages and modules in a prof file. This works well if cprofscan is invoked in
the same directory and in the same virtualenv (if any) as the program which
generated the .prof file.

Alternatively, you can provide the pythonpath that was used when generating the
prof file with the ``--prefixes`` argument:

::

  $ python cprofscan.py --prefixes /Users/barthelemy/temp,/another/path  testfiles/stats_1_python2.prof


Limiting stats for certain modules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can use the filters argument to only print stats of certain packages or
modules. Use the colon to separate packages:

::

  $ python cprofscan.py --filters django:template,my_package  my_file.prof



Using pyprofilehelper with Django
---------------------------------

If you are using Django, you should use `django-extensions
<https://github.com/django-extensions>`_ to generate a prof file for each
request:

::

  $ python manage.py runprofileserver --use-cprofile --noreload --nomedia --prof-path=.
  $ # this will produce a file like fr.007024ms.1385224022.prof
  $ python cprofscan.py --filters django,mylib fr.007024ms.1385224022.prof


TODO
----

1. Add percent mode to see the relative weight of each package/module
2. Add compare mode to compare to prof files
3. Make cprofscan slightly more modular to be used as a library
4. Add more tests
5. Enable wildcards in filters, e.g., ``*/models.py``
