$(window).on('map:init', function (e) {
    var detail = e.originalEvent ?
                 e.originalEvent.detail : e.detail;

    L.marker([50.5, 30.5]).addTo(detail.map);

});