let modal = document.querySelector('#modal-notice'),
    modalActive = document.querySelector('#modal-active'),
    modalClose = document.querySelector('#modal-close');

function activeModal() {
    modal.classList.add('active');
    document.querySelector('body').style.overflow='hidden';
}

function hideModal() {
    modal.classList.remove('active');
    document.querySelector('body').style.overflow= 'visible';
}

modalActive.addEventListener('click', activeModal)
modalClose.addEventListener('click', hideModal)

// const heart = document.querySelector(".heart");
// const animationHeart = document.querySelector(".animation-heart");

// heart.addEventListener('click', () => 
// {
//     animationHeart.classList.add('animation');
//     heart.classList.add('fill-color');
// });

// animationHeart.addEventListener('click', () => 
// {
//     animationHeart.classList.remove('animation');
//     heart.classList.remove('fill-color');
// });