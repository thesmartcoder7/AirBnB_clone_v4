$(function () {
    const dict = {}
    $('input:checkbox').change(function () {
        if ($(this).is(':checked')) {
            dict[$(this).attr('data-id')] = $(this).attr('data-name');
            console.log($(this).attr('data-name'));
        } else {
            delete dict[$(this).attr('data-id')];
        }

        $('.amenities h4').text(Object.values(dict).join(', '));
    });

    $.get('http://0.0.0.0:5001/api/v1/status/', function (data, status) {
        if (status === 'success') {
            if (data.status === 'OK') {
                $('div#api_status').addClass('available');
                $('div#api_status').css('background-color', '#ff545f');
                console.log(data.status);
            } else {
                $('div#api_status').removeClass('available');
                console.log(data.status);
            }
        } else {
            if ($('div#api_status').hasClass('available')) {
                $('div#api_status').removeClass('available');
            }
        }
    });
})