// add an event listener to listen for button click
// call server with new item text
// create a new list elemnt and add it to the page

const addbutton = document.querySelector('#addbutton')
addbutton.addEventListener('click', (event) => {
  console.log('button click')
  event.preventDefault();


const newItemInput= document.querySelector('#newListItem')
saveNewitem(newItemInput.value);
const newListElement = createListElement(newItemInput.value);
const lastElement = document.querySelector('#last')
lastElement.insertAdjacentElement('beforebegin', newListElement)

//clear old user input
newItemInput.value = '';
});

function saveNewitem(newItem){
  //url is of the form '/my_path'
  const url = '/todo?list_item=' + newItem;
  const options = {
    method :'POST',
    credentials: 'same-orgin',
  }
  const request = new Request(url, options);
  fetch(request);
}




function createListElement(newItem){
const htmlText =
  '<li>' +
    '<span>' + newItem +'</span>' +
  '  <span class="spacer"></span>'+
  '  <span class="delete"> ' +
    '  <img src="static/images/noun_Delete_1272081.svg">'+
    '</span>' +
  '</li>';
  const element = document.createElement('li');
  element.innerHTML = htmlText;
  return element;
}
