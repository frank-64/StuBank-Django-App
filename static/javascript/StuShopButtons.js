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
        button.addEventListener("click", remove) //function of the button
    }
    document.getElementsByClassName('StuBuy')[0].addEventListener('click',buy)

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

function inputChange(changes){
    let changed = changes.target;
    if (changed.value <= 0){
        changed.value = 1
    }
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
    row.innerHTML = `<div class="StuCartItems">
            <span class="StuCartTitle">` + stuff.title + `</span>
        <span class="StuCartPrice">`+ stuff.price + `</span>
        <div class="StuInputs">
            <input class="StuQuantity" type="number" value="1">
            <button class="StuDelete" type="button">Remove</button>
        </div>
        </div>`
    StuTable.append(row)
    row.getElementsByClassName('StuDelete')[0].addEventListener('click', remove)
    row.getElementsByClassName('StuQuantity')[0].addEventListener('change', inputChange)

}




function totalFunction() {

  var stuCartTable =  document.getElementsByClassName('StuTable')[0]
    var stuRows = stuCartTable.getElementsByClassName('StuCartItems')
    var total = 0
    for (var i = 0; i < stuRows.length; i++){
        var stuRow = stuRows[i]
        var stuCartPrice = stuRow.getElementsByClassName('StuCartPrice')[0]
        var stuCartQuantity = stuRow.getElementsByClassName('StuQuantity')[0]
        var price = stuCartPrice.innerHTML.replace('£','')
        var quantity = stuCartQuantity.value
        total = total + (price * quantity)
    }
     total = Math.round(total * 100) / 100
    document.getElementsByClassName('StuFinalPrice')[0].innerText = total
    var balance = document.getElementById('new_balance')
    var finalBalance = balance - total
    alert(balance)
    balance.innerText = finalBalance




}

function remove(press){
    let pressed = press.target;
    pressed.parentElement.parentElement.remove()
    totalFunction()
}

function buy(){
    var stuTable = document.getElementsByClassName('StuTable')[0]
    spoofTransaction()
    while(stuTable.hasChildNodes()){
        stuTable.removeChild(stuTable.firstChild)
    }
    totalFunction()
}

function spoofTransaction(){
        var transactionTotal = document.getElementsByClassName('StuFinalPrice')[0].innerText.replace('£','');
        //var category =
        var comment='test'
        var termini = "StuShop"; //should be stushop
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                if(xhttp.response === 'Complete'){
                    //what to do if successful
                     alert("Successful")
                }else{
                    alert("Unsuccessful")
                    //what to when when unsuccessful
                }
            }
        };
        var json_transaction = {
            'amount':transactionTotal,
            //'category':category,
            'comment':comment,
            'termini':termini
        }
        xhttp.open("POST", '/StuShop/transaction/');
        xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhttp.send(JSON.stringify(json_transaction));
    }

$(document).ready(function(){
          $("StuTotal").change(function(){
              let amount = this.value;
              let sum = available_balance-amount;
              if (sum<0){
                  alert("You do not have £"+amount+" in your bank account.")
                  document.getElementById('submit').disabled = true;
                  document.getElementById("new_balance").innerText = "£"+(sum);
                  document.getElementById("new_balance").style.color='red';
                  valid = false;
              }else if (amount<0){
                  alert("You cannot transfer a negative amount!")
                  document.getElementById('submit').disabled = true;
                  document.getElementById("new_balance").innerText = "£"+available_balance+".00";
                  valid = false;
              }else if (amount<1.00){
                  alert("You must transfer an amount more than or equal to £1.00.")
                  document.getElementById('submit').disabled = true;
                  document.getElementById("new_balance").innerText = "£"+available_balance+".00";
                  valid = false;
              } else {
                  document.getElementById('submit').disabled = false;
                  document.getElementById("new_balance").style.color='black';
                  document.getElementById("new_balance").innerText = "£"+(sum);
                  valid = true;
              }
          });
        });



