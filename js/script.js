const scrollTopButton = document.getElementById("scroll-top");
const firstSection = document.getElementById("aboutId");

window.addEventListener("scroll", () => {
  const firstSectionBottom = firstSection.getBoundingClientRect().top;
  
  if (firstSectionBottom < -150) {
    scrollTopButton.classList.add("show");
  } else {
    scrollTopButton.classList.remove("show");
  }
});

scrollTopButton.addEventListener("click", () => {
  document.body.scrollIntoView({
    behavior: "smooth"
  });
});

function onEntry(entry) {
    entry.forEach(change => {
        if (change.isIntersecting) {
            change.target.classList.add('element-show');
        } 
        // else {
        //         change.target.classList.remove('element-show');
        //     }
    });
}

let options = {
    threshold : [0.5] };
let observer = new IntersectionObserver (onEntry, options);
let elements = document.querySelectorAll('.element-animation');

for (let elm of elements) {
    observer.observe(elm)
}

const tracks = document.querySelectorAll('.testimonial-track');

tracks.forEach((track) => {
  track.addEventListener('mouseover', () => {
    track.style.animationPlayState = 'paused';
  });

  track.addEventListener('mouseout', () => {
    track.style.animationPlayState = 'running';
  });
});