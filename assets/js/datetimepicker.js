/**
 * Created 2014 by Janusz Skonieczny
 */
$(function () {
    $('.widget-datetime').datetimepicker({
        language: 'pl',
        format: 'YYYY-MM-DD hh:mm'
    });
    $('.widget-date').datetimepicker({
        language: 'pl',
        format: 'YYYY-MM-DD',
        pickTime: false
    });
});
