define(["utils/utils"],function(a){var b=Backbone.View.extend({initialize:function(b){this.model=b&&b.model||new Backbone.Model({id:a.uid(),title:"",icon:"",cls:"btn btn-default",wait:!1,wait_text:"Sending...",wait_cls:"btn btn-info",disabled:!1,percentage:-1}).set(b),this.setElement($("<button/>").attr("type","button").append(this.$icon=$("<i/>")).append(this.$title=$("<span/>")).append(this.$progress=$("<div/>").append(this.$progress_bar=$("<div/>")))),this.listenTo(this.model,"change",this.render,this),this.render()},render:function(){var a=this,b=this.model.attributes;this.$el.removeClass().addClass("ui-button-default").addClass(b.disabled&&"disabled").attr("id",b.id).attr("disabled",b.disabled).off("click").on("click",function(){$(".tooltip").hide(),b.onclick&&!a.disabled&&b.onclick()}).tooltip({title:b.tooltip,placement:"bottom"}),this.$progress.addClass("progress").css("display",-1!==b.percentage?"block":"none"),this.$progress_bar.addClass("progress-bar").css({width:b.percentage+"%"}),this.$icon.removeClass().addClass("icon fa"),this.$title.removeClass().addClass("title"),b.wait?(this.$el.addClass(b.wait_cls).prop("disabled",!0),this.$icon.addClass("fa-spinner fa-spin ui-margin-right"),this.$title.html(b.wait_text)):(this.$el.addClass(b.cls),this.$icon.addClass(b.icon),this.$title.html(b.title),b.icon&&b.title&&this.$icon.addClass("ui-margin-right"))},show:function(){this.$el.show()},hide:function(){this.$el.hide()},disable:function(){this.model.set("disabled",!0)},enable:function(){this.model.set("disabled",!1)},wait:function(){this.model.set("wait",!0)},unwait:function(){this.model.set("wait",!1)},setIcon:function(a){this.model.set("icon",a)}}),c=b.extend({initialize:function(b){this.model=b&&b.model||new Backbone.Model({id:a.uid(),title:"",icon:"",cls:""}).set(b),this.setElement($("<a/>").append(this.$icon=$("<span/>"))),this.listenTo(this.model,"change",this.render,this),this.render()},render:function(){var a=this.model.attributes;this.$el.removeClass().addClass(a.cls).attr({id:a.id,href:a.href||"javascript:void(0)",title:a.title,target:a.target||"_top",disabled:a.disabled}).tooltip({placement:"bottom"}).off("click").on("click",function(){a.onclick&&!a.disabled&&a.onclick()}),this.$icon.removeClass().addClass(a.icon)}}),d=Backbone.View.extend({initialize:function(b){this.model=b&&b.model||new Backbone.Model({id:a.uid(),title:"Select/Unselect all",icons:["fa-square-o","fa-minus-square-o","fa-check-square-o"],value:0,onchange:function(){}}).set(b),this.setElement($("<div/>").append(this.$icon=$("<span/>")).append(this.$title=$("<span/>"))),this.listenTo(this.model,"change",this.render,this),this.render()},render:function(a){var b=this,a=this.model.attributes;this.$el.addClass("ui-button-check").off("click").on("click",function(){b.model.set("value",0===b.model.get("value")&&2||0),a.onclick&&a.onclick()}),this.$title.html(a.title),this.$icon.removeClass().addClass("icon fa ui-margin-right").addClass(a.icons[a.value])},value:function(a,b){return void 0!==a&&(b&&0!==a&&(a=a!==b&&1||2),this.model.set("value",a),this.model.get("onchange")(this.model.get("value"))),this.model.get("value")}}),e=b.extend({initialize:function(b){this.model=b&&b.model||new Backbone.Model({id:a.uid(),title:"",icon:"",cls:"ui-button-icon",disabled:!1}).set(b),this.setElement($("<div/>").append(this.$button=$("<div/>").append(this.$icon=$("<i/>")).append(this.$title=$("<span/>")))),this.listenTo(this.model,"change",this.render,this),this.render()},render:function(a){var a=this.model.attributes;this.$el.removeClass().addClass(a.cls).addClass(a.disabled&&"disabled").attr("disabled",a.disabled).attr("id",a.id).off("click").on("click",function(){$(".tooltip").hide(),!a.disabled&&a.onclick&&a.onclick()}),this.$button.addClass("button").tooltip({title:a.tooltip,placement:"bottom"}),this.$icon.removeClass().addClass("icon fa").addClass(a.icon),this.$title.addClass("title").html(a.title),a.icon&&a.title&&this.$icon.addClass("ui-margin-right")}}),f=b.extend({$menu:null,initialize:function(a){this.model=a&&a.model||new Backbone.Model({id:"",title:"",pull:"right",icon:null,onclick:null,cls:"ui-button-icon ui-button-menu",tooltip:"",target:"",href:"",onunload:null,visible:!0,tag:""}).set(a),this.collection=new Backbone.Collection,this.setElement($("<div/>").append(this.$root=$("<div/>").append(this.$icon=$("<i/>")).append(this.$title=$("<span/>")))),this.listenTo(this.model,"change",this.render,this),this.listenTo(this.collection,"change add remove reset",this.render,this),this.render()},render:function(){var a=this,b=this.model.attributes;this.$el.removeClass().addClass("dropdown").addClass(b.cls).attr("id",b.id).css({display:b.visible&&this.collection.where({visible:!0}).length>0?"block":"none"}),this.$root.addClass("root button dropdown-toggle").attr("data-toggle","dropdown").tooltip({title:b.tooltip,placement:"bottom"}).off("click").on("click",function(a){$(".tooltip").hide(),a.preventDefault(),b.onclick&&b.onclick()}),this.$icon.removeClass().addClass("icon fa").addClass(b.icon),this.$title.removeClass().addClass("title").html(b.title),b.icon&&b.title&&this.$icon.addClass("ui-margin-right"),this.$menu&&this.$menu.remove(),this.collection.length>0&&(this.$menu=$("<ul/>").addClass("menu dropdown-menu").addClass("pull-"+a.model.get("pull")).attr("role","menu"),this.$el.append(this.$menu)),this.collection.each(function(b){var c=b.attributes;if(c.visible){var d=$("<a/>").addClass("dropdown-item").attr({href:c.href,target:c.target}).append($("<i/>").addClass("fa").addClass(c.icon).css("display",c.icon?"inline-block":"none")).append(c.title).on("click",function(a){c.onclick&&(a.preventDefault(),c.onclick())});a.$menu.append($("<li/>").append(d)),c.divider&&a.$menu.append($("<li/>").addClass("divider"))}})},addMenu:function(b){this.collection.add(a.merge(b,{title:"",target:"",href:"",onclick:null,divider:!1,visible:!0,icon:null,cls:"button-menu btn-group"}))}});return{ButtonDefault:b,ButtonLink:c,ButtonIcon:e,ButtonCheck:d,ButtonMenu:f}});
//# sourceMappingURL=../../../maps/mvc/ui/ui-buttons.js.map