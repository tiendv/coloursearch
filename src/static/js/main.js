let number_of_cols_in_page = 0;
let cols = [];
let selected_extractions = [];

window.onload = function () {
    // Change text of drop-down button
    $('.dropdown-menu a').click(function () {
        $('#method').text($(this).text());
        $('#method2').text($(this).text());
    });

    // Query by color layout
    $('#color-query-retrieve').click(function () {
        $('#loader').css("visibility", "visible");
        $('#loader').fadeIn();
        number_of_cols_in_page = 0;
        cols = [];
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
                'extraction_id': JSON.stringify(selected_extractions),
            },
            success: function (data) {
                if (Array.isArray(data)) {
                    let retrieval_result = document.querySelector('#retrieval-result');
                    retrieval_result.innerHTML = '';
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
                        a.className = 'img img-2 lazyload';
                        a.setAttribute('src', thumbnail_path);
                        a.setAttribute('data-src', thumbnail_path);
                        a.href = '#';
                        a.style.backgroundImage = `url(${thumbnail_path})`;
                        let text = document.createElement('div');
                        text.className = 'text text-2 pt-2 mt-3';
                        let p1 = document.createElement('p');
                        p1.className = 'mb-2';
                        p1.textContent = i + 1;
                        p1.style.fontWeight = '900';
                        p1.style.color = '#000000';
                        p1.style.wordWrap = 'break-word';
                        let span = document.createElement('span');
                        span.className = 'category mb-2 d-block';
                        span.style.color = '#000000';
                        span.textContent = similarity;
                        let p2 = document.createElement('p');
                        p2.className = 'mb-2';
                        p2.textContent = image_path;
                        p2.style.color = '#000000';
                        p2.style.wordWrap = 'break-word';
                        text.appendChild(p1);
                        text.appendChild(span);
                        text.appendChild(p2);
                        blogEntry.appendChild(a);
                        blogEntry.appendChild(text);
                        col.appendChild(blogEntry);
                        cols.push(col);
                        // retrievalResult.appendChild(col);
                    }
                    for (let i = 0; i < 50; i++) {
                        if (cols.length > (number_of_cols_in_page + i)) {
                            retrieval_result.appendChild(cols[number_of_cols_in_page + i]);
                        }
                    }
                    number_of_cols_in_page += 50;
                }
                $('#loader').fadeOut();
                console.log(data);
            }
        });
    });

    // Query by example image
    $('#image-query-retrieve').click(function () {
        $('#loader').css("visibility", "visible");
        $('#loader').fadeIn();
        number_of_cols_in_page = 0;
        cols = [];
        let colorMap = [];
        let rowCount = $('#color-map tr').length;
        let columnCount = document.getElementById('color-map').rows[0].cells.length;
        let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
        let method = $('span[id="method2"]').text();
        let image = $('#image-uploaded').attr('src');
        let base64ImageContent = image.replace(/^data:image\/(png|jpg|jpeg);base64,/, "");
        let blob = base64ToBlob(base64ImageContent, 'image/png');
        let formData = new FormData();
        formData.append('image', blob);
        formData.append('method', method);
        formData.append('csrfmiddlewaretoken', csrf_token);
        formData.append('extraction_id', JSON.stringify(selected_extractions));
        $.ajax({
            type: "post",
            url: "/retrieve/",
            cache: false,
            contentType: false,
            processData: false,
            data: formData
        }).done(function (data) {
            if (Array.isArray(data)) {
                let retrieval_result = document.querySelector('#retrieval-result');
                retrieval_result.innerHTML = '';
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
                    a.className = 'img img-2 lazyload';
                    a.setAttribute('src', thumbnail_path);
                    a.setAttribute('data-src', thumbnail_path);
                    a.href = '#';
                    a.style.backgroundImage = `url(${thumbnail_path})`;
                    let text = document.createElement('div');
                    text.className = 'text text-2 pt-2 mt-3';
                    let p1 = document.createElement('p');
                    p1.className = 'mb-2';
                    p1.textContent = i + 1;
                    p1.style.fontWeight = '900';
                    p1.style.color = '#000000';
                    p1.style.wordWrap = 'break-word';
                    let span = document.createElement('span');
                    span.className = 'category mb-2 d-block';
                    span.style.color = '#000000';
                    span.textContent = similarity;
                    let p2 = document.createElement('p');
                    p2.className = 'mb-2';
                    p2.textContent = image_path;
                    p2.style.color = '#000000';
                    p2.style.wordWrap = 'break-word';
                    text.appendChild(p1);
                    text.appendChild(span);
                    text.appendChild(p2);
                    blogEntry.appendChild(a);
                    blogEntry.appendChild(text);
                    col.appendChild(blogEntry);
                    cols.push(col);
                    // retrievalResult.appendChild(col);
                }
                for (let i = 0; i < 50; i++) {
                    if (cols.length > (number_of_cols_in_page + i)) {
                        retrieval_result.appendChild(cols[number_of_cols_in_page + i]);
                    }
                }
                number_of_cols_in_page += 50;
            }
            $('#loader').fadeOut();
            console.log(data);
        });
    });

    // Load more data when scrolled to the bottom
    $("#colorlib-main").on('scroll', function () {
        let colorlib_main = document.getElementById('colorlib-main');
        let retrieval_result = document.querySelector('#retrieval-result');
        if (colorlib_main.offsetHeight + colorlib_main.scrollTop >= colorlib_main.scrollHeight - 500) {
            for (let i = 0; i < 50; i++) {
                retrieval_result.appendChild(cols[number_of_cols_in_page + i]);
            }
            number_of_cols_in_page += 50;
        }
    });

    let extraction_table = document.querySelector('#extraction-table');
    $('#save-changes').click(function () {
        let checkbox = document.getElementsByClassName('extraction-checkbox');
        selected_extractions = [];
        for (let i = 0; i < checkbox.length; i++) {
            if (checkbox[i].checked) {
                let box_id = checkbox[i].id.split('-')[1];
                selected_extractions.push(document.getElementById('id-' + box_id).textContent);
            }
        }
    });
};

