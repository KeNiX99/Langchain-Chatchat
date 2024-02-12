import streamlit as st
import streamlit_authenticator as stauth
from webui_pages.utils import *
from streamlit_option_menu import option_menu
from webui_pages.anydialogue.anydialogue import anydialogue_page, chat_box
from webui_pages.dialogue.dialogue import dialogue_page, chat_box
from webui_pages.knowledge_base.knowledge_base import knowledge_base_page
import os
import sys
from configs import VERSION
from server.utils import api_address
import yaml
from yaml.loader import SafeLoader


api = ApiRequest(base_url=api_address())

if __name__ == "__main__":
    
    is_lite = "lite" in sys.argv

    st.set_page_config(
        "平安䇝工作台",
        os.path.join("img", "chatchat_icon_blue_square_v2.png"),
        #initial_sidebar_state="expanded",
        initial_sidebar_state="collapsed",
        menu_items={
            #'Get Help': 'https://github.com/chatchat-space/Langchain-Chatchat',
            #'Report a bug': "https://github.com/chatchat-space/Langchain-Chatchat/issues",
            'About': f"""欢迎使用 Pingan Memo WebUI Powerby langchain-chatchat {VERSION}！"""
        }
    )

    guest_pages = {
        "匿名对话": {
            "icon": "chat",
            "func": anydialogue_page,
        },
    }
    
    admin_pages = {
        
        "对话": {
            "icon": "chat",
            "func": dialogue_page,
        },
        "知识库管理": {
            "icon": "hdd-stack",
            "func": knowledge_base_page,
        },
    }

    #pages = guest_pages

    
    #if selected_page in pages:
        #pages[selected_page]["func"](api=api, is_lite=is_lite)

    
    
    with open('userconfig.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

    
    #name, authentication_status, username = authenticator.login('main')
    #print( config['credentials']['usernames'][username]['role'])
    
    #username = ''
    #authentication_status = False
    if st.session_state["authentication_status"]: #authentication_status:
        print(st.session_state['username'])
        username = st.session_state['username']
        if config['credentials']['usernames'][username]['role'] == 'admin':
            pages = admin_pages
            with st.sidebar:
                cols1,cols2 = st.columns(2)
                cols1.write('欢迎 *%s*' % (config['credentials']['usernames'][username]['name']))
                with cols2.container():
                    authenticator.logout('退出')
                st.image(
                    os.path.join(
                        "img",
                        "logo-long-chatchat-trans-v2.png"
                    ),
                    use_column_width=True
                )
                st.caption(
                    f"""<p align="right">当前版本：{VERSION}</p>""",
                    unsafe_allow_html=True,
                )
                options = list(pages)
                icons = [x["icon"] for x in pages.values()]

                default_index = 0
                selected_page = option_menu(
                    "",
                    options=options,
                    icons=icons,
                    # menu_icon="chat-quote",
                    default_index=default_index,
                )

        else:
            pages = guest_pages
            with st.sidebar:
                
                cols1,cols2 = st.columns(2)
                cols1.write('欢迎 *%s*' % (config['credentials']['usernames'][username]['name']))
                with cols2.container():
                    authenticator.logout('退出')
                
                st.caption(
                    f"""<p align="right">当前版本：{VERSION}</p>""",
                    unsafe_allow_html=True,
                )
                options = list(pages)
                icons = [x["icon"] for x in pages.values()]

                default_index = 0
                selected_page = option_menu(
                    "",
                    options=options,
                    icons=icons,
                    # menu_icon="chat-quote",
                    default_index=default_index,
                )

        if selected_page in pages:
            pages[selected_page]["func"](api=api, is_lite=is_lite)
        
        
    elif st.session_state["authentication_status"] is False:
        #st.error('Username/password is incorrect')
        print("auth False")
        pages = guest_pages
        
        with st.sidebar:
            #name, authentication_status, username = authenticator.login('sidebar')    
            st.caption(
                f"""<p align="right">当前版本：{VERSION}</p>""",
                unsafe_allow_html=True,
            )
            authenticator.login('sidebar')
            #name, authentication_status, username = authenticator.login('sidebar')
            options = list(pages)
            icons = [x["icon"] for x in pages.values()]

            default_index = 0
            selected_page = option_menu(
                "",
                options=options,
                icons=icons,
                # menu_icon="chat-quote",
                default_index=default_index,
            )

        if selected_page in pages:
            pages[selected_page]["func"](api=api, is_lite=is_lite)
    
    elif st.session_state["authentication_status"] is  None:
        print("Auth None!!!")
        pages = guest_pages
        with st.sidebar:
            st.caption(
                f"""<p align="right">当前版本：{VERSION}</p>""",
                unsafe_allow_html=True,
            )
            #name, authentication_status, username = authenticator.login('sidebar')
            authenticator.login('sidebar')
            options = list(pages)
            icons = [x["icon"] for x in pages.values()]

            default_index = 0
            selected_page = option_menu(
                "",
                options=options,
                icons=icons,
                # menu_icon="chat-quote",
                default_index=default_index,
            )

        if selected_page in pages:
            pages[selected_page]["func"](api=api, is_lite=is_lite)
        #st.warning('Please enter your username and password')
