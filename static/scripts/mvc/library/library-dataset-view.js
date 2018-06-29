define("mvc/library/library-dataset-view",["exports","utils/localization","libs/toastr","mvc/library/library-model","utils/utils","mvc/ui/ui-select"],function(t,e,s,i,a,o){"use strict";function r(t){return t&&t.__esModule?t:{default:t}}Object.defineProperty(t,"__esModule",{value:!0});var n=r(e),l=r(s),d=r(i),c=r(a),m=r(o),p=Backbone.View.extend({el:"#center",model:null,options:{},defaults:{edit_mode:!1},events:{"click .toolbtn_modify_dataset":"enableModification","click .toolbtn_cancel_modifications":"render","click .toolbtn-download-dataset":"downloadDataset","click .toolbtn-import-dataset":"importIntoHistory","click .copy-link-to-clipboard":"copyToClipboard","click .make-private":"makeDatasetPrivate","click .remove-restrictions":"removeDatasetRestrictions","click .toolbtn_save_permissions":"savePermissions","click .toolbtn_save_modifications":"saveModifications"},select_genome:null,select_extension:null,list_extensions:[],auto:{id:"auto",text:"Auto-detect",description:"This system will try to detect the file type automatically. If your file is not detected properly as one of the known formats, it most likely means that it has some format problems (e.g., different number of columns on different rows). You can still coerce the system to set your data to the format you think it should be. You can also upload compressed files, which will automatically be decompressed."},list_genomes:[],initialize:function(t){this.options=_.extend(this.options,t),this.fetchExtAndGenomes(),this.options.id&&this.fetchDataset()},fetchDataset:function(t){this.options=_.extend(this.options,t),this.model=new d.default.Item({id:this.options.id});var e=this;this.model.fetch({success:function(){e.options.show_permissions?e.showPermissions():e.options.show_version?e.fetchVersion():e.render()},error:function(t,e){void 0!==e.responseJSON?l.default.error(e.responseJSON.err_msg+" Click this to go back.","",{onclick:function(){Galaxy.libraries.library_router.back()}}):l.default.error("An error occurred. Click this to go back.","",{onclick:function(){Galaxy.libraries.library_router.back()}})}})},render:function(t){this.options=_.extend(this.options,t),$(".tooltip").remove();var e=this.templateDataset();this.$el.html(e({item:this.model})),$(".peek").html(this.model.get("peek")),$('#center [data-toggle="tooltip"]').tooltip({trigger:"hover"})},fetchVersion:function(t){this.options=_.extend(this.options,t);var e=this;this.options.ldda_id?(this.ldda=new d.default.Ldda({id:this.options.ldda_id}),this.ldda.url=this.ldda.urlRoot+this.model.id+"/versions/"+this.ldda.id,this.ldda.fetch({success:function(){e.renderVersion()},error:function(t,e){void 0!==e.responseJSON?l.default.error(e.responseJSON.err_msg):l.default.error("An error occurred.")}})):(this.render(),l.default.error("Library dataset version requested but no id provided."))},renderVersion:function(){$(".tooltip").remove();var t=this.templateVersion();this.$el.html(t({item:this.model,ldda:this.ldda})),$(".peek").html(this.ldda.get("peek"))},enableModification:function(){$(".tooltip").remove();var t=this.templateModifyDataset();this.$el.html(t({item:this.model})),this.renderSelectBoxes({genome_build:this.model.get("genome_build"),file_ext:this.model.get("file_ext")}),$(".peek").html(this.model.get("peek")),$('#center [data-toggle="tooltip"]').tooltip({trigger:"hover"})},downloadDataset:function(){var t=Galaxy.root+"api/libraries/datasets/download/uncompressed",e={ld_ids:this.id};this.processDownload(t,e)},processDownload:function(t,e,s){if(t&&e){e="string"==typeof e?e:$.param(e);var i="";$.each(e.split("&"),function(){var t=this.split("=");i+='<input type="hidden" name="'+t[0]+'" value="'+t[1]+'" />'}),$('<form action="'+t+'" method="'+(s||"post")+'">'+i+"</form>").appendTo("body").submit().remove(),l.default.info("Your download will begin soon.")}},importIntoHistory:function(){this.refreshUserHistoriesList(function(t){var e=t.templateBulkImportInModal();t.modal=Galaxy.modal,t.modal.show({closing_events:!0,title:(0,n.default)("Import into History"),body:e({histories:t.histories.models}),buttons:{Import:function(){t.importCurrentIntoHistory()},Close:function(){Galaxy.modal.hide()}}})})},refreshUserHistoriesList:function(t){var e=this;this.histories=new d.default.GalaxyHistories,this.histories.fetch({success:function(s){0===s.length?l.default.warning("You have to create history first. Click this to do so.","",{onclick:function(){window.location=Galaxy.root}}):t(e)},error:function(t,e){void 0!==e.responseJSON?l.default.error(e.responseJSON.err_msg):l.default.error("An error occurred.")}})},importCurrentIntoHistory:function(){this.modal.disableButton("Import");var t=this.modal.$("input[name=history_name]").val(),e=this;if(""!==t)$.post(Galaxy.root+"api/histories",{name:t}).done(function(t){e.processImportToHistory(t.id)}).fail(function(t,e,s){l.default.error("An error occurred.")}).always(function(){e.modal.enableButton("Import")});else{var s=$(this.modal.$el).find("select[name=dataset_import_single] option:selected").val();this.processImportToHistory(s),this.modal.enableButton("Import")}},processImportToHistory:function(t){var e=new d.default.HistoryItem;e.url=e.urlRoot+t+"/contents",jQuery.getJSON(Galaxy.root+"history/set_as_current?id="+t),e.save({content:this.id,source:"library"},{success:function(){Galaxy.modal.hide(),l.default.success("Dataset imported. Click this to start analyzing it.","",{onclick:function(){window.location=Galaxy.root}})},error:function(t,e){void 0!==e.responseJSON?l.default.error("Dataset not imported. "+e.responseJSON.err_msg):l.default.error("An error occured. Dataset not imported. Please try again.")}})},showPermissions:function(t){var e=this.templateDatasetPermissions(),s=this;this.options=_.extend(this.options,t),$(".tooltip").remove(),void 0!==this.options.fetched_permissions&&(0===this.options.fetched_permissions.access_dataset_roles.length?this.model.set({is_unrestricted:!0}):this.model.set({is_unrestricted:!1})),this.$el.html(e({item:this.model,is_admin:Galaxy.config.is_admin_user})),$.get(Galaxy.root+"api/libraries/datasets/"+s.id+"/permissions?scope=current").done(function(t){s.prepareSelectBoxes({fetched_permissions:t,is_admin:Galaxy.config.is_admin_user})}).fail(function(){l.default.error("An error occurred while attempting to fetch dataset permissions.")}),$('#center [data-toggle="tooltip"]').tooltip({trigger:"hover"}),$("#center").css("overflow","auto")},_serializeRoles:function(t){for(var e=[],s=0;s<t.length;s++)e.push(t[s][1]+":"+t[s][0].replace(":"," ").replace(","," &"));return e},prepareSelectBoxes:function(t){this.options=_.extend(this.options,t),this.accessSelectObject=new m.default.View(this._generate_select_options({selector:"access_perm",initialData:this._serializeRoles(this.options.fetched_permissions.access_dataset_roles)})),this.modifySelectObject=new m.default.View(this._generate_select_options({selector:"modify_perm",initialData:this._serializeRoles(this.options.fetched_permissions.modify_item_roles)})),this.manageSelectObject=new m.default.View(this._generate_select_options({selector:"manage_perm",initialData:this._serializeRoles(this.options.fetched_permissions.manage_dataset_roles)}))},_generate_select_options:function(t){var e={minimumInputLength:0,multiple:!0,placeholder:"Click to select a role",formatResult:function(t){return t.name+" type: "+t.type},formatSelection:function(t){return t.name},initSelection:function(t,e){var s=[];$(t.val().split(",")).each(function(){var t=this.split(":");s.push({id:t[0],name:t[1]})}),e(s)},dropdownCssClass:"bigdrop"};return e.container=this.$el.find("#"+t.selector),e.css=t.selector,e.initialData=t.initialData.join(","),e.ajax={url:Galaxy.root+"api/libraries/datasets/"+this.id+"/permissions?scope=available",dataType:"json",quietMillis:100,data:function(t,e){return{q:t,page_limit:10,page:e}},results:function(t,e){var s=10*e<t.total;return{results:t.roles,more:s}}},e},saveModifications:function(t){var e=!1,s=this.model,i=this.$el.find(".input_dataset_name").val();if(void 0!==i&&i!==s.get("name")){if(!(i.length>0))return void l.default.warning("Library dataset name has to be at least 1 character long.");s.set("name",i),e=!0}var a=this.$el.find(".input_dataset_misc_info").val();void 0!==a&&a!==s.get("misc_info")&&(s.set("misc_info",a),e=!0);var o=this.$el.find(".input_dataset_message").val();void 0!==o&&o!==s.get("message")&&(s.set("message",o),e=!0);var r=this.select_genome.$el.select2("data").id;void 0!==r&&r!==s.get("genome_build")&&(s.set("genome_build",r),e=!0);var n=this.select_extension.$el.select2("data").id;void 0!==n&&n!==s.get("file_ext")&&(s.set("file_ext",n),e=!0);var d=this;e?s.save(null,{patch:!0,success:function(t){d.render(),l.default.success("Changes to library dataset saved.")},error:function(t,e){void 0!==e.responseJSON?l.default.error(e.responseJSON.err_msg):l.default.error("An error occured while attempting to update the library dataset.")}}):(d.render(),l.default.info("Nothing has changed."))},copyToClipboard:function(t){t.preventDefault();var e=Backbone.history.location.href;-1!==e.lastIndexOf("/permissions")&&(e=e.substr(0,e.lastIndexOf("/permissions"))),window.prompt("Copy to clipboard: Ctrl+C, Enter",e)},makeDatasetPrivate:function(){var t=this;$.post(Galaxy.root+"api/libraries/datasets/"+t.id+"/permissions?action=make_private").done(function(e){t.model.set({is_unrestricted:!1}),t.showPermissions({fetched_permissions:e}),l.default.success("The dataset is now private to you.")}).fail(function(){l.default.error("An error occurred while attempting to make dataset private.")})},removeDatasetRestrictions:function(){var t=this;$.post(Galaxy.root+"api/libraries/datasets/"+t.id+"/permissions?action=remove_restrictions").done(function(e){t.model.set({is_unrestricted:!0}),t.showPermissions({fetched_permissions:e}),l.default.success("Access to this dataset is now unrestricted.")}).fail(function(){l.default.error("An error occurred while attempting to make dataset unrestricted.")})},_extractIds:function(t){for(var e=[],s=t.length-1;s>=0;s--)e.push(t[s].id);return e},savePermissions:function(t){var e=this,s=this._extractIds(this.accessSelectObject.$el.select2("data")),i=this._extractIds(this.manageSelectObject.$el.select2("data")),a=this._extractIds(this.modifySelectObject.$el.select2("data"));$.post(Galaxy.root+"api/libraries/datasets/"+e.id+"/permissions?action=set_permissions",{"access_ids[]":s,"manage_ids[]":i,"modify_ids[]":a}).done(function(t){e.showPermissions({fetched_permissions:t}),l.default.success("Permissions saved.")}).fail(function(){l.default.error("An error occurred while attempting to set dataset permissions.")})},fetchExtAndGenomes:function(){var t=this;0==this.list_genomes.length&&c.default.get({url:Galaxy.root+"api/datatypes?extension_only=False",success:function(e){for(var s in e)t.list_extensions.push({id:e[s].extension,text:e[s].extension,description:e[s].description,description_url:e[s].description_url});t.list_extensions.sort(function(t,e){return t.id>e.id?1:t.id<e.id?-1:0}),t.list_extensions.unshift(t.auto)}}),0==this.list_extensions.length&&c.default.get({url:Galaxy.root+"api/genomes",success:function(e){for(var s in e)t.list_genomes.push({id:e[s][1],text:e[s][0]});t.list_genomes.sort(function(t,e){return t.id>e.id?1:t.id<e.id?-1:0})}})},renderSelectBoxes:function(t){var e=this,s="?",i="auto";void 0!==t&&(void 0!==t.genome_build&&(s=t.genome_build),void 0!==t.file_ext&&(i=t.file_ext)),this.select_genome=new m.default.View({css:"dataset-genome-select",data:e.list_genomes,container:e.$el.find("#dataset_genome_select"),value:s}),this.select_extension=new m.default.View({css:"dataset-extension-select",data:e.list_extensions,container:e.$el.find("#dataset_extension_select"),value:i})},templateDataset:function(){return _.template(['<div class="library_style_container">','<div class="d-flex mb-2">','<button data-toggle="tooltip" data-placement="top" title="Download dataset" class="btn btn-secondary toolbtn-download-dataset toolbar-item mr-1" type="button">','<span class="fa fa-download"></span>',"&nbsp;Download","</button>",'<button data-toggle="tooltip" data-placement="top" title="Import dataset into history" class="btn btn-secondary toolbtn-import-dataset toolbar-item mr-1" type="button">','<span class="fa fa-book"></span>',"&nbsp;to History","</button>",'<% if (item.get("can_user_modify")) { %>','<button data-toggle="tooltip" data-placement="top" title="Modify library item" class="btn btn-secondary toolbtn_modify_dataset toolbar-item mr-1" type="button">','<span class="fa fa-pencil"></span>',"&nbsp;Modify","</button>","<% } %>",'<% if (item.get("can_user_manage")) { %>','<a href="#folders/<%- item.get("folder_id") %>/datasets/<%- item.id %>/permissions">','<button data-toggle="tooltip" data-placement="top" title="Manage permissions" class="btn btn-secondary toolbtn_change_permissions toolbar-item mr-1" type="button">','<span class="fa fa-group"></span>',"&nbsp;Permissions","</button>","</a>","<% } %>","</div>",'<ol class="breadcrumb">','<li class="breadcrumb-item"><a title="Return to the list of libraries" href="#">Libraries</a></li>','<% _.each(item.get("full_path"), function(path_item) { %>',"<% if (path_item[0] != item.id) { %>",'<li class="breadcrumb-item"><a title="Return to this folder" href="#/folders/<%- path_item[0] %>"><%- path_item[1] %></a> </li> ',"<% } else { %>",'<li class="breadcrumb-item active"><span title="You are here"><%- path_item[1] %></span></li>',"<% } %>","<% }); %>","</ol>",'<% if (item.get("is_unrestricted")) { %>',"<div>",'This dataset is unrestricted so everybody with the link can access it. Just share <span class="copy-link-to-clipboard"><a href=""a>this page</a></span>.',"</div>","<% } %>",'<div class="dataset_table">','<table class="grid table table-striped table-sm">',"<tr>",'<th class="dataset-first-column" scope="row" id="id_row" data-id="<%= _.escape(item.get("ldda_id")) %>">Name</th>','<td><%= _.escape(item.get("name")) %></td>',"</tr>",'<% if (item.get("file_ext")) { %>',"<tr>",'<th scope="row">Data type</th>','<td><%= _.escape(item.get("file_ext")) %></td>',"</tr>","<% } %>",'<% if (item.get("genome_build")) { %>',"<tr>",'<th scope="row">Genome build</th>','<td><%= _.escape(item.get("genome_build")) %></td>',"</tr>","<% } %>",'<% if (item.get("file_size")) { %>',"<tr>",'<th scope="row">Size</th>','<td><%= _.escape(item.get("file_size")) %></td>',"</tr>","<% } %>",'<% if (item.get("date_uploaded")) { %>',"<tr>",'<th scope="row">Date uploaded (UTC)</th>','<td><%= _.escape(item.get("date_uploaded")) %></td>',"</tr>","<% } %>",'<% if (item.get("uploaded_by")) { %>',"<tr>",'<th scope="row">Uploaded by</th>','<td><%= _.escape(item.get("uploaded_by")) %></td>',"</tr>","<% } %>",'<% if (item.get("metadata_data_lines")) { %>',"<tr>",'<th scope="row">Data Lines</th>','<td scope="row"><%= _.escape(item.get("metadata_data_lines")) %></td>',"</tr>","<% } %>",'<% if (item.get("metadata_comment_lines")) { %>',"<tr>",'<th scope="row">Comment Lines</th>','<td scope="row"><%= _.escape(item.get("metadata_comment_lines")) %></td>',"</tr>","<% } %>",'<% if (item.get("metadata_columns")) { %>',"<tr>",'<th scope="row">Number of Columns</th>','<td scope="row"><%= _.escape(item.get("metadata_columns")) %></td>',"</tr>","<% } %>",'<% if (item.get("metadata_column_types")) { %>',"<tr>",'<th scope="row">Column Types</th>','<td scope="row"><%= _.escape(item.get("metadata_column_types")) %></td>',"</tr>","<% } %>",'<% if (item.get("message")) { %>',"<tr>",'<th scope="row">Message</th>','<td scope="row"><%= _.escape(item.get("message")) %></td>',"</tr>","<% } %>",'<% if (item.get("misc_blurb")) { %>',"<tr>",'<th scope="row">Misc. blurb</th>','<td scope="row"><%= _.escape(item.get("misc_blurb")) %></td>',"</tr>","<% } %>",'<% if (item.get("misc_info")) { %>',"<tr>",'<th scope="row">Misc. info</th>','<td scope="row"><%= _.escape(item.get("misc_info")) %></td>',"</tr>","<% } %>",'<% if (item.get("tags")) { %>',"<tr>",'<th scope="row">Tags</th>','<td scope="row"><%= _.escape(item.get("tags")) %></td>',"</tr>","<% } %>",'<% if ( item.get("uuid") !== "ok" ) { %>',"<tr>",'<th scope="row">UUID</th>','<td scope="row"><%= _.escape(item.get("uuid")) %></td>',"</tr>","<% } %>",'<% if ( item.get("state") !== "ok" ) { %>',"<tr>",'<th scope="row">State</th>','<td scope="row"><%= _.escape(item.get("state")) %></td>',"</tr>","<% } %>","</table>",'<% if (item.get("job_stderr")) { %>',"<h4>Job Standard Error</h4>",'<pre class="code">','<%= _.escape(item.get("job_stderr")) %>',"</pre>","<% } %>",'<% if (item.get("job_stdout")) { %>',"<h4>Job Standard Output</h4>",'<pre class="code">','<%= _.escape(item.get("job_stdout")) %>',"</pre>","<% } %>","<div>",'<pre class="peek">',"</pre>","</div>",'<% if (item.get("has_versions")) { %>',"<div>","<h3>Expired versions:</h3>","<ul>",'<% _.each(item.get("expired_versions"), function(version) { %>','<li><a title="See details of this version" href="#folders/<%- item.get("folder_id") %>/datasets/<%- item.id %>/versions/<%- version[0] %>"><%- version[1] %></a></li>',"<% }) %>","<ul>","</div>","<% } %>","</div>","</div>"].join(""))},templateVersion:function(){return _.template(['<div class="library_style_container">','<div class="d-flex mb-2">','<a href="#folders/<%- item.get("folder_id") %>/datasets/<%- item.id %>">','<button data-toggle="tooltip" data-placement="top" title="Go to latest dataset" class="btn btn-secondary toolbar-item mr-1" type="button">','<span class="fa fa-caret-left fa-lg"></span>',"&nbsp;Latest dataset","</button>","<a>","</div>",'<ol class="breadcrumb">','<li class="breadcrumb-item"><a title="Return to the list of libraries" href="#">Libraries</a></li>','<% _.each(item.get("full_path"), function(path_item) { %>',"<% if (path_item[0] != item.id) { %>",'<li class="breadcrumb-item"><a title="Return to this folder" href="#/folders/<%- path_item[0] %>"><%- path_item[1] %></a> </li> ',"<% } else { %>",'<li class="breadcrumb-item active"><span title="You are here"><%- path_item[1] %></span></li>',"<% } %>","<% }); %>","</ol>",'<div class="alert alert-warning">This is an expired version of the library dataset: <%= _.escape(item.get("name")) %></div>','<div class="dataset_table">','<table class="grid table table-striped table-sm">',"<tr>",'<th scope="row" id="id_row" data-id="<%= _.escape(ldda.id) %>">Name</th>','<td><%= _.escape(ldda.get("name")) %></td>',"</tr>",'<% if (ldda.get("file_ext")) { %>',"<tr>",'<th scope="row">Data type</th>','<td><%= _.escape(ldda.get("file_ext")) %></td>',"</tr>","<% } %>",'<% if (ldda.get("genome_build")) { %>',"<tr>",'<th scope="row">Genome build</th>','<td><%= _.escape(ldda.get("genome_build")) %></td>',"</tr>","<% } %>",'<% if (ldda.get("file_size")) { %>',"<tr>",'<th scope="row">Size</th>','<td><%= _.escape(ldda.get("file_size")) %></td>',"</tr>","<% } %>",'<% if (ldda.get("date_uploaded")) { %>',"<tr>",'<th scope="row">Date uploaded (UTC)</th>','<td><%= _.escape(ldda.get("date_uploaded")) %></td>',"</tr>","<% } %>",'<% if (ldda.get("uploaded_by")) { %>',"<tr>",'<th scope="row">Uploaded by</th>','<td><%= _.escape(ldda.get("uploaded_by")) %></td>',"</tr>","<% } %>",'<% if (ldda.get("metadata_data_lines")) { %>',"<tr>",'<th scope="row">Data Lines</th>','<td scope="row"><%= _.escape(ldda.get("metadata_data_lines")) %></td>',"</tr>","<% } %>",'<% if (ldda.get("metadata_comment_lines")) { %>',"<tr>",'<th scope="row">Comment Lines</th>','<td scope="row"><%= _.escape(ldda.get("metadata_comment_lines")) %></td>',"</tr>","<% } %>",'<% if (ldda.get("metadata_columns")) { %>',"<tr>",'<th scope="row">Number of Columns</th>','<td scope="row"><%= _.escape(ldda.get("metadata_columns")) %></td>',"</tr>","<% } %>",'<% if (ldda.get("metadata_column_types")) { %>',"<tr>",'<th scope="row">Column Types</th>','<td scope="row"><%= _.escape(ldda.get("metadata_column_types")) %></td>',"</tr>","<% } %>",'<% if (ldda.get("message")) { %>',"<tr>",'<th scope="row">Message</th>','<td scope="row"><%= _.escape(ldda.get("message")) %></td>',"</tr>","<% } %>",'<% if (ldda.get("misc_blurb")) { %>',"<tr>",'<th scope="row">Miscellaneous blurb</th>','<td scope="row"><%= _.escape(ldda.get("misc_blurb")) %></td>',"</tr>","<% } %>",'<% if (ldda.get("misc_info")) { %>',"<tr>",'<th scope="row">Miscellaneous information</th>','<td scope="row"><%= _.escape(ldda.get("misc_info")) %></td>',"</tr>","<% } %>",'<% if (item.get("tags")) { %>',"<tr>",'<th scope="row">Tags</th>','<td scope="row"><%= _.escape(item.get("tags")) %></td>',"</tr>","<% } %>","</table>","<div>",'<pre class="peek">',"</pre>","</div>","</div>","</div>"].join(""))},templateModifyDataset:function(){return _.template(['<div class="library_style_container">','<ol class="breadcrumb">','<li class="breadcrumb-item"><a title="Return to the list of libraries" href="#">Libraries</a></li>','<% _.each(item.get("full_path"), function(path_item) { %>',"<% if (path_item[0] != item.id) { %>",'<li class="breadcrumb-item"><a title="Return to this folder" href="#/folders/<%- path_item[0] %>"><%- path_item[1] %></a> </li> ',"<% } else { %>",'<li class="breadcrumb-item active"><span title="You are here"><%- path_item[1] %></span></li>',"<% } %>","<% }); %>","</ol>",'<div class="dataset_table">','<table class="grid table table-striped table-sm">',"<tr>",'<th class="dataset-first-column" scope="row" id="id_row" data-id="<%= _.escape(item.get("ldda_id")) %>">Name</th>','<td><input class="input_dataset_name form-control" type="text" placeholder="name" value="<%= _.escape(item.get("name")) %>"></td>',"</tr>","<tr>",'<th scope="row">Data type</th>',"<td>",'<span id="dataset_extension_select" class="dataset-extension-select" />',"</td>","</tr>","<tr>",'<th scope="row">Genome build</th>',"<td>",'<span id="dataset_genome_select" class="dataset-genome-select" />',"</td>","</tr>","<tr>",'<th scope="row">Size</th>','<td><%= _.escape(item.get("file_size")) %></td>',"</tr>","<tr>",'<th scope="row">Date uploaded (UTC)</th>','<td><%= _.escape(item.get("date_uploaded")) %></td>',"</tr>","<tr>",'<th scope="row">Uploaded by</th>','<td><%= _.escape(item.get("uploaded_by")) %></td>',"</tr>",'<tr scope="row">','<th scope="row">Data Lines</th>','<td scope="row"><%= _.escape(item.get("metadata_data_lines")) %></td>',"</tr>",'<th scope="row">Comment Lines</th>','<% if (item.get("metadata_comment_lines") === "") { %>','<td scope="row"><%= _.escape(item.get("metadata_comment_lines")) %></td>',"<% } else { %>",'<td scope="row">unknown</td>',"<% } %>","</tr>","<tr>",'<th scope="row">Number of Columns</th>','<td scope="row"><%= _.escape(item.get("metadata_columns")) %></td>',"</tr>","<tr>",'<th scope="row">Column Types</th>','<td scope="row"><%= _.escape(item.get("metadata_column_types")) %></td>',"</tr>","<tr>",'<th scope="row">Message</th>','<td scope="row"><input class="input_dataset_message form-control" type="text" placeholder="message" value="<%= _.escape(item.get("message")) %>"></td>',"</tr>","<tr>",'<th scope="row">Misc. blurb</th>','<td scope="row"><%= _.escape(item.get("misc_blurb")) %></td>',"</tr>","<tr>",'<th scope="row">Misc. information</th>','<td><input class="input_dataset_misc_info form-control" type="text" placeholder="info" value="<%= _.escape(item.get("misc_info")) %>"></td>',"</tr>",'<% if (item.get("tags")) { %>',"<tr>",'<th scope="row">Tags</th>','<td scope="row"><%= _.escape(item.get("tags")) %></td>',"</tr>","<% } %>","</table>","<div>",'<pre class="peek">',"</pre>","</div>","</div>",'<div class="d-flex">','<button data-toggle="tooltip" data-placement="top" title="Cancel modifications" class="btn btn-secondary toolbtn_cancel_modifications toolbar-item mr-1" type="button">','<span class="fa fa-times"></span>',"&nbsp;Cancel","</button>",'<button data-toggle="tooltip" data-placement="top" title="Save modifications" class="btn btn-secondary toolbtn_save_modifications toolbar-item mr-1" type="button">','<span class="fa fa-floppy-o"></span>',"&nbsp;Save","</button>","</div>","</div>"].join(""))},templateDatasetPermissions:function(){return _.template(['<div class="library_style_container">','<div class="d-flex mb-2">','<a href="#folders/<%- item.get("folder_id") %>/datasets/<%- item.id %>">','<button data-toggle="tooltip" data-placement="top" title="Go back to dataset" class="btn btn-secondary toolbar-item mr-1" type="button">','<span class="fa fa-file-o"></span>',"&nbsp;Dataset Details","</button>","<a>","</div>",'<ol class="breadcrumb">','<li class="breadcrumb-item"><a title="Return to the list of libraries" href="#">Libraries</a></li>','<% _.each(item.get("full_path"), function(path_item) { %>',"<% if (path_item[0] != item.id) { %>",'<li class="breadcrumb-item"><a title="Return to this folder" href="#/folders/<%- path_item[0] %>"><%- path_item[1] %></a> </li> ',"<% } else { %>",'<li class="breadcrumb-item active"><span title="You are here"><%- path_item[1] %></span></li>',"<% } %>","<% }); %>","</ol>",'<h1>Dataset: <%= _.escape(item.get("name")) %></h1>','<div class="alert alert-warning">',"<% if (is_admin) { %>","You are logged in as an <strong>administrator</strong> therefore you can manage any dataset on this Galaxy instance. Please make sure you understand the consequences.","<% } else { %>","You can assign any number of roles to any of the following permission types. However please read carefully the implications of such actions.","<% } %>","</div>",'<div class="dataset_table">',"<h2>Library-related permissions</h2>","<h4>Roles that can modify the library item</h4>",'<div id="modify_perm" class="modify_perm roles-selection"></div>','<div class="alert alert-info roles-selection">User with <strong>any</strong> of these roles can modify name, metadata, and other information about this library item.</div>',"<hr/>","<h2>Dataset-related permissions</h2>",'<div class="alert alert-warning">Changes made below will affect <strong>every</strong> library item that was created from this dataset and also every history this dataset is part of.</div>','<% if (!item.get("is_unrestricted")) { %>','<p>You can <span class="remove-restrictions"><a href="">remove all access restrictions</a></span> on this dataset.</p>',"<% } else { %>",'<p>You can <span class="make-private"><a href="">make this dataset private</a></span> to you.</p>',"<% } %>","<h4>Roles that can access the dataset</h4>",'<div id="access_perm" class="access_perm roles-selection"></div>','<div class="alert alert-info roles-selection">',"User has to have <strong>all these roles</strong> in order to access this dataset."," Users without access permission <strong>cannot</strong> have other permissions on this dataset."," If there are no access roles set on the dataset it is considered <strong>unrestricted</strong>.","</div>","<h4>Roles that can manage permissions on the dataset</h4>",'<div id="manage_perm" class="manage_perm roles-selection"></div>','<div class="alert alert-info roles-selection">',"User with <strong>any</strong> of these roles can manage permissions of this dataset. If you remove yourself you will lose the ability manage this dataset unless you are an admin.","</div>",'<button data-toggle="tooltip" data-placement="top" title="Save modifications made on this page" class="btn btn-secondary toolbtn_save_permissions  type="button">','<span class="fa fa-floppy-o"></span>',"&nbsp;Save","</button>","</div>","</div>"].join(""))},templateBulkImportInModal:function(){return _.template(["<div>",'<div class="library-modal-item">',"Select history: ",'<select id="dataset_import_single" name="dataset_import_single" style="width:50%; margin-bottom: 1em; " autofocus>',"<% _.each(histories, function(history) { %>",'<option value="<%= _.escape(history.get("id")) %>"><%= _.escape(history.get("name")) %></option>',"<% }); %>","</select>","</div>",'<div class="library-modal-item">',"or create new: ",'<input type="text" name="history_name" value="" placeholder="name of the new history" style="width:50%;">',"</input>","</div>","</div>"].join(""))}});t.default={LibraryDatasetView:p}});