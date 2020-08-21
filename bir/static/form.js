/* pageSlider operation */
const slider = document.getElementById('pageSlider');
const currentPage = document.getElementById('current-page');
const totalPages = document.getElementById('total-pages');

slider.oninput = function() { currentPage.value = this.value; }

currentPage.oninput = function() { slider.value = this.value; }

totalPages.oninput = function() { slider.max = this.value; }

/* rating colors */
ratings = [
  document.getElementById('rating-1'),
  document.getElementById('rating-2'),
  document.getElementById('rating-3'),
  document.getElementById('rating-4'),
  document.getElementById('rating-5'),
];

ratingLabels = [
  document.getElementById('rating-label-1'),
  document.getElementById('rating-label-2'),
  document.getElementById('rating-label-3'),
  document.getElementById('rating-label-4'),
  document.getElementById('rating-label-5'),
];

ratings.forEach((radioButton) => {
  radioButton.addEventListener("change", (e) => {
    const selectedIndex = radioButton.value;
    ratingLabels.forEach((ratingLabel, radioIndex) => {
      if (radioIndex < selectedIndex) {
        ratingLabel.classList.add("rating-selected");
        ratingLabel.classList.remove("rating-label");
      } else {
        ratingLabel.classList.add("rating-label");
        ratingLabel.classList.remove("rating-selected");
      }
    });
  });
});


/* publishers autocomplete */
autocomplete = (input, dataArray) => {
  let currentElement = 0;

  input.addEventListener("input", (e) => {
    let inputData = input.value;

    // remove all previous items
    removeAutocomplete();

    dataArray.forEach((element) => {
      if (element.toLowerCase().includes(inputData.toLowerCase())){
        let listItem = document.createElement("div");
        listItem.setAttribute("class", "autocomplete-item");
        listItem.innerHTML = element;
        input.parentNode.appendChild(listItem);
        listItem.addEventListener("click", (e) => {
          input.value = listItem.innerHTML;
          removeAutocomplete();
        });
      }
    });

    input.addEventListener("keydown", (e) => {
      switch (e.keyCode) {
        case 40:
          currentElement++;
          setSelectedItem();
          break;
        case 38:
          currentElement--;
          setSelectedItem();
          break;
        case 12:
          e.preventDefault();

      }
    });

    setSelectedItem = () => {
      let autocompleteElements = document.getElementsByClassName("autocomplete-item");

      for (let i = 0; i < autocompleteElements.length; i++) {
        autocompleteElements[i].classList.remove("autocomplete-selected");
      }

      if (currentElement < 0) currentElement = autocompleteElements.length - 1;
      if (currentElement > autocompleteElements.length - 1) currentElement = 0;

      console.log(currentElement);

      autocompleteElements[currentElement].classList.add("autocomplete-selected");
    }

  });


  removeAutocomplete = () => {
    let autocompleteElements = document.getElementsByClassName("autocomplete-item");
    for (let i = 0; i < autocompleteElements.length; i++) {
      autocompleteElements[i].remove();
    }
  }

};

const publisherInput = document.getElementById("publisher-select");
autocomplete(publisherInput, publishers);
