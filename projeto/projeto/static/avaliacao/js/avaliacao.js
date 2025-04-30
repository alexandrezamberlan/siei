
function calcularNotaAvaliadorResponsavel(){
    let media = (parseInt($("#id_merito_relevancia_responsavel").val()) +
                 parseInt($("#id_merito_contribuicao_responsavel").val())+
                 parseInt($("#id_merito_metodologia_responsavel").val())+
                 parseInt($("#id_merito_fundamentacao_responsavel").val())+
                 parseInt($("#id_merito_clareza_responsavel").val())+
                 parseInt($("#id_merito_referencias_responsavel").val())+
                 parseInt($("#id_merito_resultados_responsavel").val())+
                 parseInt($("#id_merito_conclusao_responsavel").val())
                ) / 8;

    $("#id_nota_final_responsavel, #id_media_final_responsavel").val(media.toFixed(1));
    calcularMediaFinal();
}

function calcularNotaAvaliadorSuplente(){
    let media = (parseInt($("#id_merito_relevancia_suplente").val()) +
                 parseInt($("#id_merito_contribuicao_suplente").val())+
                 parseInt($("#id_merito_metodologia_suplente").val())+
                 parseInt($("#id_merito_fundamentacao_suplente").val())+
                 parseInt($("#id_merito_clareza_suplente").val())+
                 parseInt($("#id_merito_referencias_suplente").val())+
                 parseInt($("#id_merito_resultados_suplente").val())+
                 parseInt($("#id_merito_conclusao_suplente").val())
                ) / 8;

    $("#id_nota_final_suplente, #id_media_final_suplente").val(media.toFixed(1));
    calcularMediaFinal();
}

function calcularNotaAvaliadorConvidado(){
    let media = (parseInt($("#id_merito_relevancia_convidado").val()) +
                 parseInt($("#id_merito_contribuicao_convidado").val())+
                 parseInt($("#id_merito_metodologia_convidado").val())+
                 parseInt($("#id_merito_fundamentacao_convidado").val())+
                 parseInt($("#id_merito_clareza_convidado").val())+
                 parseInt($("#id_merito_referencias_convidado").val())+
                 parseInt($("#id_merito_resultados_convidado").val())+
                 parseInt($("#id_merito_conclusao_convidado").val())
                ) / 8;

    $("#id_nota_final_convidado, #id_media_final_convidado").val(media.toFixed(1));
    calcularMediaFinal();
}

function calcularMediaFinal(){
    let media = 0;
    if($("#id_nota_final_convidado").val()==undefined){
        media = (parseFloat($("#id_nota_final_responsavel").val()) +
                 parseFloat($("#id_nota_final_suplente").val())
                ) / 2;
    }else{
        media = (parseFloat($("#id_nota_final_responsavel").val()) +
                 parseFloat($("#id_nota_final_suplente").val())+
                 parseFloat($("#id_nota_final_convidado").val())
                ) / 3;
    }
    
    $("#id_media_final").val(media.toFixed(2));
}

$(document).ready(function () {
    calcularNotaAvaliadorResponsavel();
    calcularNotaAvaliadorSuplente();
    calcularNotaAvaliadorConvidado();
    calcularMediaFinal();

    $("#id_merito_relevancia_responsavel, #id_merito_contribuicao_responsavel, #id_merito_metodologia_responsavel, #id_merito_fundamentacao_responsavel, #id_merito_clareza_responsavel, #id_merito_referencias_responsavel, #id_merito_resultados_suplente, #id_merito_conclusao_responsavel").on('change', function(){
        calcularNotaAvaliadorResponsavel();
    });

    $("#id_merito_relevancia_suplente, #id_merito_contribuicao_suplente, #id_merito_metodologia_suplente, #id_merito_fundamentacao_suplente, #id_merito_clareza_suplente, #id_merito_referencias_suplente, #id_merito_resultados_suplente, #id_merito_conclusao_suplente").on('change', function(){
        calcularNotaAvaliadorSuplente();
    });

    $("#id_merito_relevancia_convidado, #id_merito_contribuicao_convidado, #id_merito_metodologia_convidado, #id_merito_fundamentacao_convidado, #id_merito_clareza_convidado, #id_merito_referencias_convidado, #id_merito_resultados_convidado, #id_merito_conclusao_convidado").on('change', function(){
        calcularNotaAvaliadorConvidado();
    });
});