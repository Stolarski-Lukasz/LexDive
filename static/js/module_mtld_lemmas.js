import {
    create_element,
    remove_element,
    remove_children
  } from "./module_elements.js"
  
import { create_separator, create_table_skeleton } from "./module_blocks.js"

var user_text = document.getElementById('exampleFormControlTextarea1');
var lexical_diversity_start_button = document.getElementById("lexical_diversity_start_button");
var text_statistics_tab = document.getElementById("profile-tab")
  
  
  
export function mtld_whole_text_lemmas() {

  // deleting any previous types table
  remove_element("types_table");

  let xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function (e) {
    if (xhr.readyState == 4 && xhr.status == 200) {
      remove_element("the_spinner");
      // obtaining the json response
      let json_response = xhr.responseText;
      // transforming the json response to js object
      let response_object = JSON.parse(json_response);
      let mtld_value = response_object.mtld_value;
      let number_of_tokens = response_object.number_of_tokens;
      let factor_count_forward = response_object.factor_count_forward;
      let forward_mtld = response_object.forward_mtld;
      let factor_count_backward = response_object.factor_count_backward;
      let backward_mtld = response_object.backward_mtld;

      // creating ld results elements
      var horizontal_line = document.createElement("hr")
      horizontal_line.id = "ld_results_horizontal_line"
      lexical_diversity.insertBefore(horizontal_line, ld_results_grandparent);

      create_element({ tag: "div", className: "col-10 text-left", id: "ld_results_parent", parent_id: "ld_results_grandparent" });
      create_element({ tag: "h4", innerText: "The value of MTLD (with lemmas instead of types) in the whole text: " + mtld_value, parent_id: "ld_results_parent" });
      create_separator("ld_results_parent");
      create_element({ tag: "p", style_margin: "1px", innerText: "The number of word tokens in the whole text: " + number_of_tokens, parent_id: "ld_results_parent" });
      create_element({ tag: "p", style_margin: "1px", innerText: 'The number of factors in the "forwards" processing: ' + factor_count_forward, parent_id: "ld_results_parent" });
      create_element({ tag: "p", style_margin: "1px", innerText: 'The value of MTLD in the "forwards" processing: ' + forward_mtld, parent_id: "ld_results_parent" });
      create_element({ tag: "p", style_margin: "1px", innerText: 'The number of factors in the "backwards" processing: ' + factor_count_backward, parent_id: "ld_results_parent" });
      create_element({ tag: "p", style_margin: "1px", innerText: 'The value of MTLD in the "backwards" processing: ' + backward_mtld, parent_id: "ld_results_parent" });

      lexical_diversity_start_button.disabled = false;
      text_statistics_tab.disabled = false;
    };
  };

  create_element({tag: "div", className: "spinner-border text-primary", role: "status", id: "the_spinner", parent_id: "ld_results_grandparent"});
  var user_text_with_punctuation = user_text.value;
  var user_text_without_punctuation = user_text_with_punctuation.match(/[^_\W]+/g).join(' ');
  var user_text_without_punctuation = user_text_without_punctuation.toLowerCase();

  lexical_diversity_start_button.disabled = true;
  text_statistics_tab.disabled = true;

  xhr.open('POST', '/count_mtld_whole_text_lemmas/', true);
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
  var data = "user_text=" + user_text_without_punctuation;
  xhr.send(data);
};




export function mtld_whole_text_lemmas_pncorrection() {

  // deleting any previous types table
  remove_element("types_table");

  let xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function (e) {
    if (xhr.readyState == 4 && xhr.status == 200) {
      remove_element("the_spinner");
      // obtaining the json response
      let json_response = xhr.responseText;
      // transforming the json response to js object
      let response_object = JSON.parse(json_response);
      let mtld_value = response_object.mtld_value;
      let number_of_tokens = response_object.number_of_tokens;
      let factor_count_forward = response_object.factor_count_forward;
      let forward_mtld = response_object.forward_mtld;
      let factor_count_backward = response_object.factor_count_backward;
      let backward_mtld = response_object.backward_mtld;

      // creating ld results elements
      var horizontal_line = document.createElement("hr")
      horizontal_line.id = "ld_results_horizontal_line"
      lexical_diversity.insertBefore(horizontal_line, ld_results_grandparent);

      create_element({ tag: "div", className: "col-10 text-left", id: "ld_results_parent", parent_id: "ld_results_grandparent" });
      create_element({ tag: "h4", innerText: "The value of MTLD (with lemmas instead of types and proper names correction) in the whole text: " + mtld_value, parent_id: "ld_results_parent" });
      create_separator("ld_results_parent");
      create_element({ tag: "p", style_margin: "1px", innerText: "The number of word tokens (without proper names) in the whole text: " + number_of_tokens, parent_id: "ld_results_parent" });
      create_element({ tag: "p", style_margin: "1px", innerText: 'The number of factors in the "forwards" processing: ' + factor_count_forward, parent_id: "ld_results_parent" });
      create_element({ tag: "p", style_margin: "1px", innerText: 'The value of MTLD in the "forwards" processing: ' + forward_mtld, parent_id: "ld_results_parent" });
      create_element({ tag: "p", style_margin: "1px", innerText: 'The number of factors in the "backwards" processing: ' + factor_count_backward, parent_id: "ld_results_parent" });
      create_element({ tag: "p", style_margin: "1px", innerText: 'The value of MTLD in the "backwards" processing: ' + backward_mtld, parent_id: "ld_results_parent" });

      lexical_diversity_start_button.disabled = false;
      text_statistics_tab.disabled = false;
    };
  };

  create_element({tag: "div", className: "spinner-border text-primary", role: "status", id: "the_spinner", parent_id: "ld_results_grandparent"});
  var user_text_with_punctuation = user_text.value;
  var user_text_without_punctuation = user_text_with_punctuation.match(/[^_\W]+/g).join(' ');
  var user_text_without_punctuation = user_text_without_punctuation.toLowerCase();

  lexical_diversity_start_button.disabled = true;
  text_statistics_tab.disabled = true;

  xhr.open('POST', '/count_mtld_whole_text_lemmas_pncorrection/', true);
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
  var data = "user_text=" + user_text_without_punctuation;
  xhr.send(data);
};