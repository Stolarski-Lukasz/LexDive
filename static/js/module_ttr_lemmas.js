import {
    create_element,
    remove_element,
    remove_children
  } from "./module_elements.js"
  
  import { create_separator, create_table_skeleton } from "./module_blocks.js"
  
  var user_text = document.getElementById('exampleFormControlTextarea1');
  var lexical_diversity_start_button = document.getElementById("lexical_diversity_start_button");
  var text_statistics_tab = document.getElementById("profile-tab")
  
  
  
  
  
  export function ttr_whole_text_lemmas() {
  
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
        let ltr_value = response_object.ltr_value;
        let number_of_tokens = response_object.number_of_tokens;
        let number_of_lemmas = response_object.number_of_lemmas;
  
        // creating ld results elements
        var horizontal_line = document.createElement("hr")
        horizontal_line.id = "ld_results_horizontal_line"
        lexical_diversity.insertBefore(horizontal_line, ld_results_grandparent);
  
        create_element({ tag: "div", className: "col-10 text-left", id: "ld_results_parent", parent_id: "ld_results_grandparent" });
        create_element({ tag: "h4", innerText: "The value of TTR (with lemmas instead of types) in the whole text: " + ltr_value, parent_id: "ld_results_parent" });
        create_separator("ld_results_parent");
        create_element({ tag: "p", style_margin: "1px", innerText: "The number of word tokens in the whole text: " + number_of_tokens, parent_id: "ld_results_parent" });
        create_element({ tag: "p", style_margin: "1px", innerText: "The number of lemmas in the whole text: " + number_of_lemmas, parent_id: "ld_results_parent" });
  
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
  
    xhr.open('POST', '/count_ttr_whole_text_lemmas/', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
    var data = "user_text=" + user_text_without_punctuation;
    xhr.send(data);
  };
  
  
  
  
  
  export function ttr_split_text_lemmas() {
  
    var sample_length_value = sample_length.value;
    sample_length_value = Number(sample_length_value);
    var size_of_subsamples_value = size_of_subsamples.value;
    size_of_subsamples_value = Number(size_of_subsamples_value);
  
    // Warnings
    if (sample_length_value > user_text.value.split(" ").length) {
      create_element({ tag: "p", id: "warning", innerText: 'The sample length should not be larger than the length of the text in the "File View" section.', parent_id: "ld_results_grandparent" });
    } else if (size_of_subsamples_value > sample_length_value) {
      create_element({ tag: "p", id: "warning", innerText: "The size of subsamples should not exceed the sample length. The sample length is currently set at " + sample_length.value + ", and the size of sub-samples should not exceed this number.", parent_id: "ld_results_grandparent" });
    } else {
  
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
          let ttr_value = response_object.ttr_value;
          let generated_sample_length = response_object.generated_sample_length;
          let size_of_subsamples_used = response_object.size_of_subsamples_used;
          let number_of_lemmas = response_object.number_of_lemmas;
          let number_of_subsamples = response_object.number_of_subsamples;
          let size_of_gaps = response_object.size_of_gaps;
          let subsamples_list = response_object.subsamples_list;
          let subsamples_array_formatted = [];
  
  
          // formatting words in subsamples to be seprated by ", "
          for (var key_name in subsamples_list) {
            subsamples_list[key_name][1] = subsamples_list[key_name][1].join(", ");
          };
  
          // creating ld results elements
          var horizontal_line = document.createElement("hr")
          horizontal_line.id = "ld_results_horizontal_line"
          lexical_diversity.insertBefore(horizontal_line, ld_results_grandparent);
  
          create_element({ tag: "div", className: "col-10 text-left", id: "ld_results_parent", parent_id: "ld_results_grandparent" });
          create_element({ tag: "h4", innerText: "The value of TTR (with lemmas instead of types) in the generated sample: " + ttr_value, parent_id: "ld_results_parent" });
          create_separator("ld_results_parent");
          create_element({ tag: "p", style_margin: "1px", innerText: "The number of word tokens in the generated sample: " + generated_sample_length, parent_id: "ld_results_parent" });
          create_element({ tag: "p", style_margin: "1px", innerText: "The number of lemmas in the generated sample is: " + number_of_lemmas, parent_id: "ld_results_parent" });
          create_element({ tag: "p", style_margin: "1px", innerText: "The size of each sub-sample: " + size_of_subsamples_used, parent_id: "ld_results_parent" });
          create_element({ tag: "p", style_margin: "1px", innerText: "The number of sub-samples used in the generated sample: " + number_of_subsamples, parent_id: "ld_results_parent" });
          create_element({ tag: "p", style_margin: "1px", innerText: "The size of gaps between sub-samples in the original text: " + size_of_gaps, parent_id: "ld_results_parent" });
          create_separator("ld_results_parent");
  
          // creating table skeleton
          create_table_skeleton("table_parent2", "example");
          
          // creating the table using datatables
          $(document).ready(function () {
            $('#example').DataTable({
              data: subsamples_list,
              columns: [{ title: "Number" }, { title: "Subsample" }]
            });
          });
  
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
  
      xhr.open('POST', '/count_ttr_split_text_lemmas/', true);
      xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
      var data = "user_text=" + user_text_without_punctuation +
        "&sample_length=" + sample_length_value +
        "&size_of_subsamples=" + size_of_subsamples_value;
      xhr.send(data);
    }
  };
  
  
  
  
  export function ttr_equal_text_lemmas() {
  
    var sample_beginning_value = sample_beginning.value;
    sample_beginning_value = Number(sample_beginning_value);
    var sample_length_value = sample_length.value;
    sample_length_value = Number(sample_length_value);
  
    // Warnings
    if (sample_length_value > user_text.value.split(" ").length) {
      create_element({ tag: "p", id: "warning", innerText: 'The sample length should not be larger than the length of the text in the "File View" section.', parent_id: "ld_results_grandparent" });
    } else if ((sample_beginning_value - 1) + sample_length_value > user_text.value.split(" ").length) {
      create_element({ tag: "p", id: "warning", innerText: "The sample cannot be generated either because the size of the sample exceeds the whole text length, or the sample should begin at an earlier word than the one specified. Change one of both of these attributes.", parent_id: "ld_results_grandparent" });
    } else {
  
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
          let ttr_value = response_object.ttr_value;
          let sample_beginning_info = response_object.sample_beginning_info;
          let number_of_tokens = response_object.number_of_tokens;
          let number_of_lemmas = response_object.number_of_lemmas;
          let generated_sample = response_object.generated_sample;
          generated_sample = generated_sample.join(", ");
  
          // creating ld results elements
          var horizontal_line = document.createElement("hr")
          horizontal_line.id = "ld_results_horizontal_line"
          lexical_diversity.insertBefore(horizontal_line, ld_results_grandparent);
  
          create_element({ tag: "div", className: "col-10 text-left", id: "ld_results_parent", parent_id: "ld_results_grandparent" });
          create_element({ tag: "h4", innerText: "The value of TTR (with lemmas instead of types) in the generated sample: " + ttr_value, parent_id: "ld_results_parent" });
          create_separator("ld_results_parent");
          create_element({ tag: "p", style_margin: "1px", innerText: "The number of word tokens in the generated sample: " + number_of_tokens, parent_id: "ld_results_parent" });
          create_element({ tag: "p", style_margin: "1px", innerText: "The number of lemmas in the generated sample: " + number_of_lemmas, parent_id: "ld_results_parent" });
          create_element({ tag: "p", style_margin: "1px", innerText: sample_beginning_info, parent_id: "ld_results_parent" });
  
          create_separator("ld_results_parent");
          // textarea with the generated sample
          create_element({ tag: "div", className: "row", id: "textarea_heading_row", parent_id: "ld_results_parent" });
          create_element({ tag: "div", className: "col-sm", id: "textarea_heading_col", parent_id: "textarea_heading_row" });
          create_element({ tag: "p", id: "textarea_heading", style_margin: "1px", innerText: "Generated sample:", parent_id: "textarea_heading_col" });
          create_element({ tag: "div", className: "row", id: "textarea_row", parent_id: "ld_results_parent" });
          create_element({ tag: "div", className: "col-sm", id: "textarea_col", parent_id: "textarea_row" });
          create_element({ tag: "div", className: "form-group", id: "textarea_formgroup", parent_id: "textarea_col" });
          create_element({ tag: "textarea", className: "form-control", id: "equal_text_generated", rows: "9", innerText: generated_sample, parent_id: "textarea_formgroup" });
  
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
  
      xhr.open('POST', '/count_ttr_equal_text_lemmas/', true);
      xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
      var data = "user_text=" + user_text_without_punctuation +
        "&sample_beginning=" + sample_beginning_value +
        "&sample_length=" + sample_length_value;
      xhr.send(data);
    };
  };