
document.addEventListener('DOMContentLoaded', function() {
    var select = document.getElementById('grupoAtendimento');

    select.addEventListener('mousedown', function(e) {
        e.preventDefault();

        var scroll = select.scrollTop;

        e.target.selected = !e.target.selected;

        setTimeout(function() {select.scrollTop = scroll;}, 0);

        select.focus();
    });

    select.addEventListener('mousemove', function(e) {
        e.preventDefault();
    });
});
