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
        button.addEventListener('click',remove) //function of the button
    }
}

function addButton(press){
    let pressed = press.target;
    let StuItem = pressed.parentElement.parentElement;
    var StuTitleAdd = StuItem.getElementsByClassName('StuTitle')[0].innerText;
    var StuPriceAdd = StuItem.getElementsByClassName('StuPrice')[0].innerText;
    var StuStuff = {price:StuPriceAdd, title:StuTitleAdd}
    addToCart(StuStuff)
    console.log(StuStuff)
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
   // row.getElementsByClassName('StuQuantity')[0].addEventListener('change', (add function here) )

}
function remove(press){
    let pressed = press.target;
    pressed.parentElement.parentElement.remove()
}


//button testing
var testingStuff = document.getElementsByClassName('StuAdd');
console.log(testingStuff)
for(let i = 0; i <testingStuff.length; i++) {
    let button = testingStuff[i];
    button.addEventListener('click', function () {
        console.log('DID IT WORK?')
    })
}

