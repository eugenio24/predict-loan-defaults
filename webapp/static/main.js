const error_div = document.querySelector('#error')
const result_span = document.querySelector('#result-span')
const form = document.querySelector('#form')

form.addEventListener('submit', async (event) => {
    event.preventDefault();
    event.stopPropagation();

    form.classList.add('was-validated')

    if (!form.checkValidity()) return

    const form_data = {
        loan_grade                  : parseFloat(document.querySelector("#loan_grade").value),
        loan_percent_income         : parseInt(document.querySelector("#loan_percent_income").value) / 100,
        person_income               : parseInt(document.querySelector("#person_income").value),
        person_home_ownership       : document.querySelector("#person_home_ownership").value,
        loan_amnt                   : parseInt(document.querySelector("#loan_amnt").value),
        cb_person_default_on_file   : parseInt(document.querySelector("#cb_person_default_on_file").value)
    }    

    result_span.innerText = ""

    const response = await fetch('/predict-default', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(form_data)
    });
    
    const data = await response.json()

    if (response.ok) {
        error_div.classList.add("d-none")        

        result_span.innerText = data.give_loan ? "YES" : "NO"
    } else {        
        error_div.classList.remove("d-none")
    
        error_div.innerText = data.error
    }
});