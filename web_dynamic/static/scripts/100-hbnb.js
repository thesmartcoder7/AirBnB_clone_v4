$(function () {
    const amenities = {};
    const states = {};
    const cities = {};
    const locations = {};
    $('.amenityCheckbox').change(function () {
        if ($(this).is(':checked')) {
            amenities[$(this).attr('data-id')] = $(this).attr('data-name');
            console.log($(this).attr('data-name'));
        } else {
            delete amenities[$(this).attr('data-id')];
        }

        $('.amenities h4').text(Object.values(amenities).join(', '));
    });

    $('.statesCheckbox').change(function () {
        if ($(this).is(':checked')) {
            states[$(this).attr('data-id')] = $(this).attr('data-name');
            locations[$(this).attr('data-id')] = $(this).attr('data-name');

        } else {
            delete states[$(this).attr('data-id')];
            delete locations[$(this).attr('data-id')];
        }
        console.log(states);
        $('.locations h4').text(Object.values(locations).join(', '));
    });

     $('.citiesCheckbox').change(function () {
        if ($(this).is(':checked')) {
            cities[$(this).attr('data-id')] = $(this).attr('data-name');
            locations[$(this).attr('data-id')] = $(this).attr('data-name');
        } else {
            delete cities[$(this).attr('data-id')];
            delete locations[$(this).attr('data-id')];
        }
        console.log(cities);
        $('.locations h4').text(Object.values(locations).join(','));
    });


    $.get('http://0.0.0.0:5001/api/v1/status/', function (data, status) {
        if (status === 'success') {
            if (data.status === 'OK') {
                $('div#api_status').addClass('available');
                $('div#api_status').css('background-color', '#ff545f');
            } else {
                $('div#api_status').removeClass('available');
            }
        } else {
            if ($('div#api_status').hasClass('available')) {
                $('div#api_status').removeClass('available');
            }
        }
    });

    $.ajax({
        url:'http://0.0.0.0:5001/api/v1/places_search/',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({}),
        datatype: 'json',
        success: function (data, status) {
            if (status === 'success'){
                data.forEach(function (place) {
                    $('section.places').append(`<article>
                    <div class="title_box">
                    <h2>${place.name}</h2>
                    <div class="price_by_night">${place.price_by_night}</div>
                    </div>
                    <div class="information">
                    <div class="max_guest">${place.max_guest} Guests</div>
                    <div class="number_rooms">${place.number_rooms} Bedrooms</div>
                    <div class="number_bathrooms">${place.number_bathrooms} Bathrooms</div>
                    </div>
                    <div class="description">${place.description}</div>
                    </article>`
                    )
                });

            }
        }

    })

    $('button:button').click(function () {
        $.ajax({
            url: 'http://0.0.0.0:5001/api/v1/places_search/',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ amenities: Object.keys(amenities), states: Object.keys(states), cities: Object.keys(cities) }),
            datatype: 'json',
            success: function (data, status) {
                if (status === 'success'){
                    $('section.places').empty();
                    data.forEach(function (place) {
                        $('section.places').append(`<article>
                        <div class="title_box">
                        <h2>${place.name}</h2>
                        <div class="price_by_night">${place.price_by_night}</div>
                        </div>
                        <div class="information">
                        <div class="max_guest">${place.max_guest} Guests</div>
                        <div class="number_rooms">${place.number_rooms} Bedrooms</div>
                        <div class="number_bathrooms">${place.number_bathrooms} Bathrooms</div>
                        </div>
                        <div class="description">${place.description}</div>
                        </article>`
                        )
                    });
                }
            }
        })
    });


    });