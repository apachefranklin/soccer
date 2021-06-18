(function($){
    $(function() { 
        /**
         * Fonction pour faire tout cocher et tout decocher
         * @author protogons
         * @link https://wwww.protogons.com
         * @version 1.0
         * @since 1.0
         */
        $(".uncheck_checkall").change(function(e) {
            if ($(this).prop("checked") === true) {
                $(".role").each(function() {
                    $(this).prop("checked", true);
                });
                $(".text_check_all").text("Tout decocher");
            } else {
                $(".role").each(function() {
                    $(this).prop("checked", false);
                });
                $(".text_check_all").text("Tout cocher");
            }
        });
        //fin de cette fonction la
        
        /** lorsque l'utilisateur cliquera sur un role
            on verifiera si tout les roles sont ckecke et faire une action
            sinon faire une autre
        */
        $(".role").click(function(e) {
            var one_checked = false;
            var all_ckecked = false;
            var i = 0;
            var j = 0;
            $(".role").each(function(e) {
                if ($(this).prop("checked") === true) {
                    one_checked = true;
                    i = i + 1;
                }
                j = j + 1;
            });
            if (j == i) {
                //donc tout est coche
                $(".uncheck_checkall").prop("checked", true);
                $(".text_check_all").text("Tout decocher");
            } else {
                $(".uncheck_checkall").prop("checked", false);
                $(".text_check_all").text("Tout cocher");
            }
        });
        //fin de la gestion du changment d'un role
    
        //gestion de la soummission du formualaire
        /**
         * Fonction permettant de gerer la jout d'un utilisateur via ajax
         *@author protogons
         *@version 1.0 
         *@since 1.0
         *
         */
        
        $(".form_add_user").on("submit",function(e){
           e.preventDefault();
            var form =$(this);
            //maintenant nous devons recuperer les roles
            var i=0;
            var roles={};
                $(".role").each(function(e){
                    if($(this).prop("checked")===true){
                        roles[$(this).val()]=$(this).val().trim();                   
                    }
                });
            var user_data=new FormData(this);
            user_data.set("user_roles",roles);
            $.ajax({
                url:$(".form_add_user").attr("action"),
                data:user_data,
                contentType: false,
                  cache: false,
                  processData: false,
                  dataType: "json",
                  method:"POST",
                  success:function(result){
                    display_result(result);
                    form.trigger("reset");
                  },
                  error:function(r){
                      alert("une erreur s'est produite");
                  }
            });});
    
        /**
         * Maintenant ce code va permmetre de rechercher
         */
        $("#searchuser").keyup(function(){
            var pattern=$(this).val().trim();
            $.post(site_url()+"/admin/rest/find_user",{searchuser:pattern},function(r){
                $(".user-list").html("");
                var l=r.length;
                if(l!=0){
                    var h=$(".user-show-model").clone();
                    var imgsrc=$(".user-profil",h).prop("src");
                    var editlink=$(".user-edit",h).prop("href");
                    var viewlink=$(".user-view",h).prop("href");
                    var i=0;
                    for(i=0;i<l;i++){
                        var g=h;
                        $(".user-last-connexion",g).text('bonjour'+i);
                        $(".user-name",g).text(r[i].name+" "+r[i].last_name);
                        $(".user-phone",g).text(r[i].phone);
                        $(".user-email",g).text(r[i].email);
                        $(".user-profil",g).prop("src",imgsrc+r[i].profil);
                        $(".user-edit",g).prop("href",editlink+(r[i].name.replace(" ","-"))+"-"+r[i].id);
                        $(".user-view",g).prop("href",viewlink+(r[i].id));
                        $(".user-list").append(g.html());
                    }
                }
                else{
                    $(".user-list").html("<h1 class='header-text'>Aucun n'utilisateur n'a ete trouve</h1>");
                }
                
            },"json");
        });
    
    
        //maintenant on gere le cas de la modification des utilisateurs
        $(".form_edit_user").submit(function(){
          
            var name=$("#user_name").val().trim();
            var last_name=$("#user_last_name").val().trim();
            var phone=$("#user_phone").val().trim();
            var email=$("#user_email").val().trim();
            var address=$("#user_address").val().trim();
            var sex=$("#user_sex").val().trim();
            var id=$("#user_id").val().trim();
            //maintenant nous devons recuperer les roles
            var i=0;
            var roles={};
                $(".role").each(function(e){
                    if($(this).prop("checked")===true){
                        roles[$(this).val()]=$(this).val().trim();                   
                    }
                });
            $.post($(this).attr("action"),{
                user_id:id,user_name:name,user_last_name:last_name,user_phone:phone,user_email:email,user_address:address,user_sex:sex,user_roles:roles
            },function(r){ 
                if(r==true){
                    showModalResult("Modification effectue avec success",true);
                }
                else{
                    showModalResult("Echec de modification de l'utilisateur",false);
                }
            },"json");
            return false;
        })
    });
    
    
})(jQuery);