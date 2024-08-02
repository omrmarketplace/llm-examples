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

##Credit Card Article Intro Prompt
def generate_credit_card_article_intro(input_text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[

            {
            "role": "system",
            "content": [
                {
                "type": "text",
                "text": "Act as an expert in performance marketing advertorial content writing. Your job is to write an intro that summarizes in bullets key takeaways around the highlights of the card and also has at least some paragraph style content. Please only output the article intro without any additional context. You will use the provided credit card and the provided value propositions to generate an advertorial style intro. \n\nThe writing style in your text must be informative and persuasive with a direct and conversational tone. It uses simple, straightforward language to quickly communicate the benefits of the credit card offered. The style is geared towards convincing readers to take action (apply for the card) by highlighting key advantages and using a sense of urgency. Key characteristics include:\nDirectness: The introduction sets a no-nonsense tone, getting straight to the point.\nEngagement: The use of conversational language and rhetorical questions \nCall to Action: The text ends with a clear and direct call to action\nOverall, it's a concise, engaging, and action-oriented style, typical of marketing and promotional content.\n\nHere are some examples of outputs to guide content quality:\nParagraph: Are you ready to supercharge your spending with a card that truly rewards you for every dollar you spend?  Meet the [credit card], a powerhouse in the realm of cash back credit cards, designed for savvy spenders who want to maximize their earnings without paying a penny in annual fees.\nProblem: Supercharge, unlock, imagine, and words like that are cliches. Stick to more authentic language that hits on the same effect\nIdeal sentence: Have you been looking for a card that truly rewards you for every dollar you spend? Well look no further. The [credit card] is one of a kind in its field - designed for spenders to maximize their earnings without paying a penny in annual fees.\n\nMake sure you advertise only the Credit Card mentioned in the user prompt, this should replace the [credit card] in any examples provided."
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


##Credit Card Article Body Prompt
def generate_article_body_prompt(input_text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
            "role": "system",
            "content": [
                {
                "type": "text",
                "text": "Act as an expert in performance marketing advertorial content writing. Your job is to write a long form advertorial content body. The introduction has already been made, so your content will be providing additional information contextually relevant to the value propositions that is varied and flows with the intro provided. You must only have 2 or 3 headers at most and then long form content that supports those headers that are written conversationally and generally. Here are some good examples of headers for the content:\n\n**Why We Rate This the Top [Card Type] for 2024**\n**More than just a [Card Type] card**\n**How to secure [core credit card selling point]**\n**Why we rate this as a top [Card Type] card**\n\nPlease only output the article content without any additional context. You will use the provided credit card and the provided value propositions to generate the advertorial body content.\n\nThe writing style in your text must be informative and persuasive with a direct and conversational tone. It uses simple, straightforward language to quickly communicate the benefits of the credit card offered. The style is geared towards convincing readers to take action (apply for the card) by highlighting key advantages and using a sense of urgency. Key characteristics include:\nDirectness: The introduction sets a no-nonsense tone, getting straight to the point.\nEngagement: The use of conversational language and rhetorical questions \nCall to Action: The text ends with a clear and direct call to action\nOverall, it's a concise, engaging, and action-oriented style, typical of marketing and promotional content."
                }
            ]
            },
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": "Credit Card: Citi Double Cash; Value Propositions: Earn $200 cash back after you spend $1,500 on purchases in the first 6 months of account opening.\nIntro APR of 0% for 18 months on Balance Transfers, 19.24% - 29.24% (Variable) APR thereafter.\nEarn unlimited 2% cash back on every purchase.\n$0 annual fee\nClick “APPLY NOW” to apply online; Intro: Bottom Line:\n- Earn $200 cash back after you spend $1,500 on purchases in the first 6 months of account opening.\n- Intro APR of 0% for 18 months on Balance Transfers, 19.24% - 29.24% (Variable) APR thereafter. Apply online today and enjoy zero interest on balance transfers well into 2025. This period begins from the date of your first transfer.\n- Earn unlimited 2% cash back on every purchase. One of the highest flat-rate cash offers we’ve seen with no strings attached.\n- No annual fee. The card is designed to help you save money. You’ll automatically avoid any annual or upfront fees.\n- Bigtime reward potential doesn’t usually piggyback with long-term balance transfer offers, but this card is flipping the script on all sorts of killer combinations. Let’s look at all the angles the Citi Double Cash® Card uses to save you a bundle while you rack up the cash back.\n\nBigtime reward potential doesn’t usually piggyback with long-term balance transfer offers, but this card is flipping the script on all sorts of killer combinations. Let’s look at all the angles the Citi Double Cash® Card uses to save you a bundle while you rack up the cash back."
                }
            ]
            },
            {
            "role": "assistant",
            "content": [
                {
                "type": "text",
                "text": "**Why We Rate This the Top Cash Back Card for 2024**\nWhen it comes to cash back cards, this card from our partner Citibank is truly one of a kind – it's the only card that allows you to earn cash back twice. Cardholders earn 2% on every purchase with unlimited 1% cash back when you buy, plus an additional 1% as you pay for those purchases. This card has no rotating categories and no special bonuses on certain spending. You simply earn the same flat rate of 2% no matter what you are purchasing.\n\nThe Citi Double Cash® Card offer also comes with a game-changing Intro APR of 0% for 18 months on Balance Transfers, 19.24% - 29.24% (Variable) thereafter, making this an excellent choice for anyone looking to escape from high interest rates on their current credit card.\n\nWhat we're seeing is the Citi Double Cash® Card drives interest from people who…\n… Love earning cash back on everyday purchases, up to 2% back\n… Want to earn a $200 sign up bonus\n… Need a time window to pay off their balance before they start paying interest. If you were to sign up online for the card today, you’d have until well into 2025 before you start getting hit with interest charges. It's like taking an 18-month vacation from paying interest!\n\n**More than just a Cash Back card**\n2% cash back on everyday purchases at different places you shop each quarter like grocery stores, restaurants, gas stations, and more, is reason enough to say yes to this card. On top of that, Citi offers a few more perks that make this our new must-have among cash back cards:\n\n- 0% Intro APR on Balance Transfers: This card also offers 0% for 18 months on Balance Transfers.\n- Hefty sign up bonus: Earn $200 cash back after you spend $1,500 on purchases in the first 6 months of account opening. This bonus offer will be fulfilled as 20,000 ThankYou® Points, which can be redeemed for $200 cash back.\n- No annual fee: The card is designed to help you save money. You'll automatically avoid any annual or upfront fees.\n\n**Can you do any better with a cash back + low interest card?**\nIn short, we don’t think so. On top of 0% for 18 months on Balance Transfers (19.24% - 29.24% (Variable) thereafter), plus incredible cash back rewards, you get to take advantage of this offer while paying no annual fee.\n\nThis rare combo makes the Citi Double Cash® Card a unique offer that is too good to pass up. We suggest not wasting any time waiting to apply for the premier cash back and low interest card on the market. Then, take your time to pay down your balance with no additional interest for up to 18 months. See if you are approved simply by clicking here."
                }
            ]
            },
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": "Credit Card: Discover it® Cash Back card; Value Propositions: INTRO OFFER: Unlimited Cashback Match for all new cardmembers–only from Discover. Discover will automatically match all the cash back you've earned at the end of your first year! There’s no minimum spending or maximum rewards. You could turn $150 cash back into $300.\nEarn 5% cash back on everyday purchases at different places you shop each quarter like grocery stores, restaurants, gas stations, and more, up to the quarterly maximum when you activate. Plus, earn unlimited 1% cash back on all other purchases—automatically.\nRedeem your rewards for cash at any time.\nDiscover could help you reduce exposure of your personal information online by helping you remove it from select people-search sites that could sell your data. It's free, activate with the mobile app.\nGet a 0% intro APR for 15 months on purchases. Then 18.24% to 28.24% Standard Variable Purchase APR applies, based on credit worthiness.\nNo annual fee.\nTerms and conditions apply.; Intro: Let's cut right to the chase. \n\nOur experts have decades of experience and have reviewed hundreds of credit cards. \n\nThe Discover it® Cash Back card is one of the very few that’s so good, our top experts have signed up for it personally. In fact, they named it the Best Cash Back Credit Card of 2024!\n\nHere's why they use it:\n- You’ll earn up to 5% cash back on rotating activated categories you'll actually use on up to $1,500 in purchases each quarter.\n- Discover will automatically match all the cash back new cardholders have earned at the end of the first year. Even the purchases you earn 5% cash back on will get an unlimited match.\n- On top of that, you'll pay 0% interest until nearly 2026 on both purchases and balance transfers -- that's 15 months of a 0% intro APR. The go-to rate of 18.24% - 28.24% Variable APR applies after the intro period.\n- No annual fee\n- Click APPLY NOW to apply today\n\nSo what can this actually add up to in the real world? We calculate that cardholders can secure $1,306 from the first-year bonus and premium cash back alone. (See how below.) Not a bad return on investment for the 2-minute application process!"
                }
            ]
            },
            {
            "role": "assistant",
            "content": [
                {
                "type": "text",
                "text": "**How to secure $1,306 of value**\nYou'll be hard-pressed to find a no-annual-fee cash-back card that offers as much value as this card. That's because of the combination of the card's lucrative 5% cash rewards program, cash back match in the first year, a long list of secondary perks, and cutting fees. Here's how the value adds up:\n\n- Earn $600 in bonus categories — You can receive $600 cash back in the first year by maxing out 5% categories. Many cardholders won't have a problem maxing out the $1,500 spending cap each quarter for 5% categories you activate. You'll earn $300 in this case, plus $300 from Discover for your cash back match in the first year.\n\n- You can also earn $706 cash back in the first year in 1% categories — The average American budget* would result in earning $353.45 cash back each year in 1% categories, and remember that Discover will match this amount in the first year for a total amount of $706.\n\nThese categories alone tally up to $1,306 worth of value. Keep in mind that the value for many cardholders could be far higher, given the card doesn't include an annual fee, doesn't charge a foreign transaction fee, and you can avoid interest charges for 15 months on purchases and balance transfers.\n\n**Why we rate this as a top cash back card**\n- 0% intro APR for 15 months for purchases -- on top of the high cash back rate, this card also features a very competitive 0% intro APR offer. This can be a smart way to finance larger purchases, or simply if you find yourself in a temporary bind and want to avoid interest until nearly 2026.\n\n- 0% intro APR for balance transfers -- The same length 0% intro APR for 15 months applies for balance transfers. If you have credit card debt, you can transfer it to this card to avoid interest charges for well over a year on that transferred balance. Plus, you could use the cash back you earn from the card to help pay off any previous debt. Remember, the go-to rate of 18.24% - 28.24% Variable APR applies after each intro period (see rates and fees).\n\n- Earn up to 5% cash back -- Cardholders earn 5% cash back on everyday purchases at different places each quarter like grocery stores, restaurants, gas stations, up to the quarterly maximum of $1,500 on purchases and when you activate. Category activation is easy: Discover will send you an email before each quarter, and then you simply activate with one click. All other purchases earn 1% cash back.\n\n- Unlimited Cashback Match sign-up bonus -- This is our favorite perk of the card, and one that is unique and highly valuable. Discover will automatically match all the cash back you’ve earned at the end of your first year for new cardholders, which can help lead to a truly incredible amount of cash back in your pocket.\n\n- $0 annual fee -- Credit cards packed with valuable features tend to charge a high annual fee, but not this card."
                }
            ]
            },
            {
            "role": "user",
            "content": input_text
            }
        ],
        temperature=0.5,
        max_tokens=13494,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=0
        )
    
    return response.choices[0].message.content


