Contributing
============

Django JET is open-source and every member of the community can contribute to it. Below are some guidelines on how
to help with the project and make it better.

.. _rules:

Rules
-----

* Git master branch should always be stable
* All pull requests are made to git dev branch
* GPL (or similar) code is not eligible for inclusion

Guidelines For Reporting An Issue/Feature
-----------------------------------------

So you've found a bug or have a great idea for a feature. Here's the steps you should take
to help get it added/fixed in Django JET:

* First check if there's an existing issue/pull request for this bug/feature. Issues can be found here
  https://github.com/geex-arts/django-jet/issues, PRs here https://github.com/geex-arts/django-jet/pulls
* If there isn't one there, please add an issue. The ideal report includes:

  * A description of the problem/suggestion
  * How to reproduce the bug
  * If relevant including the versions of your:

        * Python interpreter
        * Django
        * Django JET
        * Optionally of the other dependencies involved

  * It would be great if you also make a pull request which solves your issue

Guidelines For Contributing Code
--------------------------------

If you're ready to contribute back some code/docs, the process should look like:

* Fork the project on GitHub into your own account
* Clone your copy of Django JET to a separate folder
* Install it into your demo project using ``pip install -e PATH_TO_CLONED_JET``
* Make a new branch in git & commit your changes there
* Push your new branch up to GitHub
* Again, ensure there isn't already an issue or pull request out there on it. If there is and you feel you have
  a better fix, please take note of the issue number and mention it in your pull request
* Create a new pull request (based on your branch), including what the problem/feature is, versions of
  your software and referencing any related issues/pull requests

In order to be merged into Django JET, contributions must have the following:

* A solid patch that:

  * is clear
  * works across all supported versions of Python/Django
  * follows the existing style of the code base (mostly PEP-8)

* Desirably a test case that demonstrates the previous flaw that now passes with the included patch
* If it adds/changes a public API, it must also include documentation for those changes
* Must be appropriately licensed (see rules_)

If your contribution lacks any of these things, they will have to be added by a core contributor before
being merged into Django JET proper, which may take time to get to.
