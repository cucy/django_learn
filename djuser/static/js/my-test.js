$(function () {
    // 模态框状态        m
    $('.bd-example-modal-lg')
        .on('show.bs.modal', function (e) {
            console.log('show.bs.modal 显示之前')
        })
        .on('shown.bs.modal', function () {
            console.log(' shown.bs.modal 已经显示')
        })
        .on('hide.bs.modal', function () {
            console.log('    hide.bs.modal 隐藏之前')
        })
        .on('hidden.bs.modal', function () {
            console.log("  hidden.bs.modal 隐藏以后")
        });

    // 请求成功后
    $(document).on('after.success.ic', function (evt, elt, data, textStatus, xhr, requestId) {
        console.log("evt", evt);
        console.log("elt", elt);
        console.log("data", data);
        console.log("textStatus", textStatus);
        console.log("xhr", xhr);
        console.log("requestId", requestId);
    });

    // intercooler 请求成功，错误返回信息
    $(document)
        .on("ajaxSuccess.ic", function (event, request, settings) {

            console.log(223111111111111, "请求成功");
            console.log($(event));
            console.log(request.status);
            console.log(request);
            console.log($(settings));


            if (request.status === 201) {

                // 修改用户信息 清空内容
                result_containe_obj.html("")
            }

        })
        .on("ajaxError.ic", function (event, request, settings) {
            console.log('没有');
            console.log($(event));
            console.log(request.status === 404);
            console.log($(settings));
        });

    // 成功事件
    $(document).on('success.ic', function (evt, elt, data, textStatus, xhr, requestId) {
        console.log("success evt", evt);  // 事件
        console.log("success elt", elt);         // 当前点检的节点class选择
        console.log("success data", data);  // 返回的数据
        console.log("success textStatus", textStatus);    // 成功状态码 简语
        console.log("success xhr", xhr);      // status
        console.log("success requestId", requestId);
    });


});