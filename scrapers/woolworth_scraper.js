
// Get the nutrition html scope
let nutrition_info_area = document.getElementsByClassName('ar-product-details-nutrition-table')[0];

// Get the div elements
// There should always three
let nutrition_div_elements = nutrition_info_area.getElementsByTagName('div');

// First div element: servings per package
let servings_pack = nutrition_div_elements[0].innerText.split(":")[1].trim()

// Second div element: serving size
// Remove all non-alphabets
let servings_size = nutrition_div_elements[1].innerText.split(":")[1].trim()
metric = servings_size.replace(/[^a-z]/gi, '');
size = servings_size.replace(/[^\d.]/g,'')

// Third div element: nutrition table
// First value: Quantity per serving
// Second value: Quantity per 100g/100mL
nutrition_rows = nutrition_div_elements[2].getElementsByClassName('nutrition-row');

// We ignore the header because we know what it is.
for (let i = 1; i < nutrition_rows.length; i++) {

    // Go row by row
    nutrition_row = nutrition_rows[i].getElementsByClassName('nutrition-column');

    // Extract: Metric/Nutrient, Serving (regular), Serinvg (per 100g/100mL)
    metric = nutrition_row[0].innerText;
    serving_quantity = nutrition_row[1].innerText;
    serving_per_100 = nutrition_row[2].innerText;
    
  }
