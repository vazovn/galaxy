define( [ 'visualizations/jqplot/common/config' ], function( plot_config ) {
    return $.extend( true, {}, plot_config, {
        title       : 'Bar diagram',
        description : 'Renders a bar diagram using jqPlot hosted at http://www.jqplot.com.',
        groups      : {
            x : {
                label       : 'Values for x-axis',
                type        : 'data_column',
                is_label    : true,
                is_auto     : true
            },
            y : {
                label       : 'Values for y-axis',
                type        : 'data_column',
                is_numeric  : true
            }
        }
    });
});