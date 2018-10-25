$(document).ready(function() {
  $('select').formSelect();
});

// let selections = {{makes_models_years_set|safe}};

let makeSelection = document.getElementById('make');
let modelSelection = document.getElementById('model');
let yearSelection = document.getElementById('year');
let filterToggle = document.getElementById('filter-toggle');
let filters = document.getElementById('filters');

document.addEventListener('DOMContentLoaded', ()=>{

  for(let make of Object.keys(selections)){
    makeSelection.innerHTML +=  "<option value ='" + make + "'>" + make + "</option>";
  }
  M.FormSelect.init(makeSelection, null);
  M.FormSelect.init(modelSelection, null);
  M.FormSelect.init(yearSelection, null);
}, false);

function populateModels(makeName){
  for(let model of Object.keys(selections[makeName])){
    modelSelection.innerHTML +=  "<option value ='" + model + "'>" + model + "</option>";
  }
  M.FormSelect.init(modelSelection, null);
}

function populateYears(makeName, modelName){
  for(let year of selections[makeName][modelName]){
    yearSelection.innerHTML +=  "<option value ='" + year + "'>" + year + "</option>";
  }
  M.FormSelect.init(yearSelection, null);
}

function clearModels(){
  modelSelection.innerHTML = '<option value = "" disabled selected>Select model</option>'
  modelSelection.selectedIndex = 0;
  M.FormSelect.init(modelSelection, null);
}

function clearYears(){
  yearSelection.innerHTML = '<option value = "" disabled selected>Select year</option>'
  yearSelection.selectedIndex = 0;
  M.FormSelect.init(yearSelection, null);
}

function onMakeChanged(){
  clearModels();
  clearYears();
  populateModels(makeSelection.options[makeSelection.selectedIndex].value);
}

function onModelChanged(){
  clearYears();
  populateYears(makeSelection.options[makeSelection.selectedIndex].value, modelSelection.options[modelSelection.selectedIndex].value);
}

function onFilterToggle(){
  let current_state = filters.style.display == 'block';
  filterToggle.children[0].innerHTML = current_state ? "arrow_drop_down" : "arrow_drop_up";
  filters.style.display = current_state ? "none" : "block";
}

makeSelection.addEventListener('change', () => onMakeChanged());
modelSelection.addEventListener('change', () => onModelChanged());
filterToggle.addEventListener('click', () => onFilterToggle());

$('.sidenav').sidenav();