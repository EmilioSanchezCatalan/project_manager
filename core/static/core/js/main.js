"use strict";

/**
 * Muestra u oculta un bloque vinculado a un checkbox
 * @param {HTMLInput} checkbox  checkbox que decidirá si mostrar o no el input
 * @param {HTMLInput} input     input que se mostrará o se ocultará (uno de ellos)
 * @param {Array<HTMLInput>} exceptionsRequired excepciones de valores que no serán requeridos
 */
function inputShowHiddenBlockFunction(checkbox, input, exceptionsRequired=[]) {
    if(checkbox.is(':checked')) {   
        input.closest(".row.block").css('display', 'flex');
        input.closest(".row.block").find("input").prop('required', true);
        input.closest(".row.block").find("select").prop('required', true);
    } else {
        input.closest(".row.block").css('display', 'none');
        input.closest(".row.block").find("input").removeAttr("required")
        input.closest(".row.block").find("select").removeAttr("required")

    }
    exceptionsRequired.forEach(element => {
        element.removeAttr("required")
    });
}

/**
 * Muestra u oculta un input vinculado a un checkbox
 * @param {HTMLInput} checkbox  checkbox que decidirá si mostrar o no el input
 * @param {HTMLInput} input     input que se mostrará o se ocultará
 */
function inputShowHiddenFunction(checkbox, input) {
    if(checkbox.is(':checked')) {   
        input.closest(".form-group.row").css('display', 'flex');
    } else {
        input.closest(".form-group.row").css('display', 'none');
    }
}

/**
 * Modifica el formulario añadiendo y elmininado los formaularios de alumnos
 * en función de si es un trabajo en equipo o no, o si se van a establecer el alumno
 * asignado al proyecto o no.
 */
function setStudentsTfg() {
    if($("#alumnoCheck").is(':checked')) {
        $("#student1").css('display', 'flex')
        $("#student1").find("input").prop('required', true);

        if ($("#id_is_team").is(':checked')) {
            $(".student_number").css('display', 'inline')
            $("#student2").css('display', 'flex')
            $("#student2").find("input").prop('required', true);
        } else {
            $(".student_number").css('display', 'none')
            $("#student2").css('display', 'none')
            $("#student2").find("input").removeAttr("required")
        }
    } else {
        $("#student1").css('display', 'none')
        $("#student1").find("input").removeAttr("required")
        $("#student2").css('display', 'none')
        $("#student2").find("input").removeAttr("required")
    }
    
}

/**
 * Modifica el formulario añadiendo y elmininado los formaularios de alumnos
 * en función de si es un trabajo en equipo o no, o si se van a establecer el alumno
 * asignado al proyecto o no.
 */
function setStudentsTfm() {
    if($("#alumnoCheck").is(':checked')) {
        $("#student").css('display', 'flex')
        $("#student").find("input").prop('required', true);
    } else {
        $("#student").css('display', 'none')
        $("#student").find("input").removeAttr("required")
    }
    
}


/**
 * Actualiza la lista de checkbox de un bloque de checkbox en función de una lista
 * @param {String} block_checkbox_id    identificador del block de checkboxes
 * @param {Object} data_list            objecto con la lista de chexboxs
 */
function updateListCheckboxes(block_checkbox_id, data_list) {
    if (data_list.length > 0) {
        $("#" + block_checkbox_id).css("display", "flex")
        $("#" + block_checkbox_id).children(".col-sm-12.row").empty()
        $.each(data_list, function(key, value) {
            let checkbox = $(`
            <div class="form-check col-sm-6 form-check-label-custom">
                <label for="id_skills_${key}">
                    <input type="checkbox" name="skills" value="${value.id}" class="form-check-input" id="id_skills_${key}">
                    ${value.name} - ${value.text}
                </label>
            </div>
            `)
            $("#" + block_checkbox_id).children(".col-sm-12.row").append(checkbox)
        })
    } else {
        $("#" + block_checkbox_id).css("display", "none")
    }
}

/**
 * Actualiza las opciones de un input select dado una lista
 * @param {String} select_id    identificardor del selector que se quiere actualizar
 * @param {Object} data_list    lista con las nuevas opciones
 * @param {String} empty_label  opción por defecto
 */
function updateSelect(select_id, data_list, empty_label="Selecciona una opción") {
    if (data_list.length > 0) {
        $("#" + select_id).closest(".form-group.row").css("display", "flex")
        $("#" + select_id).empty()
        $("#" + select_id).append($("<option></option>").attr("value", "").text(empty_label))
        $.each(data_list, function(key, value) {
            $("#" + select_id).append($("<option></option>").attr("value", value.id).text(value.name))
        })
    } else {
        $("#" + select_id).closest(".form-group.row").css("display", "none")
    }
}

/**
 * Obtiene una lista en json de la dirección de una api mediante ajax
 * @param {String} full_url   ruta absoluta de la API
 * @param {Number} pk         identificador pasado a la API
 */
function getListApi(full_url, pk) {
    return new Promise((resolve, reject) => {
        if ( !isNaN(parseInt(pk)) ) {

            $.ajax({
                method: "GET",
                url: full_url + "/" + pk,
                success: function(data) {
                    resolve(data)
                },
                error: function(error) {
                    reject(error)
                }
            })
        } else {
            resolve([])
        }
    });
}

/**
 * Oculta todos los selectores que no posean mas que la opcion por 
 * defecto
 */
function cleanEmptySelects() {
    $.each($("select"), function(key, value) {
        if ($(value).children("option").length <= 1) {
            $(this).closest(".form-group.row").css("display", "none")
        }
    });
}

/**
 * Cambia el estado de los filtros extendidos, mostrandolos y ocultandolos
 * @param {HTMLElement} button      botton con el que cambiará el estado
 * @param {HTMLDivElement} divBlock block con la extensión de los filtros
 */
function changeExtendsFiltersState(button, divBlock) {
    button.children("i").toggle()
    $("hr").toggle()
    divBlock.toggle()
  }

/**
 * Limipia los atributos required de un AdminFileWidget
 * @param {String} field nombre del campo del formulario
 * @param {String} prefix prefijo si fuera necesario
 */
function cleanFileFieldRequired(field, prefix="") {
    if (prefix != "") { 
        prefix += "-";
    }
    $("#id_"+prefix+field).removeAttr("required");
    $("#"+prefix+field+"-clear_id").removeAttr("required");
}