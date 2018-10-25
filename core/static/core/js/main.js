"use strict";
$(document).ready(function(){

    // Inicialización del estado del formulario
    inputShowHiddenFunction($("#tutorCheck"), $("#tutorInput"));
    inputShowHiddenFunction($("#teamCheck"), $("#inputNumberStudent"));

    // Añade la funcionalidades a un evento
    $("#tutorCheck").click(() => {
        inputShowHiddenFunction($("#tutorCheck"), $("#tutorInput"))
    });
    $("#teamCheck").click(() => {
        inputShowHiddenFunction($("#teamCheck"), $("#inputNumberStudent"))
        initNoTeam($("#teamCheck"));
    });

    $("#refreshNumberStudents").click(() => {
        generateSelect($("#inputNumberStudent"), $("#alumno"));
    })
});

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
 * Elimina los selectores de grupo y habilita el selector alumno único
 * @param {HTMLInput} checkbox  checkbox que decidirá si mostrar o no el input
 */
function initNoTeam(checkbox) {
if(!checkbox.is(':checked')) {
    $("#alumno").css("display", "flex");
    $("div[id^='alumnoL']").remove();
} else {
    generateSelect($("#inputNumberStudent"), $("#alumno"));
}
} 

/**
 * Genera el número de selectores alumno en función del número de alumnos introducidos.
 * @param {HTMLInput}   inputNumber     input tipo number con la cantidad de selectores a generar.
 * @param {HTMLDiv}     brotherElement  div apartir del cual se genraran los selectores y se clonaran.
 */
function generateSelect(inputNumber, brotherElement) {
    if (inputNumber.val() > 1) {
        $("div[id^='alumnoL']").remove();
        brotherElement.css("display", "none");
        for( let i = inputNumber.val(); i>=1; i--) {
            var new_element = `
                <div class="row" id="alumnoL${i}">
                    <div class="col-sm-12">
                        Alumno<span class="number">${i}</span>
                    </div>
                    <div class="pl-3 pl-sm-5 col-sm-12">
                        <div class="form-group row">
                        <label for="alumnoNameInput${i}" class="col-sm-2 col-form-label">Nombre:</label>
                        <div class="col-sm-10">
                            <input type="text" name="name" id="alumnoNameInput${i}" class="form-control">
                        </div>
                        </div>
                        <div class="form-group row">
                        <label for="alumnoDireccionInput${i}" class="col-sm-2 col-form-label">Dirección:</label>
                        <div class="col-sm-10">
                            <input type="text" name="address" id="alumnoDireccionInput${i}" class="form-control">
                        </div>
                        </div>
                        <div class="form-group row">
                        <label for="alumnoDniInput${i}" class="col-sm-2 col-form-label">DNI:</label>
                        <div class="col-sm-10">
                            <input type="text" name="dni" id="alumnoDniInput${i}" class="form-control">
                        </div>
                        </div>
                        <div class="form-group row">
                        <label for="alumnotlfInput${i}" class="col-sm-2 col-form-label">Teléfono:</label>
                        <div class="col-sm-10">
                            <input type="text" name="tlf" id="alumnotlfInput${i}" class="form-control">
                        </div>
                        </div>
                    </div>
                </div>
            `;
            brotherElement.after(new_element);
        }
    } else {
        alert('Es necesario que el numero de alumnos sea mayor de 1');
    }
}