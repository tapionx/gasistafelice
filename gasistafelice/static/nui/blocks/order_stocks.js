
jQuery.UIBlockOrderStockList = jQuery.UIBlockWithList.extend({

    init: function() {
        this._super("order_stocks", "table");
    },

    rendering_table_post_load_handler: function() {

        // Init dataTables
        var oTable = this.block_el.find('.dataTable').dataTable({
                'sPaginationType': 'full_numbers', 
                "bServerSide": true,
                "bStateSave": true,
                "sAjaxSource": this.get_data_source(),
                "aoColumns": [
                    null,
                    null,
                    null,
                    { "sType": "currency" },
                    null
                ]
            }); 

        return this._super();

    }
    
});

jQuery.BLOCKS["order_stocks"] = new jQuery.UIBlockOrderStockList();

