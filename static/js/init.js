function signOut() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
      console.log('User signed out.');
    });
}

window.onLoadCallback = function() {
    gapi.load('auth2', function() {
      gapi.auth2.init();
    });
}

$(document).ready(function() {
    $("#logout-button").click(function() {
        signOut();
    });

    $('.dropdown').hover(function() {
        $(this).addClass('open');
    },
    function() {
        $(this).removeClass('open');
    });
})
