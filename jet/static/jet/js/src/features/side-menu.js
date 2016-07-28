require('./../utils/jquery-icontains');
require('./../utils/jquery-slidefade');

var $ = window.jQuery = require('jquery');

require('jquery-ui/ui/core');
require('jquery-ui/ui/widget');
require('jquery-ui/ui/mouse');
require('jquery-ui/ui/draggable');
require('jquery-ui/ui/resizable');
require('jquery-ui/ui/button');
require('jquery-ui/ui/dialog');

require('perfect-scrollbar/jquery')($);

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

var initScrollbars = function() {
    $('.sidebar-menu-wrapper').perfectScrollbar();
};

$(document).ready(function() {
    initSideMenu();
    initScrollbars();
});
