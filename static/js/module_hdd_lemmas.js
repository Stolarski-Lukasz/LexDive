import {
    create_element,
    remove_element,
    remove_children
  } from "./module_elements.js"
  
  
  var user_text = document.getElementById('exampleFormControlTextarea1');
  var lexical_diversity_start_button = document.getElementById("lexical_diversity_start_button");
  var text_statistics_tab = document.getElementById("profile-tab")
  
  
  
  
  
  export function hdd_whole_text_lemmas() {
  
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
        let hdd_value = response_object.hdd_value;
  
        // creating ld results elements
        var horizontal_line = document.createElement("hr")
        horizontal_line.id = "ld_results_horizontal_line"
        lexical_diversity.insertBefore(horizontal_line, ld_results_grandparent);
  
        create_element({ tag: "div", className: "col-10 text-left", id: "ld_results_parent", parent_id: "ld_results_grandparent" });
        create_element({ tag: "h4", innerText: "The value of HDD (with lemmas instead of types) in the whole text: " + hdd_value, parent_id: "ld_results_parent" });
  
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
  
    xhr.open('POST', '/count_hdd_whole_text_lemmas/', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
    var data = "user_text=" + user_text_without_punctuation;
    xhr.send(data);
  };