Changelog
=========

0.1.5
-----
* Add inlines.min.js
* Specify IE compatibility version
* Add previous/next buttons to change form
* Add preserving filters when returning to changelist
* Add opened tab remembering
* Fix breadcrumbs text overflow
* PR-65: Fixed Django 1.8+ compatibility issues (thanks to hanuprateek, SalahAdDin, cdrx for pull requests)
* PR-73: Added missing safe template tag on the change password page (thanks to JensAstrup for pull request)


0.1.4
-----
* [Feature] Side bar compact mode (lists all models without opening second menu)
* [Feature] Custom side bar menu applications and models content and ordering
* [Feature] Related objects actions in nice-looking popup instead of new window
* [Feature] Add changelist row selection on row background click
* [Fix] Better 3rd party applications template compatibility
* [Fix] JET and Django js translation conflicts
* [Fix] Hide empty model form labels
* [Fix] Wrong positioning for 0 column
* [Fix] Issue-21: Init label wrapped checkboxes
* [Improvement] Add top bar arrow transition


0.1.3
-----
* [Feature] Add theme choosing ability
* [Feature] New color themes
* [Fix] Refactor themes
* [Fix] Rename JET_THEME configuration option to JET_DEFAULT_OPTION
* [Fix] Fixed scrolling to top when side menu opens
* [Fix] Fixed read only fields paddings
* [Fix] Issue-18: Remove unused resources which may brake static processing (thanks to DheerendraRathor for the report)
* [Fix] Issue-19: Fixed datetime today button (thanks to carlosfvieira for the report)


0.1.2
-----
* [Fix] Issue-14: Fixed ajax fields choices being rendered in page (thanks to dnmellen for the report)
* [Fix] Issue-15: Fixed textarea text wrapping in Firefox
* [Feature] PR-16: Allow usage of select2_lookups filter in ModelForms outside of Admin (thansk to dnmellen for pull request)
* [Fix] Fixed select2_lookups for posted data
* [Feature] Issue-14: Added ajax related field filters
* [Fix] Made booleanfield icons cross browser compatible
* [Fix] Issue-13: Added zh-hans i18n
* [Feature] Separate static browser cache for each jet version


0.1.1
-----
* [Feature] Added fade animation to sidebar application popup
* [Fix] Issue-10: Fixed ability to display multiple admin form fields on the same line (thanks to blueicefield for the report)
* [Fix] Fixed broken auth page layout for some translations
* [Fix] Issue-11: Fixed setup.py open file in case utf-8 path (thanks to edvm for the report)


0.1.0
-----
* [Fix] Issue-9: Fixed dashboard application templates not being loaded because of bad manifest (thanks to blueicefield for the report)
* [Fix] Added missing localization for django 1.6
* [Fix] Added importlib requirement for python 2.6
* [Fix] Added python 2.6 test
* [Fix] Fixed coveralls 1.0 failing for python 3.2
* [Improvement] Expand non dashboard sidebar width


0.0.9
-----
* [Feature] Replace sidemenu scrollbars with Mac-like ones
* [Feature] Added dashboard reset button
* [Feature] Updated sidebar links ui
* [Fix] Fixed filter submit block text alignment
* [Fix] Made boolean field icon style global
* [Fix] Fixed metrics requests timezone to be TIME_ZONE from settings


0.0.8
-----
* Change license to GPLv2


0.0.7
-----
* [Feature] Added Google Analytics visitors totals dashboard widget
* [Feature] Added Google Analytics visitors chart dashboard widget
* [Feature] Added Google Analytics period visitors dashboard widget
* [Feature] Added Yandex Metrika visitors totals dashboard widget
* [Feature] Added Yandex Metrika visitors chart dashboard widget
* [Feature] Added Yandex Metrika period visitors dashboard widget
* [Feature] Animated ajax loaded modules height on load
* [Feature] Added initial docs
* [Feature] Added ability to use custom checkboxes without labels styled
* [Feature] Added ability to specify optional modules urls
* [Feature] Added pop/update module settings methods
* [Feature] Added module contrast style
* [Feature] Added module custom style property
* [Feature] Pass module to module settings form
* [Feature] Set dashboard widgets minimum width
* [Feature] Added dashboard widgets class helpers
* [Fix] Fixed toggle all checkbox
* [Fix] Fixed 500 when module class cannot be loaded
* [Fix] Fixed datetime json encoder
* [Fix] Fixed double shadow for tables in dashboard modules
* [Fix] Fixed tables forced alignment
* [Fix] Fixed dashboard ul layout
* [Fix] Fixed language code formatting for js
* [Fix] Fixed 500 when adding module if no module type specified


0.0.6
-----

* [Feature] Added initial unit tests
* [Fixes] Compatibility fixes


0.0.5
-----

* [Feature] Added ability to set your own branding in the top of the sidebar


0.0.4
-----

* [Feature] Added Python 3 support


0.0.1
-----

* Initial release




