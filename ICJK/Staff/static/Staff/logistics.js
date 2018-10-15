let startingDropdown,endingDropdown,filterToggle;

let startLocation = "Anywhere";
let endLocation = "Anywhere";
let useFilter = false;

$(document).ready(()=>{
    $('.dropdown-trigger').dropdown();
    startingDropdown = document.getElementById("starting-dropdown");
    startingDropdown.innerHTML = startLocation;
    endingDropdown = document.getElementById("ending-dropdown");
    endingDropdown.innerHTML = endLocation;
    filterToggle = document.getElementById("filterToggle");
    filterToggle.checked = useFilter;
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
}

function toggleToggle(enabled){
    filterToggle.disabled = !enabled;
    if(!enabled){
        filterToggle.checked = false;
    }else{
        filterToggle.checked = useFilter;
    }
}

function updateGraph(){
    //Todo:
    // Send request to server with start and end locations, and whether to filter start and ending locations
    // Server sends top 100 results
    // Display on frontend
    // ...
    // Profit?
}