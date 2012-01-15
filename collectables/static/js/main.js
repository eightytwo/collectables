var mouse_inside = false;

$(function() {
    // Focus the first visible and enabled textbox that isn't the search box.
    $(":text:visible:enabled:eq(1)").focus();

    // Show and hide a visual indicator when interacting with section headings.
    $('.collection_container').hover(
        function() {
            $(this).find('.section_heading_indicator').show();
        },
        function() {
            $(this).find('.section_heading_indicator').hide();
        }
    );   
    
    
    /*
     * Custom Combo Box
     *
     * The click and hover events associated with a custom
     * combo box and its items.
     */

    // Checks if the LMB was released while the point was outside
    // the combo box.
    $('body').mouseup(function() {
        if (!mouse_inside)
            $('.combo_box').hide();
    });

    // Switches the combo box mouse tracking flag
    $('.combo_box').hover(
        function() {
            mouse_inside = true;
        },
        function() {
            mouse_inside = false;
        }
    );

    // Handles the click event of the combo box glyph
    $('.combo_glyph').click(function() {
        $(this).parent().find('.combo_box').toggle();
    });


    // Handles the click event of a combo box item
    $('.combo_box_item').click(function() {
        $(this).parent().parent().find('input').val($(this).text());
        $(this).parent().hide();
    });

    // Handles the click event of a combo box item
    $('.combo_box_item').hover(
        function() {
            $(this).addClass('combo_box_item_selected');
        },
        function() {
            $(this).removeClass('combo_box_item_selected');
        }
    );




    /*
     * Love Button
     *
     * Hover and click handlers for the love button.
     */

    // Handles the hover event on a love glyph
    $('.love_button').hover(
        function() {
            $(this).addClass('love_glyph_active');
        },
        function() {
            $(this).removeClass('love_glyph_active');
        }
    );

    // Handles the click of a remove glyph
    $('.love_button').click(function() {
        // Get the item the love is being applied to
        var context = $(this).val();
        var target = $(this);

        // Call the server function
        $.post(
            '/_add_vote',
            { context: context },
            function(response) {
                if (response.result) {
                    // Get the number of votes
                    var votes = parseInt($('.love_counter').text());
                
                    // Update the vote count text and ensure visible
                    $('.love_counter').text(votes + 1);
                    $('.love_counter').removeClass('hidden');

                    // Remove the button and show the glyph
                    $('<div class="love_glyph love_glyph_active"></div>').insertAfter(target);
                    target.remove();
                }
            },
            'json'
        );

        return false;
    });


    /*
     * Item Property Edit Controls
     *
     * The following handlers are for the hover and click
     * events of the editing controls (enter edit mode,
     * accept edit and cancel edit mode) of an item.
     */ 

    // Show the pilcrow if hovering over the next sibling
    $('.item_property').hover(
        function() {
            $(this).find('.pilcrow').css('visibility', 'visible');
        },
        function() {
            $(this).find('.pilcrow').css('visibility', 'hidden');
        }
    );

    // Handle the click event of the pilcrow
    $('.pilcrow').click(function() {
        var itemProperty = $(this).closest('.item_property');

        // Toggle the display of the edit controls
        $(this).hide();
        $(this).next().show();
        $(this).next().next().show();

        // Toggle the display of the label and form control
        $(this).parent().parent().children('.edit_label').hide();
        $(this).parent().parent().children('.edit_control').show();
    });

    // Handle the click event of the cancel edit button
    $('.cancel_edit').click(function() {
        var itemProperty = $(this).closest('.item_property');
        
        // Toggle the display of the edit controls
        $(this).hide();
        $(this).prev().hide();
        $(this).prev().prev().show();

        // Toggle the display of the label and form control
        itemProperty.find('.edit_label').show();
        itemProperty.find('.edit_control').hide();
    });

    // Show and hide a remove glyph when interacting with removeable item
    // properties.
    $('.item_property_list_value').live({
        mouseover: function() {
            $(this).find('.remove_glyph').css('visibility', 'visible');
        },
        mouseout: function() {
            $(this).find('.remove_glyph').css('visibility', 'hidden');
        }
    });

    // Handles the click of a remove glyph
    $('.remove_glyph').live({
        click: function() {
            // Get the operation, parameter and context
            var operation = 'remove_' + $(this).attr('name');
            var parameter = $(this).prev().text();
            var context = $(this).val();
            var target = $(this);

            // Call the server function
            $.post('/_edit_item',
                   { operation: operation,
                     parameter: parameter,
                     context: context
                   },
                   function(response) {
                     if (response.result) {
                       target.parent().remove();
                     }
                   },
                   'json'
            );

            return false;
        }
    });

    // Handle the update item description button click
    $('#update_item_description').click(function() {
        var target = $(this);
        var itemProperty = target.closest('.item_property');
        var parameter = itemProperty.find('.edit_control').children('[name=parameter]');
        var context = target.val();
        
        $.post(
            '/_edit_item',
            { operation: 'update_description',
              parameter: parameter.val(),
              context: context
            },
            function(response) {
                if (response.result) {
                    itemProperty.find('.edit_label').children(':first').text(parameter.val());
                    target.next().click();
                }
            },
            'json'
        );
    });

    // Handle the update item year button click
    $('#update_item_year').click(function() {
        var target = $(this);
        var itemProperty = target.closest('.item_property');
        var parameter = itemProperty.find('.edit_control').children('[name=parameter]');
        var context = target.val();
        
        $.post(
            '/_edit_item',
            { operation: 'update_year',
              parameter: parameter.val(),
              context: context
            },
            function(response) {
                if (response.result) {
                    var newValue = (parameter.val() === "") ? "-" : parameter.val();
                    itemProperty.find('.edit_label').children(':first').text(newValue);
                    target.next().click();
                }
            },
            'json'
        );
    });

    // Handle the add item collection button click
    $('#add_item_collection').click(function() {
        var target = $(this);
        var itemProperty = target.closest('.item_property');
        var parameter = itemProperty.find('.edit_control').children('[name=parameter]');
        var context = target.val();
        
        $.post(
            '/_edit_item',
            { operation: 'add_collection',
              parameter: parameter.val(),
              context: context
            },
            function(response) {
                if (response.result) {
                    itemProperty.children('.edit_control').before(renderItemPropertyListValue('collection', response.result, context, parameter.val()));
                    parameter.val('');
                    target.next().click();
                }
            },
            'json'
        );
    });
    
    // Handle the add item tag button click
    $('#add_item_tag').click(function() {
        var target = $(this);
        var itemProperty = target.closest('.item_property');
        var parameter = itemProperty.find('.edit_control').children('[name=parameter]');
        var context = target.val();
        
        $.post(
            '/_edit_item',
            { operation: 'add_tag',
              parameter: parameter.val(),
              context: context
            },
            function(response) {
                if (response.result) {
                    itemProperty.children('.edit_control').before(renderItemPropertyListValue('tag', response.result, context, parameter.val()));
                    parameter.val('');
                    target.next().click();
                }
            },
            'json'
        );
    });

    // Renders the html for an item property list value
    function renderItemPropertyListValue(type, url, id, text) {
        return $('<div />')
            .addClass('item_property_list_value')
            .append($('<a />')
                    .text(text)
                    .attr({'href': url})
            )
            .append('&nbsp;')
            .append($('<button type="submit"></button>')
                    .addClass('remove_glyph')
                    .html("&#10006;")
                    .attr({'name': type,
                           'value': id})
            )
    }


    /*
     * Item Thumbnail/Image Controls
     *
     * The following handlers are for the item thumbnail and image
     * controls and events.
     */

    // Handles the hover event for a thumbnail, displaying the remove link
    $('.item_thumbnail_container').hover(
        function() {
            $(this).find('.item_thumbnail_remove').toggle();
        },
        function() {
            $(this).find('.item_thumbnail_remove').toggle();
        }
    );

    // Handles the click of a thumbnail
    $('.item_thumbnail').click(function() {
        var thumbUrl = $(this).attr('src');
        var previewUrl = thumbUrl.replace('/thumb_', '/preview_');
        $('#item_preview').attr('src', previewUrl);
    });

    // Handles the click event for the remove link of a thumbnail
    $('.item_thumbnail_remove').click(function(e) {
        var target = $(this).next();
        var parameter = target.attr('alt');
        var context = $('#item_safe_id').val();
        
        $.post(
            '/_edit_item',
            { operation: 'remove_image',
              parameter: parameter,
              context: context
            },
            function(response) {
                if (response.result) {
                    target.parent().remove();
                }
            },
            'json'
        );
    });

    // Handles the click event of the item thumbnail placeholder
    $('.item_thumbnail_placeholder').click(function() {
        $('.item_image_add').show();
    });
});
