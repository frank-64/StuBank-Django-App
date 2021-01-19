if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', ready)
} else {
    ready()
}
function ready() {
    //Put all buttons here to ensure they are loaded and work
    var stuAdd = document.getElementsByClassName('StuAdd')
    for (let i = 0; i < stuAdd.length; i++) {
        let button = stuAdd[i];
        button.addEventListener('click',addButton) //function of the button
    }

    var stuRemove = document.getElementsByClassName('StuDelete')
    for (let i = 0; i < stuRemove.length; i++) {
        let button = stuRemove[i];
        button.addEventListener("click",remove) //function of the button
    }
    document.getElementsByClassName('StuBuy')[0].addEventListener('click',buy)

}

function buy(){
    var stuTable = document.getElementsByClassName('StuTable')[0]
    while(stuTable.hasChildNodes()){
        stuTable.removeChild(stuTable.firstChild)
    }
}

function inputChange(changes){
    let changed = changes.target;
    if (changed.value <= 0){
        changed.value = 1
    }
    totalFunction()
}


function addButton(press){
    let pressed = press.target;
    let StuItem = pressed.parentElement.parentElement;
    var StuTitleAdd = StuItem.getElementsByClassName('StuTitle')[0].innerText;
    var StuPriceAdd = StuItem.getElementsByClassName('StuPrice')[0].innerText;
    var StuStuff = {price:StuPriceAdd, title:StuTitleAdd}
    addToCart(StuStuff)
    totalFunction()
}

function addToCart(StuStuff){
    var row = document.createElement('div')
    row.classList.add('StuCart')
    let stuff = StuStuff
    var StuTable = document.getElementsByClassName('StuTable')[0]
    var StuNames = StuTable.getElementsByClassName('StuCartTitle')
    for (let i = 0; i < StuNames.length; i++) {
        if (StuNames[i].innerText === stuff.title) {
            alert('If you want to add more, change the quantity :D')
            return
        }
    }
    row.innerHTML = `<div class="cart-item cart-column">
            <span class="StuCartTitle">` + stuff.title + `</span>
        </div>
        <span class="StuCartPrice">`+ stuff.price + `</span>
        <div class="StuInputs">
            <input class="StuQuantity" type="number" value="1">
            <button class="StuDelete" type="button">Remove</button>
        </div>`
    StuTable.append(row)
    row.getElementsByClassName('StuDelete')[0].addEventListener('click', remove)
    row.getElementsByClassName('StuQuantity')[0].addEventListener('change', inputChange )

}
function totalFunction(){
    var cartTable = document.getElementsByClassName('StuTable')[0]
    var stuRow = cartTable.getElementsByClassName('CartItem')
    let total = 0
    for(let i = 0; i < stuRow.length; i++){
        var stuRows = stuRow[i]
        var tablePrice = stuRows.getElementsByClassName('StuFinalPrice')[0]
        let tableQuantity = stuRows.getElementsByClassName('StuQuantity')
        var price = parseFloat(tablePrice.innerHTML.replace('£',''))
        var quantity = tableQuantity.value
        total = total + (price * quantity)
    }
    document.getElementsByClassName('StuFinalPrice')[0].innerHTML = '£' + total
}
function remove(press){
    let pressed = press.target;
    pressed.parentElement.parentElement.remove()
    totalFunction()
}

//button testing
var testingStuff = document.getElementsByClassName('StuQuantity');
console.log(testingStuff)
for(let i = 0; i <testingStuff.length; i++) {
    let button = testingStuff[i];
    button.addEventListener('change', function () {
        console.log('DID IT WORK?')
    })
}

