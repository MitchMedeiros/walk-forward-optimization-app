from dash import html, dcc
import dash_bootstrap_components as dbc

nwindows_input = html.Div(
    [
        dbc.Label("Number of windows (1-20)"),
        dbc.Input(type='number', min=1, max=20, step=1, value=6, id='nwindows_in')
    ],
    className='dbc'
)

insample_dropdown = html.Div(
    [
        dbc.Label("In-sample percent"),
        dcc.Dropdown(['50%','55%','60%','65%','70%','75%','80%','85%','90%'], value='80%', id='insample_drop'),
    ],
    className='dbc'
)

# run_button = dbc.Button("Run Test", color="info", className="mt-auto")

# windowplot_button = dbc.Button("Show Windows", color="warning", className="mt-auto")

# accordion = html.Div(
#     dbc.Accordion(
#         [
#             dbc.AccordionItem(
#                 [
#                     html.P(
#                         "Optimize the strategy on a single in-sample period "
#                         "and check the results on an out-of-sample period immediately following. "
#                         "This test will provide more in-depth data and trade history." ,
#                         className="dbc"
#                     ),
#                     windowplot_button,
#                     run_button
#                 ],
#                 title="Single Window Test"
#             ),
#             dbc.AccordionItem(
#                 [
#                     html.P(
#                         "Test on a specified number of walk-forward windows. " 
#                         "Each in-sample period's optimized parameters will be used "
#                         "to test against the following out-of-sample period. "
#                         "Results from the out-of-sample windows will then be averaged across.",
#                         className="dbc"
#                     ),
#                     nwindows_dropdown,
#                     insample_dropdown,
#                     windowplot_button,
#                     run_button
#                 ],
#                 title="Walk-Forward Test"
#             )
#         ], 
#         active_item="item-1"
#     )
# )


# cards = dbc.CardGroup(
#     [
#         dbc.Card(
#             [
#                 dbc.CardHeader("Single Window Test"),
#                 dbc.CardBody(
#                     [
#                         html.P(
#                             "Optimize the strategy on a single in-sample period "
#                             "and check the results on an out-of-sample period immediately following. "
#                             "This test will provide more in-depth data and trade history." ,
#                             className="card-text"
#                         )
#                     ]
#                 ),
#                 dbc.CardFooter(
#                     [
#                         windowplot_button,
#                         run_button
#                     ]
#                 )
#             ],
#             color="primary", outline=True
#         ),
#         dbc.Card(
#             [
#                 dbc.CardHeader("Walk-Forward Test"),
#                 dbc.CardBody(
#                     [
#                         html.P(
#                             "Test on a specified number of walk-forward windows. " 
#                             "Each in-sample period's optimized parameters will be used "
#                             "to test against the following out-of-sample period. Results will then be averaged across.",
#                             className="card-text"
#                         )
#                     ]
#                 ),
#                 dbc.CardFooter(
#                     [
#                         nwindows_dropdown,
#                         insample_dropdown,
#                         windowplot_button,
#                         run_button
#                     ]
#                 )
#             ],
#             color="primary", outline=True
#         )
#     ], className="dbc"
# )