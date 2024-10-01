function process(index) {
    $.post("/process_data/", {'index': index}, function (data, status) {
        alert(`Data: ${data}\nStatus: ${status}`);
    });
}