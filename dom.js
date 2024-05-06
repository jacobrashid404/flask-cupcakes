const BASE_URL = "http://localhost:5000/api";

//select the cupcake list element
//const $cupcakeList = document.querySelector("#cupcake-list");

function generateCupcakeMarkup(cupcake){
  return `<li>${cupcake.flavor} | ${cupcake.size} | ${cupcake.rating}</li>`
}

async function getCupcakes(){
  const response = await fetch(`${BASE_URL}/cupcakes`);
  const cupcakeData = await response.json();
  return cupcakeData;
}

function putCupcakesOnPage(){
  cupcakes = getCupcakes()
  for(const cupcake of cupcakes){
    generateCupcakeMarkup(cupcake);
  }
}