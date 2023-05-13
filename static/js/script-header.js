const svg = document.querySelector('#id_svg');
        const info = document.querySelector('.user_info_window');

        svg.addEventListener('click', function () {
            info.classList.toggle('user_info_display');
        });