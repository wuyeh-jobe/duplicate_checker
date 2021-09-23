import streamlit as st
import pandas as pd



st.header("Duplicate Detector for current cycle")

# add_selectbox = st.sidebar.selectbox(
#     "How would you like to be contacted?",
#     ("Email", "Home phone", "Mobile phone")
# )
uploaded_file = st.file_uploader('Upload a file')
email_set = set()
chat_links_set = set()
name_set = set()

def get_duplicates(data, option, email_column_name, first_name_column_name, last_name_column_name, chat_link_column_name):
    all_duplicates = set()
    duplicate_found = False
    # duplicates base on email
    emails = data[email_column_name.strip()]
    first_names = data[first_name_column_name.strip()] 
    last_names = data[last_name_column_name.strip()]
    chat_links = data[chat_link_column_name.strip()]

    # st.info("Duplicate found by email")
    # st.write(emails)
    
    
    for i,email in enumerate(emails):
        # print(f"{email}, type {type(email) == float}")
        if type(email) == str:
            if email.lower().strip() in email_set:
                # st.write(f"user with email ({email}) - {first_names[i]} {last_names[i]} is repeated")
                all_duplicates.add(f"{first_names[i]} {last_names[i]} - {emails[i]} - {chat_links[i]}")
                duplicate_found = True
            else:
                if option == "duplicate":
                    email_set.add(email.lower().strip())
    
    # duplicates base on chat links
    # st.info("Duplicate found by Chat Link")

    for i,chat_link in enumerate(chat_links):
        if chat_link.strip() in chat_links_set:
            duplicate_found = True
            # st.write(f"User with chat link ({chat_link}), email ({emails[i]}) - {first_names[i]} {last_names[i]} is repeated")
            all_duplicates.add(f"{first_names[i]} {last_names[i]} - {emails[i]} - {chat_links[i]}")
        else:
            if option == "duplicate" and chat_link != "No Baobab account":
                    chat_links_set.add(chat_link.strip())

    # duplicates base on first name and last name
    # st.info("Duplicate found by name")
    for i,first_name in enumerate(first_names):
        if f"{first_name.strip()}{last_names[i].strip()}".lower().replace(" ","") in name_set:
            duplicate_found = True
            # st.write(f"User with name ({first_name.strip()} {last_names[i].strip()}) is repeated")
            all_duplicates.add(f"{first_names[i]} {last_names[i]} - {emails[i]} - {chat_links[i]}")
        else:
            if option == "duplicate":
                name_set.add(f"{first_name.strip()}{last_names[i].strip()}".lower().replace(" ",""))
    
    if not duplicate_found:
        st.write("No duplicates found within the document")
    else:
        st.warning(f"All results found by email, first and last names, and chat link ({len(all_duplicates)})")
        for person in all_duplicates:
            st.write(person)


    

    



if uploaded_file is not None:
    data = pd.read_excel(uploaded_file, converters={"Mentee's Baobab Email":str})
    # This should be used if we want to use the first row as the column names
    # header = data.iloc[0]
    # data = data[1:]
    # data.columns = header
    st.subheader("Data colums")
    st.write(data.columns)
    st.subheader("Enter column names (you can copy from data columns above)")
    email_column_name = st.text_input("Enter exact column name for email as in the sheet")
    first_name_column_name = st.text_input("Enter exact column name for first name as in the sheet")
    last_name_column_name = st.text_input("Enter exact column name for last name as in the sheet")
    chat_link_column_name = st.text_input("Enter exact column name for chat link as in the sheet")
    if not email_column_name or  not first_name_column_name or not last_name_column_name or not chat_link_column_name:
        st.warning("Please enter something in all the fields above to contine")
        st.stop()

    # st.subheader("Here is your data")
    # st.dataframe(data[[email_column_name, first_name_column_name, last_name_column_name, chat_link_column_name]])

    st.subheader("Duplicate detection result")
    get_duplicates(data, "duplicate", email_column_name, first_name_column_name, last_name_column_name, chat_link_column_name)

    st.header("Duplicate Detector -  comparison with old document")
    uploaded_file2 = st.file_uploader('Upload second file')
    if uploaded_file2 is not None:
        # st.subheader("Here is your data")
        data = pd.read_excel(uploaded_file2)
        # st.write(data)
        st.subheader("People who applied previously")
        get_duplicates(data, "comparison", email_column_name, first_name_column_name, last_name_column_name, chat_link_column_name)

