
$("button.before").on("click", function() {
    $("div.comments").slideDown();
});

$("button.after").on("click", function() {
    $("div.comments").slideUp();
});


$("button.define-goals").on("click", function() {
    $("div.goals").slideToggle();
});

$("button.show-goals-stake").on("click", function() {
    $("div.goal-list-stake").slideToggle();
});

$("button.show-goals-business").on("click", function() {
    $("div.goal-list-business").slideToggle();
});

$("button.show-goals-value").on("click", function() {
    $("div.goal-list-value").slideToggle();
});

$("button.show-goals-percept").on("click", function() {
    $("div.goal-list-percept").slideToggle();
});




//$("button.goals").on("click", function() {
//    $("div.goals").slideUp();
//});



$("a.btn.btn-primary.float-right.authorize").on("mouseover", function() {
    var fop_name = $("h2.fop_name").text();
//    alert("Only ACM may edit FoP: " + " " + fop_name + "!" + " Please use Comments.");
    $.getJSON('/check_account_manager', {
    a:fop_name
    }, function(data) {
        if (data.result == false) {
        alert("Only ACM may edit FoP: " + " " + fop_name + "!" + " Please use Comments.");
        };
        return false;
    });
});