// light-dark switch functionality
const light_dark_switch = document.getElementById("light_dark_switch");
light_dark_switch.addEventListener("change", function(e) {
  console.log(e.target.checked);
  if (e.target.checked == true) {
    var css_light = document.getElementById("css_light")
    css_light.rel = "stylesheet alternate";
    var css_light2 = document.getElementById("css_light2");
    css_light2.rel2 = "stylesheet alternate";
    var css_dark = document.getElementById("css_dark")
    css_dark.rel = "stylesheet";
  } else if (e.target.checked == false) {
    var css_light = document.getElementById("css_light");
    css_light.rel = "stylesheet";
    var css_light2 = document.getElementById("css_light2")
    css_light2.rel2 = "stylesheet";
    var css_dark = document.getElementById("css_dark")
    css_dark.rel = "stylesheet alternate";
  }
});

// importing modules
import { create_element, remove_element, remove_children } from "./module_elements.js"
import { delete_ld_results, create_table_skeleton } from "./module_blocks.js"

import { mtld_whole_text, mtld_whole_text_pncorrection } from "./module_mtld.js"
import { mtld_whole_text_lemmas, mtld_whole_text_lemmas_pncorrection } from "./module_mtld_lemmas.js"
import { hdd_whole_text } from "./module_hdd.js"
import { hdd_whole_text_lemmas } from "./module_hdd_lemmas.js"
import { ttr_whole_text, ttr_split_text, ttr_equal_text } from "./module_ttr.js"
import { ttr_whole_text_lemmas, ttr_split_text_lemmas, ttr_equal_text_lemmas } from "./module_ttr_lemmas.js"
import { herdans_c_whole_text, herdans_c_split_text, herdans_c_equal_text } from "./module_herdans_c.js"
import { herdans_c_whole_text_lemmas, herdans_c_split_text_lemmas, herdans_c_equal_text_lemmas } from "./module_herdans_c_lemmas.js"
import { guirauds_r_whole_text, guirauds_r_split_text, guirauds_r_equal_text } from "./module_guirauds_r.js"
import { guirauds_r_whole_text_lemmas, guirauds_r_split_text_lemmas, guirauds_r_equal_text_lemmas } from "./module_guirauds_r_lemmas.js"
import { uber_u_whole_text, uber_u_split_text, uber_u_equal_text } from "./module_uber_u.js"
import { uber_u_whole_text_lemmas, uber_u_split_text_lemmas, uber_u_equal_text_lemmas } from "./module_uber_u_lemmas.js"


//widget variables declarations
var load_button = document.getElementById('load_button');
var user_text = document.getElementById('exampleFormControlTextarea1');
var loaded_text_label = document.getElementById('loaded_text_label');
var tokens_count_text = document.getElementById('tokens_count_text');
var count_tokens_button = document.getElementById('count_tokens_button');
var count_types_button = document.getElementById('count_types_button');
var types_table = document.getElementById('types_table');
var table_body = document.getElementById('table_body');
var example = document.getElementById('example');
var sampling_method = document.getElementById('sampling_method');
var sample_beginning = document.getElementById('sample_beginning');
var sample_length = document.getElementById('sample_length');
var size_of_subsamples = document.getElementById('size_of_subsamples');
var lexical_diversity_index = document.getElementById('lexical_diversity_index');
var sample_beginning = document.getElementById('sample_beginning');
var sample_length = document.getElementById('sample_length');
var size_of_subsamples = document.getElementById('size_of_subsamples');
var lexical_diversity_start_button = document.getElementById('lexical_diversity_start_button');
var ld_results_grandparent = document.getElementById('ld_results_grandparent');
var start_button_parent = document.getElementById('start_button_parent');
var single_break = document.getElementById('single_break');
var lexical_diversity = document.getElementById('lexical_diversity');
var lexical_diversity_pane = document.getElementById("contact-tab");
var parameters_split_text = document.getElementById("parameters_split_text");
var parameters_equal_text = document.getElementById("parameters_equal_text");


// @@@@@@@@@
// File View
// @@@@@@@@@


// this function clears the value kept in the button so that
// a file is loaded each time, not only when a new file is chose
load_button.addEventListener('click', function (e) {
  load_button.value = "";
});


