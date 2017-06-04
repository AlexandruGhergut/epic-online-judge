$(document).ready(function() {
    function updatePendingSubmissions() {
        pending_id_tds = $('tr.pending > td.submission_id');
        pending_status_tds = $('tr.pending > td.submission_status');
        pending_ids = [];
        for (td of pending_id_tds)
            pending_ids.push(td.innerText);

        if (pending_id_tds.length > 0) {
            $.ajax({
                url: "/submission/status/",
                type: 'POST',
                data: { 'ids[]' : pending_ids },
                success: function(result) {
                    for (var i = 0; i < pending_ids.length; i++) {
                        var current_id = pending_ids[i];
                        pending_status_tds[i].innerText = result[current_id];
                        if (result[current_id] != 'Pending')
                            pending_status_tds[i].parentElement.classList.remove('pending');
                    }

                    setTimeout(updatePendingSubmissions, 5000);
                }
            });
        }
    }

    setTimeout(updatePendingSubmissions, 2000);
});
