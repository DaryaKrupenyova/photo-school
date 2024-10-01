function calc(event) {
    'use_strict';
    let a = Number(firstval.value)
    let b = Number(secondval.value)

    let d = document.createElement('div')
    d.classList.add('alert')
    d.classList.add('alert-success')
    d.classList.add('text-center')
    d.innerHTML = a + b

    calc_result.innerHTML = ''
    calc_result.appendChild(d)
}

calc_btn.addEventListener('click', calc)