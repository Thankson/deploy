$('#commond').click(function(){
    var linkk;
    linkk = "/commondexe"
    $.get(linkk, $("#form_commond").serialize(), function(data){
        $('#things').html('执行结果: ' +  JSON.stringify(data));
    });
});
//see: http://www.w3school.com.cn/jquery/ajax_serialize.asp


var a = $('#test-link');
a.click(function () {
    alert('Hello!');
});
