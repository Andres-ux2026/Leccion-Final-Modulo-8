(function() {
    var win = window;
    var doc = document.documentElement;

    doc.classList.remove('is-preload');

    if (win.innerWidth <= 736) {
        var navButton = document.createElement('div');
        navButton.id = 'navButton';
        navButton.innerHTML = '<a href="#navPanel" class="toggle"></a>';
        document.body.appendChild(navButton);

        var navPanel = document.createElement('div');
        navPanel.id = 'navPanel';
        var nav = document.getElementById('nav');
        if (nav) {
            var links = nav.querySelectorAll('a, button, span');
            links.forEach(function(link) {
                var clone = document.createElement('a');
                clone.className = 'link depth-0';
                clone.textContent = link.textContent.trim();
                if (link.tagName === 'A' && link.getAttribute('href')) {
                    clone.href = link.getAttribute('href');
                } else if (link.tagName === 'BUTTON') {
                    clone.href = '#';
                } else if (link.tagName === 'FORM') {
                    return;
                }
                navPanel.appendChild(clone);
            });
        }
        document.body.appendChild(navPanel);

        navButton.addEventListener('click', function(e) {
            e.preventDefault();
            doc.classList.toggle('navPanel-visible');
        });
    }
})();
