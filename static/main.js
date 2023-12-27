function register_rpc(params) {
    const loginuser = document.querySelector('[name=loginuser]').value;
    const password = document.querySelector('[name=password]').value;
    const username = document.querySelector('[name=username]').value;
    const userage = document.querySelector('[name=userage]').value;
    const gender = document.querySelector('[name=gender]').value;
    const gender_poisk = document.querySelector('[name=gender_poisk]').value;
    const info = document.querySelector('[name=info]').value;
    const foto = document.querySelector('[name=foto]').value;

    const obj = {
        "params": {
            loginuser: loginuser,
            password: password,
            username: username,
            userage: userage,
            gender: gender,
            gender_poisk: gender_poisk,
            info: info,
            foto: foto
        }
    };

    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'  // Set the correct Content-Type header
        },
        body: JSON.stringify(obj)
    })
    .then(function(resp) {
        return resp.json();
    })
    .then(function(data) {
        console.log(data);
        document.querySelector('#message').style.display = 'Вы успешно зарегистрировались';
    })
}
