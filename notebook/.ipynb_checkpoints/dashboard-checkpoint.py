from bokeh.io import curdoc
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
import random
import time
import pandas as pd
from bokeh.models import HoverTool
from bokeh.models import glyphs
from bokeh.layouts import column, row
import pymongo
from pymongo import MongoClient
#######################################################################################

def get_last_row(collection):
    conn = MongoClient('mongodb', 27017)
    db=conn.btc
    cur=db[collection].find().sort('timestamp',pymongo.DESCENDING).limit(1)
    conn.close()
    return cur[0]

# the style of tooltips
# refer to official tutorial, A1 Models and Primitives
tooltips_buy = """
<div>
    <span style="font-size: 17px; font-weight: bold;">@buy</span>&nbsp;
</div>
"""
tooltips_sell = """
<div>
    <span style="font-size: 17px; font-weight: bold;">@sell</span>&nbsp;
</div>
"""

tooltips_buy_ave = """
<div>
    <span style="font-size: 17px; font-weight: bold;">@buy_avg</span>&nbsp;
</div>
"""
tooltips_sell_ave = """
<div>
    <span style="font-size: 17px; font-weight: bold;">@sell_avg</span>&nbsp;
</div>
"""
init = get_last_row('realtime')
init_ave = get_last_row('average')
#######################################################################################
### buy figure
fig_buy = figure(plot_width=850, plot_height=450, x_axis_type='datetime',
                   title='USD'.format(20))
fig_buy.xaxis.axis_label = 'time'  # axis label
fig_buy.yaxis.axis_label = 'buy price'
fig_buy.background_fill_color = 'beige'  # the color of background is 'beige'
fig_buy.background_fill_alpha = 0.5
source_buy = ColumnDataSource(data=dict(x=[pd.to_datetime(init['timestamp'])], 
                                        y=[float(init['buy_price'])]))
# line figure, the data of x axis come from key x of dict 'source_buy'
fig_buy.line(x='x', y='y', alpha=0.5, legend='buy_price', source=source_buy)
buy_glyph = glyphs.Circle(x='x', y='y', size=3, fill_color='white')
buy_add = fig_buy.add_glyph(source_or_glyph=source_buy, glyph=buy_glyph)
hover = HoverTool(tooltips=tooltips_buy, renderers=[buy_add])
fig_buy.legend.location = 'bottom_left'
fig_buy.add_tools(hover)
#######################################################################################
### sell figure
fig_sell = figure(plot_width=850, plot_height=450, x_axis_type='datetime',
                   title='USD'.format(20))
fig_sell.xaxis.axis_label = 'time'  # axis label
fig_sell.yaxis.axis_label = 'sell price'
fig_sell.background_fill_color = 'beige'  # the color of background is 'beige'
fig_sell.background_fill_alpha = 0.5
source_sell = ColumnDataSource(data=dict(x=[pd.to_datetime(init['timestamp'])], 
                                         y=[float(init['sell_price'])]))
# line figure, the data of x axis come from key x of dict 'source_sell'
fig_sell.line(x='x', y='y', alpha=0.5, legend='sell_price', source=source_sell)
sell_glyph = glyphs.Circle(x='x', y='y', size=3, fill_color='white')
sell_add = fig_sell.add_glyph(source_or_glyph=source_sell, glyph=sell_glyph)
hover = HoverTool(tooltips=tooltips_sell, renderers=[sell_add])
fig_sell.legend.location = 'bottom_left'
fig_sell.add_tools(hover)
#######################################################################################
### buy_ave figure
fig_buy_ave = figure(plot_width=850, plot_height=450, x_axis_type='datetime',
                   title='USD'.format(20))
fig_buy_ave.xaxis.axis_label = 'time'  # axis label
fig_buy_ave.yaxis.axis_label = 'buy average price'
fig_buy_ave.background_fill_color = 'beige'  # the color of background is 'beige'
fig_buy_ave.background_fill_alpha = 0.5
source_buy_ave = ColumnDataSource(data=dict(x=[pd.to_datetime(init_ave['timestamp'])], 
                                        y=[float(init_ave['buy_price'])]))
# line figure, the data of x axis come from key x of dict 'source_buy'
fig_buy_ave.line(x='x', y='y', alpha=0.5, legend='buy_average_price', source=source_buy_ave)
buy_ave_glyph = glyphs.Circle(x='x', y='y', size=3, fill_color='white')
buy_ave_add = fig_buy_ave.add_glyph(source_or_glyph=source_buy_ave, glyph=buy_ave_glyph)
hover = HoverTool(tooltips=tooltips_buy_ave, renderers=[buy_ave_add])
fig_buy_ave.legend.location = 'bottom_left'
fig_buy_ave.add_tools(hover)
#######################################################################################
### sell_ave figure
fig_sell_ave = figure(plot_width=850, plot_height=450, x_axis_type='datetime',
                   title='USD'.format(20))
fig_sell_ave.xaxis.axis_label = 'time'  # axis label
fig_sell_ave.yaxis.axis_label = 'sell average price'
fig_sell_ave.background_fill_color = 'beige'  # the color of background is 'beige'
fig_sell_ave.background_fill_alpha = 0.5
source_sell_ave = ColumnDataSource(data=dict(x=[pd.to_datetime(init_ave['timestamp'])], 
                                         y=[float(init_ave['sell_price'])]))
# line figure, the data of x axis come from key x of dict 'source_sell'
fig_sell_ave.line(x='x', y='y', alpha=0.5, legend='sell_average_price', source=source_sell_ave)
sell_ave_glyph = glyphs.Circle(x='x', y='y', size=3, fill_color='white')
sell_ave_add = fig_sell_ave.add_glyph(source_or_glyph=source_sell_ave, glyph=sell_ave_glyph)
hover = HoverTool(tooltips=tooltips_sell_ave, renderers=[sell_ave_add])
fig_sell_ave.legend.location = 'bottom_left'
fig_sell_ave.add_tools(hover)
#######################################################################################
cnt = 0
                               
def update():
    global cnt
    cnt += 1
    data_dict = get_last_row('realtime')
    new_data_buy = dict(x=[pd.to_datetime(data_dict['timestamp'])],
                        y=[float(data_dict['buy_price'])]) 
    source_buy.stream(new_data=new_data_buy, rollover=200)

    new_data_sell=dict(x=[pd.to_datetime(data_dict['timestamp'])],
                       y=[float(data_dict['sell_price'])])
    source_sell.stream(new_data=new_data_sell,rollover=200)
    
    if cnt % 4 == 0:
        data_dict_ave = get_last_row('average')
        new_data_buy_ave = dict(x=[pd.to_datetime(data_dict_ave['timestamp'])],
                            y=[float(data_dict_ave['buy_price'])]) 
        source_buy_ave.stream(new_data=new_data_buy_ave, rollover=200)

        new_data_sell_ave=dict(x=[pd.to_datetime(data_dict_ave['timestamp'])],
                           y=[float(data_dict_ave['sell_price'])])
        source_sell_ave.stream(new_data=new_data_sell_ave,rollover=200)
#######################################################################################
# the second parameter is refresh duration, unit is millisecond
# refer to https://bokeh.pydata.org/en/latest/docs/reference/document.html#bokeh.document.document.Document
curdoc().add_periodic_callback(update, 5 * 1000)
curdoc().add_root(row(column(fig_buy,fig_sell),column(fig_buy_ave, fig_sell_ave)))