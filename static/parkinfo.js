let $activity=$(".activity");
$("#activitiesShowLess").hide();
if($activity.length > 10){
    $activity.slice(10,$activity.length).hide();
}
if($activity.length <= 10){
    $("#activitiesLodeMore").hide();
}

$("#activitiesLodeMore").on("click",function () {
    $activity.show();
    $("#activitiesLodeMore").hide();
    $("#activitiesShowLess").show();
});

$("#activitiesShowLess").on("click",function () {
    $activity.slice(10,$activity.length).hide();
    $("#activitiesLodeMore").show();
    $("#activitiesShowLess").hide();
});
