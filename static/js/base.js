$(document).ready(function() {
    /* Dropdown */
    $('.dropdown-trigger').dropdown({
        coverTrigger: false,
        hover: true,
        constrainWidth: false,
        alignment: 'center',
        inDuration: 300,
        outDuration: 150,
    });

    $('.parallax').parallax();
})