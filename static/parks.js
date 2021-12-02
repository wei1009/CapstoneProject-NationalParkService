

const $parkSearchField = $(".parkSearchField");
const $searchParkList = $(".searchParkList");
const $searchParkDiv = $(".searchParkDiv");
const $searchBarSubmit = $(".searchBarSubmit");

// This is the global list of all state parks
const parkList = {};
let allStates;
let is_blur = true;

async function loadAllStateParks() {

  const response = await axios({
    url:　 "/getparks",
    method: "GET",
  });

  parkList.stateParks = response.data.data;

  let tempStateSet = new Set();

  for (let park of parkList.stateParks){
    let temArray = park.states.split(',')

    temArray.forEach(e => tempStateSet.add(e));
  }

  allStates = Array.from(tempStateSet).sort();

  dropdownStateslist();
  dropdownParkslist();
  $(".searchParkDropdownItem[type=state]").hide();
}

function dropdownStateslist() {
  $searchParkList.empty();
  for (let state of allStates) {
    let $item = $(
      `
      <li class="searchParkDropdownItem border-bottom" type='state' stateCode=${state}>
      <a href="/parks/state/${state}" class="dropDownpParkList">
        <div>
          <span class="searchParkDropdownState">${state}</span>
          <div>
            <small>
              United States of America
            </small>
          </div>
        </div>
        </a>
       </li>
    `
    );

    $searchParkList.append($item);
  }
}

function dropdownParkslist() {
  for (let park of parkList.stateParks) {
    let $item = $(
      `
      <li class="searchParkDropdownItem border-bottom" type='park' parkId=${park.id}>
      <a href="/parkinfo/${park.parkCode}" class="dropDownpParkList">
        <div>
          <span class="searchParkDropdownPark">${park.fullName}</span>
          <div>
            <small>
              ${park.addresses[0].city}, ${park.states}
            </small>
          </div>
        </div>
        </a>
       </li>
    `
    );
    $searchParkList.append($item);
  }
}

async function start() {
  await loadAllStateParks();
}

function searchFieldChange(e) {
  let searchTxt = "";
  searchTxt = e.target.value.trim().toLowerCase();

  if (searchTxt == ""){
    //Only display parks in the search dropdown
    $(".searchParkDropdownItem[type=state]").hide();
    $(".searchParkDropdownItem[type=park]").show();
  }
  else if (searchTxt !== "") {
    //Hide all search dropdown items
    $(".searchParkDropdownItem ").hide();

    //Display states if match
    let searchWords = [];
    searchWords = searchTxt.split(" ");

    //Display states if match
    for (let state of allStates) {
      let isMatch = searchWords.every(function (e) {
        let findSate = state.toLowerCase().indexOf(e);

        return (
          findSate >= 0
        );
      });
      if (isMatch) {
        $(".searchParkDropdownItem[type=state][stateCode=" + state + "]").show();
      }
    }

    //Display parks if match
    for (let park of parkList.stateParks) {
      let isMatch = searchWords.every(function (e) {
        let fullName = park.fullName.toLowerCase().indexOf(e);
        let states = park.states.toLowerCase().indexOf(e);
        let city = park.addresses[0].city.toLowerCase().indexOf(e);
        return (
          fullName >= 0 ||
          states >= 0 ||
          city >= 0
        );
      });
      if (isMatch) {
        $(".searchParkDropdownItem[type=park][parkId=" + park.id + "]").show();
      }
    }
  }
}

$searchBarSubmit.on("click", function (e) {
  e.preventDefault();
  let showlists = [];
  for (let i = 0; i < $searchParkList.children().length; i++) {
    if ($searchParkList.children()[i].style.display !== "none") {
      showlists.push($searchParkList.children()[i]);
    }
  }
  window.location = showlists[0].firstElementChild.getAttribute("href");
});

start();
$searchParkDiv.hide();

$parkSearchField.keyup(searchFieldChange);

$parkSearchField.focus(function (e) {
  $searchParkDiv.show();
});

$parkSearchField.focusout(function (e) {
  setTimeout(function () {
    $searchParkDiv.hide();
  }, 250);
});
