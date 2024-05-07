const BASE_URL = "http://localhost:5000/api";

//select the cupcake list element
const $cupcakeList = document.querySelector("#cupcake-list");
const $submitForm = document.querySelector('#new-cupcake-form');


async function handleAddCupcake(evt) {

  const flavor = document.querySelector("#cupcake-flavor").value;
  const size = document.querySelector("#cupcake-size").value;
  const rating = document.querySelector("#cupcake-rating").value;
  const url = document.querySelector("#cupcake-url").value;

  const requestBody = {
    "flavor": flavor,
    "size": size,
    "rating": rating,
    "image_url": url
  };

  await fetch(
    '/api/cupcakes',
    {
      method: "POST",
      body: JSON.stringify(requestBody),
      headers: {
        "Content-Type": "application/json"
      }
    }
  );

  putCupcakesOnPage();

}

$submitForm.addEventListener("submit", (evt) => {
  evt.preventDefault();
  handleAddCupcake();
});

function generateCupcakeMarkup(cupcake) {
  const $li = document.createElement("li");
  const $img = document.createElement("img");
  $img.style = "width:40px";
  $img.src = cupcake.image_url;

  $li.innerText =
    `${cupcake.flavor} | ${cupcake.size} | rating: ${cupcake.rating}`;
  $li.appendChild($img);

  return $li;
}

export async function getCupcakes() {
  console.log("in get cupcakes!");
  const response = await fetch(`${BASE_URL}/cupcakes`);
  const cupcakeData = await response.json();
  return cupcakeData.cupcakes;
}

export async function putCupcakesOnPage() {
  $cupcakeList.innerHTML = "";
  const cupcakes = await getCupcakes();
  for (const cupcake of cupcakes) {
    const listItem = generateCupcakeMarkup(cupcake);
    $cupcakeList.appendChild(listItem);
  }
}

export async function start() {
  console.debug("start");

  await putCupcakesOnPage();

}
