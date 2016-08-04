(function ($) {
    $(document).ready(function() {
        var initFilters = function() {
            $('.changelist-filter-select').on('change', function () {
                var $select = $(this);
                var $selectedOption = $select.find('option:selected');
                var url = $selectedOption.data('url');
                var querysetLookup = $select.data('queryset--lookup');

                if (url) {
                    document.location = $selectedOption.data('url');
                } else if (querysetLookup) {
                    document.location = '?' + querysetLookup + '=' + $selectedOption.val();
                }
            });
        };

        var initChangeformTabs = function() {
            $('.changeform').each(function() {
                var $changeform = $(this);
                var $tabItems = $changeform.find('.changeform-tabs-item');
                var $modules = $changeform.find('.module');

                if ($tabItems.length == 0) {
                    return;
                }

                var showTab = function(selector) {
                    selector = selector.replace(/^#\/?/, '');

                    var $module = selector.length > 0 ? $modules.filter('#' + selector) : $();

                    if ($module && $module.length == 0) {
                        selector = $tabItems.first().find('a').attr('href').replace(/^#\/?/, '');
                    }

                    var $tabItem = $tabItems.find('a[href="#/' + selector + '"]').closest('.changeform-tabs-item');


                    $tabItems.removeClass('selected');
                    $tabItem.addClass('selected');
                    $module = $modules.removeClass('selected').filter('#' + selector).addClass('selected');
                    $module.find('select').trigger('select:init');
                };

                $('.changeform-tabs-item-link').click(function (e) {
                    var moduleSelector = $(this).attr('href');

                    showTab(moduleSelector);
                });

                showTab(location.hash);
            });
        };

        var initCheckboxesWithoutLabel = function () {
            var uniqueCheckboxIdCounter = 0;
            var uniqueCheckboxIdPrefix = 'unique_checkbox_id_';

            var addLabelToCheckbox = function($checkbox) {
                var checkboxId = $checkbox.attr('id') ? $checkbox.attr('id') : uniqueCheckboxIdPrefix + uniqueCheckboxIdCounter++;
                var $label = $('<label>').attr('for', checkboxId);

                $checkbox.hide().attr('id', checkboxId);
                $label.insertAfter($checkbox);
            };

            var addLabelToCheckboxes = function() {
                var $containers = $('.action-checkbox, .action-checkbox-column').add('.tabular.inline-related .form-row');
                var $checkboxes = $containers.find('input[type="checkbox"]').add('.checkbox-without-label').add('label > input[type="checkbox"]');

                $checkboxes.each(function() {
                    addLabelToCheckbox($(this));
                });
            };

            addLabelToCheckboxes();
        };

        var initUserTools = function() {
            var $userTools = $('.top-user-tools');
            var closeTimeout;

            $userTools.on('mouseenter', function() {
                if (closeTimeout) {
                    clearTimeout(closeTimeout);
                }
                $userTools.addClass('opened');
            });

            $userTools.on('mouseleave', function() {
                closeTimeout = setTimeout(function() {
                    $userTools.removeClass('opened');
                    closeTimeout = null;
                }, 200);
            });
        };

        var initSideMenu = function() {
            var initPopupItems = function() {
                var $popupContainer = $('.sidebar-popup-container');
                var $popup = $('.sidebar-popup');
                var $popupItems = $('.sidebar-popup-item');
                var $popupLinks = $('.popup-item-link');
                var $popupLink;
                var t;
                var $currentPopupItem;
                var $currentPopupItemListItem;
                var $currentPopupItemListItems = function() { return $currentPopupItem.find('.sidebar-popup-list-item:visible') };

                var resetCurrentPopupItemListItems = function() {
                    $currentPopupItemListItems().removeClass('selected');
                };

                var initPopupItemsSearch = function() {
                    $popupItems.each(function() {
                        var $popupItem = $(this);
                        var $search = $popupItem.find('.sidebar-popup-search');
                        var $items = $popupItem.find('.sidebar-popup-list-item');

                        $search.on('change keyup', function() {
                            var text = $(this).val();

                            $items.hide();
                            $popupItem
                                .find('.sidebar-popup-list-item-link:icontains("' + text + '")')
                                .closest('.sidebar-popup-list-item')
                                .show();
                        });
                    });
                };

                var showPopup = function ($popupLink) {
                    clearHideTimeout();

                    var popupItemId = $popupLink.data('popup-item-id');
                    var $popupItem = $('#' + popupItemId);
                    var $search = $popupItem.find('.sidebar-popup-search');

                    $popupItems.hide();
                    $popupItem.show();
                    $popupContainer.stop().fadeIn(200, 'swing');
                    $popupLinks.removeClass('hovered');
                    $popupLink.addClass('hovered');
                    $('body').addClass('non-scrollable');

                    $currentPopupItem = $popupItem;
                    $currentPopupItemListItem = null;
                    resetCurrentPopupItemListItems();

                    $search.val('').trigger('change').focus();
                };

                var hidePopup = function () {
                    t = setTimeout(function() {
                        $popupItems.hide();
                        $popupContainer.stop().fadeOut(200, 'swing');
                        $popupLinks.removeClass('hovered');
                        $('body').removeClass('non-scrollable');

                        $currentPopupItem = null;
                    }, 200);
                };

                var clearHideTimeout = function() {
                    if (t != null) {
                        clearTimeout(t);
                    }
                    t = null;
                };

                $popupLinks.on('mouseenter', function () {
                    $popupLink = $(this);

                    showPopup($popupLink);
                });

                $popupLinks.on('mouseleave', function (e) {
                    var $toElement = $(e.toElement);

                    if ($toElement.hasClass('sidebar-popup') || $toElement.parents('.sidebar-popup').length) {
                        return;
                    }

                    hidePopup();
                });

                $popup.on('mouseenter', function (e) {
                    clearHideTimeout();
                });

                $popup.on('mouseleave', function (e) {
                    var $toElement = $(e.toElement);

                    if ($toElement.hasClass('popup-item-link')
                        && $popupLink.data('popup-item-id') == $toElement.data('popup-item-id')) {
                        return;
                    }

                    hidePopup();
                });

                $popup.find('.sidebar-popup-list-item-link').on('mouseenter', function() {
                    var $link = $(this);
                    var $item = $link.closest('.sidebar-popup-list-item');

                    $currentPopupItemListItem = $item;

                    resetCurrentPopupItemListItems();
                    $currentPopupItemListItem.addClass('selected');
                });

                var selectCurrentPopupItemListItem = function(next) {
                    if ($currentPopupItemListItem != null) {
                        $currentPopupItemListItem = next ? $currentPopupItemListItem.nextAll(':visible').first() : $currentPopupItemListItem.prevAll(':visible').first();
                    }

                    if ($currentPopupItemListItem == null || $currentPopupItemListItem.length == 0) {
                        $currentPopupItemListItem = next ? $currentPopupItemListItems().first() : $currentPopupItemListItems().last();
                    }

                    resetCurrentPopupItemListItems();
                    $currentPopupItemListItem.addClass('selected');
                };

                $(document).keydown(function(e) {
                    if ($currentPopupItem == null) {
                        return;
                    }

                    if (e.which == 38) { //up
                        selectCurrentPopupItemListItem(false);
                    } else if (e.which == 40) { //down
                        selectCurrentPopupItemListItem(true);
                    } else if (e.which == 13) {
                        if ($currentPopupItemListItem) {
                            document.location = $currentPopupItemListItem.find('a').attr('href');
                        }
                    } else {
                        return;
                    }

                    e.preventDefault();
                });

                initPopupItemsSearch();
            };

            var initBookmarks = function() {
                var $addForm = $('#bookmarks-add-form');
                var $removeForm = $('#bookmarks-remove-form');
                var $addTitleInput = $addForm.find('input[name="title"]');
                var $addUrlInput = $addForm.find('input[name="url"]');
                var $removeIdInput = $removeForm.find('input[name="id"]');

                $('.bookmarks-add').on('click', function(e) {
                    e.preventDefault();

                    var $link = $(this);
                    var defaultTitle = $link.data('title') ? $link.data('title') : document.title;
                    var url = window.location.href;

                    $addTitleInput.val(defaultTitle);
                    $addUrlInput.val(url);

                    var addBookmark = function() {
                        $.ajax({
                            url: $addForm.attr('action'),
                            method: $addForm.attr('method'),
                            dataType: 'json',
                            data: $addForm.serialize(),
                            success: function (result) {
                                if (result.error) {
                                    return;
                                }

                                var $list = $('.bookmarks-list');
                                var $item = $('.sidebar-menu-item-list-item.empty').clone().removeClass('empty');

                                $item.find('.sidebar-menu-item-list-item-link')
                                    .attr('href', url)
                                    .append($addTitleInput.val());

                                $item.find('.sidebar-menu-item-list-item-link-remove').attr('data-bookmark-id', result.id);

                                $list.append($item);
                            }
                        });
                    };

                    var buttons = {};

                    buttons[django.gettext('Add')] = function() {
                        addBookmark();
                        $(this).dialog('close');
                    };

                    buttons[django.gettext('Cancel')] = function() {
                        $(this).dialog('close');
                    };

                    $('#bookmarks-add-dialog').dialog({
                        resizable: false,
                        modal: true,
                        buttons: buttons
                    });
                });

                $(document).on('click', '.bookmarks-remove', function(e) {
                    e.preventDefault();

                    var $remove = $(this);
                    var bookmarkId = $remove.data('bookmark-id');

                    var deleteBookmark = function() {
                        $removeIdInput.val(bookmarkId);

                        $.ajax({
                            url: $removeForm.attr('action'),
                            method: $removeForm.attr('method'),
                            dataType: 'json',
                            data: $removeForm.serialize(),
                            success: function (result) {
                                if (result.error) {
                                    return;
                                }

                                var $item = $remove.closest('.sidebar-menu-item-list-item');

                                $item.remove();
                            }
                        });
                    };

                    var buttons = {};

                    buttons[django.gettext('Delete')] = function() {
                        deleteBookmark();
                        $(this).dialog('close');
                    };

                    buttons[django.gettext('Cancel')] = function() {
                        $(this).dialog('close');
                    };

                    $('#bookmarks-remove-dialog').dialog({
                        resizable: false,
                        modal: true,
                        buttons: buttons
                    });
                });
            };

            var initApplicationPinning = function() {
                var $appsList = $('.apps-list');
                var $pinnedAppsList = $('.apps-list-pinned');
                var $appsHide = $('.apps-hide');

                var updateAppsHide = function () {
                    var text;

                    if ($appsList.is(':visible')) {
                        text = django.gettext('Hide applications');
                    } else {
                        text = django.gettext('Show hidden');
                    }

                    $appsHide.text(text);

                    if (($appsList.children().length == 0 || $pinnedAppsList.children().length == 0) && $appsList.is(':visible')) {
                        $appsHide.hide();
                    } else {
                        $appsHide.show();
                    }
                };

                $appsHide.on('click', function (e) {
                    e.preventDefault();

                    $appsList.slideFadeToggle(200, 'swing', function () {
                        localStorage['side_menu_apps_list_visible'] = $appsList.is(':visible');
                        updateAppsHide();
                    });
                });

                $('.app-item .pin-toggle').on('click', function (e) {
                    var $appItem = $(this).closest('.app-item');
                    var appLabel = $appItem.data('app-label');
                    var $form = $('#toggle-application-pin-form');

                    $form.find('input[name="app_label"]').val(appLabel);

                    $.ajax({
                        url: $form.attr('action'),
                        method: $form.attr('method'),
                        dataType: 'json',
                        data: $form.serialize(),
                        success: function (result) {
                            if (result.error) {
                                return;
                            }

                            var $target = result.pinned ? $('.apps-list-pinned') : $('.apps-list');

                            if (result.pinned) {
                                $appItem.addClass('pinned');
                            } else {
                                $appItem.removeClass('pinned');
                            }

                            $appItem.detach();
                            $appItem.appendTo($target);

                            updateAppsHide();
                        }
                    });

                    e.preventDefault();
                });

                if (localStorage['side_menu_apps_list_visible'] === 'false') {
                    if ($pinnedAppsList.children().length != 0) {
                        $appsList.hide();
                    } else {
                        localStorage['side_menu_apps_list_visible'] = true;
                    }
                }

                updateAppsHide();
            };

            initPopupItems();
            initBookmarks();
            initApplicationPinning();
        };

        var initDeleteObjects = function() {
            $('.delete-objects-list-item.collapsable').each(function() {
                var $item = $(this);
                var $link = $item.find('.delete-objects-list-item-row-collapse');
                var $collapsable = $item.find('.delete-objects-list-item-collapsable');

                $link.on('click', function(e) {
                    e.preventDefault();

                    $collapsable.slideToggle(200, 'swing');
                });
            });
        };

        var initjQueryCaseInsensitiveSelector = function() {
            $.expr[":"].icontains = $.expr.createPseudo(function (arg) {
                return function (elem) {
                    return $(elem).text().toUpperCase().indexOf(arg.toUpperCase()) >= 0;
                };
            });
        };

        var initjQuerySlideFadeToggle = function() {
            $.fn.slideFadeToggle = function (speed, easing, callback) {
                return this.animate({opacity: 'toggle', height: 'toggle'}, speed, easing, callback);
            };
        };

        var initDateTimeWidgets = function() {
            var removePreviousSibling = function($element) {
                var node = $element[0].previousSibling;
                node.parentNode.removeChild(node);
            };

            var djangoDateTimeFormatToJs = function(format) {
                return format.toLowerCase().replace(/%\w/g, function(format) {
                    format = format.replace(/%/,"");
                    return format + format;
                });
            };

            var updateDatetimeLayout = function() {
                $('.form-row .datetime').each(function () {
                    var $dateTime = $(this);
                    var $dateField = $dateTime.find('.vDateField');
                    var $timeField = $dateTime.find('.vTimeField');

                    removePreviousSibling($dateField);
                    removePreviousSibling($timeField);

                    $dateField.nextAll('br').first().remove();
                });
            };

            var initDateWidget = function() {
                $('.form-row .vDateField').each(function () {
                    var $dateField = $(this);
                    var $dateLink = $('<a href="#">').addClass('vDateField-link');
                    var $dateButton = $('<span>').addClass('icon-calendar');

                    $dateLink.append($dateButton).insertAfter($dateField);

                    $dateField.datepicker({
                        dateFormat: djangoDateTimeFormatToJs(DATE_FORMAT),
                        showButtonPanel: true,
                        nextText: '',
                        prevText: ''
                    });
                    $dateLink.on('click', function (e) {
                        if ($dateField.datepicker('widget').is(':visible')) {
                            $dateField.datepicker('hide');
                        } else {
                            $dateField.datepicker('show');
                        }

                        e.preventDefault();
                    });
                });

                var old_goToToday = $.datepicker._gotoToday;
                $.datepicker._gotoToday = function(id) {
                    old_goToToday.call(this,id);
                    this._selectDate(id);
                };
            };

            var initTimeWidget = function() {
                $('.form-row .vTimeField').each(function () {
                    var $timeField = $(this);
                    var $timeLink = $('<a href="#">').addClass('vTimeField-link');
                    var $timeButton = $('<span>').addClass('icon-clock');

                    $timeLink.append($timeButton).insertAfter($timeField);

                    $timeField.timepicker({
                        showPeriodLabels: false,
                        showCloseButton: true,
                        showNowButton: true
                    });
                    $timeLink.on('click', function (e) {
                        if ($timeField.datepicker('widget').is(':visible')) {
                            $timeField.datepicker('hide');
                        } else {
                            $timeField.timepicker('show');
                        }

                        e.preventDefault();
                    });
                });
            };

            updateDatetimeLayout();
            initDateWidget();
            initTimeWidget();
        };

        var initInlines = function() {
            $('.module').each(function() {
                var $module = $(this);
                var $items = function() { return $module.find('.stacked-inline-list-item'); };
                var $inlinesRelated = function() { return $module.find('.inline-related'); };

                $module.on('click', '.stacked-inline-list-item-link', function(e) {
                    var $itemLink = $(this);
                    var $item = $itemLink.closest('.stacked-inline-list-item');
                    var moduleId = $itemLink.data('inline-related-id');

                    $items().removeClass('selected');
                    $item.addClass('selected');
                    $inlinesRelated().removeClass('selected').filter('#' + moduleId).addClass('selected');

                    e.preventDefault();
                });

                $module.on('click', '.stacked-inline-list-item-link-remove', function(e) {
                    var $itemLink = $(this).closest('.stacked-inline-list-item-link');
                    var $item = $itemLink.closest('.stacked-inline-list-item');
                    var moduleId = $itemLink.data('inline-related-id');

                    $item.remove();
                    $inlinesRelated().filter('#' + moduleId).remove();

                    e.preventDefault();
                });

                $module.find('.inline-related').each(function() {
                    var $inline = $(this);

                    $inline.find('.delete input').on('change', function(e) {
                        var $input = $(this);
                        var id = $inline.attr('id');
                        var $link = $module.find('.stacked-inline-list-item-link[data-inline-related-id="' + id + '"]');
                        var $item = $link.closest('.stacked-inline-list-item');

                        if ($input.is(':checked')) {
                            $item.addClass('delete');
                        } else {
                            $item.removeClass('delete');
                        }
                    });
                });

                $module.find('.add-row a').on('click', function() {
                   $module.find('select').trigger('select:init');
                });
            });
        };

        var initChangelist = function() {
            var initChangelistHeaders = function() {
                var $originalThead = $('.results thead');

                if ($originalThead.length == 0) {
                    return;
                }

                var $thead = $originalThead.clone();
                var $table = $('<table>').addClass('table helper').append($thead);

                $table.find('.action-checkbox-column').empty();
                $table.appendTo(document.body);

                var updateChangelistHeaderVisibility = function () {
                    if ($(window).scrollTop() > $originalThead.offset().top) {
                        $table.show();
                    } else {
                        $table.hide();
                    }
                };

                var updateChangelistHeaderWidth = function () {
                    var $originalTheadColumns = $originalThead.find('th');
                    var $theadColumns = $thead.find('th');

                    $originalTheadColumns.each(function (i) {
                        $theadColumns.eq(i).css('width', $(this).width());
                    });
                };

                $(window).on('scroll', updateChangelistHeaderVisibility);
                $(window).on('resize', updateChangelistHeaderWidth);

                updateChangelistHeaderWidth();
            };

            var initChangelistFooters = function() {
                var $changelistFooters = $('.changelist-footer');

                if ($changelistFooters.length == 0) {
                    return;
                }

                var updateChangelistFooters = function () {
                    $changelistFooters.each(function () {
                        var $changelistFooter = $(this);
                        var $results = $changelistFooter.siblings('.results');

                        if ($(window).scrollTop() + $(window).height() < $(document).height()) {
                            if (!$changelistFooter.hasClass('fixed')) {
                                var previousScrollTop = $(window).scrollTop();

                                $changelistFooter.addClass('fixed');
                                $results.css('margin-bottom', ($changelistFooter.outerHeight(false) - 20 - 2) + 'px');

                                $(window).scrollTop(previousScrollTop);
                            }
                        } else {
                            if ($changelistFooter.hasClass('fixed')) {
                                $changelistFooter.removeClass('fixed');
                                $results.css('margin-bottom', 0);
                            }
                        }
                    });
                };

                $(window).on('scroll', updateChangelistFooters);
                $(window).on('resize', updateChangelistFooters);

                updateChangelistFooters();
            };

            var initChangelistImages = function() {
                $('img[src$="admin/img/icon-yes.gif"]').after($('<span class="icon-tick">'));
                $('img[src$="admin/img/icon-no.gif"]').after($('<span class="icon-cross">'));
                $('img[src$="admin/img/icon-unknown.gif"]').after($('<span class="icon-question">'));
            };

            var initChangelistRowSelection = function() {
                $('#result_list tbody th, #result_list tbody td').on('click', function(e) {
                    // Fix selection on clicking elements inside row (e.x. links)
                    if (e.target != this) {
                        return;
                    }

                    $(this).closest('tr').find('.action-checkbox .action-select').click();
                });
            };

            initChangelistHeaders();
            initChangelistFooters();
            initChangelistImages();
            initChangelistRowSelection();
        };

        var initTooltips = function() {
            $('a[title],.tooltip[title]').tooltip({
                track: true
            });
        };

        var initDashboard = function() {
            var updateDashboardModules = function () {
                var $form = $('#update-dashboard-modules-form');
                var modules = [];

                $('.dashboard-column').each(function () {
                    var $column = $(this);
                    var column = $column.closest('.dashboard-column-wrapper').index();

                    $column.find('.dashboard-item').each(function () {
                        var $item = $(this);
                        var order = $item.index();
                        var id = $item.data('module-id');

                        modules.push({
                            id: id,
                            column: column,
                            order: order
                        });
                    });
                });

                $form.find('[name="modules"]').val(JSON.stringify(modules));

                $.ajax({
                    url: $form.attr('action'),
                    method: $form.attr('method'),
                    dataType: 'json',
                    data: $form.serialize()
                });
            };

            $('.dashboard-column').droppable({
                activeClass: 'active',
                hoverClass: 'hovered',
                tolerance: 'pointer',
                accept: '.dashboard-item'
            }).sortable({
                items: '.dashboard-item',
                handle: '.dashboard-item-header',
                tolerance: 'pointer',
                connectWith: '.dashboard-column',
                cursor: 'move',
                placeholder: 'dashboard-item placeholder',
                forcePlaceholderSize: true,
                update: function (event, ui) {
                    updateDashboardModules();
                }
            });

            $('.dashboard-item.collapsible').each(function () {
                var $item = $(this);
                var $link = $item.find('.dashboard-item-collapse');
                var $collapsible = $item.find('.dashboard-item-content');
                var $form = $('#update-dashboard-module-collapse-form');
                var moduleId = $item.data('module-id');

                $link.on('click', function (e) {
                    e.preventDefault();

                    $collapsible.slideFadeToggle(200, 'swing', function () {
                        var collapsed = $collapsible.is(':visible') == false;

                        if (collapsed) {
                            $item.addClass('collapsed')
                        } else {
                            $item.removeClass('collapsed')
                        }

                        $form.find('[name="id"]').val(moduleId);
                        $form.find('[name="collapsed"]').val(collapsed ? 'true' : 'false');

                        $.ajax({
                            url: $form.attr('action'),
                            method: $form.attr('method'),
                            dataType: 'json',
                            data: $form.serialize()
                        });
                    });
                });
            });

            $('.dashboard-item.deletable').each(function () {
                var $item = $(this);
                var $link = $item.find('.dashboard-item-remove');
                var $form = $('#remove-dashboard-module-form');
                var moduleId = $item.data('module-id');

                $link.on('click', function (e) {
                    e.preventDefault();

                    var buttons = {};

                    var deleteModule = function () {
                        $item.fadeOut(200, 'swing', function () {
                            $form.find('[name="id"]').val(moduleId);

                            $.ajax({
                                url: $form.attr('action'),
                                method: $form.attr('method'),
                                dataType: 'json',
                                data: $form.serialize()
                            });
                        });
                    };

                    buttons[django.gettext('Delete')] = function () {
                        deleteModule();
                        $(this).dialog('close');
                    };

                    buttons[django.gettext('Cancel')] = function () {
                        $(this).dialog('close');
                    };

                    $('#module-remove-dialog').dialog({
                        resizable: false,
                        modal: true,
                        buttons: buttons
                    });
                });
            });

            var $form = $('#add-dashboard-module-form');

            $form.find('.add-dashboard-link').on('click', function (e) {
                var $typeInput = $form.find('[name="type"]');
                var type = $form.find('[name="module"] option:selected').data('type');

                if (type) {
                    $typeInput.val(type);

                    $.ajax({
                        url: $form.attr('action'),
                        method: $form.attr('method'),
                        dataType: 'json',
                        data: $form.serialize(),
                        success: function (result) {
                            if (result.error) {
                                return;
                            }

                            document.location = result.success_url;
                        }
                    });
                }

                e.preventDefault();
            });

            $('.dashboard-item.ajax').each(function () {
                var $item = $(this);
                var $content = $item.find('.dashboard-item-content');
                var url = $item.data('ajax-url');
                var moduleId = $item.data('module-id');

                $form.find('[name="id"]').val(moduleId);

                $.ajax({
                    url: url,
                    dataType: 'json',
                    success: function (result) {
                        if (result.error) {
                            $content.empty();
                            return;
                        }

                        var oldHeight = $content.height();
                        $content.html(result.html);
                        var newHeight = $content.height();

                        $content.height(oldHeight);
                        $content.animate({
                            height: newHeight
                        }, 250);
                    },
                    error: function() {
                        $content.empty();
                    }
                });
            });

            $('.reset-dashboard-link').on('click', function(e) {
                var buttons = {};
                var resetDashboard = function () {
                    var $form = $('#reset-dashboard-form');

                    $.ajax({
                        url: $form.attr('action'),
                        method: $form.attr('method'),
                        dataType: 'json',
                        data: $form.serialize(),
                        success: function (result) {
                            if (result.error) {
                                return;
                            }

                            location.reload();
                        }
                    });
                };

                buttons[django.gettext('Yes')] = function() {
                    resetDashboard();
                    $(this).dialog('close');
                };

                buttons[django.gettext('Cancel')] = function() {
                    $(this).dialog('close');
                };

                $('#reset-dashboard-dialog').dialog({
                    resizable: false,
                    modal: true,
                    buttons: buttons
                });

                e.preventDefault();
            });
        };

        var initUnsavedChangesWarning = function() {
            var $changeform = $('.changeform');

            if ($changeform.length) {
                var $inputs = $changeform.find('input, textarea, select');
                var bound = false;

                var onBeforeUnload = function (){
                    return django.gettext('Warning: you have unsaved changes');
                };

                var onChange = function () {
                    $inputs.off('change', onChange);

                    if (!bound) {
                        $(window).bind('beforeunload', onBeforeUnload);

                        bound = true;
                    }
                };

                $(document).on('submit', 'form', function() {
                    $(window).off('beforeunload', onBeforeUnload);
                });

                $inputs.on('change', onChange);
            }
        };

        var initScrollbars = function() {
            $('.sidebar-menu-wrapper').perfectScrollbar();
        };

        var initThemeChoosing = function() {
            $('.choose-theme').on('click', function () {
                var $link = $(this);

                $.cookie('JET_THEME', $link.data('theme'), { expires: 365, path: '/' });

                var cssToLoad = [
                    { url: $link.data('base-stylesheet'), class: 'base-stylesheet' },
                    { url: $link.data('select2-stylesheet'), class: 'select2-stylesheet' },
                    { url: $link.data('jquery-ui-stylesheet'), class: 'jquery-ui-stylesheet' }
                ];

                var loadedCss = 0;

                var onCssLoaded = function() {
                    ++loadedCss;

                    if (loadedCss == cssToLoad.length) {
                        $(document).trigger('theme:changed');
                    }
                };

                cssToLoad.forEach(function(css) {
                    $('<link>')
                        .attr('rel', 'stylesheet')
                        .addClass(css['class'])
                        .attr('href', css['url'])
                        .load(onCssLoaded)
                        .appendTo('head');
                    $('.' + css['class'])
                        .slice(0, -2)
                        .remove();
                });

                $('.choose-theme').removeClass('selected');
                $link.addClass('selected');
            });
        };

        var initRelatedPopups = function() {
            var closeRelatedPopup = function () {
                var $popups = $('.related-popup');
                var $container = $('.related-popup-container');
                var $popup = $popups.last();

                $popup.remove();

                if ($popups.length == 1) {
                    $container.fadeOut(200, 'swing', function () {
                        $('.related-popup-back').hide();
                        $('body').removeClass('non-scrollable');
                    });
                }
            };

            $('.related-popup-back').on('click', function (e) {
                e.preventDefault();
                closeRelatedPopup();
            });

            $(window).on('related-popup:close', function () {
                closeRelatedPopup();
            });
        };

        initjQueryCaseInsensitiveSelector();
        initjQuerySlideFadeToggle();
        initFilters();
        initChangeformTabs();
        initCheckboxesWithoutLabel();
        initUserTools();
        initSideMenu();
        initDeleteObjects();
        initDateTimeWidgets();
        initInlines();
        initChangelist();
        initTooltips();
        initDashboard();
        initUnsavedChangesWarning();
        initScrollbars();
        initThemeChoosing();
        initRelatedPopups();
    });
})(jet.jQuery);