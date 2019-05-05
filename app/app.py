import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import geocoder


app = dash.Dash(__name__)

app.layout = html.Div(children=[

    # zipcode input box
    dcc.Input(
        id='zipcode',
        placeholder='Enter Zip Code',
        type='text',
        value=''
    ),

    html.Button('Search', id='button', n_clicks=0),

    html.Div(id='output-submit'),

    # Item selection menu
    dcc.Dropdown(
        id='item',
        placeholder='Select Item',
        options=[
            {'label': u'Dairy & Eggs', 'value': 'dairy_egg'},
            {'label': u'Produce', 'value': 'produce'},
            {'label': u'MEAT & SOY PRODUCTS', 'value': 'meat_soy'},
            {'label': u'NON-PERISHABLE (Soft Packed)', 'value':'non_peri_soft'},
            {'label': u'NON-PERISHABLE (Hard Packed)', 'value':'non_peri_hard'},
            {'label': u'NON-PERISHABLE (Frozen)', 'value':'non_peri_frozen'}
        ]),

    dcc.Checklist(
        id='dairy_eggs',
        options=[
            {'label': r'Refrigerated', 'value': 'refrigerated'},
            {'label': r'Damaged or compromised packaging', 'value': 'damage_compromised_packaged'},
            {'label': r'Off odor or discoloration', 'value': 'odor_discoloration'},
            {'label': r'Mold', 'value': 'mold'}
            ],
        values=[]
    ),

    dcc.Checklist(
        id='produce',
        options=[
            {'label': r'Refrigerated', 'value': 'refrigerated'},
            {'label': r'80-90% of product good for additional 3-5 days after pick-up', 'value': '89'},
            {'label': r'Off odor or discoloration', 'value': 'odor'},
            {'label': r'Mold, fungus, insects, or significant decay', 'value': 'mold_fungus_insects_decay'},
        ],
        values=[]
    ),

    dcc.Checklist(
        id='meat_soy',
        options=[
            {'label': r'Frozen within 24 hours of product date', 'value': 'frozen24'},
            {'label': r'Accepted up to 180 days after product date', 'value': 'accepted_180'},
            {'label': r'Defrosted', 'value': 'defrosted'},
            {'label': r'Severe freezer burn', 'value': 'severe_freezer_burn'},
            {'label': r'Off odor or discoloration', 'value': 'odor_discoloration'},
            {'label': r'Bloated package', 'value': 'bloated'},
        ],
        values=[]
    ),

    dcc.Checklist(
        id='non_peri_soft',
        options=[
            {'label': r'Intack packaging', 'value': 'intack'},
            {'label': r'Punctured packaging', 'value': 'puncture'},
            {'label': r'Accepted up to 180 days after product date', 'value': 'accepted_180'},
            {'label': r'Leaking ', 'value': 'leaking'}
        ],
        values=[]
    ),

    dcc.Checklist(
        id='non_peri_hard',
        options=[
            {'label': r'Canned & Jarred products (Soup, Condiments, Vegetables, Fish, Meat)', 'value': 'canned_jarred'},
            {'label': r'Room temperature', 'value': 'room_temp'},
            {'label': r'Open, punctured, bulging, leaking, or seriously damaged', 'value': 'open_punctured_bulding_leak'},
            {'label': r'Broken or chipped glass ', 'value': 'broken_chipped'}
        ],
        values=[]
    ),

    dcc.Checklist(
        id='non_peri_frozen',
        options=[
            {'label': r'frozen', 'value': 'frozen'},
            {'label': r'Severe freezer burn', 'value': 'freezer_burn'},
            {'label': r'Seriously damaged', 'value': 'damaged'},
        ],
        values=[]
    ),

    dcc.Checklist(
        id='dairy_eggs_subcat',
        options=[
            {'label': r'Fluid Dairy (Milk, Half and Half, Eggnog, etc)', 'value': 'fluid_dairy'},
            {'label': r'Yogurt, Sour Cream, Cottage Cheese, Pasta', 'value': 'multi'},
            {'label': r'Salad, Potato Salad, Coleslaw', 'value': 'salads'},
            {'label': r'Hummus', 'value': 'hummus'},
            {'label': r'Refrigerated Juice, Perishable Beverages', 'value': 'juice'},
            {'label': r'Soy Milk', 'value': 'soy_milk'}
        ],
        values=[]
    )
])

@app.callback(Output('output-submit', 'children'),
              [Input('button', 'n_clicks')],
              [State('zipcode', 'value')])
def update_output(_, input):
    print(input)

@app.callback(Output(component_id='dairy_eggs', component_property='style'),
              [Input(component_id='item', component_property='value')])
def toggle_container(toggle_value):
    if toggle_value == 'dairy_egg':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(Output(component_id='produce', component_property='style'),
              [Input(component_id='item', component_property='value')])
def toggle_container(toggle_value):
    if toggle_value == 'produce':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(Output(component_id='meat_soy', component_property='style'),
              [Input(component_id='item', component_property='value')])
def toggle_container(toggle_value):
    if toggle_value == 'meat_soy':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(Output(component_id='non_peri_soft', component_property='style'),
              [Input(component_id='item', component_property='value')])
def toggle_container(toggle_value):
    if toggle_value == 'non_peri_soft':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(Output(component_id='non_peri_hard', component_property='style'),
              [Input(component_id='item', component_property='value')])
def toggle_container(toggle_value):
    if toggle_value == 'non_peri_hard':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(Output(component_id='non_peri_frozen', component_property='style'),
              [Input(component_id='item', component_property='value')])
def toggle_container(toggle_value):
    if toggle_value == 'non_peri_frozen':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(Output(component_id='dairy_eggs_subcat', component_property='style'),
              [Input(component_id='dairy_eggs', component_property='values')])
def toggle_container(checklist_values):
    if 'refrigerated' in checklist_values and \
            'damage_compromised_packaged' not in checklist_values and  \
            'odor_discoloration' not in checklist_values and 'mold' not in checklist_values:
        return {'display': 'block'}
    else:
        return {'display': 'none'}

def get_lat_long():
    g = geocoder.ip('me')
    print(g.latlng)

if __name__ == '__main__':
    app.run_server(debug=True, port=8000)