// Price toggle changing color
const bills = document.querySelectorAll('.toggle-month-year p')
const toggleCheck = document.querySelector('.toggle-month-year input')
toggleCheck.onchange = function() {
    if (toggleCheck.checked) {
        bills[0].style.color = 'black'
        bills[1].style.color = '#2196F3'
    }
    else {
        bills[1].style.color = 'black'
        bills[0].style.color = '#2196F3'
    }
}