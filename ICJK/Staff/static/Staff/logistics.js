let startingDropdown,endingDropdown,filterToggle;

let startLocation = "Anywhere";
let endLocation = "Anywhere";
let useFilter = false;

let loadingBox, resultContainer;

$(document).ready(()=>{
    $('.dropdown-trigger').dropdown();
    startingDropdown = document.getElementById("starting-dropdown");
    startingDropdown.innerHTML = startLocation;
    endingDropdown = document.getElementById("ending-dropdown");
    endingDropdown.innerHTML = endLocation;
    filterToggle = document.getElementById("filterToggle");
    filterToggle.checked = useFilter;

    loadingBox = document.getElementById("loading-box");
    resultContainer = document.getElementById("result-container");
    updateGraph();
})

function setStart(location){
    startLocation = location;
    startingDropdown.innerHTML = startLocation;
    if(!(endLocation == "Anywhere" || startLocation == "Anywhere")){
        toggleToggle(false);
    }else{
        toggleToggle(true);
    }
    updateGraph();
}

function setEnd(location){
    endLocation = location;
    endingDropdown.innerHTML = endLocation;
    if(!(endLocation == "Anywhere" || startLocation == "Anywhere")){
        toggleToggle(false);
    }else{
        toggleToggle(true);
    }
    updateGraph();
}

function toggleFilter(){
    let state = filterToggle.checked;
    useFilter = state;
    updateGraph();
}

function toggleToggle(enabled){
    filterToggle.disabled = !enabled;
    if(!enabled){
        filterToggle.checked = false;
    }else{
        filterToggle.checked = useFilter;
    }
}

function addResult(order){
    let resultHTML = `<div class='card'>
        <div class="card-content black-text">
            <span class="card-title">${order.purchaser}</span>
            <table>
                <tr><td>Customer Address</td><td>${order.address}</td></tr>
                <tr><td>Pickup Location</td><td>${order.begin}</td></tr>
                <tr><td>Pickup Date</td><td>${order.begindate}</td></tr>
                <tr><td>Dropoff Location</td><td>${order.end}</td></tr>
                <tr><td>Dropoff Date</td><td>${order.enddate}</td></tr>
                <tr><td>Car Rented</td><td><a href="${order.carlink}">${order.car}</a></td></tr>
            </table>
            </div>
        </div>
    </div>`;
    resultContainer.innerHTML += resultHTML;
}

function clearResults(){
    resultContainer.innerHTML = "";
}

function setLoading(enabled){
    loadingBox.style.display = enabled ? "block" : "none";
}
