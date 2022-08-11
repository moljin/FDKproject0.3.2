document.addEventListener('DOMContentLoaded',  function () {
    const hamburger = document.querySelector('.hamburger');
    const accordion_panel = document.querySelectorAll('.accordion .tab-panel');
    document.addEventListener('click', function (e) {
        if (e.target.classList.contains('tab')) {
            let pairedPanel = e.target.nextElementSibling;
            pairedPanel.slideToggle(500);
            accordion_panel.forEach(function (el) {
                if (el.style.display !== "none" && el !== pairedPanel) {
                    el.slideUp(200);
                }
            });
        } else {
            accordion_panel.forEach(function (el) {
                if (el.style.display !== "none") {
                    el.slideUp(300);
                }
            });
        }
    });

    hamburger.addEventListener('click', function (e) {
        e.preventDefault();
        hamburger.classList.toggle('is-active');
        document.querySelector('.site-navigation').slideToggle(300);
    });


});