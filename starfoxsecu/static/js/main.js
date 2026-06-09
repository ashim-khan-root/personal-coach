document.addEventListener('DOMContentLoaded', function() {

  // === Mobile Menu ===
  var toggle = document.querySelector('.mobile-toggle');
  var nav = document.querySelector('.nav-main');
  var overlay = document.querySelector('.nav-overlay');

  function toggleMenu(open) {
    nav.classList.toggle('open', open);
    toggle.classList.toggle('open', open);
    if (overlay) overlay.classList.toggle('open', open);
    document.body.style.overflow = open ? 'hidden' : '';
  }

  if (toggle) {
    toggle.addEventListener('click', function() {
      toggleMenu(!nav.classList.contains('open'));
    });
  }

  if (overlay) {
    overlay.addEventListener('click', function() {
      toggleMenu(false);
    });
  }

  document.querySelectorAll('.nav-main a').forEach(function(link) {
    link.addEventListener('click', function() {
      toggleMenu(false);
    });
  });

  // Close menu on escape key
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && nav.classList.contains('open')) {
      toggleMenu(false);
    }
  });


  // === Header Shrink on Scroll ===
  var header = document.querySelector('.site-header');
  var lastScroll = 0;

  window.addEventListener('scroll', function() {
    var scrollY = window.pageYOffset || document.documentElement.scrollTop;

    if (scrollY > 80) {
      header.classList.add('shrink');
    } else {
      header.classList.remove('shrink');
    }

    lastScroll = scrollY;
  }, { passive: true });


  // === Scroll Progress Bar ===
  var progressBar = document.querySelector('.scroll-progress');

  if (progressBar) {
    window.addEventListener('scroll', function() {
      var scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
      var scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      var progress = (scrollTop / scrollHeight) * 100;
      progressBar.style.width = progress + '%';
    }, { passive: true });
  }


  // === Back to Top Button ===
  var backToTop = document.querySelector('.back-to-top');

  if (backToTop) {
    window.addEventListener('scroll', function() {
      if (window.pageYOffset > 400) {
        backToTop.classList.add('visible');
      } else {
        backToTop.classList.remove('visible');
      }
    }, { passive: true });

    backToTop.addEventListener('click', function() {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }


  // === Active Nav Link Highlighting ===
  var navLinks = document.querySelectorAll('.nav-main a');
  var currentPath = window.location.pathname;

  navLinks.forEach(function(link) {
    var href = link.getAttribute('href');
    if (href === currentPath || (href !== '/' && currentPath.startsWith(href))) {
      link.classList.add('active');
    }
    if (href === '/' && currentPath === '/') {
      link.classList.add('active');
    }
  });


  // === Scroll-Triggered Animations ===
  var animateElements = document.querySelectorAll(
    '.about-preview, .solutions, .services-overview, .partners, .testimonials, .cta-section, ' +
    '.solution-card, .service-card, .post-card, .stat-item, .partner-logo'
  );

  if ('IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          if (entry.target.classList.contains('solution-card') ||
              entry.target.classList.contains('service-card') ||
              entry.target.classList.contains('post-card') ||
              entry.target.classList.contains('partner-logo') ||
              entry.target.classList.contains('stat-item')) {
            observer.unobserve(entry.target);
          }
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    animateElements.forEach(function(el) {
      if (el.classList.contains('solution-card') ||
          el.classList.contains('service-card') ||
          el.classList.contains('post-card') ||
          el.classList.contains('partner-logo')) {
        el.classList.add('animate-in');
      }
      if (el.classList.contains('stat-item')) {
        el.classList.add('animate-scale');
      }
      observer.observe(el);
    });

    document.querySelector('.about-preview')?.classList.add('animate-in');
    document.querySelector('.solutions')?.classList.add('animate-in');
    document.querySelector('.services-overview')?.classList.add('animate-in');
    document.querySelector('.partners')?.classList.add('animate-in');
    document.querySelector('.testimonials')?.classList.add('animate-in');
    document.querySelector('.cta-section')?.classList.add('animate-in');

    document.querySelectorAll('.about-preview, .solutions, .services-overview, .partners, .testimonials, .cta-section')
      .forEach(function(el) { observer.observe(el); });
  } else {
    animateElements.forEach(function(el) { el.classList.add('visible'); });
  }


  // === Animated Counters ===
  var statNumbers = document.querySelectorAll('.trust-stats .stat-number');

  if (statNumbers.length && 'IntersectionObserver' in window) {
    var counterObserver = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          var el = entry.target;
          var text = el.textContent.trim();
          var suffix = '';
          var targetNumber = 0;

          if (text.indexOf('+') > -1) {
            suffix = '+';
            targetNumber = parseInt(text.replace('+', ''), 10);
          } else if (text.indexOf('%') > -1) {
            suffix = '%';
            targetNumber = parseInt(text.replace('%', ''), 10);
          } else {
            targetNumber = parseInt(text, 10);
          }

          if (isNaN(targetNumber)) return;

          var duration = 1500;
          var startTime = null;

          function animateCount(timestamp) {
            if (!startTime) startTime = timestamp;
            var progress = Math.min((timestamp - startTime) / duration, 1);
            var eased = 1 - Math.pow(1 - progress, 3);
            var current = Math.floor(eased * targetNumber);

            el.innerHTML = current + '<span class="suffix">' + suffix + '</span>';

            if (progress < 1) {
              requestAnimationFrame(animateCount);
            } else {
              el.innerHTML = targetNumber + '<span class="suffix">' + suffix + '</span>';
            }
          }

          requestAnimationFrame(animateCount);
          counterObserver.unobserve(el);
        }
      });
    }, { threshold: 0.5 });

    statNumbers.forEach(function(el) {
      counterObserver.observe(el);
    });
  }


  // === Testimonial Carousel ===
  var carousel = document.querySelector('.testimonial-carousel');

  if (carousel) {
    var track = carousel.querySelector('.testimonial-track');
    var slides = track.querySelectorAll('.testimonial-slide');
    var dots = carousel.querySelectorAll('.testimonial-dot');
    var prevBtn = carousel.querySelector('.testimonial-nav-btn.prev');
    var nextBtn = carousel.querySelector('.testimonial-nav-btn.next');
    var currentIndex = 0;
    var autoPlayInterval;

    function goToSlide(index) {
      if (index < 0) index = slides.length - 1;
      if (index >= slides.length) index = 0;
      currentIndex = index;
      track.style.transform = 'translateX(-' + (index * 100) + '%)';
      dots.forEach(function(dot, i) {
        dot.classList.toggle('active', i === index);
      });
    }

    function nextSlide() { goToSlide(currentIndex + 1); }
    function prevSlide() { goToSlide(currentIndex - 1); }

    function startAutoPlay() {
      autoPlayInterval = setInterval(nextSlide, 5000);
    }

    function stopAutoPlay() {
      clearInterval(autoPlayInterval);
    }

    if (prevBtn) prevBtn.addEventListener('click', function() { stopAutoPlay(); prevSlide(); startAutoPlay(); });
    if (nextBtn) nextBtn.addEventListener('click', function() { stopAutoPlay(); nextSlide(); startAutoPlay(); });

    dots.forEach(function(dot) {
      dot.addEventListener('click', function() {
        stopAutoPlay();
        goToSlide(parseInt(this.getAttribute('data-index'), 10));
        startAutoPlay();
      });
    });

    // Pause on hover
    carousel.addEventListener('mouseenter', stopAutoPlay);
    carousel.addEventListener('mouseleave', startAutoPlay);

    startAutoPlay();
  }


  // === Contact Form Validation ===
  var form = document.querySelector('.contact-form form');

  if (form) {
    var inputs = form.querySelectorAll('input, textarea');

    function validateField(input) {
      var group = input.closest('.form-group');
      if (!group) return true;

      var value = input.value.trim();

      if (input.hasAttribute('required') && !value) {
        group.classList.add('error');
        return false;
      }

      if (input.type === 'email' && value) {
        var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
          group.classList.add('error');
          return false;
        }
      }

      if (input.type === 'tel' && value) {
        var phoneRegex = /^[\d\s\-\+\(\)]{7,20}$/;
        if (!phoneRegex.test(value)) {
          group.classList.add('error');
          return false;
        }
      }

      group.classList.remove('error');
      return true;
    }

    inputs.forEach(function(input) {
      input.addEventListener('blur', function() { validateField(this); });
      input.addEventListener('input', function() {
        this.closest('.form-group')?.classList.remove('error');
      });
    });

    form.addEventListener('submit', function(e) {
      var valid = true;
      inputs.forEach(function(input) {
        if (!validateField(input)) valid = false;
      });

      if (!valid) {
        e.preventDefault();
        var firstError = form.querySelector('.form-group.error input, .form-group.error textarea');
        if (firstError) firstError.focus();
      } else {
        var successMsg = document.querySelector('.form-success');
        if (successMsg) {
          e.preventDefault();
          successMsg.classList.add('visible');
          form.style.display = 'none';
          // In production, submit via fetch()
        }
      }
    });
  }


  // === Smooth Scroll for Anchor Links ===
  document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
    anchor.addEventListener('click', function(e) {
      var targetId = this.getAttribute('href');
      if (targetId === '#') return;
      var target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        var headerOffset = 80;
        var elementPosition = target.getBoundingClientRect().top;
        var offsetPosition = elementPosition + window.pageYOffset - headerOffset;
        window.scrollTo({ top: offsetPosition, behavior: 'smooth' });
      }
    });
  });

});
