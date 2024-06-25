import streamlit as st
from db import create_table,add_post,view_records,get_title,get_author,delete_blog
from PIL import Image
import base64
import pandas as pd
import matplotlib.pyplot as plt
st.set_option('deprecation.showPyplotGlobalUse', False)
template_html='''<div style="background-color:#008080;padding:10px,margin:10ox;">
                 <h4 style="color:black;text-align:center;">{}</h4>
                 <h4 style="color:black;text-align:center;">{}</h4>
                 <h4 style="color:black;text-align:center;">{}</h4>
                 <h4 style="color:black;text-align:center;">{}</h4>
                 <img src="data:image/jpg;base64,{}" alt="Image" 
            style='horizontal-align:center' width="700px" height="450px">
                 </div>'''
st.title("Blog Database Management System")
choice=st.sidebar.selectbox("Select Menu",['Home','Add Post','Search','Manage Blog'])
create_table()
if choice=='Home':
    st.subheader("Home")
    d1=view_records()
    #st.write(d1) # data visuliation in list within list
    for i in d1:
        title=i[0]
        author=i[1]
        artical=i[2]
        data=i[3]
        #image=i[4]
        image="%s.jpg"%author
        file=open(image,"rb")
        contents=file.read()
        b_image=base64.b64encode(contents).decode("utf-8")
        file.close()
        st.markdown(template_html.format(title,author,artical,data,b_image),unsafe_allow_html=True)
elif choice=='Add Post':
    st.subheader("Add Post")
    blog_title=st.text_input("Title")# title of blog
    blog_author=st.text_input("Author")# author name input
    blog_artical=st.text_area("Artical")# artical input
    #blog_image=st.file_uploader("Image")# image input
    blog_date=st.date_input("date")# date input
    try:
        img_file=st.file_uploader("upload an image",type=["png","jpg","jpeg"])
        image=Image.open(img_file)
        #convert image into jpg format
        image=image.convert('RGB')
        img='{}.jpg'.format(blog_author)# connect with author name ( save image with author name)
        image.save(img)# save the image
        # open a file in binary mode
        file=open(img,'rb').read()
        #we must encode the file to get base64 string
        blog_image=base64.b64encode(file)
    except:
        print("ERROR1: could not open the image , please upload image jpg,png,jpeg format only")
    if st.button("Add records"):# for submit the record
        add_post(blog_title,blog_author,blog_artical,blog_date,blog_image) # for adding the blog
        st.success(f"{blog_title}Blog added successfully")
elif choice=='Search':
    st.subheader("Search")
    search_term=st.text_input("enter search term")
    r=st.radio("enter the choice",('title','author'))
    if(r=='title'):
        result_of_title=get_title(search_term)
        #st.write(result_of_title)
        for i in result_of_title:
            title=i[0]
            author=i[1]
            artical=i[2]
            data=i[3]
            image="%s.jpg"%author
            file=open(image,"rb")
            contents=file.read()
            b_image=base64.b64encode(contents).decode("utf-8")
            file.close()
            st.markdown(template_html.format(title,author,artical,data,b_image),unsafe_allow_html=True)
    if(r=='author'):
        result_of_author=get_author(search_term)
        #st.write(result_of_author)
        for i in result_of_author:
            title=i[0]
            author=i[1]
            artical=i[2]
            data=i[3]
            image="%s.jpg"%author
            file=open(image,"rb")
            contents=file.read()
            b_image=base64.b64encode(contents).decode("utf-8")
            file.close()
            st.markdown(template_html.format(title,author,artical,data,b_image),unsafe_allow_html=True)
elif choice=='Manage Blog':
    st.subheader("Manage Blog")
    data=view_records()
    #blog_data=pd.DataFrame(data)
    blog_data=pd.DataFrame(data,columns=['Title','Author','Artical','Post Date','Image'])
    d=blog_data.iloc[:,:-1] # indexing rows and coloums
    st.dataframe(d)
    #blog_author=st.text_input("enter the author")
    author_list=[i[1] for i in data]
    blog_author=st.selectbox("Author name",author_list)
    if st.button('Delete'):
        delete_blog(blog_author)
        st.success(f"{blog_author} record deleted successfully")
    updated_data=view_records()
    blog_data=pd.DataFrame(updated_data,columns=['Title','Author','Artical','Post Date','Image'])
    d=blog_data.iloc[:,:-1] # indexing rows and coloums(-ve indexing), slicing
    st.dataframe(d)
    st.subheader("Graphical Visualization")
    title_count=d['Title'].value_counts()
    st.write(title_count)
    title_count.plot(kind='bar')
    st.pyplot()