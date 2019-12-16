window.onload = function () {
    // Change text of drop-down button
    $('.dropdown-menu a').click(function () {
        $('#method').text($(this).text());
        let param1_label = $('#param1-label');
        let param2_label = $('#param2-label');
        let param3_label = $('#param3-label');
        let param1 = $('#param1');
        let param2 = $('#param2');
        let param3 = $('#param3');
        switch ($(this).text()) {
            case 'Fuzzy Color Histogram':
                param1_label.text('Number of coarse colors');
                param2_label.show();
                param2_label.text('Number of fine colors');
                param3_label.show();
                param3_label.text('m (weighting exponent)');
                param2.show();
                param3.show();
                break;
            case 'Color Coherence Vector':
                param1_label.text('Number of colors');
                param2_label.show();
                param2_label.text('τ (tau - coherence value)');
                param3_label.hide();
                param2.show();
                param3.hide();
                break;
            case 'Color Correlogram':
                param1_label.text('Number of colors');
                param2_label.show();
                param2_label.text('d');
                param3_label.show();
                param3_label.text('increment');
                param2.show();
                param3.show();
                break;
            case 'Cumulative Color Histogram':
                param1_label.text('Number of colors');
                param2_label.text('d');
                param2_label.hide();
                param3_label.hide();
                param2.hide();
                param3.hide();
                break;
        }
    });

    // Post form data
    $('#extract-submit').on('submit', function (event) {
        event.preventDefault();
        let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
        let method = $('span[id="method"]').text();
        let formData = {
            'folder_path': $('input[name="folder_path"]').val(),
            'method': method,
            'csrfmiddlewaretoken': csrf_token,
        };
        switch (method) {
            case 'Fuzzy Color Histogram':
            case 'Color Correlogram':
                formData['param1_name'] = $('#param1-label');
                formData['param2_name'] = $('#param2-label');
                formData['param3_name'] = $('#param3-label');
                formData['param1_value'] = $('#param1');
                formData['param2_value'] = $('#param2');
                formData['param3_value'] = $('#param3');
                break;
            case 'Color Coherence Vector':
                formData['param1_name'] = $('#param1-label');
                formData['param2_name'] = $('#param2-label');
                formData['param1_value'] = $('#param1');
                formData['param2_value'] = $('#param2');
                break;
            case 'Cumulative Color Histogram':
                formData['param1_name'] = $('#param1-label');
                formData['param1_value'] = $('#param1');
                break;
        }
        csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
        $.ajax({
            url: '',
            type: 'post',
            data: formData,
            success: function (message) {
                alert(message);
            }
        })
    });

    $('#retrieve').click(function () {
        let colorMap = [];
        let rowCount = $('#color-map tr').length;
        let columnCount = document.getElementById('color-map').rows[0].cells.length;
        for (let i = 1; i <= rowCount; i++) {
            let colorRow = [];
            for (let j = 1; j <= columnCount; j++) {
                let cell_id = '#cell-' + i + '-' + j;
                let color = $(cell_id).css('backgroundColor');
                colorRow.push(color);
            }
            colorMap.push(colorRow);
        }

        let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
        let method = $('span[id="method"]').text();
        $.ajax({
            type: "post",
            url: "/retrieve/",
            data: {
                'colorMap': JSON.stringify(colorMap),
                'method': method,
                'csrfmiddlewaretoken': csrf_token,
            },
            success: function (data) {
                if (Array.isArray(data)) {
                    let retrievalResult = document.querySelector('.retrieval-result');
                    for (let i = 0; i < data.length; i++) {
                        let image_path = data[i]['image_path'];
                        let thumbnail_path = data[i]['thumbnail_path'];
                        thumbnail_path = thumbnail_path.replace(/\s/g, '');
                        thumbnail_path = thumbnail_path.replace(/\\/g, "/");
                        let similarity = data[i]['similarity'];
                        let col = document.createElement('div');
                        col.className = 'col-md-4';
                        let blogEntry = document.createElement('div');
                        blogEntry.className = 'blog-entry ftco-animate';
                        let a = document.createElement('a');
                        a.className = 'img img-2';
                        a.href = '#';
                        a.style.backgroundImage = `url(${thumbnail_path})`;
                        let text = document.createElement('div');
                        text.className = 'text text-2 pt-2 mt-3';
                        let span = document.createElement('span');
                        span.className = 'category mb-3 d-block';
                        span.style.color = '#000000';
                        span.textContent = similarity;
                        let p = document.createElement('p');
                        p.className = 'mb-2';
                        p.textContent = image_path;
                        p.style.color = '#000000';
                        text.appendChild(span);
                        text.appendChild(p);
                        blogEntry.appendChild(a);
                        blogEntry.appendChild(text);
                        col.appendChild(blogEntry);
                        retrievalResult.appendChild(col);
                    }
                }
                console.log(data);
            }
        });
    })

};

