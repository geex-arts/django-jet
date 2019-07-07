Changelog
=========

1.0.8
-----
* PR-345: Django 2.1 compatability fix
* PR-337: Fix get_model_queryset exception when model_admin is None
* PR-309: Add French locale
* PR-311: Add an `s` for grammar
* PR-312: Add grammar fixes
* PR-356: Remove duplicate entries in autocomplete
* PR-327: Fixed typo


1.0.7
-----
* PR-265: Fixed Django 2 support (thanks to HarryLafranc for PR)
* PR-219: Added Persian/Farsi translation (thanks to pyzenberg for PR)
* PR-271: Fix locale names (thanks to leonardoarroyo for PR)


1.0.6
-----
* PR-191: Added sidebar pinning functionality (thanks to grigory51 for PR)
* Issue-199: Fixed Django 1.11 context issue (thanks to gileadslostson for report)
* Issue-202: Fixed inline-group-row:added event (thanks to a1Gupta for report)
* Issue-188: Make testing use latest major Django versions and Python 3.5, 3.6 (thanks to liminspace for report)
* Added new flexible menu customizing setting JET_SIDE_MENU_ITEMS
* Added labels to sibling buttons
* Fixed django.jQuery select change events
* Fixed sidebar "Search..." label localization
* Added select disabled style
* Fixed initial value for select2 ajax fields when POST request


1.0.5
-----
* PR-167: Added fallback to window.opener to support old Django popups (thanks to michaelkuty for PR)
* PR-169: Added zh-cn localization (thanks to hbiboluo for PR)
* PR-172: Added Polish localization (thanks to lburdzy for PR)
* PR-174: Fixed permission error on ModelLookupForm (thanks to brenouchoa for PR)
* PR-178: Added Arabic localization by KUWAITNET (thanks to Bashar for PR)
* Removed "powered by Django JET" copyright
* Fixed exception when initial object not found for RelatedFieldAjaxListFilter


1.0.4
-----
* IMPORTANT: Fixed security issue with accessing model_lookup_view (when using RelatedFieldAjaxListFilter) without permissions
* Fixed admin filters custom class attribute overrides
* Fixed RelatedFieldAjaxListFilter to work with m2m fields


1.0.3
-----
* PR-140: Added change message as tooltip to recent action dashboard module (thanks to michaelkuty for PR)
* PR-130: Implement JET ui for django-admin-rangefilter (thanks to timur-orudzhov for PR)
* PR-131: Use WSGIRequest resolver_match instead of resolve (thanks to m-vdb for PR)
* PR-138: Fixed encoding error in jet_popup_response_data (thanks to michaelkuty for PR)
* PR-137,138: Fixed UnicodeEncodeError in related popups (thanks to michaelkuty, Copperfield for PRs)
* Issue-146: Fixed Django CMS plugin edit issue (thanks to bculpepper for report)
* Issue-147: Fixed login for non superusers (thanks to gio82 for report)
* Issue-147: Fixed RelatedFieldAjaxListFilter in Django 0.9+ (thanks to a1Gupta for report)
* Issue-126: Fixed related popups for new items in tabular inlines (thanks to kmorey for report)


1.0.2
-----
* PR-115: Removed mock request from get_model_queryset to fix 3rd party packages (thanks to imdario for PR)
* PR-106: Added Spanish localization (thanks to SalahAdDin for PR)
* PR-107, 119: Added Brazilian Portuguese localization (thanks to sedir, mord4z for PR)
* PR-109: Added German localization (thanks to dbartenstein for PR)
* PR-123: Added Czech localization (thanks to usakc for PR)
* Added breadcrumbs text wrapping
* Issue-127: Removed forgotten untranslated label in breadcrumbs (thanks to hermanocabral for report)
* PR-121, 122: Fixed jet_custom_apps_example.py for Django 1.10 (thanks to retailify for PR)
* Fixed CompactInline opening first navigation item when there are no items
* Issue-118: Fixed inlines max_forms field for CompactInline (thanks to a1Gupta for report)
* Issue-117: Fixed draggable field for dashboard modules (thanks to a1Gupta for report)
* Issue-117: Added LinkList module draggable/deletable/collapsible settings saving (thanks to a1Gupta for report)
* Issue-114: Fixed Django 1.10 filter_horizontal not working (thanks to vishalbanwari for report)
* Issue-126: Fixed related popup links for new inline items (thanks to kmorey for report)
* Issue-128: Fixed delete confirmation submit button misplacement (thanks to retailify for report)


1.0.1
-----
* StackedInline from earlier JET versions is back as a CompactInline custom class
* Changed license to AGPLv3
* Fixed filters with multiple selectable items behavior


1.0.0
-----
* Fixed dashboard module buttons mobile layout misplacement
* Fixed double tap menu issue for iOS devices
* Fixed changelist footer from fixed position transition
* Fixed system messages style
* Fixed jQuery UI base styles broken image paths
* Issue-69, 72: Updated checkboxes without label UI (thanks to h00p, JuniorLima for report)
* Issue-89: Fixed multiple admin sites support (thanks to sysint64 for report)
* Added missing locale files to PyPI package (thanks to SalahAdDin for report)
* Issue-49: Fixed AppList and ModelList models/exclude parsers (thanks to eltismerino for report)
* Issue-50: Fixed pinned application user filtering (thanks to eltismerino for report)
* Fixed empty branding visibility
* Fixed IE dashboard list items wrapping
* Fixed IE sidebar popup items spacing
* Fixed dashboard module wrong height after animation
* Fixed dashboard module change form breadcrumbs
* Improved paginator 'show all' layout
* Updated documentation
* Added support for filters with multiple select


0.9.1
-----
* Mobile UX improved
* Refactored and optimized locale files
* More documentation added
* Improved object tools and toolbar arrangement
* Fixed change list footer misplacement
* Fixed chromium sidebar scrollbar misplacement
* Remove unused tags
* Prefixed JET template tags
* Fixed jet_custom_apps_example command
* Fixed Django 1.6 user tools permission check
* Issue-93: Fixed static urls version appending (thanks to kbruner32 for report)
* Fixed Django 1.6 line.has_visible_field field
* Updated default dashboard action list style
* Added Django 1.10.0 tests


0.9.0
-----
* Almost complete layout rewrite with only 3 template overrides
* Responsive layout for mobile devices
* Reorganized scripts (Browserify + gulp)
* Updated table sortable headers style
* Fixed related object popups bugs
* Added check for JS language files existence before load
* Refactored locale files
* Fixed admin permissions checks
* Fixed compatibility issue with Django 1.10


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




