import streamlit as st
from openai import OpenAI
import datetime

api_key = st.secrets["openai"]["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

#Credit Card Article Title Prompt
def generate_credit_card_article_title(input_text):
    today_date = datetime.date.today().strftime("%B %d, %Y")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"Act as an expert in performance marketing advertorial content writing. Please only output the article title without any additional context. You will use the provided credit card and the provided value propositions to generate an advertorial style title. Here are some structural examples to adhere to:\n\nGenerated title: Unlock $200 Welcome Bonus & 0% Interest For 18 Months\nProblems: Avoid cliche words often used by LLMs such as 'Unlock', when presented with temporary promotions we want to reference the end year of the promotion rather than simply stating it. Use today's date of {today_date} as the reference point.\nIdeal title: Massive $200 Welcome Bonus & 0% Interest Until Nearly 2026\n\nGenerated title: Claim Your $200 Cash Rewards Bonus & 0% Interest Until Late 2025\nProblems: Consumers generally want promotions for as long as possible, so it is better to say 'until nearly 2026' rather than 'until late 2025'.\nIdeal title: Massive $200 Welcome Bonus & 0% Interest Until Nearly 2026\n\nGenerated title: Double Your Cash Back with Unlimited Match & 0% Intro APR Until Early 2025\nProblems: Consumers generally want promotions for as long as possible, so it is better to say just '2025' instead of 'early 2025'.\nIdeal title: Double Your Cash Back with Unlimited Match & 0% Intro APR Until 2025"
            },
            {
                "role": "user",
                "content": "Credit Card: Citi Double Cash; Value Propositions: Earn $200 cash back after you spend $1,500 on purchases in the first 6 months of account opening.\nIntro APR of 0% for 18 months on Balance Transfers, 19.24% - 29.24% (Variable) APR thereafter.\nEarn unlimited 2% cash back on every purchase.\n$0 annual fee\nClick “APPLY NOW” to apply online"
            },
            {
                "role": "assistant",
                "content": "Massive $200 Welcome Bonus & 0% Interest Until 2026"
            },
            {
                "role": "user",
                "content": "Credit Card: Discover it® Cash Back card; Value Propositions: INTRO OFFER: Unlimited Cashback Match for all new cardmembers–only from Discover. Discover will automatically match all the cash back you've earned at the end of your first year! There’s no minimum spending or maximum rewards. You could turn $150 cash back into $300.\nEarn 5% cash back on everyday purchases at different places you shop each quarter like grocery stores, restaurants, gas stations, and more, up to the quarterly maximum when you activate. Plus, earn unlimited 1% cash back on all other purchases—automatically.\nRedeem your rewards for cash at any time.\nDiscover could help you reduce exposure of your personal information online by helping you remove it from select people-search sites that could sell your data. It's free, activate with the mobile app.\nGet a 0% intro APR for 15 months on purchases. Then 18.24% to 28.24% Standard Variable Purchase APR applies, based on credit worthiness.\nNo annual fee.\nTerms and conditions apply."
            },
            {
                "role": "assistant",
                "content": "The Highest Cash Back Card We've Come Across Has 0% Intro APR Until Nearly 2026"
            },

            {
                "role": "user",
                "content": input_text
            }
        ],
        temperature=0.49,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0.99,
        presence_penalty=0
    )
    return response.choices[0].message.content