const sizePicker = document.querySelector('.size-picker');
const pixelCanvas = document.querySelector('.pixel-canvas');
const quickFill = document.querySelector('.quick-fill');

function makeGrid() {
    let gridHeight = document.querySelector('.input-height').value;
    let gridWidth = document.querySelector('.input-width').value;
    // If grid already present, clears any cells that have been filled in
    while (pixelCanvas.firstChild) {
        pixelCanvas.removeChild(pixelCanvas.firstChild);
    }

    // Creates rows and cells
    for (let i = 1; i <= gridHeight; i++) {
        let gridRow = document.createElement('tr');
        gridRow.id = 'row-' + i.toString();
        pixelCanvas.appendChild(gridRow);
        for (let j = 1; j <= gridWidth; j++) {
            let gridCell = document.createElement('td');
            gridCell.className = 'color-cell';
            gridCell.id = 'cell-' + i.toString() + '-' + j.toString();
            gridRow.appendChild(gridCell);
            // Fills in cell with selected color upon mouse press ('mousedown', unlike 'click', doesn't also require release of mouse button)
            gridCell.addEventListener('mousedown', function () {
                // 'color' defined here rather than globally so JS checks whether user has changed color with each new mouse press on cell
                this.style.backgroundColor = document.querySelector('#bgcolor-button').innerHTML;
            })
        }
    }

    let cellLength = Math.floor(document.getElementById('color-map-div').offsetWidth / gridWidth);
    let tds = document.getElementsByClassName('color-cell');
    for (let i = 0; i < tds.length; i++) {
        tds[i].style.setProperty('width', cellLength + 'px', 'important');
        tds[i].style.setProperty('height', (cellLength - 2) + 'px', 'important');
        tds[i].style.backgroundColor = 'rgb(255, 255, 255)'
    }
}

// Upon user's submitting height and width selections, callback function (inside method) calls makeGrid function. But event method preventDefault() first intercepts the 'submit' event, which would normally submit the form and refresh the page, preventing makeGrid() from being processed
sizePicker.addEventListener('submit', function (e) {
    e.preventDefault();
    makeGrid();
});

// Enables color dragging with selected color (code for filling in single cell is above)
let down = false; // tracks whether or not mouse pointer is pressed

// Listens for mouse pointer press and release on grid. Changes value to true when pressed, but sets it back to false as soon as released
pixelCanvas.addEventListener('mousedown', function (e) {
    down = true;
    pixelCanvas.addEventListener('mouseup', function () {
        down = false;
    });
    // Ensures cells won't be colored if grid is left while pointer is held down
    pixelCanvas.addEventListener('mouseleave', function () {
        down = false;
    });

    pixelCanvas.addEventListener('mouseover', function (e) {
        // 'color' defined here rather than globally so JS checks whether user has changed color with each new mouse press on cell
        const color = document.querySelector('#bgcolor-button').innerHTML;
        // While mouse pointer is pressed and within grid boundaries, fills cell with selected color. Inner if statement fixes bug that fills in entire grid
        if (down) {
            // 'TD' capitalized because element.tagName returns upper case for DOM trees that represent HTML elements
            if (e.target.tagName === 'TD') {
                e.target.style.backgroundColor = color;
            }
        }
    });
});

makeGrid(15, 15);

// Removes color from cell upon double-click
pixelCanvas.addEventListener('dblclick', e => {
    e.target.style.backgroundColor = null;
});

quickFill.addEventListener('click', function () {
    const color = document.querySelector('#bgcolor-button').innerHTML;
    pixelCanvas.querySelectorAll('td').forEach(td => td.style.backgroundColor = color);
});


// elen theme
AOS.init({
    duration: 800,
    easing: 'slide'
});