function base64ToBlob(base64, mime) {
    mime = mime || '';
    let sliceSize = 1024;
    let byteChars = window.atob(base64);
    let byteArrays = [];

    for (let offset = 0, len = byteChars.length; offset < len; offset += sliceSize) {
        let slice = byteChars.slice(offset, offset + sliceSize);

        let byteNumbers = new Array(slice.length);
        for (let i = 0; i < slice.length; i++) {
            byteNumbers[i] = slice.charCodeAt(i);
        }

        let byteArray = new Uint8Array(byteNumbers);

        byteArrays.push(byteArray);
    }

    return new Blob(byteArrays, {type: mime});
}

window.addEventListener("load", function (event) {
    lazyload();
});

const sizePicker = document.querySelector('.size-picker');
const pixelCanvas = document.querySelector('.pixel-canvas');
const clearAll = document.querySelector('.clear-all');
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
        tds[i].style.backgroundColor = 'rgb(255, 255, 255)'
    }
    let $cells = $('.color-cell');
    $cells.each(function () {
        let width = $(this).width();
        $(this).height(width);
    });
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

clearAll.addEventListener('click', function () {
    pixelCanvas.querySelectorAll('td').forEach(td => td.style.backgroundColor = '#FFFFFF');
});

quickFill.addEventListener('click', function () {
    const color = $('#bgcolor-button').text();
    pixelCanvas.querySelectorAll('td').forEach(td => td.style.backgroundColor = color);
});


// elen theme
AOS.init({
    duration: 800,
    easing: 'slide'
});

$(".box-file").change(function (e) {

    for (let i = 0; i < e.originalEvent.srcElement.files.length; i++) {

        let file = e.originalEvent.srcElement.files[i];

        let img = document.getElementById('image-uploaded');
        let reader = new FileReader();
        reader.onloadend = function () {
            img.src = reader.result;
        };
        reader.readAsDataURL(file);
        $(".box-file").after(img);
    }
});

(function ($) {
    let burgerMenu = function () {

        $('.js-colorlib-nav-toggle').on('click', function (event) {
            event.preventDefault();
            let $this = $(this);

            if ($('body').hasClass('offcanvas')) {
                $this.removeClass('active');
                $('body').removeClass('offcanvas');
            } else {
                $this.addClass('active');
                $('body').addClass('offcanvas');
            }
        });
    };
    burgerMenu();

    // Click outside of offcanvass
    let mobileMenuOutsideClick = function () {

        $(document).click(function (e) {
            let container = $("#colorlib-aside, .js-colorlib-nav-toggle");
            if (!container.is(e.target) && container.has(e.target).length === 0) {

                if ($('body').hasClass('offcanvas')) {

                    $('body').removeClass('offcanvas');
                    $('.js-colorlib-nav-toggle').removeClass('active');

                }

            }
        });

        $(window).scroll(function () {
            if ($('body').hasClass('offcanvas')) {

                $('body').removeClass('offcanvas');
                $('.js-colorlib-nav-toggle').removeClass('active');

            }
        });

    };
})(jQuery);