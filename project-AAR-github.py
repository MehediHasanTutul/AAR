import streamlit as st
import plotly.express as px
import pandas as pd
from PIL import Image
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
st.set_page_config(layout="wide")


def layout_for_firefighter_icon(source, length, loop_j, x_val, y_val, sizexy=0.2, xanchor="center", xyref="paper"):
    return dict(
        # row=1,
        # col=col + 1,
        source=source,
        xref=xyref,
        yref=xyref,
        x=(loop_j+x_val)/length,
        y=y_val,
        xanchor=xanchor,
        # yanchor="top",
        sizex=sizexy,
        sizey=sizexy,
        )

tcol1, tcol2, tcol3 = st.columns([1, 8, 1])
tcol1.image(Image.open('fire_icon.png'),width=70)
tcol2.markdown("<h2 style='text-align: center; color: white;'>AAR Webapp</h2>", unsafe_allow_html=True)
tcol3.image(Image.open('IISRI_logo.png'),width=150)

col1,col2,col3 = st.columns(3)

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        col2.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        col2.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True


if check_password():

    # st.button("Click me")     
    tab0, tab1, tab2, tab3, tab4, tab5 = st.tabs(['Home', "Individual Analysis", "Comparative Analysis", "Objective Analysis", "Machine Learning", "Progress through Sessions"])

    with tab0:
        
        tcol1, tcol2 = st.columns(2)
        

                                                
    with tab1:
        
    
        # st.subheader("Single Firefighter Report")
        
    
        
        col1,col2,col3 = st.columns(3)
        col21,col22 = st.columns(2)
        col31,col32 = st.columns(2)
        col41,col42 = st.columns(2)
        col = [col21,col22, col31,col32, col41, col42]
        file = "data_all_collectionData_211116_data_analysisDate_211118.csv"
        df = pd.read_csv(file)
        
        subject_select = col1.selectbox(label="Select Subject", options = df['subject'].unique())
        
        df1 = df.loc[df['subject'] == subject_select]
        # fig_name_dict = {
        #     'total_air_usage': 'AC_Report.png',
        #     'BTs' : 'BT_Report.png',
        #     'HRs': 'heart_icon.png',             
        # }
        
        y_val = ['HRs', 'BTs', 'BRs']
        title_val = ['Heart Rate', 'Body Temperature', 'Respiration Rate']
        img_val = ['heart_icon.png', 'BT_Report.png', 'lung_icon.png']
        text_val = ['Heart Rate', 'Body <br>Temperature', 'Respiration <br> Rate']
        
        chart_select = col2.selectbox(label="Select plot type", options = ['line', 'violin','histogram', 'box' ])
        for i in range(3):
            
            if chart_select=='line':
                plot  = px.line(data_frame = df1, x = 'time', y = y_val[i],
                    labels={'time': "Time (Sec.)",y_val[i]: "", },
                title=f"<b>Time vs. {title_val[i]}</b>",)  ##   Heart Rate
            else:
                plot  = px.scatter(data_frame = df1, x = 'time', y = y_val[i], marginal_y=chart_select,  
                    labels={'time': "Time (Sec.)",y_val[i]: "", },
                title=f"<b>Time vs. {title_val[i]}</b>",)  ##   Heart Rate
            
            
            icon_src = Image.open(f"{img_val[i]}")
             ##  
            plot.add_layout_image(dict(
            # row=1,
            # col=col + 1,
            source=icon_src,
            xref="paper",
            yref="paper",
            x=-0.14,
            y=.8,
            xanchor="center",
            # yanchor="top",
            sizex=0.3,
            sizey=0.3,
            )
                )
            plot.update_layout(
                width=550,
            # title="Annotations' position",
            # yaxis=dict(
            #     # title_text="Y-axis Title",
            #     ticktext=["Very long title", "long title", "5", "short title"],
            #     tickvals=[max(df1[y_values])],
            #     tickmode="array",
            #     titlefont=dict(size=20),
            # ),
            
            annotations=\
            [
            {"xref": "paper", "yref": "paper","xanchor": "center","x":-0.14, "y":0, 
             "text": f"<b>Max. {max(df1[y_val[i]]):.2f}</b>",'font': {'size': 16, 'color': 'white'}, "showarrow":False},
            {"xref": "paper", "yref": "paper","xanchor": "center","x":-0.14, "y":0.2, 
             "text": f"<b>Avg. {(df1[y_val[i]]).mean():.2f}</b>",'font': {'size': 16, 'color': 'white'}, "showarrow":False},
            {"xref": "paper", "yref": "paper","xanchor": "center","x":-0.14, "y":0.4, 
             "text": f"<b>Min. {min(df1[y_val[i]]):.2f}</b>",'font': {'size': 16, 'color': 'white'}, "showarrow":False},
            {"xref": "paper", "yref": "paper", "xanchor": "center","x":-0.14, "y":1, 
             "text": f"<b>{text_val[i]}</b>", 'font': {'size': 16, 'color': 'white'}, "showarrow":False}  ## 
            ],
            margin={"l":150, "r": 10},
            )
            plot.update_yaxes(automargin=True)
            
            
            col[i].plotly_chart(plot)
        
        
        # for air usage Gauge meter
        
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",  #+delta
            value = df1['total_air_usage'].mean()/1000,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "<b>Total Air Usage (Litres)</b>", 'font': {'size': 24}},
            # delta = {'reference': 400, 'increasing': {'color': "RebeccaPurple"}},
            gauge = {
                'axis': {'range': [None, 500], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "darkblue"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 250], 'color': 'lightblue'},
                    {'range': [250, 400], 'color': 'royalblue'},
                    {'range': [400, 500], 'color': 'red'}
                ],
        #         'threshold': {
        #             'line': {'color': "red", 'width': 4},
        #             'thickness': 0.75,
        #             'value': 490}
            }))
        
        icon_src2 = Image.open("AC_Report.png")
        fig.add_layout_image(dict(
        # row=1,
        # col=col + 1,
        source=icon_src2,
        xref="paper",
        yref="paper",
        x=0.5,
        y=.6,
        xanchor="center",
        # yanchor="top",
        sizex=0.3,
        sizey=0.3,
        )
            )
        
        fig.update_layout(
        # autosize=False,
        width=500,
        # height=500,
        # annotations=\
        # [
        # {"xref": "paper", "yref": "paper","xanchor": "center","x":-0.14, "y":0, 
        #  "text": f"<b>Max. {max(df1[y_values]):.2f}</b>",'font': {'size': 16, 'color': 'white'}, "showarrow":False},
        
        # ],
        margin={"l":1, "r": 1},
        )
        col[4].plotly_chart(fig)
        
        
        
        # generate fire intensity chart
        
        def processToShowFireIntensity(df1,subject='subject_1'):
            
            length = len(df1)
            df1 = df1.set_index('time')
        
            vertical_stack = pd.concat([df1['Intensity_1'], df1['Intensity_2'],df1['Intensity_3'],
                                        df1['Intensity_4'],df1['Intensity_5']], axis=0)
        
        
            tag =pd.Series(['Intensity_1' for i in range(length)]+ ['Intensity_2' for i in range(length)]+  \
                        ['Intensity_3' for i in range(length)]+ \
                        ['Intensity_4' for i in range(length)]+ ['Intensity_5' for i in range(length)],index = vertical_stack.index)
        
            vertical_stack = pd.concat([vertical_stack, tag], axis=1)
        
            vertical_stack.columns=["Fire Intensity","level"]
        
            vertical_stack.reset_index(inplace=True)
            return vertical_stack 
        vertical_stack=processToShowFireIntensity(df1,subject=subject_select)
        
        
        col_intense = ['Intensity_1', 'Intensity_2', 'Intensity_3', 'Intensity_4','Intensity_5']
        mx = df1[col_intense].max().values
        avg = df1[col_intense].mean().values
        
        # icon_path = "D:/OneDrive - Deakin University/abbas web app project/project 2 - fire fighter/icon/Icons/Icons 1/"
        
        if chart_select=='line':
            plot = px.line(data_frame = vertical_stack, x = 'time', y = "Fire Intensity", color = 'level' ,
                           labels={'time': "Time (Sec.)",})
        else:
            plot = px.scatter(data_frame = vertical_stack, x = 'time', y = "Fire Intensity", 
                              color = 'level',marginal_y=chart_select , labels={'time': "Time (Sec.)",})
          
        
        plot.update_layout(
            annotations=\
            [
            {"xref": "paper", "yref": "paper","xanchor": "center","x":-0., "y":1.35, 
             "text": "<b>Max. Intensity</b>",'font': {'size': 15, 'color': 'white'}, "showarrow":False},  #{mx[0]:.2f}
            {"xref": "paper", "yref": "paper","xanchor": "center","x":-0., "y":1.20, 
             "text": "<b>Avg. Intensity</b>",'font': {'size': 15, 'color': 'white'}, "showarrow":False},  # {avg[0]:.2f}
                
            {"xref": "paper", "yref": "paper","xanchor": "center","x":0.2, "y":1.35, 
             "text": f"<b>{mx[0]:.2f} %</b>",'font': {'size': 15, 'color': 'white'}, "showarrow":False},  #
            {"xref": "paper", "yref": "paper","xanchor": "center","x":0.2, "y":1.20, 
             "text": f"<b>{avg[0]:.2f} %</b>",'font': {'size': 15, 'color': 'white'}, "showarrow":False},  # 
                
                {"xref": "paper", "yref": "paper","xanchor": "center","x":0.4, "y":1.35, 
             "text": f"<b>{mx[1]:.2f} %</b>",'font': {'size': 15, 'color': 'white'}, "showarrow":False},  #{mx[0]:.2f}
            {"xref": "paper", "yref": "paper","xanchor": "center","x":0.4, "y":1.20, 
             "text": f"<b>{avg[1]:.2f} %</b>",'font': {'size': 15, 'color': 'white'}, "showarrow":False},  # {avg[0]:.2f}
                
                {"xref": "paper", "yref": "paper","xanchor": "center","x":0.6, "y":1.35, 
             "text": f"<b>{mx[2]:.2f} %</b>",'font': {'size': 15, 'color': 'white'}, "showarrow":False},  #{mx[0]:.2f}
            {"xref": "paper", "yref": "paper","xanchor": "center","x":0.6, "y":1.20, 
             "text": f"<b>{avg[2]:.2f} %</b>",'font': {'size': 15, 'color': 'white'}, "showarrow":False},  # {avg[0]:.2f}
                
                {"xref": "paper", "yref": "paper","xanchor": "center","x":0.8, "y":1.35, 
             "text": f"<b>{mx[3]:.2f} %</b>",'font': {'size': 15, 'color': 'white'}, "showarrow":False},  #{mx[0]:.2f}
            {"xref": "paper", "yref": "paper","xanchor": "center","x":0.8, "y":1.20, 
             "text": f"<b>{avg[3]:.2f} %</b>",'font': {'size': 15, 'color': 'white'}, "showarrow":False},  # {avg[0]:.2f}
                
                {"xref": "paper", "yref": "paper","xanchor": "center","x":1., "y":1.35, 
             "text": f"<b>{mx[4]:.2f} %</b>",'font': {'size': 15, 'color': 'white'}, "showarrow":False},  #{mx[0]:.2f}
            {"xref": "paper", "yref": "paper","xanchor": "center","x":1., "y":1.20, 
             "text": f"<b>{avg[4]:.2f} %</b>",'font': {'size': 15, 'color': 'white'}, "showarrow":False},  # {avg[0]:.2f}
        #     {"xref": "paper", "yref": "paper","xanchor": "center","x":-0.14, "y":0.4, 
        #      "text": f"<b>Min. {mn[0]:.2f}</b>",'font': {'size': 15, 'color': 'white'}, "showarrow":False},
            {"xref": "paper", "yref": "paper", "xanchor": "center","x":-0., "y":1.8, 
             "text": "<b>Fires</b>", 'font': {'size': 15, 'color': 'white'}, "showarrow":False}
            ],
            width=600,
            height=500,
            margin={"l":30, "r": 10,"t":200},
            )
        plot.add_layout_image(dict(
        # row=1,
        # col=col + 1,
        source=Image.open("fire_icon.png"),
        xref="paper",
        yref="paper",
        x=0.,
        y=1.7,
        xanchor="center",
        # yanchor="top",
        sizex=0.3,
        sizey=0.3,
        )
            )
        for i in range(5):
            plot.add_layout_image(dict(
                # row=1,
                # col=col + 1,
                source=Image.open(f'{i+1}.png'),
                xref="paper",
                yref="paper",
                x=(i+1)*0.2,
                y=1.7,
                xanchor="center",
                # yanchor="top",
                sizex=0.18,
                sizey=0.18,
                )
                    )
        
        col[3].plotly_chart(plot)
        
        
        # for air usage Gauge meter
        
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",  #+delta
            value = df1['total_water_usage'].mean()/1000,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "<b>Total Water Usage (Litres)</b>", 'font': {'size': 24}},
            # delta = {'reference': 400, 'increasing': {'color': "RebeccaPurple"}},
            gauge = {
                'axis': {'range': [None, 500], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "darkblue"},
                'bgcolor': "black",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 250], 'color': 'lightblue'},
                    {'range': [250, 400], 'color': 'royalblue'},
                    {'range': [400, 500], 'color': 'red'}
                ],
        #         'threshold': {
        #             'line': {'color': "red", 'width': 4},
        #             'thickness': 0.75,
        #             'value': 490}
            }))
        
        icon_src2 = Image.open("water_icon.png")
        fig.add_layout_image(dict(
        # row=1,
        # col=col + 1,
        source=icon_src2,
        xref="paper",
        yref="paper",
        x=0.5,
        y=.6,
        xanchor="center",
        # yanchor="top",
        sizex=0.3,
        sizey=0.3,
        )
            )
        
        fig.update_layout(
        # autosize=False,
        width=500,
        # height=500,
        # annotations=\
        # [
        # {"xref": "paper", "yref": "paper","xanchor": "center","x":-0.14, "y":0, 
        #  "text": f"<b>Max. {max(df1[y_values]):.2f}</b>",'font': {'size': 16, 'color': 'white'}, "showarrow":False},
        
        # ],
        margin={"l":1, "r": 1},
        )
        col[5].plotly_chart(fig)
            
    
    with tab2:
        
        # st.subheader("Comparison among Firefighters")
        
        col1,col2,col3 = st.columns(3)
        col21,col22 = st.columns(2)
        col31,col32 = st.columns(2)
        col41,col42 = st.columns(2)
        col = [col21,col22, col31,col32, col41, col42]
        file = "data_all_collectionData_211116_data_analysisDate_211118.csv"
        df = pd.read_csv(file)
        
        subject_select = col1.multiselect(label="Select the subjects you want to compare", options = df['subject'].unique(), default=['subject_1', 'subject_2'])
        chart_select = col2.selectbox(label="Select plot type", options = ['line', 'violin', 'box', 'histogram'])
        
        
        total_air_usage = ['Air <br>Comsumption']
        total_water_usage = []
        
        if subject_select != []:
            df1=pd.DataFrame()
            for sub in subject_select:
                dff = df.loc[df['subject'] == sub]
                dff['total_water_usage'] = dff['total_water_usage']/(1000*len(dff['total_water_usage']))
                dff['total_air_usage'] = dff['total_air_usage']/(1000*len(dff['total_air_usage']))
                df1 = pd.concat([df1,dff], axis=0)
                
                # total_water_usage.append(round(df1['total_water_usage'].mean()/1000,2))
             
            y_val = ['HRs', 'BTs', 'BRs']
            title_val = ['Heart Rate', 'Body Temperature', 'Respiration Rate']
            img_val = ['heart_icon.png', 'BT_Report.png', 'lung_icon.png']
            text_val = ['Heart Rate', 'Body <br>Temperature', 'Respiration <br> Rate']
            length = len(subject_select)
            
            for i in range(3):
                
                if chart_select=='line':
                    plot  = px.line(data_frame = df1, x = 'time', y = y_val[i], color = 'subject',
                        labels={'time': "Time (Sec.)",y_val[i]: title_val[i], },
                    # title=f"<b>Time vs. {title_val[i]}</b>",
                    )  ##   Heart Rate
                else:
                    plot  = px.scatter(data_frame = df1, x = 'time', y = y_val[i], marginal_y=chart_select,color = 'subject',
                        labels={'time': "Time (Sec.)",y_val[i]: title_val[i], },
                    # title=f"<b>Time vs. {title_val[i]}</b>",
                    )  ##   Heart Rate
                
                
                icon_src = Image.open(f"{img_val[i]}")
                 ##  
                plot.add_layout_image(
                    dict(
                # row=1,
                # col=col + 1,
                source=icon_src,
                xref="paper",
                yref="paper",
                x=0.,
                y=1.65,
                xanchor="center",
                # yanchor="top",
                sizex=0.25,
                sizey=0.25,
                )
                    )
                
                source=Image.open("firefighter_Report.png")
                
                annotate_value = []
                
                for j in range(length):
                    plot.add_layout_image(
                        layout_for_firefighter_icon(source=source, length=length, loop_j=j, x_val=1, y_val=1.65, sizexy=0.22, xanchor="center", xyref="paper")
                        
                        )
                    
                    
                    
                    annotate_value.extend([
                    {"xref": "paper", "yref": "paper","xanchor": "center","x":(j+1)/length, "y":1.4, 
                     "text": f"<b>{max(df1.loc[df1['subject'] == subject_select[j]][y_val[i]]):.1f}</b>",'font': {'size': 16, 'color': 'white'}, "showarrow":False},
                    {"xref": "paper", "yref": "paper","xanchor": "center","x":(j+1)/length, "y":1.28, 
                     "text": f"<b>{(df1.loc[df1['subject'] == subject_select[j]][y_val[i]]).mean():.1f}</b>",'font': {'size': 16, 'color': 'white'}, "showarrow":False},
                    {"xref": "paper", "yref": "paper","xanchor": "center","x":(j+1)/length, "y":1.16, 
                     "text": f"<b>{min(df1.loc[df1['subject'] == subject_select[j]][y_val[i]]):.1f}</b>",'font': {'size': 16, 'color': 'white'}, "showarrow":False},
                    # {"xref": "paper", "yref": "paper", "xanchor": "center","x":-0.14, "y":1, 
                    #  "text": f"<b>{text_val[i]}</b>", 'font': {'size': 16, 'color': 'white'}, "showarrow":False}  ## 
                    ])
                    
                plot.update_layout(
                    width=500,
                    height = 500,
                # title="Annotations' position",
                # yaxis=dict(
                #     # title_text="Y-axis Title",
                #     ticktext=["Very long title", "long title", "5", "short title"],
                #     tickvals=[max(df1[y_values])],
                #     tickmode="array",
                #     titlefont=dict(size=20),
                # ),
                
                annotations=annotate_value+\
                [
                {"xref": "paper", "yref": "paper","xanchor": "center","x":-0., "y":1.4, 
                 "text": "<b>Max.</b>",'font': {'size': 16, 'color': 'white'}, "showarrow":False},
                {"xref": "paper", "yref": "paper","xanchor": "center","x":-0., "y":1.28, 
                 "text": "<b>Avg.</b>",'font': {'size': 16, 'color': 'white'}, "showarrow":False},
                {"xref": "paper", "yref": "paper","xanchor": "center","x":-0., "y":1.16, 
                 "text": "<b>Min.</b>",'font': {'size': 16, 'color': 'white'}, "showarrow":False},
                {"xref": "paper", "yref": "paper", "xanchor": "center","x":-0., "y":1.84, 
                 "text": f"<b>{text_val[i]}</b>", 'font': {'size': 15, 'color': 'white'}, "showarrow":False}
                # {"xref": "paper", "yref": "paper", "xanchor": "center","x":-0.14, "y":1, 
                #  "text": f"<b>{text_val[i]}</b>", 'font': {'size': 16, 'color': 'white'}, "showarrow":False}  ## 
                ],
                margin={"l":5, "r": 5, 't':200},
                )
                plot.update_yaxes(automargin=True)
                
                
                col[i].plotly_chart(plot)
            
            
            # for air usage Gauge meter
            
            
        
        
            
            icon_src2 = Image.open("AC_Report.png")
            
            
            plot = px.histogram(df1, x="subject", y= 'total_air_usage', title="Total Air Consumption (Litre)", 
                          text_auto='.0f', color_discrete_sequence =['lightblue'],
                          labels={'total_air_usage': 'Air Usage',})
            
            
            plot.add_layout_image(dict(
                # row=1,
                # col=col + 1,
                source=icon_src2,
                xref="paper",
                yref="paper",
                x=0.+0.5,
                y=1.5,
                xanchor="center",
                # yanchor="top",
                sizex=0.25,
                sizey=0.25,
                )
                    )
            
            for j in range(length):
                plot.add_layout_image(
                    
                    layout_for_firefighter_icon(source=source, length=length, loop_j=j, x_val=0.5, y_val=1.25, sizexy=0.22, xanchor="center", xyref="paper")
     
                    )
            # plot.update_layout(width=600, margin={"l":0, "r": 0,"t":200, 'b':0},) 
            
            plot.update_layout(width=500, margin={"l":0, "r": 0,"t":200, 'b':0},
                               title='Total Air Consumption (Litre)') 
            col[4].plotly_chart(plot)
            
            
            
            # generate fire intensity chart
            
            
            col_intense = ['Intensity_1', 'Intensity_2', 'Intensity_3', 'Intensity_4','Intensity_5']
            mx = df1[col_intense].max().values
            avg = df1[col_intense].mean().values
        
            # icon_path = "D:/OneDrive - Deakin University/abbas web app project/project 2 - fire fighter/icon/Icons/Icons 1/"
            
            if chart_select=='line':
                plot = px.line(data_frame = df1, x = 'time', y = "fire_intensity", color = 'subject' ,
                               labels={'time': "Time (Sec.)","fire_intensity":"Total Fire Intensity"})
            else:
                plot = px.scatter(data_frame = df1, x = 'time', y = "fire_intensity", color = 'subject',
                                  marginal_y=chart_select, labels={'time': "Time (Sec.)","fire_intensity":"Total Fire Intensity"} )
              
            annotate_value=[]
            for j in range(length):
                plot.add_layout_image(
                    layout_for_firefighter_icon(source=source, length=length, loop_j=j, x_val=1, y_val=1.65, sizexy=0.22, xanchor="center", xyref="paper")
        
                    )
                
                annotate_value.extend([
                {"xref": "paper", "yref": "paper","xanchor": "center","x":(j+1)/length, "y":1.35, 
                 "text": f"<b>{max(df1.loc[df1['subject'] == subject_select[j]]['fire_intensity']):.1f}</b>",'font': {'size': 16, 'color': 'white'}, "showarrow":False},
                {"xref": "paper", "yref": "paper","xanchor": "center","x":(j+1)/length, "y":1.20, 
                 "text": f"<b>{(df1.loc[df1['subject'] == subject_select[j]]['fire_intensity']).mean():.1f}</b>",'font': {'size': 16, 'color': 'white'}, "showarrow":False},
                
                ])
            
            plot.update_layout(
                annotations=annotate_value+\
                [
                {"xref": "paper", "yref": "paper","xanchor": "center","x":-0., "y":1.35, 
                 "text": "<b>Max.</b>",'font': {'size': 15, 'color': 'white'}, "showarrow":False},  #{mx[0]:.2f}
                {"xref": "paper", "yref": "paper","xanchor": "center","x":-0., "y":1.20, 
                 "text": "<b>Avg.</b>",'font': {'size': 15, 'color': 'white'}, "showarrow":False},  # {avg[0]:.2f}
                    
                {"xref": "paper", "yref": "paper", "xanchor": "center","x":-0., "y":1.8, 
                 "text": "<b>Fires</b>", 'font': {'size': 15, 'color': 'white'}, "showarrow":False}
                ],
                width=500,
                height=500,
                margin={"l":30, "r": 10,"t":200},
                )
            plot.add_layout_image(dict(
            # row=1,
            # col=col + 1,
            source=Image.open("fire_icon.png"),
            xref="paper",
            yref="paper",
            x=0.,
            y=1.7,
            xanchor="center",
            # yanchor="top",
            sizex=0.3,
            sizey=0.3,
            )
                )
        
            col[3].plotly_chart(plot)
            
            
            # for Water Usage
            
            
            # value = df1['total_water_usage'].mean()/1000,
                
            icon_src2 = Image.open("water_icon.png")
            
            
            plot = px.histogram(df1, x="subject", y= 'total_water_usage', title="Total Water Usage (Litre)", 
                          text_auto='.0f', color_discrete_sequence =['lightblue'],
                          labels={'total_water_usage': 'Water Usage',})
            
            
            plot.add_layout_image(dict(
                # row=1,
                # col=col + 1,
                source=icon_src2,
                xref="paper",
                yref="paper",
                x=0.+0.5,
                y=1.5,
                xanchor="center",
                # yanchor="top",
                sizex=0.25,
                sizey=0.25,
                )
                    )
            
            for j in range(length):
                plot.add_layout_image(
                    
                    layout_for_firefighter_icon(source=source, length=length, loop_j=j, x_val=0.5, y_val=1.25, sizexy=0.22, xanchor="center", xyref="paper")
    
                    )
            plot.update_layout(width=500, margin={"l":0, "r": 0,"t":200, 'b':0},) 
            col[5].plotly_chart(plot)
            
    
    
    
    with tab3:
        
        # st.subheader("Objective Analysis of performance among Firefighters")
        
        
        
        col1,col2,col3 = st.columns(3)
        col21,col22 = st.columns(2)
        col31,col32 = st.columns(2)
        col41,col42 = st.columns(2)
        col = [col21,col22, col31,col32, col41, col42]
        file = "data_all_collectionData_211116_data_analysisDate_211118.csv"
        df = pd.read_csv(file)
        
        subject_select = col1.multiselect(label="Select the subjects you want to compare", options = df['subject'].unique(), default=df['subject'].unique()[:3])
        chart_select = col2.selectbox(label="Select plot type", options = ['violin', 'box', 'histogram'])
        
        def integrate(x, y):
            sm = 0
            for i in range(1, len(x)):
               h = x[i] - x[i-1]
               sm += h * (y[i-1] + y[i]) / 2
        
            return sm
            
        if subject_select != []:
            df1=pd.DataFrame()
            for sub in subject_select:
                dff = df.loc[df['subject'] == sub]
                dff['total_water_usage'] = round(dff['total_water_usage']/1000,1)
                dff['total_air_usage'] = round(dff['total_air_usage']/1000,1)
                dff['total_air_usage_during_fire_attack'] = dff['total_air_usage_during_fire_attack']/1000
                dff['fire_attack_duration'] = round(integrate(dff.loc[dff['attack_flag']==1,'time'].values,
                                                        dff.loc[dff['attack_flag']==1,'fire_intensity'].values)/ \
                                                dff.loc[dff['attack_flag']==1,'fire_intensity'].values[0],1)
                df1 = pd.concat([df1,dff], axis=0)
             
            df1.rename(columns = {'fire_attack_duration':'Relative Area Under Fire Intensity Curve'}, inplace = True)
                # total_water_usage.append(round(df1['total_water_usage'].mean()/1000,2))
             
            y_val = ['HRs', 'BTs', 'BRs']
            title_val = ['Heart Rate', 'Body Temperature', 'Respiration Rate']
            img_val = ['heart_icon.png', 'BT_Report.png', 'lung_icon.png']
            text_val = ['Heart Rate', 'Body <br>Temperature', 'Respiration <br> Rate']
            length = len(subject_select)
            
            plot  = px.scatter(data_frame = df1, x = 'AirUsage', y = 'water_usage', marginal_y=chart_select,marginal_x=chart_select,
                               color = 'subject',labels={'AirUsage': 'Air Usage','water_usage': 'Water Usage', },
            # title=f"<b>Time vs. {title_val[i]}</b>",
            ) 
            
            source=Image.open("firefighter_Report.png")
            
            
            
            for j in range(length):
                plot.add_layout_image(
                    
                    layout_for_firefighter_icon(source=source, length=length, loop_j=j, x_val=0.5, y_val=1.25, sizexy=0.16, xanchor="center", xyref="paper")
    
                    )
            plot.update_layout(
                width=550,
                height = 500,
            # title= 'Air Usage and Water Usage',
        
            
            annotations=\
            [
            {"xref": "paper", "yref": "paper","xanchor": "left","x":-0., "y":1.33, 
              "text": "<b>Water Usage vs. Air Usage</b>",'font': {'size': 16, 'color': 'white'}, "showarrow":False},
        
            ],
            margin={"l":5, "r": 5, 't':100},
            )
            plot.update_yaxes(automargin=True)
            
            
            col21.plotly_chart(plot)
            
            plot  = px.scatter(data_frame = df1, x = 'fire_intensity', y = 'water_usage', marginal_y=chart_select,marginal_x=chart_select,
                               color = 'subject',labels={'fire_intensity': 'Fire Intensity','water_usage': 'Water Usage', },
            # title=f"<b>Time vs. {title_val[i]}</b>",
            ) 
            
            
            for j in range(length):
                plot.add_layout_image(
                    
                    layout_for_firefighter_icon(source=source, length=length, loop_j=j, x_val=0.5, y_val=1.25, sizexy=0.16, xanchor="center", xyref="paper")
    
                    )
            plot.update_layout(
                width=550,
                height = 500,
            # title= 'Air Usage and Water Usage',
        
            
            annotations=\
            [
            {"xref": "paper", "yref": "paper","xanchor": "left","x":-0., "y":1.33, 
              "text": "<b>Water Usage Vs. Fire Intensity</b>",'font': {'size': 16, 'color': 'white'}, "showarrow":False},
        
            ],
            margin={"l":5, "r": 5, 't':100},
            )
            plot.update_yaxes(automargin=True)
            
            col22.plotly_chart(plot)
            
            
            # plot  = px.scatter(data_frame = df1, x = 'time', y = 'AirUsage', marginal_y=chart_select,
            #                    facet_row='subject', color = 'attack_flag',labels={'time': 'Time (Sec.)','AirUsage': 'Air Consumption', },
            # # title=f"<b>Time vs. {title_val[i]}</b>",
            # ) 
            
            plot  = px.scatter(data_frame = df1, x = 'time', y = 'AirUsage', marginal_y=chart_select,
                               color = 'subject',labels={'time': 'Time (Sec.)','AirUsage': 'Air Consumption', },
            # title=f"<b>Time vs. {title_val[i]}</b>",
            ) 
            
            for j in range(length):
                plot.add_layout_image(
                    
                    layout_for_firefighter_icon(source=source, length=length, loop_j=j, x_val=0.5, y_val=1.25, sizexy=0.16, xanchor="center", xyref="paper")
    
                    )
            plot.update_layout(
                width=550,
                height = 500,
            # title= 'Air Usage and Water Usage',
        
            
            annotations=\
            [
            {"xref": "paper", "yref": "paper","xanchor": "left","x":-0., "y":1.33, 
              "text": "<b>Air Consumption During Simulation</b>",'font': {'size': 16, 'color': 'white'}, "showarrow":False},
        
            ],
            margin={"l":5, "r": 5, 't':100},
            )
            # plot.update_yaxes(automargin=True)
            plot.add_hline(y=400, line_dash="dot", col=1,
                      annotation_text="Maximum baseline Air Cosumption", 
                      annotation_position="top right")#bottom right
            # for k in range(3):
            #     plot.add_vrect(x0=k*50, x1=k*50, col = 1,
            #               annotation_text="During Fight", annotation_position="top left",
            #               fillcolor="royalblue", opacity=0.5, line_width=0)
            col31.plotly_chart(plot)
            
            
            # calculating area in fire intensity curve
        
        
            plot  = px.scatter(data_frame = df1, x = 'total_water_usage', y = 'total_air_usage_during_fire_attack', 
                               color = 'subject',size = 'Relative Area Under Fire Intensity Curve', 
                               labels={'total_water_usage': 'Total Water Usage',
                                       'total_air_usage_during_fire_attack':'Total Air Usage During Fire Attack', },
            # title=f"<b>Time vs. {title_val[i]}</b>",   #size = 'fire_attack_duration',symbol = 'fire_attack_duration',
            ) 
            
            for j in range(length):
                plot.add_layout_image(
                    
                    layout_for_firefighter_icon(source=source, length=length, loop_j=j, x_val=0.5, y_val=1.25, sizexy=0.16, xanchor="center", xyref="paper")
    
                    )
            
            plot.update_layout(
                width=550,
                height = 500,
            # title= 'Air Usage and Water Usage',
        
            
            annotations=\
            [
            {"xref": "paper", "yref": "paper","xanchor": "left","x":-0., "y":1.33, 
              "text": "<b>Total Air Usage, Water Usage and Relative Area Under Fire intensity Curve</b>",'font': {'size': 16, 'color': 'white'}, "showarrow":False},
        
            ],
            margin={"l":5, "r": 5, 't':100},
            )
                
            # plot.update_yaxes(automargin=True)
        
            col32.plotly_chart(plot)
            
    with tab4:
        
        
        # st.subheader('Machine Learning Analysis and Clustering')
        
        def integrate(x, y):
            sm = 0
            for i in range(1, len(x)):
               h = x[i] - x[i-1]
               sm += h * (y[i-1] + y[i]) / 2
        
            return sm
        
        col1,col2,col3 = st.columns([1,1,2])
        col21,col22 = st.columns(2)
        
        file = "data_all_collectionData_211116_data_analysisDate_211118.csv"
        df = pd.read_csv(file)
        dff=pd.DataFrame()
        df2 =pd.DataFrame(df.loc[df['attack_flag']==1].groupby('subject')[['total_water_usage', 'total_air_usage_during_fire_attack', ]].mean())
        dff = pd.concat([dff,df2],axis=1)
        df2 =pd.DataFrame(df.loc[df['attack_flag']==1].groupby('subject')[['BRs', 'BTs', 'HRs', 'fire_intensity']].min())
        df2.columns=['BRs_min', 'BTs_min', 'HRs_min', 'fire_intensity_min']
        dff = pd.concat([dff,df2],axis=1)
        df2 =pd.DataFrame(df.loc[df['attack_flag']==1].groupby('subject')[['BRs', 'BTs', 'HRs', 'fire_intensity']].max())
        df2.columns=['BRs_max', 'BTs_max', 'HRs_max', 'fire_intensity_max']
        dff = pd.concat([dff,df2],axis=1)
        df2 =pd.DataFrame(df.loc[df['attack_flag']==1].groupby('subject')[['BRs', 'BTs', 'HRs', 'fire_intensity']].mean())
        df2.columns=['BRs_mean', 'BTs_mean', 'HRs_mean', 'fire_intensity_mean']
        dff = pd.concat([dff,df2],axis=1)
        df2 =pd.DataFrame(df.loc[df['attack_flag']==1].groupby('subject')[['BRs', 'BTs', 'HRs', 'fire_intensity']].std())
        df2.columns=['BRs_std', 'BTs_std', 'HRs_std', 'fire_intensity_std']
        dff = pd.concat([dff,df2],axis=1)
        
        dfg = df.loc[df['attack_flag']==1]
        area = []
        for sub in dfg.subject.unique():
            area.append(integrate(dfg.loc[dfg['subject']==sub,'time'].values,dfg.loc[dfg['subject']==sub,'fire_intensity'].values)/\
                    dfg.loc[dfg['subject']==sub,'fire_intensity'].values[0])
                
        dff['relative_area_under_fire_intensity_curve']=area        
        
        # file_group = "D:/OneDrive - Deakin University/abbas web app project/project 2 - fire fighter/data/group"
        # dff.to_csv('session_1.csv')
        dff = dff/dff.max()

        # n_compo = col1.selectbox(label="How much variance you want to preserve in PCA?", options = [0.9,0.95, 0.99, 0.999])
        # @st.cache
        # def cache_func1(dff):
        #     pca = PCA(n_components=0.9)
        #     return pca.fit_transform(dff)
        
        # principalComponents = cache_func1(dff)
        # components = []
        # for i in range(principalComponents.shape[1]):
        #     components.append(f'component_{i+1}')
        # principalDf = pd.DataFrame(data = principalComponents, columns = components, index=dff.index.values)
        
        
        # x_axis_select = col1.selectbox(label="Select X axis", options = principalDf.columns)
        # y_axis_select = col2.selectbox(label="Select Y axis", options = principalDf.columns, index=3)
        
        # plot  = px.scatter(data_frame = principalDf, x = x_axis_select, y = y_axis_select, color = principalDf.index,
        #                    # labels={'time': "Time (Sec.)",y_val[i]: "", },
        #                    title=f"<b>PCA Analysis: {x_axis_select} vs. {y_axis_select}</b>",)  ##   Heart Rate
        
        # plot.update_layout(
        #     width=550,
        #     # height = 500,
        #     )
    
        # col21.plotly_chart(plot)
        
        # def cache_func4(principalDf):
        #     model1 = KMeans(n_clusters=3)
        #     model1.fit(principalDf)
        #     return model1.predict(principalDf)
        
        # dff['cluster_KMEANS_using_PCA_component']= cache_func4(principalDf)
        
        # plot  = px.scatter(data_frame = principalDf, x = 'component_1', y = 'component_2', 
        #                    color = principalDf.index, symbol = dff['cluster_KMEANS_using_PCA_component'],
        #                    # labels={'time': "Time (Sec.)",y_val[i]: "", },
        #                    title="<b>K-MEANS clustering using PCA components</b>",)  ##   Heart Rate
        
        # plot.update_layout(
        #     width=550,
        #     # height = 500,
        #     )
        # col22.plotly_chart(plot)
        
        #ML result
        
        # @st.cache
        def cache_func2(dff):
            model = KMeans(n_clusters=3)
            model.fit(dff)
            return model.predict(dff)
        
        
        col31,col32 = st.columns(2)
        dff['cluster_KMEANS_using_features']= cache_func2(dff[['total_water_usage', 
                                                               
                                                                'total_air_usage_during_fire_attack',
                                                                'relative_area_under_fire_intensity_curve',]])
        
        plot  = px.scatter(data_frame = dff, x = 'total_water_usage', y = 'total_air_usage_during_fire_attack', 
                            size = 'relative_area_under_fire_intensity_curve',color = dff.index, 
                            symbol = dff['cluster_KMEANS_using_features'],
                            labels={'total_water_usage': "Total Water Usage",
                                    'total_air_usage_during_fire_attack': "Total Air Usage During Fire Attack", 
                                    'cluster_KMEANS_using_features':'Category'},
                            title="<b>K-MEANS clustering using Resource Features</b>",)  ##   Heart Rate
        
        plot.update_layout(
            width=550,
            # height = 500,
            )
        col31.plotly_chart(plot)
        
        
        # @st.cache
        def cache_func3(dff):
            model_ = KMeans(n_clusters=3)
            model_.fit(dff)
            return model_.predict(dff)
        
        dff['cluster_KMEANS_using_all_features']= cache_func3(dff)
        
        plot  = px.scatter(data_frame = dff, x = 'total_water_usage', y = 'total_air_usage_during_fire_attack', 
                           size = 'relative_area_under_fire_intensity_curve',color = dff.index, 
                           symbol = dff['cluster_KMEANS_using_all_features'],
                           labels={'total_water_usage': "Total Water Usage",
                                   'total_air_usage_during_fire_attack': "Total Air Usage During Fire Attack", 
                                   'cluster_KMEANS_using_all_features': 'Category'},
                           title="<b>K-MEANS clustering using All Features</b>",)  ##   Heart Rate
        
        plot.update_layout(
            width=550,
            # height = 500,
            )
        col32.plotly_chart(plot)
        
        # plot  = px.scatter_3d(dff, x='total_water_usage', y='total_air_usage_during_fire_attack', 
        #                       z='relative_area_under_fire_intensity_curve',color=dff.index)
        # plot.update_layout(
        #     width=600,
        #     # height = 500,
        #     )
        # st.plotly_chart(plot)
        # @st.cache
        
        
        
        # with st.expander("Click here to see PCA pairplot"):
        #     plot  = px.scatter_matrix(principalDf.reset_index(), dimensions = components, color='index')
            
        #     plot.update_layout(
        #         width=1200,
        #         height = 1000,
        #         )
        #     st.plotly_chart(plot)
            
        # import numpy as np
        
        # principalDf1 = pd.DataFrame()
        # cov = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])/10
        # for sub in principalDf.index.values:
        #     mean = principalDf.loc[sub].values
        #     z = np.random.multivariate_normal(mean, cov, 100)
        #     principalDf1 = pd.concat([principalDf1, pd.DataFrame(z, columns = components)], axis=0)  #, join='inner'
        
        # principalDf1 = pd.concat([principalDf1, principalDf], axis=0)
        # model = KMeans(n_clusters=3)
        # model.fit(principalDf1)
        # kmeans_gauss = model.predict(principalDf1)
        # principalDf1 = pd.concat([principalDf1, pd.DataFrame(kmeans_gauss,index=principalDf1.index, columns = ['cluster'])], axis=1)
        
        # # st.write(kmeans_gauss[-8:])
        
        # import matplotlib.pyplot as plt
        # from scipy.spatial import ConvexHull
        # principalDf2 = principalDf1.iloc[-8:]
        # colors = ['r', 'g', 'b', 'k']
        # fig = plt.figure(figsize = (5, 3))
        # for k in range(4):
        #     hull = ConvexHull(principalDf1[principalDf1['cluster']==k][['component_1','component_2']])
        #     plt.fill(principalDf1[principalDf1['cluster']==k].iloc[hull.vertices,0], 
        #               principalDf1[principalDf1['cluster']==k].iloc[hull.vertices,1], color = colors[k], alpha=0.1)
        #     plt.plot(principalDf2[principalDf2['cluster']==k]['component_1'], 
        #               principalDf2[principalDf2['cluster']==k]['component_2'], '.', color = colors[k])
        # plt.xlabel('component_1')
        # plt.ylabel('component_2')
        
        # col31,col32 = st.columns([4,5])
        # col31.pyplot(fig)
        
        # col41,col42, col43 = st.columns(3)
        
        col51,col52 = st.columns([2,3])
        col51.subheader('Resource Importance Scale:')
        col52.subheader('Performace of Each Subject:',anchor='center')
        a = col51.slider(label='Select the importance parameter for water usage', min_value=0.05, max_value=1.0, value=0.5, step=0.05)
        b = col51.slider(label='Select the importance parameter for air usage', min_value=0.05, max_value=1.0, value=0.5, step=0.05)
        c = col51.slider(label='Select the importance parameter for area under fire intensity curve', min_value=0.05, max_value=1.0, value=0.5, step=0.05)
        
        
        import numpy as np
        dff['metric'] = a*np.exp(1-dff['total_water_usage'].values) + \
                        b*np.exp(1-dff['total_air_usage_during_fire_attack'].values) + \
                        c*np.exp(1-dff['relative_area_under_fire_intensity_curve'].values) 
                        
        
        plot = px.bar(dff.reset_index(), x = "subject", y = "metric",
                      labels={"metric":'Performance metric'},)
        
        col52.plotly_chart(plot)
        
        
        
        
        with tab5:
            # file_group = "D:/OneDrive - Deakin University/abbas web app project/project 2 - fire fighter/data/group"
            df_session=pd.DataFrame()
            for i in range(5):
                df2=pd.read_csv(f'session_{i+1}.csv',index_col='subject')
                df2['session']=f's_{i+1}'
                df_session=pd.concat([df_session,df2],axis=0)
            col11,col12=st.columns(2)
            feature_select = col11.selectbox(label="Select feature", options = df_session.columns)
            plot=px.line(data_frame = df_session, x = 'session', y = feature_select, color = df_session.index,
                        labels={"total_water_usage":"Total Water Usage","total_air_usage_during_fire_attack":
                                "Total Air Usage During Fire Attack"},
                    title=f"<b>Session vs. Features</b>",
                    )  ##   Heart Rate
            plot.update_layout(
                width=550,
                # height = 500,
                )
            col11.plotly_chart(plot)
            
            
            subject_select = col12.selectbox(label="Select subject", options = df_session.index.unique().values
                                               )
            
            df_sess_relative = df_session.loc[:, df_session.columns != 'session']/df_session.loc[:, df_session.columns != 'session'].max()
            df_sess_relative = pd.concat([df_sess_relative,df_session['session']],axis=1)
            # df1=pd.DataFrame()
            # for sub in subject_select:
            df1 = df_sess_relative.loc[df_session.index == subject_select]
                
            
            plot  = px.scatter(data_frame = df1, x = 'total_water_usage', y = 'total_air_usage_during_fire_attack', 
                 color=df1.index, symbol='session', size='relative_area_under_fire_intensity_curve', 
                 labels={"total_water_usage":"Total Water Usage","total_air_usage_during_fire_attack":
                         "Total Air Usage During Fire Attack"},
            title=f"<b>Progress of subjects through session</b>",
            )  ##   Heart Rate
            plot.update_layout(
                width=550,
                # height = 500,
                )
            plot.add_shape(type="circle",
                xref="x", yref="y",
                x0=-0.5, y0=-0.5,
                x1=0.5, y1=0.5,
                opacity=0.2,
                fillcolor="orange",
                line_color="orange",
            )
            plot.add_shape(type="circle",
                xref="x", yref="y",
                x0=-0.8, y0=-0.8,
                x1=0.8, y1=0.8,
                opacity=0.2,
                fillcolor="orange",
                line_color="orange",
            )
            plot.add_shape(type="circle",
                xref="x", yref="y",
                x0=-1.8, y0=-1.8,
                x1=1.8, y1=1.8,
                opacity=0.2,
                fillcolor="orange",
                line_color="orange",
            )
            plot.update_layout(
                        width=550,yaxis_range=[0,1.01],xaxis_range=[0,1.01]
                        # height = 500,
                        )
            plot.add_annotation(x=.650, y=.05, text="Intermediate", showarrow=False)
            plot.add_annotation(x=.20, y=.05, text="Expert", showarrow=False)
            plot.add_annotation(x=.90, y=.05, text="Novice", showarrow=False)
            col12.plotly_chart(plot)
        
        
            col61,col62 = st.columns([2,3])
            col61.subheader('Resource Importance Scale:')
            col62.subheader('Performace of Each Subject:',anchor='center')
            a = col61.slider(label='Select the importance parameter for water usage:', min_value=0.05, max_value=1.0, value=0.5, step=0.05)
            b = col61.slider(label='Select the importance parameter for air usage:', min_value=0.05, max_value=1.0, value=0.5, step=0.05)
            c = col61.slider(label='Select the importance parameter for area under fire intensity curve:', min_value=0.05, max_value=1.0, value=0.5, step=0.05)
            
            df_sess_relative = df_session.loc[:, df_session.columns != 'session']/df_session.loc[:, df_session.columns != 'session'].max()
            df_sess_relative = pd.concat([df_sess_relative,df_session['session']],axis=1)

            import numpy as np
            df_sess_relative['metric'] = a*np.exp(1-df_sess_relative['total_water_usage'].values) + \
                            b*np.exp(1-df_sess_relative['total_air_usage_during_fire_attack'].values) + \
                            c*np.exp(1-df_sess_relative['relative_area_under_fire_intensity_curve'].values) 
                            
            
            plot = px.line(data_frame = df_sess_relative , x = 'session', y = 'metric', 
                           color = df_sess_relative.index,labels={'metric': "Performance metric",},)
            
            col62.plotly_chart(plot)