import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import geocoder


app = dash.Dash()

app.layout = html.Div(children=[
    dcc.Input(
        id='zipcode',
        placeholder='Enter Zip Code',
        type='text',
        value=''
    ),

    dcc.Dropdown(
        id='dropdown',
        placeholder='Select Item',
        options=[
            {'label': u'Dairy & Eggs', 'value': 'dairy_egg'},
            {'label': u'Produce', 'value': 'msd'},
            {'label': u'MEAT & SOY PRODUCTS', 'value': 'ch'},
            {'label': u'NON-PERISHABLE (Soft Packed)', 'value':'other'}
        ]
    ),

    html.Div(
        id='checkboxes',
        children=[
        dcc.Checklist(
            options=[
                {'label': u'Yes', 'value': 'NYC'},
                {'label': u'No', 'value': 'MTL'}
            ],
        values=[]
        )])
])

@app.callback(Output('checkboxes', 'style'), [Input('dropdown', 'value')])
def toggle_container(toggle_value):
    if toggle_value == 'dairy_egg':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

def get_lat_long():
    g = geocoder.ip('me')
    print(g.latlng)

if __name__ == '__main__':
    app.run_server(debug=True, port=8000)