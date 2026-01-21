document.addEventListener('DOMContentLoaded', function () {
  function buildHref(target) {
    var path = window.location.pathname;
    var from = null;
    if (path.indexOf('/zh/') !== -1) {
      from = 'zh';
    } else if (path.indexOf('/en/') !== -1) {
      from = 'en';
    }

    if (!from) {
      return '/' + target + '/';
    }

    return path.replace('/' + from + '/', '/' + target + '/');
  }

  var links = document.querySelectorAll('a.lang-link[data-lang]');
  links.forEach(function (link) {
    var target = link.getAttribute('data-lang');
    link.href = buildHref(target);
    var isActive = window.location.pathname.indexOf('/' + target + '/') !== -1;
    link.classList.toggle('is-active', isActive);
    link.style.display = isActive ? 'none' : 'inline';
  });

  var placeholder = document.getElementById('lang-switcher-placeholder');
  if (placeholder) {
    var title = document.querySelector('.rst-content h1');
    if (title && title.parentNode) {
      title.parentNode.insertBefore(placeholder, title.nextSibling);
    }
  }
});
