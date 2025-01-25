window.onscroll = function() {
    var scrollPosition = window.scrollY;
    var imageContainer = document.querySelector('.image');
    var stickyTitle = document.querySelector('.sticky-title');
    var formContainer = document.querySelector('.form-container');
    if (scrollPosition > 100) {
      imageContainer.style.height = '70px';
      imageContainer.querySelector('img').style.transform = 'scale(1.2)';
      imageContainer.querySelector('img').style.opacity = '0';
      stickyTitle.style.opacity = '1';
      formContainer.style.display = 'block'; // Show the form
    } else {
      imageContainer.style.height = '100vh';
      imageContainer.querySelector('img').style.transform = 'scale(1)';
      imageContainer.querySelector('img').style.opacity = '1';
      stickyTitle.style.opacity = '0';
      formContainer.style.display = 'none';
    }
  };
  