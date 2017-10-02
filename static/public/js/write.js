$(document).ready(function() {
    $(".publish").click(function () {
        $("input[name='status']").val("P");
        $("form").submit();
    });

    $(".draft").click(function () {
        $("input[name='status']").val("D");
        $("form").submit();
    });


      //preview-content,category,title
    //var categoryItem = document.getElementById("id_category");
    //var alloptions = categoryItem.options[2].text;
    //console.log(alloptions)
    //$("#preview-category").html(alloptions)

    var titleItem = $("#id_title");
    $("#preview-title").html(titleItem.val())
    var contentInput = $("#id_content");
       // $("#preview-content").html(marked(contentItem.val()))

        function setContent(value){
            var markedContent = marked(value)
            $("#preview-content").html(markedContent)
            $("#preview-content img").each(function(){
                $(this).addClass('img-responsive')
            })
        }

        setContent(contentInput.val())

        contentInput.keyup(function(){
            var newContent = $(this).val()
            setContent(newContent)
        })

        //preview-title
        var titleInput = $("#id_title");

        function setTitle(value){
            $("#preview-title").html(value)
        }

        setTitle(titleInput.val())

        titleInput.keyup(function(){
            var newTitle = $(this).val()
            setTitle(newTitle)
        })
});
