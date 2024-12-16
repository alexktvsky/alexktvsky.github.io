const styleElement = document.createElement('style');
styleElement.innerHTML = `
  #darkOverlay {
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.9);
      z-index: 1;
  }
  .modal {
      display: none;
      position: fixed;
      z-index: 2;
      left: 50%;
      top: 50%;
      overflow: auto;
      transform: translate(-50%, -50%);
  }
  .modal-content {
      display: block;
      margin: 0 auto;
      z-index: 3;
      animation-name: zoom;
      animation-duration: 0.6s;
      max-width: 90vw;
      max-height: 90vh;
  }
  .close {
      position: fixed;
      top: -10px;
      right: 0;
      color: #f1f1f1;
      font-size: 40px;
      font-weight: bold;
      transform: 0.3s;
      z-index: 4;
      opacity: 0;
      animation: fadeIn 0.4s 0.4s forwards;
  }
  @keyframes fadeIn {
      to {opacity: 1;}
  }
  .close:hover, .close:focus {
    color: #bbb;
    text-decoration: none;
    cursor: pointer;
  }
  .modal-content {
    -webkit-animation-name: zoom;
    -webkit-animation-duration: 0.6s;
    animation-name: zoom;
    animation-duration: 0.6s;
  }
  @-webkit-keyframes zoom {
    from { webkit-transform: scale(0) }
    to { webkit-transform: scale(1) }
  }
  @keyframes zoom {
    from { transform: scale(0) }
    to { transform: scale(1) }
  }
  @media only screen and (max-width: 940px) {
    .modal-content {
      width: 90%;
      max-height: 90vh;
      max-width: 90vw;
    }
  }
  @media only screen and (max-width: 700px) {
    .modal-content {
      width: auto;
      height: auto;
      max-height: 100vh;
      max-width: 95vw;
    }
    .modal {
      left: 50%;
      top: 50%;
      transform: translate(-50%, -50%);
    }
  }
  @media only screen and (max-width: 700px) and (orientation: landscape) and (min-aspect-ratio: 16/9) {
    .modal-content {
      max-width: 100vw;
      max-height: 100vh;
      width: auto;
      height: auto;
    }
  }
  @media only screen and (max-width: 940px) and (orientation: landscape) {
    .close {
      top: -10px;
      right: 20px;
    }
  }
`;

document.head.appendChild(styleElement);

const images = document.querySelectorAll('.myImg');
const modal = document.querySelector('.modal');
const modalContent = document.getElementById('modalImage');
const darkOverlay = document.getElementById('darkOverlay');
const closeModalBtn = document.getElementById('closeModalBtn');

images.forEach((img) => {
    img.addEventListener('click', () => {
        modal.style.display = 'block';
        modalContent.src = img.src;
        darkOverlay.style.display = 'block';
    });
});

closeModalBtn.addEventListener('click', () => {
    modal.style.display = 'none';
    darkOverlay.style.display = 'none';
});

darkOverlay.addEventListener('click', () => {
    modal.style.display = 'none';
    darkOverlay.style.display = 'none';
});

window.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
        modal.style.display = 'none';
        darkOverlay.style.display = 'none';
    }
});
