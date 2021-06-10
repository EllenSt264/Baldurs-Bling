$(document).ready(function() {
    /* Dropdown */
    $('.dropdown-trigger').dropdown({
        coverTrigger: false,
        hover: true,
        constrainWidth: false,
        alignment: 'center',
        inDuration: 0,
        outDuration: 800,
    });

    $('.parallax').parallax();
})