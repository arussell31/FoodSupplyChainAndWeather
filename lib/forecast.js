// $(document).ready(function() {

    // $.get('../most_recent_weather.csv', function(data) {
    //   console.log(data)
    // }, 'csv');
// });

window.onload=function(){
    var queryString = location.search.substring(1);
    console.log(queryString)
    var countryCropArray = queryString.split("|");
    var country = countryCropArray[0];
    var country = country.replaceAll("_"," ");
    var crop = countryCropArray[1];
    var crop = crop.replaceAll("_"," ");

    $.ajax({
        type: "GET",
        url: "../most_recent_weather.csv",
        dataType: "text",
        success: function(data) {
          var lines = data.split("\n");
          var weatherDict = {}
          var doubleArray = []
          lines.forEach(function(line){
            var lineList = line.split(",");
            var lineCountry = lineList[1];

            if (lineCountry == 'Country'){
              var header = lineList.slice(1)
              console.log("header")
              console.log(header)
              doubleArray.push(header)
              console.log('weatherDict')
              console.log(weatherDict)
            }
            if (lineCountry == country){
              var countryWeather = lineList.slice(1)
              doubleArray.push(countryWeather)
              console.log('weatherDict with data')
              console.log(weatherDict)
            }

          })
          console.log('doubleArray')
          console.log(doubleArray)
          doubleArray[0].forEach(function(cell,i){
            weatherDict[cell] = doubleArray[1][i]
          })
          console.log(weatherDict)
        }
     });

};
