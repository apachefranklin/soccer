$(function(e){
    var main_tiltle_page=$('title').text();
    /**
     * cette focntion ira chercher les notifcations des utilisateurs 
     * dans la base de donnees
     * @author apachefranklin
     */

     function find_current_notification()
     {
         $.get(site_url()+"/notification/find_for_current_session",{},function(r){
            var len=r.length;
            if(len==0){
                $(".notification sup").text("");
                $("title").text(main_tiltle_page);
            }
            else{
                
                var title="("+len+")"+main_tiltle_page;
                $("title").text(title);
                $(".notification sup").text(len);

                $("#menu-notfication").html("");
                var toshow=(len>=8)?7:len;
                var html_menu="<ul>";
                for(var i=0;i<toshow;i++){
                    html_menu+="<li><a href='"+r[i].notification_url+"'>"+
                        r[i].notification_text
                    +"</a></li>";
                }
                html_menu+="</ul>";
                $("#menu-notification").html(html_menu);
            }
           
         },"json");
     }

     find_current_notification();
     setInterval(function(){
         find_current_notification();
     },60000);
});