def generate_credit_card_article_intro(input_text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
                    {
            "role": "system",
            "content": [
                {
                "type": "text",
                "text": "Act as an expert in performance marketing advertorial content writing. Your job is to write an intro that summarizes in bullets key takeaways around the highlights of the card and also has at least some paragraph style content. Please only output the article intro without any additional context. You will use the provided credit card and the provided value propositions to generate an advertorial style intro. \n\nThe writing style in your text must be informative and persuasive with a direct and conversational tone. It uses simple, straightforward language to quickly communicate the benefits of the credit card offered. The style is geared towards convincing readers to take action (apply for the card) by highlighting key advantages and using a sense of urgency. Key characteristics include:\nDirectness: The introduction sets a no-nonsense tone, getting straight to the point.\nEngagement: The use of conversational language and rhetorical questions \nCall to Action: The text ends with a clear and direct call to action\nOverall, it's a concise, engaging, and action-oriented style, typical of marketing and promotional content.\n\nHere are some examples of outputs to guide content quality:\nParagraph: Are you ready to supercharge your spending with a card that truly rewards you for every dollar you spend?  Meet the [credit card], a powerhouse in the realm of cash back credit cards, designed for savvy spenders who want to maximize their earnings without paying a penny in annual fees.\nProblem: Supercharge, unlock, imagine, and words like that are cliches. Stick to more authentic language that hits on the same effect\nIdeal sentence: Have you been looking for a card that truly rewards you for every dollar you spend? Well look no further. The [credit card] is one of a kind in its field - designed for spenders to maximize their earnings without paying a penny in annual fees."
                }
            ]
            },
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": "Credit Card: Citi Double Cash; Value Propositions: Earn $200 cash back after you spend $1,500 on purchases in the first 6 months of account opening.\nIntro APR of 0% for 18 months on Balance Transfers, 19.24% - 29.24% (Variable) APR thereafter.\nEarn unlimited 2% cash back on every purchase.\n$0 annual fee\nClick “APPLY NOW” to apply online"
                }
            ]
            },
            {
            "role": "assistant",
            "content": [
                {
                "type": "text",
                "text": "Bottom Line:\n- Earn $200 cash back after you spend $1,500 on purchases in the first 6 months of account opening.\n- Intro APR of 0% for 18 months on Balance Transfers, 19.24% - 29.24% (Variable) APR thereafter. Apply online today and enjoy zero interest on balance transfers well into 2025. This period begins from the date of your first transfer.\n- Earn unlimited 2% cash back on every purchase. One of the highest flat-rate cash offers we’ve seen with no strings attached.\n- No annual fee. The card is designed to help you save money. You’ll automatically avoid any annual or upfront fees.\n- Bigtime reward potential doesn’t usually piggyback with long-term balance transfer offers, but this card is flipping the script on all sorts of killer combinations. Let’s look at all the angles the Citi Double Cash® Card uses to save you a bundle while you rack up the cash back.\n\nBigtime reward potential doesn’t usually piggyback with long-term balance transfer offers, but this card is flipping the script on all sorts of killer combinations. Let’s look at all the angles the Citi Double Cash® Card uses to save you a bundle while you rack up the cash back."
                }
            ]
            },
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": "Credit Card: Discover it® Cash Back card; Value Propositions: INTRO OFFER: Unlimited Cashback Match for all new cardmembers–only from Discover. Discover will automatically match all the cash back you've earned at the end of your first year! There’s no minimum spending or maximum rewards. You could turn $150 cash back into $300.\nEarn 5% cash back on everyday purchases at different places you shop each quarter like grocery stores, restaurants, gas stations, and more, up to the quarterly maximum when you activate. Plus, earn unlimited 1% cash back on all other purchases—automatically.\nRedeem your rewards for cash at any time.\nDiscover could help you reduce exposure of your personal information online by helping you remove it from select people-search sites that could sell your data. It's free, activate with the mobile app.\nGet a 0% intro APR for 15 months on purchases. Then 18.24% to 28.24% Standard Variable Purchase APR applies, based on credit worthiness.\nNo annual fee.\nTerms and conditions apply."
                }
            ]
            },
            {
            "role": "assistant",
            "content": [
                {
                "type": "text",
                "text": "Let's cut right to the chase. \n\nOur experts have decades of experience and have reviewed hundreds of credit cards. \n\nThe Discover it® Cash Back card is one of the very few that’s so good, our top experts have signed up for it personally. In fact, they named it the Best Cash Back Credit Card of 2024!\n\nHere's why they use it:\n- You’ll earn up to 5% cash back on rotating activated categories you'll actually use on up to $1,500 in purchases each quarter.\n- Discover will automatically match all the cash back new cardholders have earned at the end of the first year. Even the purchases you earn 5% cash back on will get an unlimited match.\n- On top of that, you'll pay 0% interest until nearly 2026 on both purchases and balance transfers -- that's 15 months of a 0% intro APR. The go-to rate of 18.24% - 28.24% Variable APR applies after the intro period.\n- No annual fee\n- Click APPLY NOW to apply today\n\nSo what can this actually add up to in the real world? We calculate that cardholders can secure $1,306 from the first-year bonus and premium cash back alone. (See how below.) Not a bad return on investment for the 2-minute application process!"
                }
            ]
            },
                    {
                "role": "user",
                "content": input_text
            }
        ],
        temperature=1,
        max_tokens=3727,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
    
    return response.choices[0].message.content


# Main app
def main():
    st.title("Advertorial Automation (Credit Cards)")

    # Text input for credit card type
    credit_card_type = st.text_input("Enter Credit Card")

    # Text input for value propositions
    value_propositions = st.text_area("Enter Value Propositions", height=200)

    # Button to generate article title
    if st.button("Generate Article Title"):
        if credit_card_type and value_propositions:
            input_text = f"Credit Card: {credit_card_type}; Value Propositions: {value_propositions}"
            article_title = generate_credit_card_article_title(input_text)
            st.session_state['article_title'] = article_title  # Store in session state
            st.session_state.pop('article_intro', None)  # Clear intro if title is regenerated

    # Display the generated article title if it exists
    if 'article_title' in st.session_state and st.session_state['article_title']:
        st.subheader("Generated Article Title")
        st.text(st.session_state['article_title'])

        # Button to generate article introduction
        if st.button("Generate Article Intro"):
            input_text = st.session_state['article_title']
            article_intro = generate_credit_card_article_intro(input_text)
            st.session_state['article_intro'] = article_intro  # Store in session state

    # Display the generated article introduction if it exists
    if 'article_intro' in st.session_state:
        st.subheader("Stored Article Intro")
        st.text(st.session_state['article_intro'])




if __name__ == "__main__":
    main()
