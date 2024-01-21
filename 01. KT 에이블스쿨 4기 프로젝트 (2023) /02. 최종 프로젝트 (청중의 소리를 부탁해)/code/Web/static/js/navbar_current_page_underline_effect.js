document.addEventListener("DOMContentLoaded", function() {
    // 현재 페이지의 URL을 가져옵니다.
    var currentLocation = window.location.href;
  
    // 모든 링크를 찾습니다.
    var navLinks = document.querySelectorAll('.nav-btn');
  
    // 각 링크에 대해 반복합니다.
    navLinks.forEach(function(link) {
      // 링크의 href 속성을 확인합니다.
      if (link.href === currentLocation) {
          console.log(link.href);
        // 현재 페이지 링크에 클래스를 추가합니다.
        link.classList.add('current-page');
      }
    });
  });
  