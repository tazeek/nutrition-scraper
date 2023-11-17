
function get_div_elements() {

    // Get the nutrition html scope
    class_name = 'ar-product-details-nutrition-table'
    let nutrition_info_area = document.getElementsByClassName(class_name)[0];
    return nutrition_info_area.getElementsByTagName('div');
}

function get_serving_size(serving_div) {
    let servings_size = serving_div.innerText.split(":")[1].trim()
    let metric = servings_size.replace(/[^a-z]/gi, '');
    let size = servings_size.replace(/[^\d.]/g,'')

    return metric, size
}

// This is where we will store the data
let json_nutrition = {}

// Get the div elements
// There should always three
nutrition_div_elements = get_div_elements()

// First div element: servings per package
let servings_pack = nutrition_div_elements[0].innerText.split(":")[1].trim()
json_nutrition['servings_per_pack'] = servings_pack

// Second div element: serving size
// Remove all non-alphabets
let metric, size = get_serving_size(nutrition_div_elements[1])
json_nutrition[`serving_size(${metric})`] = size

// Third div element: nutrition table
// First value: Quantity per serving
// Second value: Quantity per 100g/100mL
nutrition_rows = nutrition_div_elements[2].getElementsByClassName('nutrition-row');

// We ignore the header because we know what it is.
for (let i = 1; i < nutrition_rows.length; i++) {

    // Go row by row
    nutrition_row = nutrition_rows[i].getElementsByClassName('nutrition-column');

    // Extract: Metric/Nutrient, Serving (regular), Serinvg (per 100g/100mL)
    information = nutrition_row[0].innerText;
    information = information.replace(/[^a-z ]/gi, '').trim();

    serving_quantity = nutrition_row[1].innerText;
    serving_per_100 = nutrition_row[2].innerText;

    console.log(`${information} for ${serving_quantity} and ${serving_per_100}`)
}

console.log(json_nutrition)
