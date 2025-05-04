const menuToggle=document.querySelector('.menu-toggle')
const navLinks=document.querySelector('.nav-links')
menuToggle.addEventListener('click',()=>{navLinks.classList.toggle('active')
menuToggle.classList.toggle('active')})
const navItems=document.querySelectorAll('.nav-links a')
navItems.forEach((item)=>{item.addEventListener('click',()=>{navLinks.classList.remove('active')
menuToggle.classList.remove('active')})});