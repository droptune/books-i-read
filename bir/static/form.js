/* pageSlider operation */
const slider = document.getElementById('pageSlider');
const currentPage = document.getElementById('current-page');
const totalPages = document.getElementById('total-pages');

slider.oninput = function() { currentPage.value = this.value; }

currentPage.oninput = function() { slider.value = this.value; }

totalPages.oninput = function() { slider.max = this.value; }

/* rating colors */
const ratings = [
  document.getElementById('rating-1'),
  document.getElementById('rating-2'),
  document.getElementById('rating-3'),
  document.getElementById('rating-4'),
  document.getElementById('rating-5'),
];

const ratingLabels = [
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

// Review sizing
const review = document.getElementById("review");
review.addEventListener('input', autoResize, false);

function autoResize() {
  this.style.height = 'auto';
  this.style.height = this.scrollHeight + 'px';
}
