function openCSVFile(CSVfileName){
// create the object
  var httpRequest = new XMLHttpRequest();
  httpRequest.onreadystatechange = function() {
    processCSVContents(httpRequest);
  }
  // Send the request
  httpRequest.open("POST", CSVfileName, true);
  httpRequest.send(null);
}

function processCSVContents(httpRequest){
  console.log("--> here");
  if (httpRequest.readyState == 4){
  // everything is good, the response is received
    if ((httpRequest.status == 200)
        || (httpRequest.status == 0)){
        // Analys the contents using the stats library
        // and display the results
          CSVContents = httpRequest.responseText;
          console.log($.csv.toObjects(CSVContents));
          console.log(" => Response status: " + httpRequest.status)
          console.log(CSVContents);
        } else {
          alert(' => There was a problem with the request. '
          + httpRequest.status + httpRequest.responseText);
        }
      }
    }

window.onload=function(){
    var queryString = location.search.substring(1);
    console.log(queryString)
    var countryCropArray = queryString.split("|");
    var country = countryCropArray[0];
    var country = country.replaceAll("_"," ");
    var crop = countryCropArray[1];
    var crop = crop.replaceAll("_"," ");

    openCSVFile("..most_recent_weather.csv")


};
