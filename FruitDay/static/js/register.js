$(function () {

    // 表示手機號是否已經被註冊過的狀態值
    // var registStatus = 1;
    window.registStatus = 1;

    // 1. 為uphone控件綁定blur事件
    $("input[name='uphone']").blur(function () {
        // 如果文本框內沒有任何東西則返回
        if ($(this).val().trim().length == 0){
            return;
        }
        // 如果文本框內有數據的話則發送ajax請求判斷數據是否存在
        $.get(
            '/check_uphone/',
            {'uphone': $(this).val()},
            function (data) {
                $("#uphone-tip").html(data.msg);
                // 為registStatus賦值，以便在提交表單時使用
                window.registStatus = data.status;
            }, 'json'
        );
    });

    // 2. 為#formReg表單元素綁定submit事件
    $("#formReg").submit(function () {
        // 判斷registStatus的值，決定表單是否要被提交
        if (window.registStatus == 1){
            return false;
        }
        return true;
    })
});