// (function ($) {
//
//     "use strict";
//
//     $(window).stellar({
//         responsive: true,
//         parallaxBackgrounds: true,
//         parallaxElements: true,
//         horizontalScrolling: false,
//         hideDistantElements: false,
//         scrollProperty: 'scroll'
//     });
//
//
//     var fullHeight = function () {
//
//         $('.js-fullheight').css('height', $(window).height());
//         $(window).resize(function () {
//             $('.js-fullheight').css('height', $(window).height());
//         });
//
//     };
//     fullHeight();
//
//     // loader
//     var loader = function () {
//         setTimeout(function () {
//             if ($('#ftco-loader').length > 0) {
//                 $('#ftco-loader').removeClass('show');
//             }
//         }, 1);
//     };
//     loader();
//
//     // Scrollax
//     $.Scrollax();
//
//
//     var burgerMenu = function () {
//
//         $('.js-colorlib-nav-toggle').on('click', function (event) {
//             event.preventDefault();
//             var $this = $(this);
//
//             if ($('body').hasClass('offcanvas')) {
//                 $this.removeClass('active');
//                 $('body').removeClass('offcanvas');
//             } else {
//                 $this.addClass('active');
//                 $('body').addClass('offcanvas');
//             }
//         });
//     };
//     burgerMenu();
//
//     // Click outside of offcanvass
//     var mobileMenuOutsideClick = function () {
//
//         $(document).click(function (e) {
//             var container = $("#colorlib-aside, .js-colorlib-nav-toggle");
//             if (!container.is(e.target) && container.has(e.target).length === 0) {
//
//                 if ($('body').hasClass('offcanvas')) {
//
//                     $('body').removeClass('offcanvas');
//                     $('.js-colorlib-nav-toggle').removeClass('active');
//
//                 }
//
//             }
//         });
//
//         $(window).scroll(function () {
//             if ($('body').hasClass('offcanvas')) {
//
//                 $('body').removeClass('offcanvas');
//                 $('.js-colorlib-nav-toggle').removeClass('active');
//
//             }
//         });
//
//     };
//     mobileMenuOutsideClick();
//
//     var carousel = function () {
//         $('.home-slider').owlCarousel({
//             loop: true,
//             autoplay: true,
//             margin: 0,
//             animateOut: 'fadeOut',
//             animateIn: 'fadeIn',
//             nav: false,
//             autoplayHoverPause: false,
//             items: 1,
//             navText: ["<span class='ion-md-arrow-back'></span>", "<span class='ion-chevron-right'></span>"],
//             responsive: {
//                 0: {
//                     items: 1
//                 },
//                 600: {
//                     items: 1
//                 },
//                 1000: {
//                     items: 1
//                 }
//             }
//         });
//
//     };
//     carousel();
//
//
//     var contentWayPoint = function () {
//         var i = 0;
//         $('.ftco-animate').waypoint(function (direction) {
//
//             if (direction === 'down' && !$(this.element).hasClass('ftco-animated')) {
//
//                 i++;
//
//                 $(this.element).addClass('item-animate');
//                 setTimeout(function () {
//
//                     $('body .ftco-animate.item-animate').each(function (k) {
//                         var el = $(this);
//                         setTimeout(function () {
//                             var effect = el.data('animate-effect');
//                             if (effect === 'fadeIn') {
//                                 el.addClass('fadeIn ftco-animated');
//                             } else if (effect === 'fadeInLeft') {
//                                 el.addClass('fadeInLeft ftco-animated');
//                             } else if (effect === 'fadeInRight') {
//                                 el.addClass('fadeInRight ftco-animated');
//                             } else {
//                                 el.addClass('fadeInUp ftco-animated');
//                             }
//                             el.removeClass('item-animate');
//                         }, k * 50, 'easeInOutExpo');
//                     });
//
//                 }, 100);
//
//             }
//
//         }, {offset: '95%'});
//     };
//     contentWayPoint();
//
//
//     // magnific popup
//     $('.image-popup').magnificPopup({
//         type: 'image',
//         closeOnContentClick: true,
//         closeBtnInside: false,
//         fixedContentPos: true,
//         mainClass: 'mfp-no-margins mfp-with-zoom', // class to remove default margin from left and right side
//         gallery: {
//             enabled: true,
//             navigateByImgClick: true,
//             preload: [0, 1] // Will preload 0 - before current, and 1 after the current image
//         },
//         image: {
//             verticalFit: true
//         },
//         zoom: {
//             enabled: true,
//             duration: 300 // don't foget to change the duration also in CSS
//         }
//     });
//
//     $('.popup-youtube, .popup-vimeo, .popup-gmaps').magnificPopup({
//         disableOn: 700,
//         type: 'iframe',
//         mainClass: 'mfp-fade',
//         removalDelay: 160,
//         preloader: false,
//
//         fixedContentPos: false
//     });
//
// })(jQuery);

