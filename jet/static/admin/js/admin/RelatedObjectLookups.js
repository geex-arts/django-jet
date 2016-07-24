// Handles related-objects functionality: lookup link for raw_id_fields
// and Add Another links.

function html_unescape(text) {
    // Unescape a string that was escaped using django.utils.html.escape.
    text = text.replace(/&lt;/g, '<');
    text = text.replace(/&gt;/g, '>');
    text = text.replace(/&quot;/g, '"');
    text = text.replace(/&#39;/g, "'");
    text = text.replace(/&amp;/g, '&');
    return text;
}

// IE doesn't accept periods or dashes in the window name, but the element IDs
// we use to generate popup window names may contain them, therefore we map them
// to allowed characters in a reversible way so that we can locate the correct
// element when the popup window is dismissed.
function id_to_windowname(text) {
    text = text.replace(/\./g, '__dot__');
    text = text.replace(/\-/g, '__dash__');
    return text;
}

function windowname_to_id(text) {
    text = text.replace(/__dot__/g, '.');
    text = text.replace(/__dash__/g, '-');
    return text;
}

function showAdminPopup(triggeringLink, name_regexp) {
    var name = triggeringLink.id.replace(name_regexp, '');
    name = id_to_windowname(name);
    var href = triggeringLink.href;
    if (href.indexOf('?') == -1) {
        href += '?_popup=1';
    } else {
        href  += '&_popup=1';
    }

    // Django JET
    showRelatedPopup(name, href);

    return false;
}

function showRelatedObjectLookupPopup(triggeringLink) {
    return showAdminPopup(triggeringLink, /^lookup_/);
}

function dismissRelatedLookupPopup(win, chosenId) {
    var name = windowname_to_id(win.name);
    var elem = document.getElementById(name);
    if (elem.className.indexOf('vManyToManyRawIdAdminField') != -1 && elem.value) {
        elem.value += ',' + chosenId;
    } else {
        document.getElementById(name).value = chosenId;
    }

    // Django JET
    closeRelatedPopup(win);
}

function showRelatedObjectPopup(triggeringLink) {
    var name = triggeringLink.id.replace(/^(change|add|delete)_/, '');
    name = id_to_windowname(name);
    var href = triggeringLink.href;

    // Django JET
    if (href.indexOf('_popup=1') == -1) {
        if (href.indexOf('?') == -1) {
            href += '?_popup=1';
        } else {
            href += '&_popup=1';
        }
    }

    showRelatedPopup(name, href);

    return false;
}

function dismissAddRelatedObjectPopup(win, newId, newRepr) {
    // newId and newRepr are expected to have previously been escaped by
    // django.utils.html.escape.
    newId = html_unescape(newId);
    newRepr = html_unescape(newRepr);
    var name = windowname_to_id(win.name);
    var elem = document.getElementById(name);
    var o;
    if (elem) {
        var elemName = elem.nodeName.toUpperCase();
        if (elemName == 'SELECT') {
            o = new Option(newRepr, newId);
            elem.options[elem.options.length] = o;
            o.selected = true;
        } else if (elemName == 'INPUT') {
            if (elem.className.indexOf('vManyToManyRawIdAdminField') != -1 && elem.value) {
                elem.value += ',' + newId;
            } else {
                elem.value = newId;
            }
        }
        // Trigger a change event to update related links if required.
        django.jQuery(elem).trigger('change');
    } else {
        var toId = name + "_to";
        o = new Option(newRepr, newId);
        SelectBox.add_to_cache(toId, o);
        SelectBox.redisplay(toId);
    }

    // Django JET
    closeRelatedPopup(win);
}

function dismissChangeRelatedObjectPopup(win, objId, newRepr, newId) {
    objId = html_unescape(objId);
    newRepr = html_unescape(newRepr);
    var id = windowname_to_id(win.name).replace(/^edit_/, '');
    var selectsSelector = interpolate('#%s, #%s_from, #%s_to', [id, id, id]);
    var selects = django.jQuery(selectsSelector);
    selects.find('option').each(function() {
        if (this.value == objId) {
            this.innerHTML = newRepr;
            this.value = newId;
        }
    });

    // Django JET
    closeRelatedPopup(win);
};

function dismissDeleteRelatedObjectPopup(win, objId) {
    objId = html_unescape(objId);
    var id = windowname_to_id(win.name).replace(/^delete_/, '');
    var selectsSelector = interpolate('#%s, #%s_from, #%s_to', [id, id, id]);
    var selects = django.jQuery(selectsSelector);
    selects.find('option').each(function() {
        if (this.value == objId) {
            django.jQuery(this).remove();
        }
    }).trigger('change');

    // Django JET
    closeRelatedPopup(win);
};

// Kept for backward compatibility
showAddAnotherPopup = showRelatedObjectPopup;
dismissAddAnotherPopup = dismissAddRelatedObjectPopup;

// Django JET

opener = parent.window;

function showRelatedPopup(name, href) {
    django.jQuery(function($) {
        var $container = $('.related-popup-container', parent.document);
        var $loading = $container.find('.loading-indicator', parent.document);
        var $body = $('body').addClass('non-scrollable', parent.document);
        var $popup = $('<iframe>').attr('name', name).attr('src', href).addClass('related-popup').on('load', function() {
            $popup.add($('.related-popup-back')).fadeIn(200, 'swing', function() {
                $loading.hide();
            });
        });

        $loading.show();
        $container.fadeIn(200, 'swing', function() {
            $container.append($popup);
        });
        $body.addClass('non-scrollable', parent.document);
    });
}

function closeRelatedPopup(win) {
    jet.jQuery('select').trigger('select:init');
    jet.jQuery(win.parent).trigger('related-popup:close');
}

django.jQuery(document).ready(function() {
    jet.jQuery(function($){
        function updateLinks() {
            var $this = $(this);
            var siblings = $this.nextAll('.change-related, .delete-related');
            if (!siblings.length) return;
            var value = $this.val();
            if (value) {
                siblings.each(function(){
                    var elm = $(this);
                    elm.attr('href', elm.attr('data-href-template').replace('__fk__', value));
                });
            } else siblings.removeAttr('href');
        }
        var container = $(document);
        container.on('change', '.related-widget-wrapper select', updateLinks);
        container.find('.related-widget-wrapper select').each(updateLinks);
        container.on('click', '.related-widget-wrapper-link', function(event){
            if (this.href) {
                showRelatedObjectPopup(this);
            }
            event.preventDefault();
        });
    });
});
