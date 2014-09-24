define(["utils/utils","mvc/ui/ui-misc","mvc/ui/ui-tabs","mvc/tools/tools-template"],function(c,e,b,a){var d=Backbone.View.extend({initialize:function(n,h){this.options=h;var g=this;this.setElement("<div/>");this.current="hda";this.button_new=new e.RadioButton.View({value:this.current,data:[{icon:"fa-file-o",label:"Select datasets",value:"hda"},{icon:"fa-files-o",label:"Select a collection",value:"hdca"}],onchange:function(i){g.current=i;g.refresh();g.trigger("change")}});var l=n.datasets.filterType({content_type:"dataset",data_types:h.extensions});var k=[];for(var j in l){k.push({label:l[j].get("name"),value:l[j].get("id")})}this.select_datasets=new e.Select.View({multiple:true,data:k,value:k[0]&&k[0].value,onchange:function(){g.trigger("change")}});var m=n.datasets.filterType({content_type:"collection",data_types:h.extensions});var f=[];for(var j in m){f.push({label:m[j].get("name"),value:m[j].get("id")})}this.select_collection=new e.Select.View({data:f,value:f[0]&&f[0].value,onchange:function(){g.trigger("change")}});this.$el.append(c.wrap(this.button_new.$el));this.$el.append(this.select_datasets.$el);this.$el.append(this.select_collection.$el);if(!this.options.multiple){this.$el.append(a.batchMode())}this.refresh();this.on("change",function(){if(h.onchange){h.onchange(g.value())}})},value:function(){var g=null;switch(this.current){case"hda":g=this.select_datasets;break;case"hdca":g=this.select_collection;break}var j=g.value();if(!(j instanceof Array)){j=[j]}var f={batch:!this.options.multiple,values:[]};for(var h in j){f.values.push({id:j[h],src:this.current})}return f},validate:function(){switch(this.current){case"hda":return this.select_datasets.validate();case"hdca":return this.select_collection.validate()}},refresh:function(){switch(this.current){case"hda":this.select_datasets.$el.fadeIn();this.select_collection.$el.hide();break;case"hdca":this.select_datasets.$el.hide();this.select_collection.$el.fadeIn();break}}});return{View:d}});