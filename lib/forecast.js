//var DOBfield = document.getElementById("uDOB");
//DOBfield.setAttribute('value', pt.birthDate);

//input country as parameter for now.
var jQueryScript = document.createElement('script');
jQueryScript.setAttribute('src','https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js');
document.head.appendChild(jQueryScript);

window.onload=function(){
    var queryString = location.search.substring(1);
    console.log(queryString)
    var countryCropArray = queryString.split("|");
    var country = countryCropArray[0];
    var country = country.replaceAll("_"," ");
    var crop = countryCropArray[1];
    var crop = crop.replaceAll("_"," ");

    var data = $.csv.toObjects("..most_recent_weather.csv")
    console.log(data)

};
