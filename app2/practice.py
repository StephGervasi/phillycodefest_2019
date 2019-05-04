import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server=app.server
app.title = 'Lyme Spotter'
colors = {"background": "#ffb549", "text": "#111111"}
app.layout = html.Div(
    style={
        "backgroundColor": colors["background"],
        "width": "50%",
        "margin-left": "auto",
        "margin-right": "auto",
    },
    children=[
        html.H1(
            children='"Lyme Spotter"',
            style={"textAlign": "center", "color": colors["text"]},
        ),
        html.Div(
            "A companion diagnostic tool for patients with suspected Lyme disease",
            style={"textAlign": "center", "color": colors["text"]},
        ),
        html.Label("Rash Size"),
        dcc.Dropdown(
            id="large_rash",
            options=[
                {"label": "> 5 cm", "value": "0"},
                {"label": "< 5 cm", "value": "1"},
            ],
            value=1
        ),
        html.Label("Prophylactic Antibiotics Taken Today or Prior to Today?"),
        dcc.Dropdown(
            id="proph_abs",
            options=[{"label": "No", "value": "0"}, {"label": "Yes", "value": "1"}],
            value=1
        ),
        html.Label("Rash Expansion"),
        dcc.Dropdown(
            id="expansion",
            options=[{"label": "Yes", "value": "1"}, {"label": "No", "value": "0"}],
            value=1
        ),
        html.Label("Bullseye Shape Rash"),
        dcc.Dropdown(
            id="bullseye_shape",
            options=[{"label": "Yes", "value": "1"}, {"label": "No", "value": "0"}],
            value=1
        ),
        html.Label("Past History of Lyme Disease"),
        dcc.Dropdown(
            id="past_history_lyme",
            options=[{"label": "Yes", "value": "1"}, {"label": "No", "value": "0"}],
            value=1
        ),
        html.Label("Currently Taking Other Medications"),
        dcc.Dropdown(
            id="other_meds",
            options=[{"label": "Yes", "value": "1"}, {"label": "No", "value": "0"}],
            value=1
        ),
        html.Label("Observed Tick/Recall Seeing Tick Bite?"),
        dcc.Dropdown(
            id="recall_current_bite",
            options=[{"label": "Yes", "value": "1"}, {"label": "No", "value": "0"}],
            value=1
        ),
        html.Label("Past History of Cancer"),
        dcc.Dropdown(
            id="cancer_history",
            options=[{"label": "Yes", "value": "1"}, {"label": "No", "value": "0"}],
            value=1
        ),
        html.Label("Headache"),
        dcc.Dropdown(
            id="headache",
            options=[{"label": "Yes", "value": "1"}, {"label": "No", "value": "0"}],
            value=1
        ),
        html.Label("Fatigue"),
        dcc.Dropdown(
            id="fatigue",
            options=[{"label": "Yes", "value": "1"}, {"label": "No", "value": "0"}],
            value=1
        ),
        html.Label("City of Current Residence is Lyme Endemic (Northeast US)"),
        dcc.Dropdown(
            id="city_binary",
            options=[{"label": "Yes", "value": "1"}, {"label": "No", "value": "0"}],
            value=1
        ),
        html.Label("Multiple Locations of Rash on Body"),
        dcc.Dropdown(
            id="multiple_EM",
            options=[{"label": "Yes", "value": "1"}, {"label": "No", "value": "0"}],
            value=1
        ),
        html.Label("Month at First Visit to Clinic (no zero): "),
        dcc.Input(id="month_entry", value="0", type="number"),
        html.Br(),
        html.Label("Body Mass Index: "),
        dcc.Input(id="body_mass_index", value="0", type="number"),
        html.Br(),
        html.Label("Years at Current Residence: "),
        dcc.Input(id="yrs_at_residence", value="0", type="number"),
        html.Br(),
        html.Button(id="submit-button", children="Submit"),
        html.Div(id="output-a", style={"font-size": "40px", "text-align": "center"}),
    ]
)
@app.callback(
    Output("output-a", "children"),
    [Input("submit-button", "n_clicks")],
    [
        State("large_rash", "value"),
        State("proph_abs", "value"),
        State("expansion", "value"),
        State("bullseye_shape", "value"),
        State("past_history_lyme", "value"),
        State("other_meds", "value"),
        State("recall_current_bite", "value"),
        State("cancer_history", "value"),
        State("headache", "value"),
        State("fatigue", "value"),
        State("city_binary", "value"),
        State("multiple_EM", "value"),
        State("month_entry", "value"),
        State("body_mass_index", "value"),
        State("yrs_at_residence", "value"),
    ],
)
def predict(
    n_clicks,
    large_rash,
    proph_abs,
    expansion,
    bullseye_shape,
    past_history_lyme,
    other_meds,
    recall_current_bite,
    cancer_history,
    headache,
    fatigue,
    city_binary,
    multiple_EM,
    month_entry,
    body_mass_index,
    yrs_at_residence,
):
    imp = dict()
    imp["large_rash"] = large_rash
    imp["proph_abs"] = proph_abs
    imp["expansion"] = expansion
    imp["bullseye_shape"] = bullseye_shape
    imp["past_history_lyme"] = past_history_lyme
    imp["other_meds"] = other_meds
    imp["recall_current_bite"] = recall_current_bite
    imp["cancer_history"] = cancer_history
    imp["headache"] = headache
    imp["fatigue"] = fatigue
    imp["city_binary"] = city_binary
    imp["multiple_EM"] = multiple_EM
    imp["month_entry"] = month_entry
    imp["body_mass_index"] = body_mass_index
    imp["yrs_at_residence"] = yrs_at_residence
    imp = pd.Series(imp)
    print(imp)
    print(imp.dtypes)
    probs = model.predict_proba(imp.values.reshape(1, -1)) * 100
    print(probs)
    return f"{probs[0][1]:.2f}% risk of being positive for Lyme disease"
if __name__ == "__main__":
    app.run_server(debug=True)