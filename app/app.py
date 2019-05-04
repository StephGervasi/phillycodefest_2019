import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import geocoder


app = dash.Dash(__name__)

app.layout = html.Div(children=[
    # dcc.Input(
    #     id='zipcode',
    #     placeholder='Enter Zip Code',
    #     type='text',
    #     value=''
    # ),
    #
    dcc.Dropdown(
        id='item',
        placeholder='Select Item',
        options=[
            {'label': u'Dairy & Eggs', 'value': 'dairy_egg'},
            {'label': u'Produce', 'value': 'msd'},
            {'label': u'MEAT & SOY PRODUCTS', 'value': 'ch'},
            {'label': u'NON-PERISHABLE (Soft Packed)', 'value':'other'}
        ]),

    html.Div(
        id='dairy_eggs',
        children=[
        dcc.Checklist(
            options=[
                {'label': r'Refrigerated', 'value': 'refrigerated'},
                {'label': r'Damaged or compromised packaging', 'value': 'damage_compromised_packaged'},
                {'label': r'Off odor or discoloration', 'value': 'odor_discoloration'},
                {'label': r'Mold', 'value': 'mold'}
            ],
        values=[],
        labelStyle={'display': 'inline-block'}
        )]),

    html.Div(
        id='dairy_eggs_subcat',
        children=[
        dcc.Checklist(
            options=[
                {'label': r'Fluid Dairy (Milk, Half and Half, Eggnog, etc)', 'value': 'fluid_dairy'},
                {'label': r'Yogurt, Sour Cream, Cottage Cheese, Pasta', 'value': 'multi'},
                {'label': r'Salad, Potato Salad, Coleslaw', 'value':'salads'},
                {'label': r'Hummus', 'value': 'hummus'},
                {'label': r'Refrigerated Juice, Perishable Beverages', 'value': 'juice'},
                {'label': r'Soy Milk', 'value': 'soy_milk'}
            ],
            values=[]
        )]),
])

@app.callback(Output(component_id='dairy_eggs', component_property='style'),
              [Input(component_id='item', component_property='value')])
def toggle_container(toggle_value):
    if toggle_value == 'dairy_egg':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(Output(component_id='dairy_eggs_subcat', component_property='style'),
              [Input(component_id='dairy_eggs', component_property='children')])
def toggle_container(toggle_value):
    values = toggle_value[0]['props']['values']
    print('values = {0}'.format(values))
    if values == 'refrigerated' and values not in ['damage_compromised_packaged', 'odor_discoloration', 'mold']:
        return {'display': 'block'}
    else:
        return {'display': 'none'}

def get_lat_long():
    g = geocoder.ip('me')
    print(g.latlng)

if __name__ == '__main__':
    app.run_server(debug=True, port=8000)