load_button.addEventListener("change", function (event) {
  var input = event.target;
  var reader = new FileReader();
  reader.onload = function () {
    var text = reader.result;
    var fileName = document.getElementById('load_button').files[0].name;
    user_text.value = text;
    user_text.style.backgroundColor = 'white';
    loaded_text_label.innerText = "Loaded: " + fileName;
  };
  reader.readAsText(input.files[0]);
});



// @@@@@@@@@@@@@@@
// Text Statistics
// @@@@@@@@@@@@@@@

// cleaning any previous results after clicking Text Statistics pane
document.getElementById('home-tab').addEventListener('click', function (e) {

  // deleting any previous types table
  tokens_count_text.style.visibility = 'hidden';
  var types_table = document.querySelector("#types_table");
  if (typeof (types_table) != 'undefined' && types_table != null) {
    types_table.parentNode.removeChild(types_table);
  };
});


// Count Tokens
count_tokens_button.addEventListener('click', function (e) {

  remove_element("warning");

  // warning if no text...
  var user_text_with_punctuation = user_text.value;
  if (user_text.value == "") {
    create_element({ tag: "p", id: "warning", innerText: 'Please paste text or load a txt file in the "File View" section...', parent_id: "table_parent" });
  } else {

    // deleting any previous types table
    var types_table = document.querySelector("#types_table");
    if (typeof (types_table) != 'undefined' && types_table != null) {
      types_table.parentNode.removeChild(types_table);
    };

    let xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function (e) {
      if (xhr.readyState == 4 && xhr.status == 200) {
        remove_element("the_spinner");
        // obtaining the json response
        let json_response = xhr.responseText;
        // transforming the json response to js object
        let response_object = JSON.parse(json_response);
        let result = response_object.result;
        tokens_count_text.innerText = "The number of word tokens: " + result + ".";
        tokens_count_text.style.visibility = 'visible';
        count_tokens_button.disabled = false;
        count_types_button.disabled = false;
        count_lemmas_button.disabled = false;
        lexical_diversity_pane.disabled = false;
      };
    };

    create_element({ tag: "div", className: "spinner-border text-primary", role: "status", id: "the_spinner", parent_id: "table_parent" });
    var user_text_with_punctuation = user_text.value;
    var user_text_without_punctuation = user_text_with_punctuation.match(/[^_\W]+/g).join(' ');
    var user_text_without_punctuation = user_text_without_punctuation.toLowerCase();

    count_tokens_button.disabled = true;
    count_types_button.disabled = true;
    count_lemmas_button.disabled = true;

    lexical_diversity_pane.disabled = true;

    xhr.open('POST', '/count_tokens/', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
    var data = 'user_text=' + user_text_without_punctuation;
    xhr.send(data);
  }
});



// Count Types
count_types_button.addEventListener('click', function (e) {

  remove_element("warning");

  // warning if no text...
  var user_text_with_punctuation = user_text.value;
  if (user_text.value == "") {
    create_element({ tag: "p", id: "warning", innerText: 'Please paste text or load a txt file in the "File View" section...', parent_id: "table_parent" });
  } else {

    // deleting any previous types table
    var types_table = document.querySelector("#types_table");
    if (typeof (types_table) != 'undefined' && types_table != null) {
      types_table.parentNode.removeChild(types_table);
    };

    let xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function (e) {
      if (xhr.readyState == 4 && xhr.status == 200) {
        remove_element("the_spinner");
        // obtaining the json response
        let json_response = xhr.responseText;
        // transforming the json response to js object
        let response_object = JSON.parse(json_response);
        let types_object = response_object.types_list;
        let object_length = Object.keys(types_object).length;

        // creating elements for table
        var table_container_div = document.createElement("div");
        table_container_div.className = "card mb-4";
        table_container_div.id = "types_table";
        var card_header_div = document.createElement("div");
        card_header_div.className = "card-header";
        card_header_div.innerText = "Types List";
        var i_something = document.createElement("i");
        i_something.className = "fas fa-table mr-1"
        var card_body_div = document.createElement("div");
        card_body_div.className = "card-body";
        var table_responsive_div = document.createElement("div");
        table_responsive_div.className = "table-responsive";
        var table_el = document.createElement("table");
        table_el.className = "display";
        table_el.id = "example"
        table_el.style.width = "100%";

        card_header_div.appendChild(i_something);
        table_responsive_div.appendChild(table_el);
        card_body_div.appendChild(table_responsive_div);
        table_container_div.appendChild(card_header_div);
        table_container_div.appendChild(card_body_div);
        document.getElementById('table_parent').appendChild(table_container_div)


        // creating the table using datatables
        $(document).ready(function () {
          $('#example').DataTable({
            data: types_object,
            columns: [{ title: "Rank" }, { title: "Type" }, { title: "Frequency" }]
          });
        });

        tokens_count_text.innerText = "The number of word types: " + object_length + ".";
        tokens_count_text.style.visibility = 'visible';

        count_tokens_button.disabled = false;
        count_types_button.disabled = false;
        count_lemmas_button.disabled = false;
        lexical_diversity_pane.disabled = false;
      };
    };

    create_element({ tag: "div", className: "spinner-border text-primary", role: "status", id: "the_spinner", parent_id: "table_parent" });
    var user_text_with_punctuation = user_text.value;
    var user_text_without_punctuation = user_text_with_punctuation.match(/[^_\W]+/g).join(' ');
    var user_text_without_punctuation = user_text_without_punctuation.toLowerCase();

    count_tokens_button.disabled = true;
    count_types_button.disabled = true;
    count_lemmas_button.disabled = true;
    lexical_diversity_pane.disabled = true;

    xhr.open('POST', '/count_types/', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
    var data = 'user_text=' + user_text_without_punctuation;
    xhr.send(data);
  }
});



// Count Lemmas
count_lemmas_button.addEventListener('click', function (e) {

  remove_element("warning");

  // warning if no text...
  var user_text_with_punctuation = user_text.value;
  if (user_text.value == "") {
    create_element({ tag: "p", id: "warning", innerText: 'Please paste text or load a txt file in the "File View" section...', parent_id: "table_parent" });
  } else {

    // deleting any previous types table
    var types_table = document.querySelector("#types_table");
    if (typeof (types_table) != 'undefined' && types_table != null) {
      types_table.parentNode.removeChild(types_table);
    };

    let xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function (e) {
      if (xhr.readyState == 4 && xhr.status == 200) {
        remove_element("the_spinner");
        // obtaining the json response
        let json_response = xhr.responseText;
        // transforming the json response to js object
        let response_object = JSON.parse(json_response);
        let lemmas_object = response_object.lemmas_list;
        console.log(lemmas_object);
        let object_length = Object.keys(lemmas_object).length;

        // creating elements for table
        var table_container_div = document.createElement("div");
        table_container_div.className = "card mb-4";
        table_container_div.id = "types_table";
        var card_header_div = document.createElement("div");
        card_header_div.className = "card-header";
        card_header_div.innerText = "Lemmas List";
        var i_something = document.createElement("i");
        i_something.className = "fas fa-table mr-1"
        var card_body_div = document.createElement("div");
        card_body_div.className = "card-body";
        var table_responsive_div = document.createElement("div");
        table_responsive_div.className = "table-responsive";
        var table_el = document.createElement("table");
        table_el.className = "display";
        table_el.id = "example"
        table_el.style.width = "100%";

        card_header_div.appendChild(i_something);
        table_responsive_div.appendChild(table_el);
        card_body_div.appendChild(table_responsive_div);
        table_container_div.appendChild(card_header_div);
        table_container_div.appendChild(card_body_div);
        document.getElementById('table_parent').appendChild(table_container_div)


        // creating the table using datatables
        $(document).ready(function () {
          $('#example').DataTable({
            data: lemmas_object,
            columns: [{ title: "Rank" }, { title: "Lemma" }, { title: "Frequency" }]
          });
        });

        tokens_count_text.innerText = "The number of lemmas: " + object_length + ".";
        tokens_count_text.style.visibility = 'visible';

        count_tokens_button.disabled = false;
        count_types_button.disabled = false;
        count_lemmas_button.disabled = false;
        lexical_diversity_pane.disabled = false;
      };
    };

    create_element({ tag: "div", className: "spinner-border text-primary", role: "status", id: "the_spinner", parent_id: "table_parent" });
    var user_text_with_punctuation = user_text.value;
    var user_text_without_punctuation = user_text_with_punctuation.match(/[^_\W]+/g).join(' ');
    var user_text_without_punctuation = user_text_without_punctuation.toLowerCase();

    count_tokens_button.disabled = true;
    count_types_button.disabled = true;
    count_lemmas_button.disabled = true;
    lexical_diversity_pane.disabled = true;

    xhr.open('POST', '/count_lemmas/', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
    var data = 'user_text=' + user_text_without_punctuation;
    xhr.send(data);
  }
});





// @@@@@@@@@@@@@@@@@
// Lexical diversity
// @@@@@@@@@@@@@@@@@


// cleaning any previous results after clicking Lexical Diversity pane
document.getElementById('contact-tab').addEventListener('click', function (e) {
  delete_ld_results();
});

// Spinbox activation dependent on sampling method and ld index
sampling_method.addEventListener('change', function (e) {
  var sampling_method_value = sampling_method.options[sampling_method.selectedIndex].value;
  if (sampling_method_value == "Split text") {
    parameters_split_text.className = "collapse.show"
    parameters_equal_text.className = "collapse"
  };
  if (sampling_method_value == "Equal text") {
    parameters_split_text.className = "collapse"
    parameters_equal_text.className = "collapse.show"
  };
  if (sampling_method_value == "Whole text") {
    parameters_split_text.className = "collapse"
    parameters_equal_text.className = "collapse"
  };
});

lexical_diversity_index.addEventListener('change', function (e) {
  var lexical_diversity_index_value = lexical_diversity_index.options[lexical_diversity_index.selectedIndex].value;
  if (lexical_diversity_index_value == "MTLD" || lexical_diversity_index_value == "MTLD (lemmas)" ||
    lexical_diversity_index_value == "MTLD (proper names correction)" || 
    lexical_diversity_index_value == "MTLD (lemmas, proper names correction)") {
    sampling_method.disabled = true;
    sampling_method.value = "Whole text";
    parameters_split_text.className = "collapse"
    parameters_equal_text.className = "collapse"
  };
  if (lexical_diversity_index_value == "HDD" || lexical_diversity_index_value == "HDD (lemmas)") {
    sampling_method.disabled = true;
    sampling_method.value = "Whole text";
    parameters_split_text.className = "collapse"
    parameters_equal_text.className = "collapse"
  };
  if (lexical_diversity_index_value == "TTR" || lexical_diversity_index_value == "TTR (lemmas)") {
    sampling_method.disabled = false;
  };
  if (lexical_diversity_index_value == "Herdan's C" || lexical_diversity_index_value == "Herdan's C (lemmas)") {
    sampling_method.disabled = false;
  };
  if (lexical_diversity_index_value == "Guiraud's R" || lexical_diversity_index_value == "Guiraud's R (lemmas)") {
    sampling_method.disabled = false;
  };
  if (lexical_diversity_index_value == "Uber U" || lexical_diversity_index_value == "Uber U (lemmas)") {
    sampling_method.disabled = false;
  };
});






lexical_diversity_start_button.addEventListener('click', function (e) {
  delete_ld_results();

  var lexical_diversity_index_value = lexical_diversity_index.options[lexical_diversity_index.selectedIndex].value;
  var sampling_method_value = sampling_method.options[sampling_method.selectedIndex].value;

  // GENERAL WARNINGS
  if (user_text.value == "") {
    create_element({ tag: "p", id: "warning", innerText: 'Please paste text or load a txt file in the "File View" section...', parent_id: "ld_results_grandparent" });
  } else if (user_text.value.split(" ").length < 30) {
    create_element({ tag: "p", id: "warning", innerText: 'Your text needs to be longer to measure lexical diversity. In this program it means at least 30 word tokens, although for reliable results the value should potentially be higher. Please make necessary changes in the "File View" section.', parent_id: "ld_results_grandparent" });

    // CALLING LD FUNCTIONS
  } else if (lexical_diversity_index_value == "MTLD" && sampling_method_value == "Whole text") {
    mtld_whole_text();
  } else if (lexical_diversity_index_value == "MTLD (lemmas)" && sampling_method_value == "Whole text") {
    mtld_whole_text_lemmas();
  } else if (lexical_diversity_index_value == "MTLD (proper names correction)" && sampling_method_value == "Whole text") {
    mtld_whole_text_pncorrection();
  } else if (lexical_diversity_index_value == "MTLD (lemmas, proper names correction)" && sampling_method_value == "Whole text") {
    mtld_whole_text_lemmas_pncorrection();
  } else if (lexical_diversity_index_value == "HDD" && sampling_method_value == "Whole text") {
    hdd_whole_text();
  } else if (lexical_diversity_index_value == "HDD (lemmas)" && sampling_method_value == "Whole text") {
    hdd_whole_text_lemmas();
  } else if (lexical_diversity_index_value == "TTR" && sampling_method_value == "Whole text") {
    ttr_whole_text();
  } else if (lexical_diversity_index_value == "TTR (lemmas)" && sampling_method_value == "Whole text") {
    ttr_whole_text_lemmas();
  } else if (lexical_diversity_index_value == "TTR" && sampling_method_value == "Split text") {
    ttr_split_text();
  } else if (lexical_diversity_index_value == "TTR (lemmas)" && sampling_method_value == "Split text") {
    ttr_split_text_lemmas();
  } else if (lexical_diversity_index_value == "TTR" && sampling_method_value == "Equal text") {
    ttr_equal_text();
  } else if (lexical_diversity_index_value == "TTR (lemmas)" && sampling_method_value == "Equal text") {
    ttr_equal_text_lemmas();
  } else if (lexical_diversity_index_value == "Herdan's C" && sampling_method_value == "Whole text") {
    herdans_c_whole_text();
  } else if (lexical_diversity_index_value == "Herdan's C (lemmas)" && sampling_method_value == "Whole text") {
    herdans_c_whole_text_lemmas();
  } else if (lexical_diversity_index_value == "Herdan's C" && sampling_method_value == "Split text") {
    herdans_c_split_text();
  } else if (lexical_diversity_index_value == "Herdan's C (lemmas)" && sampling_method_value == "Split text") {
    herdans_c_split_text_lemmas();
  } else if (lexical_diversity_index_value == "Herdan's C" && sampling_method_value == "Equal text") {
    herdans_c_equal_text();
  } else if (lexical_diversity_index_value == "Herdan's C (lemmas)" && sampling_method_value == "Equal text") {
    herdans_c_equal_text_lemmas();
  } else if (lexical_diversity_index_value == "Guiraud's R" && sampling_method_value == "Whole text") {
    guirauds_r_whole_text();
  } else if (lexical_diversity_index_value == "Guiraud's R (lemmas)" && sampling_method_value == "Whole text") {
    guirauds_r_whole_text_lemmas();
  } else if (lexical_diversity_index_value == "Guiraud's R" && sampling_method_value == "Split text") {
    guirauds_r_split_text();
  } else if (lexical_diversity_index_value == "Guiraud's R (lemmas)" && sampling_method_value == "Split text") {
    guirauds_r_split_text_lemmas();
  } else if (lexical_diversity_index_value == "Guiraud's R" && sampling_method_value == "Equal text") {
    guirauds_r_equal_text();
  } else if (lexical_diversity_index_value == "Guiraud's R (lemmas)" && sampling_method_value == "Equal text") {
    guirauds_r_equal_text_lemmas();
  } else if (lexical_diversity_index_value == "Uber U" && sampling_method_value == "Whole text") {
    uber_u_whole_text();
  } else if (lexical_diversity_index_value == "Uber U (lemmas)" && sampling_method_value == "Whole text") {
    uber_u_whole_text_lemmas();
  } else if (lexical_diversity_index_value == "Uber U" && sampling_method_value == "Split text") {
    uber_u_split_text();
  } else if (lexical_diversity_index_value == "Uber U (lemmas)" && sampling_method_value == "Split text") {
    uber_u_split_text_lemmas();
  } else if (lexical_diversity_index_value == "Uber U" && sampling_method_value == "Equal text") {
    uber_u_equal_text();
  } else if (lexical_diversity_index_value == "Uber U (lemmas)" && sampling_method_value == "Equal text") {
    uber_u_equal_text_lemmas();
  }
});