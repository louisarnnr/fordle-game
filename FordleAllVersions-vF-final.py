#importing necessary libraries
import pandas as pd
import yfinance as yf
import numpy as np
import altair as alt
import streamlit as st
import matplotlib.pyplot as plt
import random
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


# easy version for beginners
def beginner():
    #get information about S&P500 stocks, such as ticker, industry and location
    st.session_state.level = "beginner"
    page=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    df=page[0]
    df.set_index('Symbol', inplace=True)
    df.head()


    # get today's date and let user choose time period displayed by graph
    today = date.today()
    datetime_delta = timedelta(days=1)
    end_of_period = date.today() - datetime_delta
    start_of_period = end_of_period - relativedelta(years=5)


    # let the system pick a random stock ticker out of the S&P 500 list
    def random_choice():
        stock_to_be_guessed=random.choice(df.index.values)
        st.session_state.stock_to_be_guessed = stock_to_be_guessed
        return stock_to_be_guessed

    # Retrieves the data for the graph that needs to be guessed from the Yahoo Finance API
    def plot():
        data = yf.download(st.session_state.stock_to_be_guessed)
        st.write('Note: To see the stock development in a more narrow time frame, you can zoom in within the graph and move the chart.')
        st.line_chart(data.Close) 


    # initialization of the game. Displays the graph to be guessed.
    def new_game():
        st.title('Fordle - The Wordle for Finance Nerds')
        st.markdown('Which stock is being displayed here? It is quoted within the S&P 500')
        st.write(f'**Here is a hint:** The stock is in the _{industry}_ industry and its headquarters are located in _{headquarters}_. Try again!')
        plot()

    # display hints about stock to player. This loop is the essence of the game and decides on victories or losses. 
    def form_callback():
        if st.session_state.guess == st.session_state.stock_to_be_guessed:
            random_choice()
            st.session_state.counter = 0
            st.session_state.victories += 1
            new_game()
            st.write('**You have guessed correctly!** \U0001F60D')
            st.write('Keep doing what you are doing. Next stock!')

        elif st.session_state.counter >= 2:
            random_choice()
            st.session_state.counter = 0
            st.session_state.loss += 1
            new_game()
            st.write('**You have lost.** New try, with a new stock!')

        else:
            new_game()
            st.write('**Wrong choice** \U0001F612')
            st.session_state.counter += 1
            industry = df.loc[st.session_state.stock_to_be_guessed, 'GICS Sector']
            headquarters = df.loc[st.session_state.stock_to_be_guessed, 'Headquarters Location']
            if st.session_state.counter > 0:
                st.write("Wrong! Try again. Maybe you could try zooming in to last week's prices, if you stay updated with the markets daily.")
            if st.session_state.counter > 1 and st.session_state.counter <= 2:
                st.write(f"**Still wrong?** Let's see if this helps. The ticker is: **{st.session_state.stock_to_be_guessed}**.")


    # initialize state variables needed within streamlit for the game to run and run the game methods 
    if "counter" not in st.session_state:
        st.session_state.guess = "MMM"
        st.session_state.period = "y"
        st.session_state.new_game = True
        st.session_state.counter = 0
        st.session_state.victories = 0
        st.session_state.loss = 0
        random_choice()
        new_game()


    #with st.form(key='my_form'):
    #creates the select box with different company names to guess the stock displayed in the chart that helps the player to input their guesses
    ticks = df.index.values
    with st.form(key=f"my_form"):
        guess = st.selectbox("Make your choice", ticks, format_func=lambda x: df.loc[x, "Security"], key="guess")
        submit_button = st.form_submit_button(label='Submit', on_click=form_callback) 

    # side bar with information on number of games, wins and losses
    with st.sidebar:
        st.title("Score count")
        st.write("You played ", st.session_state.victories + st.session_state.loss, " times ", f"and have won {st.session_state.victories} times and lost {st.session_state.loss} times.")
        if st.session_state.victories + st.session_state.loss > 0:
            if st.session_state.victories > st.session_state.loss:
                st.write("**Amazing score, keep going!** Maybe you should try the advanced mode? Refresh your browser and choose *Advanced* :wink:")
            elif st.session_state.victories == st.session_state.loss:
                st.write("**Just a few more wins. You got this!**")
            else:
                st.write("How about a Master in Finance at Nova SBE? It will certainly help to win this game!")
                st.write("Check out the program: https://www.novasbe.unl.pt/en/programs/masters/finance/")
                
