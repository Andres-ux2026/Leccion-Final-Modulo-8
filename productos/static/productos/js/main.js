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
            var items = nav.querySelectorAll('li');
            items.forEach(function(li) {
                var link = li.querySelector('a');
                var button = li.querySelector('button');
                var span = li.querySelector('span');
                if (link) {
                    var clone = document.createElement('a');
                    clone.className = 'link depth-0';
                    clone.textContent = link.textContent.trim();
                    clone.href = link.getAttribute('href');
                    navPanel.appendChild(clone);
                } else if (button) {
                    var clone = document.createElement('a');
                    clone.className = 'link depth-0';
                    clone.textContent = button.textContent.trim();
                    clone.href = '#';
                    clone.addEventListener('click', function(e) {
                        e.preventDefault();
                        var form = button.closest('form');
                        if (form) {
                            var input = document.createElement('input');
                            input.type = 'hidden';
                            input.name = 'csrfmiddlewaretoken';
                            input.value = document.querySelector('[name=csrfmiddlewaretoken]').value;
                            form.appendChild(input);
                            form.submit();
                        }
                    });
                    navPanel.appendChild(clone);
                } else if (span) {
                    var clone = document.createElement('span');
                    clone.className = 'link depth-0';
                    clone.textContent = span.textContent.trim();
                    clone.style.opacity = '0.6';
                    navPanel.appendChild(clone);
                }
            });
        }
        document.body.appendChild(navPanel);

        navButton.addEventListener('click', function(e) {
            e.preventDefault();
            doc.classList.toggle('navPanel-visible');
        });
    }
})();
