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
        button.addEventListener('click',addToQuantity) //function of the button
    }
    var stuRemove = document.getElementsByClassName('StuDelete')
    for (let i = 0; i < stuRemove.length; i++) {
        let button = stuRemove[i];
        button.addEventListener('click',remove) //function of the button
    }
}

function addToQuantity(){

}
function remove(){

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