def advanced():
    st.session_state.level = "advanced"
    
    # get information about S&P500 stocks, such as ticker, industry and location
    page=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    df=page[0]
    df.set_index('Symbol', inplace=True)
    df.head()

    # let the system pick a random stock ticker out of the S&P 500 list
    def random_choice():
        stock_to_be_guessed=random.choice(df.index.values)
        st.session_state.stock_to_be_guessed = stock_to_be_guessed
        st.session_state.stock_to_be_guessed ###
        return stock_to_be_guessed

    # Retrieves the data for the graph that needs to be guessed from the Yahoo Finance API
    def plot():
        data = yf.download(st.session_state.stock_to_be_guessed)
        st.write('Note: To see the stock development in a more narrow time frame, you can zoom in within the graph and move the chart.')
        st.line_chart(data.Close) 


    # Initialization of the game. Displays the graph to be guessed and the input form
    def new_game():
        st.title('Fordle - The Wordle for Finance Nerds')
        st.markdown('Which stock is being displayed here?')
        industry = df.loc[st.session_state.stock_to_be_guessed, 'GICS Sector']
        headquarters = df.loc[st.session_state.stock_to_be_guessed, 'Headquarters Location']
        plot()
        display_input()
        
        
    # Display of guess input fields. Triggers form_callback on submission
    def display_input():
        with st.form(key='my_form', clear_on_submit=True): 
            col1, col2, col3, col4, col5 = st.columns(5) 
            with col1:
                st.text_input(label="Letter 1: ", max_chars=1, key="guess1")
            with col2:
                st.text_input(label="Letter 2: ", max_chars=1, key="guess2")
            with col3:
                if len(st.session_state.stock_to_be_guessed) > 2:
                    st.text_input(label="Letter 3: ", max_chars=1, key="guess3")
            with col4:
                if len(st.session_state.stock_to_be_guessed) > 3:
                    st.text_input(label="Letter 4: ", max_chars=1, key="guess4") 
            with col5:
                ":bulb: Hint:"
                "Press tab to navigate across cells"
            submit_button = st.form_submit_button(label='Submit', on_click=form_callback)

    # Saves the guessed letters as a word        
    def save_guess():
        guess = st.session_state.guess1 + st.session_state.guess2
        if len(st.session_state.stock_to_be_guessed) > 2:
            guess += st.session_state.guess3
        if len(st.session_state.stock_to_be_guessed) > 3:
            guess += st.session_state.guess4
        st.session_state.guess = guess.upper()
    
    # Updates the empty dataframe with the guesses of the first round
    def update_df_round1():
        st.session_state.guess_df.iloc[[st.session_state.counter],[0]] = st.session_state.guess1.upper()
        st.session_state.guess_df.iloc[[st.session_state.counter],[1]] = st.session_state.guess2.upper()
        if len(st.session_state.stock_to_be_guessed) > 2:
            st.session_state.guess_df.iloc[[st.session_state.counter],[2]] = st.session_state.guess3.upper()
        if len(st.session_state.stock_to_be_guessed) > 3:
            st.session_state.guess_df.iloc[[st.session_state.counter],[3]] = st.session_state.guess4.upper()
        prep_for_coloring(st.session_state.guess_df)
        colored_df = st.session_state.guess_df.style.applymap(coloring)
        colored_df
        st.session_state.guess_df.to_csv('guesses.csv', index=True)

    # Updates the dataframe of the preceding round(s) with the guesses    
    def update_df_round2():
        guess_df = pd.read_csv('guesses.csv', index_col='Try', na_filter=False)
        guess_df.iloc[[st.session_state.counter],[0]] = st.session_state.guess1.upper()
        guess_df.iloc[[st.session_state.counter],[1]] = st.session_state.guess2.upper()
        if len(st.session_state.stock_to_be_guessed) > 2:
            guess_df.iloc[[st.session_state.counter],[2]] = st.session_state.guess3.upper()
        if len(st.session_state.stock_to_be_guessed) > 3:
            guess_df.iloc[[st.session_state.counter],[3]] = st.session_state.guess4.upper()
        prep_for_coloring(guess_df)
        colored_df = guess_df.style.applymap(coloring)
        colored_df
        guess_df.to_csv('guesses.csv', index=True)

    # Assigns whitespaces to characters depending on if letter is correct and in right place, used for coloring
    def prep_for_coloring(dataframe): 
        for index in range(len(st.session_state.stock_to_be_guessed)):
            if st.session_state.guess[index] == st.session_state.stock_to_be_guessed[index]:
                pass
            elif st.session_state.guess[index] in st.session_state.stock_to_be_guessed:
                dataframe.iloc[[st.session_state.counter],[index]] += " "
            else: 
                dataframe.iloc[[st.session_state.counter],[index]] += "  "

    # Colors the dataframe with criteria of prep_for_coloring            
    def coloring(field):  
        global color
        if len(field) == 1:
            color = 'green'
        elif len(field) == 2:
            color = 'goldenrod'
        elif len(field) == 3:
            color = 'grey'
        else: 
            color = None
        return 'background-color: %s' % color 
        

    # display hints about stock to player. This loop is the essence of the game and decides on victories or losses. 
    def form_callback():
        save_guess()
        # Case: entered word is correct
        if st.session_state.guess == st.session_state.stock_to_be_guessed:
            random_choice()
            st.session_state.counter = 0
            st.session_state.victories += 1 ###add display of dataframe
            new_game()
            st.write('**You have guessed correctly!** \U0001F60D')
            st.write('Keep doing what you are doing. Next stock!') ###maybe first display text + button that lets you click for next stock
        # Case: The maximum number of rounds have been exceeded
        elif st.session_state.counter >= 4:
            random_choice()
            st.session_state.counter = 0
            st.session_state.loss += 1
            new_game()
            st.write('**You have lost.** New try, with a new stock!') #first display text+ actual solution + button that lets you click for next stock
        # Case: round 1
        elif st.session_state.counter == 0:
            new_game()
            st.write('**Wrong choice** \U0001F612')
            update_df_round1()
            st.session_state.counter += 1
        # Case: round 2+
        else:
            new_game()
            st.write('**Wrong choice** \U0001F612')
            update_df_round2()
            st.session_state.counter += 1
            industry = df.loc[st.session_state.stock_to_be_guessed, 'GICS Sector']
            headquarters = df.loc[st.session_state.stock_to_be_guessed, 'Headquarters Location']
            st.write(f'**Here is a hint:** The stock is in the _{industry}_ industry and its headquarters are located in _{headquarters}_. Try again!')


    # initialize state variables needed within streamlit for the game to run and run the game methods 

    if "counter" not in st.session_state:
        st.session_state.period = "y"
        st.session_state.new_game = True
        st.session_state.counter = 0
        st.session_state.victories = 0
        st.session_state.loss = 0
        random_choice()
        new_game()


    #counts the number of times we lost or won a game 
    amount_win = st.session_state.victories
    amount_losses = st.session_state.loss


    # side bar with information on number of games, wins and losses
    with st.sidebar:
        st.title("Score count")
        st.write("You played ", st.session_state.victories + st.session_state.loss, " times ", f"and have won {st.session_state.victories} times and lost {st.session_state.loss} times.") ###clean up code
        if st.session_state.victories + st.session_state.loss > 0:
            if st.session_state.victories > st.session_state.loss:
                st.write("**Amazing score, keep going!**")
            elif st.session_state.victories == st.session_state.loss:
                st.write("**Just a few more wins. You got this!**")
            else:
                st.write("How about a Master in Finance at Nova SBE? It will certainly help to win this game!")
                st.write("Check out the program: https://www.novasbe.unl.pt/en/programs/masters/finance/")

                
    # Creates an empty dataframe in which guesses can be displayed later
    tries = ['1st', '2nd', '3rd', '4th', '5th']  

    if len(st.session_state.stock_to_be_guessed) == 2: 
        guess_df=pd.DataFrame({'Try': tries,'Letter 1':['','','','',''], 'Letter 2':['','','','','']})
    if len(st.session_state.stock_to_be_guessed) == 3: 
        guess_df=pd.DataFrame({'Try': tries,'Letter 1':['','','','',''], 'Letter 2':['','','','',''], 'Letter 3':['','','','','']})
    if len(st.session_state.stock_to_be_guessed) == 4: 
        guess_df=pd.DataFrame({'Try': tries,'Letter 1':['','','','',''], 'Letter 2':['','','','',''], 'Letter 3':['','','','',''], 'Letter 4':['','','','','']})

    guess_df.set_index('Try', inplace=True)
    st.session_state.guess_df = guess_df 


    
    ###to be deleted in the end       
    for item in st.session_state.items():
        item
    
                    
def landing_page():
    st.title('Fordle - The Wordle for Finance Nerds')
    with st.expander("See explanation of the game"):
        st.write("""**How does the game work?** \n\n Each time you must guess a concrete company name which can be found in the drop-down menu. After one try you will get a hint regarding the industry and headquarter location and after three tries you will get the ticker hint.\n\n Hit the enter button to submit your answer.
                 """)
        st.image("https://th.bing.com/th/id/R.7e47d1b5f1ec42e32ddaab0d85fb9951?rik=%2bckFqF3%2fX95xdQ&pid=ImgRaw&r=0")
    st.markdown('Guess the **FORDLE** in **three** (Beginner) or **five** (Expert) tries.')
    st.header('Lets get started!')

# button to choose which game player wants to pick
if 'absolute_counter' not in st.session_state:
    st.session_state.absolute_counter = 0
    landing_page()
    button = st.button("Beginner", on_click=beginner)
    button = st.button("Advanced", on_click=advanced)
elif st.session_state.absolute_counter == 0:
    st.session_state.absolute_counter += 1
else:
    st.session_state.absolute_counter += 1
    if st.session_state.level == "beginner":
        beginner()
    else:
        advanced()
