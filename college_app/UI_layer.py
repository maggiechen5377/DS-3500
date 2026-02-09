"""
1. make a drop down menu/list to select the states
2. sliding bar to increase or decrease enrollment number
3. two different tabs to click on for different data
    - completion rate
    - median earning (10 yrs)
4. 2 more sliding bars to decrease/increase the width or height
5. & 6. 2 tabs allowing us to click to show either college data/table or the sankey diagram

UI Layer
Aspects that form the front end (our dashboard).
Dashboard goals:
Plot -- Sankey Diagram
Pick a state and see selectiveness to median income flow/grad rates
- Dropdown -- state picker
- IntSlider -- minimum enrollment
- RadioGroup -- see grad rates vs median income
"""
import panel as pn
import sankey as sk
import college_api_mock as college_api

# DIMENSIONS
CARD_WIDTH = 320

def main():
    # Loads javascript dependencies and configures Panel (required)
    pn.extension()

    # Initialize API
    api = college_api.college_api_mock(college_api.DATA_FILE_PATH)
    api.proccess_data()

    # WIDGET DECLARATIONS
    state_slct = pn.widgets.Select(name = 'State', options = api.get_states())
    enrollment_sldr = pn.widgets.IntSlider(name = 'Enrollment', start=0, end = 100000, step = 10, value=0)

    # Search Widgets
    # Plotting widgets

    # CALLBACK FUNCTIONS
    # CALLBACK BINDINGS (Connecting widgets to callback functions)

    # DASHBOARD WIDGET CONTAINERS ("CARDS")
    search_card = pn.Card(
        pn.Column(
            state_slct
            enrollment_sldr
            # Widget 3
        ),
        title="Search", width=CARD_WIDTH, collapsed=False
    )


    plot_card = pn.Card(
        pn.Column(
            # Widget 1
            # Widget 2
            # Widget 3
        ),

        title="Plot", width=CARD_WIDTH, collapsed=True
    )


    # LAYOUT

    layout = pn.template.FastListTemplate(
        title="Maggie's College Explorer Dashboard",
        sidebar=[
            search_card,
            plot_card,
        ],
        theme_toggle=False,
        main=[
            pn.Tabs(
                ("Dataset", None),  # Replace None with callback binding
                ("Plot", None),  # Replace None with callback binding
                active=1  # Which tab is active by default?
            )
        ],
        header_background='#a93226'

    ).servable()

    layout.show()

if __name__ == "__main__":
    main()