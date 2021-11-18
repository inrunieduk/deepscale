// get photo-fileR image and send it to http://localhost:5000/model/predict
function send() {
    const file = document.getElementById('photo-fileR').files[0];

    var formdata = new FormData();
    formdata.append('image', file);

    fetch('http://localhost:5000/model/predict', {
        method: 'POST',
        headers: {
            "Accept": "application/json"
        },
        body: formdata,
        redirect: 'follow'
    }).then(
        response => response.blob()
    ).then(
        blob => {
            var url = window.URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = "filename";
            document.body.appendChild(a); 
            a.click();    
            a.remove();    
        }).catch(
            error => console.log(error)
        );
}
