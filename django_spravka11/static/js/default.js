$(function(){
	$.fn.disableSelection = function() {
		return this.attr('unselectable', 'on')
			.css({'-moz-user-select':'-moz-none',
					'-moz-user-select':'none',
					'-o-user-select':'none',
					'-khtml-user-select':'none',
					'-webkit-user-select':'none',
					'-ms-user-select':'none',
					'user-select':'none'}).bind('selectstart', false);
	};
	$.fn.clearDefault = function(){
		return this.each(function(){
			var default_value = $(this).val();
			$(this).focus(function(){
				if ($(this).val() == default_value) {
					$(this).val("");
				};
			});
			$(this).blur(function(){
				if ($(this).val() == "") {
					$(this).val(default_value);
				};
			});
		});
	};
});
$(document).ready(function () {
	$("input[type='text'],textarea").clearDefault();
	
	$("a").nivoLightbox();

	$("#dialog").dialog({
		autoOpen:false,
		modal:true
	});
	$("body").on("click",".ui-widget-overlay", function () {
		$("#dialog").dialog("close");
	});

	 $("body").on("click",".org-form__address-action--add",function(e){
  		e.preventDefault();
  		var added = $(".org-form__address:first").clone();
  		added.find("input").val("");
  		added.find("textarea").val("");
  		added.addClass("org-form__address--added").insertAfter(".org-form__address:first");
  		added.find(".org-form__address-action").html('<a class="org-form__address-action--delete" href="">Удалить адрес</a>');
 	});

	$("body").on("click",".org-form__address-action--delete",function(e){
		e.preventDefault();
		$(this).closest(".org-form__address").remove();
	});

	$(".weather-tabs").tabs();

	$("#dialog-control").click(function(e){
		e.preventDefault();
		$("#dialog").dialog("open");
	});

	if($(".header-search__input input").val() == ''){
		$(".header-search__remove").hide();
	}
	$(".header-search__input").on("input",function(){
		$(".header-search__remove").show();
	});

	$(".header-search__remove").click(function(e){
		e.preventDefault();
		$(".header-search__remove").hide();
		$(this).prev("input").val("").focus();
	});
	$(".select-replacement").each(function(){
		$(this).prepend('<span class="select-replacement__arrow" style="visibility:visible;"></span><span class="select-replacement__option-selected">'+$(this).find('select>option:selected').text()+'</span>');
	});
	$(".select-replacement__select").change(function(){
		$(".select-replacement__option-selected").text($("option:selected",this).text());
	});
	
	$(".useful-list__item").disableSelection().one("click",usefulhandler1);
	 function usefulhandler1(event){
	  var target = $(event.target);
	  if(target.is(".bbdb")){
	   $(this).addClass("useful-list__item--nobull");
	   $(".catalog-entry__h",this).addClass("catalog-entry__h--active");
	   $(".catalog-entry__rubrics",this).show();
	   $(this).one("click",usefulhandler2);
	  } else {$(this).one("click",usefulhandler1);}
	  
	 }
	 function usefulhandler2(event){
	  var target = $(event.target);
	  if(target.is(".bbdb")){
	   $(this).removeClass("useful-list__item--nobull");
	   $(".catalog-entry__h",this).removeClass("catalog-entry__h--active");
	   $(".catalog-entry__rubrics",this).hide();
	   $(this).one("click",usefulhandler1);
	  } else {$(this).one("click",usefulhandler2);}
	 }
	
	$(".contacts-list__toggle").disableSelection().one("click",contactslisthandler1).nextUntil().hide();
	function contactslisthandler1(event){
		$(this).html('<span class="bbdb">Скрыть адреса</span>');
		$(this).nextUntil().show();
		$(this).one("click",contactslisthandler2);
	}
	function contactslisthandler2(event){
		$(this).html('<span class="bbdb">Показать адреса</span>');
		$(this).nextUntil().hide();
		$(this).one("click",contactslisthandler1);
	}
	
	$("body").on("change",".org-address,.org-phone,.org-timework",function(){
		var orgAllInfo = "";
		var c = 0;
		$(".org-form__address").each(function(){
			orgAllInfo += "(";
			orgAllInfo += $(".org-address",this).val() + ",";
			orgAllInfo += $(".org-phone",this).val() + ",";
			orgAllInfo += $(".org-timework",this).val();
			orgAllInfo += ")" + (++c) + ",";
		});
		if(orgAllInfo != ""){orgAllInfo=orgAllInfo.slice(0,-1);}
		$("#org-allinfo").val(orgAllInfo);
	});

	$("#call-dialog").dialog({
		autoOpen:false,
		modal:true
	 });
	$("body").on("click",".ui-widget-overlay", function () {
		$("#call-dialog").dialog("close");
	});

	$("#call-dialog-control").click(function(e){
  		e.preventDefault();
  	$("#call-dialog").dialog("open");
 	});

 	$("#ads-dialog").dialog({
		autoOpen:false,
		modal:true
	 });
	$("body").on("click",".ui-widget-overlay", function () {
		$("#ads-dialog").dialog("close");
	});

	$(".ads-dialog-control").click(function(e){
  		e.preventDefault();
  	$("#ads-dialog").dialog("open");
 	});

 	$("#logo-dialog").dialog({
		autoOpen:false,
		modal:true
	 });
	$("body").on("click",".ui-widget-overlay", function () {
		$("#logo-dialog").dialog("close");
	});

	$(".logo-dialog-control").click(function(e){
  		e.preventDefault();
  	$("#logo-dialog").dialog("open");
 	});
});

