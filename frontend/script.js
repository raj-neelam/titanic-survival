async function predict() {
    const name = document.getElementById("name").value;
    const sex = document.getElementById("gender").value;
    const age = document.getElementById("age").value;
    const pclass = document.getElementById("pclass").value;

    const data_to_send = {
        "sex":sex,
        "age": age,
        "pclass":pclass
    };

    console.log("data to send : ", data_to_send);


    const result = await fetch("/predict",{
        method: 'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify(data_to_send)
    });

    const data = await result.json();

    let html_to_insert;
    console.log("recived data : ", data)
    if (data.prediction == "Survived"){
        html_to_insert = `<span color=green>Prediction: ${name} survived 😇</span>`;
    }else if (data.prediction == "Died"){
        html_to_insert = `<span color=red>Prediction: ${name} Died 🙏</span>`;
    }else{
        html_to_insert = "<span color=yellow>Prediction: Invalid response  </span>";
    }
    document.getElementById('prediction_result').innerHTML = html_to_insert
}