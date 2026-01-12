let sections = document.querySelectorAll('section');
let navLinks = document.querySelectorAll('header nav a');

let menuIcon = document.querySelector('#menu-icon');
let navbar = document.querySelector('.navbar');

menuIcon.onclick = () => {
    menuIcon.classList.toggle('bx-x');
    navbar.classList.toggle('active');
}

navLinks.forEach(link => {
    link.addEventListener('click', () => {
        menuIcon.classList.remove('bx-x');
        navbar.classList.remove('active');
    });
});

window.addEventListener('scroll', () => {
    let top = window.scrollY;

    navLinks.forEach(link => link.classList.remove('active'));

    sections.forEach(sec => {
        let offset = sec.offsetTop - 150;
        let height = sec.offsetHeight;
        let id = sec.id;

        if (top >= offset && top < offset + height) {

            const activeLink = document.querySelector(
                `header nav a[href="#${id}"]`
            );

            if (activeLink) {
                activeLink.classList.add('active');
            }
        }
    });
});

function hireMe(){
    const recipient = "dhirajdhunganaofficial@gmail.com";
    const subject = "I am Interested in Hiring You";
    const body = "Hello Dhiraj,\n\nI’m contacting you to explore a possible collaboration.\n\nI’m interested in hiring you for a project or a job and discussing how your skills could help achieve our goals.\n\nContact Email / Number: __________\nProject / Job Detail: __________\n\nI am looking forward to connect with you.\n\nKind Regards,\n__________\n__________\n__________";

    window.location.href = `mailto:${recipient}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
}
