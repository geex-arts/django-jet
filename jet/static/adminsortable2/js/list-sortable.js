"use strict";

jQuery.extend({
	getQueryParams: function() {
		var vars = [], hash, i;
		var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
		for (i = 0; i < hashes.length; i++) {
			hash = hashes[i].split('=');
			vars.push(hash[0]);
			vars[hash[0]] = hash[1];
		}
		return vars;
	},
	getQueryParam: function(name) {
		return jQuery.getQueryParams()[name];
	}
});

// make list view sortable
jQuery(function($) {
	var startindex, startorder, endindex, endorder;
	var csrfvalue = $('form').find('input[name="csrfmiddlewaretoken"]').val();
	var ordering = $.getQueryParam('o');

	if (window.admin_sortable2 === undefined)
		return;  // global variables not initialized by change_list.html
	if (ordering === undefined) {
		ordering = '1';
	}

	var $helper;

	$('#result_list').sortable({
        tolerance: 'pointer',
		items: 'tr',
        cursor: 'move',
        axis: 'y',
		containment: $('#result_list tbody'),
        forcePlaceholderSize: true,
		helper: function(e, tr){
            var $originals = tr.children();
            $helper = tr.clone().addClass('dragging');
            $helper.children().each(function(index) {
                $(this).width($originals.eq(index).width())
            });

            return $helper;
        },
		start: function(event, dragged_rows) {
			$('#result_list tr.ui-sortable-placeholder').attr('height', $helper.height() + 1);
			startindex = dragged_rows.item.index();
		},
		stop: function(event, dragged_rows) {
			var $result_list = $(this);
			$result_list.find('tbody tr').each(function(index) {
				$(this).removeClass('row1 row2').addClass(index % 2 ? 'row2' : 'row1');
			});
			endindex = dragged_rows.item.index()

			if (startindex == endindex) return;
			else if (endindex == 0) {
				if (ordering.split('.')[0] === '-1')
					endorder = parseInt($(dragged_rows.item.context.nextElementSibling).find('div.drag').attr('order')) + 1;
				else
					endorder = parseInt($(dragged_rows.item.context.nextElementSibling).find('div.drag').attr('order')) - 1;
			} else {
				endorder = $(dragged_rows.item.context.previousElementSibling).find('div.drag').attr('order');
			}
			startorder = $(dragged_rows.item.context).find('div.drag').attr('order');

			$.ajax({
				url: window.admin_sortable2.update_url,
				type: 'POST',
				data: {
					o: ordering,
					startorder: startorder,
					endorder: endorder,
					csrfmiddlewaretoken: csrfvalue
				},
				success: function(moved_items) {
					$.each(moved_items, function(index, item) {
						$result_list.find('tbody tr input.action-select[value=' + item.pk + ']').parents('tr').each(function() {
							$(this).find('div.drag').attr('order', item.order);
						});
					});
				},
				error: function(response) {
					console.error('The server responded: ' + response.responseText);
				}
			});
		}
	});
	$('#result_list, tbody, tr, td, th').disableSelection();
});
