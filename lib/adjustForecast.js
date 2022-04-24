//var DOBfield = document.getElementById("uDOB");
//DOBfield.setAttribute('value', pt.birthDate);

//input country as parameter for now.

//for file in output.zip:
  //filenameList = filename.split('-')
  //if filenameList[0] == input parameter country:
    //read file
    //save header row and row where year = 2018

function populateBoxes(country){
  const fs = require('fs')
  const dir = '../output.zip'
  const files = fs.readdirSync(dir)

  for (const file of files) {
    console.log(file)
  }
};

function recalculate(){
}

window.onload=function(){
  document.getElementById('recalculateButton').addEventListener('click', recalculate);
  populateBoxes('France')
};
