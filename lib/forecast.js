$(document).ready(function() {
    // $.ajax({
    //     type: "GET",
    //     url: "..most_recent_weather.csv",
    //     dataType: "text",
    //     success: function(data) {console.log(data);}
    //  });
    $.get('../most_recent_weather.csv', function(data) {
      console.log(data)
    }, 'csv');
});

window.onload=function(){
    var queryString = location.search.substring(1);
    console.log(queryString)
    var countryCropArray = queryString.split("|");
    var country = countryCropArray[0];
    var country = country.replaceAll("_"," ");
    var crop = countryCropArray[1];
    var crop = crop.replaceAll("_"," ");


};
