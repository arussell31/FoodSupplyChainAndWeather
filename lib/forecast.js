//var DOBfield = document.getElementById("uDOB");
//DOBfield.setAttribute('value', pt.birthDate);

//input country as parameter for now.
window.onload=function(){
    var queryString = location.search.substring(1);
    console.log(queryString)
    var countryCropArray = queryString.split("|");
    var country = countryCropArray[0];
    var country = country.replaceAll("_"," ");
    var crop = countryCropArray[1];
    var crop = crop.replaceAll("_"," ");
    console.log(crop)
    console.log(country)

};
