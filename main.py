import streamlit as st 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
from io import BytesIO
from matplotlib.backends.backend_pdf import PdfPages

st.title ("Daily Handover")
st.caption("Handover for teams that work in shifts.")


def save_dataframe_as_pdf(dataframe):
    with BytesIO() as output:
        with PdfPages(output) as pdf:
            fig, ax = plt.subplots()
            ax.axis('off')

            # Adjust column widths for better word wrapping
            col_widths = [0.2] * len(dataframe.columns)

            table = ax.table(cellText=dataframe.values, colLabels=dataframe.columns, cellLoc='center', loc='center', colWidths=col_widths)
            
            # Enable word wrapping for cell text
            for cell in table.get_celld().values():
                cell.set_text_props(wrap=True)

            pdf.savefig(fig, bbox_inches='tight')
            plt.close(fig)

        # Move to the beginning of the BytesIO buffer
        output.seek(0)
        return output.read()


today=st.date_input("Date")

team=st.selectbox("Team",["Early","Late","Night","Office"])

header = ["Date","Team","Type","Room no.","Guest","Primary Note","Resolution", "C/O","C/I","Action","Status"]


type=st.selectbox("Type",["Guest Issues/Complaint","Front Office & Operations","Other"])

room=st.select_slider(
    'Select Room Number',
    options=["N/A","100", "101", "102", "103", "104", "105", "106", "107", "108", "109", "110", "111", "112", "113", "114", "115", "116", "117", "118", "119", "120", "121", "122", "123", "124", "125", "126", "127", 
"201", "202", "203", "204", "205", "206", "207", "208", "209", "210", "211", "212", "213", "214", "215", "216", "217", "218", "219", "220", "221", "222", "223", "224", "225", "226", "227", "228", 
"301", "302", "303", "304", "305", "306", "307", "308", "309", "310", "311", "312", "313", "314", "315", "316", "317", "318", "319", "320", "321", "322", "323", "324", "325", "326", "327", "328", 
"401", "402", "403", "404", "405", "406", "407", "408", "409", "410", "411", "412", "413", "414", "415", "416", "417", "418", "419", "420", "421", "422"
])
guest=st.text_input("Guest Name")

note=st.text_area("Primary Note")

resolution=st.text_area("Resolution")
ci=st.date_input("CheckIn")

co=st.date_input("CheckOut")



action=st.text_area("Action")

status=st.selectbox("Status",["Open","Closed", "Pending"])


session_state = st.session_state

if "data" not in session_state:
    session_state.data = pd.DataFrame(columns=header)
     
append_data = st.button("Add to Handover")

new_row = {"Date":today,"Team":team,"Type":type,"Room no.":room,"Guest":guest,"Primary Note":note,"Resolution":resolution, "C/O":co,"C/I":ci,"Action":action,"Status":status}
if append_data:
    session_state.date= session_state.data.loc[len(session_state.data)] = new_row 
    # session_state.data = session_state.data.append({"Date":today,"Team":team,"Type":type,"Room no.":room,"Guest":guest,"Primary Note":note,"Resolution":resolution, "C/O":co,"C/I":ci,"Action":action,"Status":status}, ignore_index=True)

st.dataframe(session_state.data)


save = st.button("Save")

if save:
    pdf_data = save_dataframe_as_pdf(session_state.data)
    st.download_button("Download PDF", pdf_data, key="download_pdf", file_name="output.pdf", mime="application/pdf")
