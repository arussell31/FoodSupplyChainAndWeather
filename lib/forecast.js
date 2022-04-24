function recalculate(country,crop){
  var queryString = location.search.substring(1);
  var countryCropArray = queryString.split("|");
  var country = countryCropArray[0];
  var country = country.replaceAll("_"," ");
  var crop = countryCropArray[1];
  var crop = crop.replaceAll("_"," ");
  var filename = country + '_' + crop + '.csv'
  var filepath = "../models/final_models/" + filename
  console.log(filepath);
  $.ajax({
      type: "GET",
      url: filepath,
      dataType: "text",
      success: function(data) {
        var lines = data.split("\n");
        var header = lines[0];
        var header = header.split(",");
        var coefficients = lines[1];
        var coefficients = coefficients.split(",");
        var checkboxes = ['flood','droug','disas']

        formulaDict = {}
        var twoArrays = [header,coefficients];
        twoArrays[0].forEach(function(cell,i){
          var cell = cell.replace("Agricultural Land Mass", "ag_land");
          var cell = cell.replace("\r","");
          formulaDict[cell] = parseFloat(twoArrays[1][i])
        })
        console.log(formulaDict)
        var projection = formulaDict['intercept']
        console.log('projection = intercept')
        console.log(projection)
        for (const [key, value] of Object.entries(formulaDict)) {
          if(key!=""){
            if(key!='intercept'){
              var keyList = key.split(" ");
              console.log(keyList)
              if(keyList.length == 1){
                var last2 = keyList[0].slice(-2);
                console.log(last2)
                if(last2=="^2"){
                  var uInput = document.getElementById(keyList[0].slice(0,-2)).value
                  var addMe = (uInput**2)*value
                  console.log('add me')
                  console.log(addMe)
                  var projection = projection + addMe
                }
                if(last2!="^2"){
                  firstFive = keyList[0].substring(0, 5);
                  if (checkboxes.includes(firstFive) == true){
                    var uInput = document.getElementById(keyList[0])
                    var checked = uInput.checked;
                    console.log('CHECKBOX VAL')
                    console.log(keyList[0])
                    console.log(checked)
                    if (checked == true){
                      val = 1
                    }
                    if(checked == false){
                      val = 0
                    }
                    var addMe = (val)*value
                    console.log('add me')
                    console.log(addMe)
                    var projection = projection + addMe
                  }
                  if (checkboxes.includes(firstFive) == false){
                    var uInput = document.getElementById(keyList[0]).value
                    var addMe = (uInput)*value
                    console.log('add me')
                    console.log(addMe)
                    var projection = projection + addMe
                  }
                }
              }
              if(keyList.length == 2){
                firstFive1 = keyList[0].substring(0, 5);
                firstFive2 = keyList[1].substring(0, 5);
                var uInput1 = document.getElementById(keyList[0]).value
                var uInput2 = document.getElementById(keyList[1]).value

                if (checkboxes.includes(firstFive1) == true){
                  var uInput1 = document.getElementById(keyList[0])
                  var checked = uInput1.checked;
                  console.log('CHECKBOX VAL')
                  console.log(keyList[0])
                  console.log(checked)
                  if (checked == true){
                    var uInput1 = 1
                  }
                  if(checked == false){
                    var uInput1 = 0
                  }
                }

                if (checkboxes.includes(firstFive2) == true){
                  var uInput2 = document.getElementById(keyList[1])
                  var checked = uInput2.checked;
                  console.log('CHECKBOX VAL')
                  console.log(keyList[1])
                  console.log(checked)
                  if (checked == true){
                    var uInput2 = 1
                  }
                  if(checked == false){
                    var uInput2 = 0
                  }
                }
                var addMe = uInput1*uInput2*value
                console.log('add me')
                console.log(addMe)
                var projection = projection + addMe
              }
            }
          }
          console.log('new projection')
          console.log(projection)
        }
        document.getElementById("projection").innerHTML = "Projecting <span style='color:black;'>" + projection.toLocaleString("en-US") + "</span> tons of " + crop + " will be produced in " + country +" in 2022."
        if(projection<0){
          document.getElementById('resultsExplanation').innerHTML ='This model is currently projecting a negative crop yield, which is inaccurate. The models are based only on the data shown on this page, and could be improved by exploring the impacts of other independent variables on crop yield.';
        }
        if(projection>0){
          document.getElementById('resultsExplanation').innerHTML = ''
        }
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
