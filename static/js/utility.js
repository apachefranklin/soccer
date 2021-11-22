

$(function(e){
    //validateur de formulaire universelle
    function display_result(result,form_id="",pso="mid-center"){
        $(".jq-toast-wrap *").hide();
        var icon_d="success";
        if(result["status"]==false){
            icon_d="error";
        }
            $.toast({
                text:result["msg"],
                icon:icon_d,
                hideAfter:false,
                position:pso,
                afterHidden:function(){
                    if(result['status']==true){
                        $(form_id).trigger("reset")
                        if(result["redirect"]!=undefined){
                            window.location.replace(result['redirect']);
                        }
                    }
                }
            });
            
            if(result["redirect"]!=undefined){
                window.location.replace(result['redirect']);
            }
    }
    
    $(".ajax-form").on("submit",function(e){
        e.preventDefault();
        $("#pageloader").fadeIn();
        var form_data=new FormData(this);
        var form_title=$(this).attr("form_title");
        var form_method=$(this).attr("method");
        var form_id=$(this).attr("id")
        $.ajax({
            url:$(this).attr("action"),
            method: form_method,
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            dataType: "json",
            success:function(result){
                $("#pageloader").fadeOut();
                display_result(result)
            },
            error:function(result){
                $("#pageloader").fadeOut();
                $.toast({
                    heading:form_title,
                    text:"Une erreur innatendue s'est produite",
                    icon:"error"
                });
            }
    });
});
//fin du submitteur universel
});

jQuery(function(e){
    maxheight = 0;
    tabs = jQuery('.make-same-height .tab-pane');
    jQuery.each(tabs, function() {
        this.classList.add("active"); /* make all visible */
        maxheight = (this.clientHeight > maxheight ? this.clientHeight : maxheight);
        if (!jQuery(this).hasClass("show")) {
            this.classList.remove("active"); /* hide again */
        }
    });
    jQuery.each(tabs, function() {
        jQuery(this).height(maxheight);
    });
//jquery for sidebar toggle
$(".sidenav-toggle").click(function(){
    var target_id=$(this).attr("target");
    if(target_id!=""){
        $("#"+target_id).toggle("slide:left"); 
    }
});
$(".close").click(function(){
    
    var target_id=$(this).attr("target");
    if(target_id!=""){
        $("#"+target_id).toggle("slide:right"); 
    }
});
$(".nocontent").click(function(){
    $(this).parent().toggle("slide:rigth")
});
    //fonction formulaire contact
$("#contact_form").on("submit",function(e){
    e.preventDefault();
    var user_data=new FormData(this);
    $.ajax({
        url:$(this).attr("action"),
        data:user_data,
        cache:false,
        contentType:false,
        processData:false,
        dataType:"json",
        method:"POST",
        success:function(e){
            display_result(e,"#contact_form")
            $("#form_contact").trigger("reset")
        },
        error:function(e){
            $.toast({
                "icon":"error",
                "text":"une erreur innatendue s'est produite"
            })
        }
    })
});
});
