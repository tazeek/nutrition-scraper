
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
servings_size = servings_size.replace(/[^\d.]/g,'')

// Third div element: nutrition table
