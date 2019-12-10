window.onload = function() {
  // Change text of drop-down button
  $('.dropdown-menu a').click(function(){
    $('#algorithm').text($(this).text());
    let param1_label = $('#param1-label');
    let param2_label = $('#param2-label');
    let param3_label = $('#param3-label');
    let param1 = $('#param1');
    let param2 = $('#param2');
    let param3 = $('#param3');
    switch($(this).text()) {
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
    csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    let algorithm = $('span[id="algorithm"]').text();
    let formData = {
      'folder_path': $('input[name="folder_path"]').val(),
      'algorithm': algorithm,
      'csrfmiddlewaretoken': csrf_token,
    };
    switch(algorithm) {
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
    let colorMap = []
    let rowCount = $('#color-map tr').length;
    let columnCount = document.getElementById('color-map').rows[0].cells.length;
    for (let i = 1; i < rowCount; i++) {
      for (let j = 1; j < columnCount; j++) {

      }
    }
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
      gridCell.addEventListener('mousedown', function() {
        // 'color' defined here rather than globally so JS checks whether user has changed color with each new mouse press on cell
        const color = document.querySelector('#bgcolor-hex').value;
        this.style.backgroundColor = color;
      })
     }
  }

  let cellLength = Math.floor(document.getElementById('demo-app').offsetWidth / gridWidth);
  let tds = document.getElementsByClassName('color-cell');
  for (let i = 0; i < tds.length; i++) {
    tds[i].style.width = cellLength + 'px';
    tds[i].style.height = cellLength + 'px';
  }
}

// Upon user's submitting height and width selections, callback function (inside method) calls makeGrid function. But event method preventDefault() first intercepts the 'submit' event, which would normally submit the form and refresh the page, preventing makeGrid() from being processed
sizePicker.addEventListener('submit', function(e) {
  e.preventDefault();
  makeGrid();
});

// Enables color dragging with selected color (code for filling in single cell is above)
let down = false; // tracks whether or not mouse pointer is pressed

// Listens for mouse pointer press and release on grid. Changes value to true when pressed, but sets it back to false as soon as released
pixelCanvas.addEventListener('mousedown', function(e) {
	down = true;
	pixelCanvas.addEventListener('mouseup', function() {
		down = false;
	});
  // Ensures cells won't be colored if grid is left while pointer is held down
  pixelCanvas.addEventListener('mouseleave', function() {
    down = false;
  });

  pixelCanvas.addEventListener('mouseover', function(e) {
    // 'color' defined here rather than globally so JS checks whether user has changed color with each new mouse press on cell
    const color = document.querySelector('#bgcolor-hex').value;
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

quickFill.addEventListener('click', function() {
  const color = document.querySelector('#bgcolor-hex').value;
  console.log(document.querySelector('#bgcolor-hex').value);
  pixelCanvas.querySelectorAll('td').forEach(td => td.style.backgroundColor = color);
});






(function ($) {
    "use strict";

    /*==================================================================
    [ Validate ]*/
    var input = $('.validate-input .input100');

    $('.validate-form').on('submit',function(){
        var check = true;

        for(var i=0; i<input.length; i++) {
            if(validate(input[i]) == false){
                showValidate(input[i]);
                check=false;
            }
        }

        return check;
    });


    $('.validate-form .input100').each(function(){
        $(this).focus(function(){
           hideValidate(this);
        });
    });

    function validate (input) {
        if($(input).attr('type') == 'email' || $(input).attr('name') == 'email') {
            if($(input).val().trim().match(/^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{1,5}|[0-9]{1,3})(\]?)$/) == null) {
                return false;
            }
        }
        else {
            if($(input).val().trim() == ''){
                return false;
            }
        }
    }

    function showValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).addClass('alert-validate');
    }

    function hideValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).removeClass('alert-validate');
    }




})(jQuery);