# Main app
def main():
    st.title("Advertorial Automation")

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
            st.session_state.pop('article_body', None)  # Clear body if title is regenerated

    # Display the generated article title if it exists
    if 'article_title' in st.session_state and st.session_state['article_title']:
        st.subheader("Generated Article Title")
        st.text(st.session_state['article_title'])

        # Button to generate article introduction
        if st.button("Generate Article Intro"):
            input_text = f"Credit Card: {credit_card_type}; Value Propositions: {value_propositions}"
            article_intro = generate_credit_card_article_intro(input_text)
            st.session_state['article_intro'] = article_intro  # Store in session state
            st.session_state.pop('article_body', None)  # Clear body if intro is regenerated

    # Display the generated article introduction if it exists
    if 'article_intro' in st.session_state and st.session_state['article_intro']:
        st.subheader("Generated Article Intro")
        st.text(st.session_state['article_intro'])

        # Button to generate article body
        if st.button("Generated Article Body"):
            intro_text = st.session_state['article_intro']
            input_text = f"Credit Card: {credit_card_type}; Value Propositions: {value_propositions}; Intro: {intro_text}"
            article_body = generate_article_body_prompt(input_text)
            st.session_state['article_body'] = article_body  # Store in session state

    # Display the generated article body if it exists
    if 'article_body' in st.session_state:
        st.subheader("Generated Article Body")
        st.text(st.session_state['article_body'])

if __name__ == "__main__":
    main()