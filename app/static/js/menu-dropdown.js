document.addEventListener('DOMContentLoaded', () => {
    const dropdownToggle = document.querySelector('.panel-nav-dropdown-toggle');
    const dropdownMenu = document.querySelector('.panel-nav-dropdown');

    dropdownToggle.addEventListener('mouseenter', () => {
        dropdownMenu.classList.add('open');
    });

    dropdownToggle.addEventListener('mouseleave', () => {
        if (!dropdownMenu.matches(':hover')) {
            dropdownMenu.classList.remove('open');
        }
    });

    dropdownMenu.addEventListener('mouseleave', () => {
        dropdownMenu.classList.remove('open');
    });

    dropdownMenu.addEventListener('mouseenter', () => {
        dropdownMenu.classList.add('open');
    });
});
