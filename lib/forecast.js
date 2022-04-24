function recalculate(country,crop){
  var queryString = location.search.substring(1);
  var countryCropArray = queryString.split("|");
  var country = countryCropArray[0];
  var country = country.replaceAll("_"," ");
  var crop = countryCropArray[1];
  var crop = crop.replaceAll("_"," ");
  console.log(country);
  console.log(crop);
  var filename = country + '_' + crop + '.csv'
  var filepath = "../models/final_models/" + filename
  console.log(filename);
  console.log(filepath);
  $.ajax({
      type: "GET",
      url: filepath,
      dataType: "text",
      success: function(data) {
        console.log(data);
        var lines = data.split("\n");
        var header = lines[0];
        var header = header.split(",");
        var coefficients = lines[1];
        var coefficients = coefficients.split(",");
        console.log("header:")
        console.log(header)
        console.log("coefficients")
        console.log(coefficients)
        formulaDict = {}
        var twoArrays = [header,coefficients];
        twoArrays[0].forEach(function(cell,i){
          formulaDict[cell] = parseFloat(twoArrays[1][i])
        })
        console.log(formulaDict)
      }
    });
}
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
          var includeOnly = ['max','avg','min','pre']
          var checkboxes = ['flood','droug','disas']
          for (const [key, value] of Object.entries(weatherDict)) {
            var id = String(key);
            if (id == "Agricultural Land Mass"){
              var field = document.getElementById("ag_land");
              field.setAttribute('value',parseFloat(value.trim()).toFixed(2))
            }
            idBeginning = id.substring(0, 3);
            if (includeOnly.includes(idBeginning) == true){
              var field = document.getElementById(id);
              field.setAttribute('value', parseFloat(value.trim()));
            }
            idFive = id.substring(0, 5);
            if (checkboxes.includes(idFive) == true){
              var valueInt = parseInt(value.trim())
              console.log("valueInt")
              console.log(valueInt)
              if (valueInt==1){
                document.getElementById(id).checked = true;
              }
              if (valueInt==0){
                document.getElementById(id).checked = false;
              }
            }
          }
        }
     });
};
