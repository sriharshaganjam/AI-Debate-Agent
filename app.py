import streamlit as st
import random
import time

# Set page configuration
st.set_page_config(
    page_title="AI Debate Simulator",
    page_icon="🎭",
    layout="wide"
)

# Initialize session state
if 'pro_score' not in st.session_state:
    st.session_state.pro_score = 0
if 'con_score' not in st.session_state:
    st.session_state.con_score = 0
if 'current_round' not in st.session_state:
    st.session_state.current_round = 1
if 'sub_round' not in st.session_state:
    st.session_state.sub_round = 1
if 'debate_history' not in st.session_state:
    st.session_state.debate_history = []
if 'current_topic' not in st.session_state:
    st.session_state.current_topic = ""
if 'game_active' not in st.session_state:
    st.session_state.game_active = False
if 'winner_declared' not in st.session_state:
    st.session_state.winner_declared = False

# Pro arguments database (simulating research)
pro_arguments = {
    "climate change": [
        "Climate change demands immediate action as scientific consensus confirms human activities are the primary cause of global warming. Rising temperatures have already increased extreme weather events by 40% since 1980, threatening food security and infrastructure. Clean energy solutions are economically viable, with solar costs dropping 89% since 2010. Early investments in climate mitigation save $7 for every $1 spent and create sustainable jobs. The IPCC warns that limiting warming to 1.5°C requires 45% emissions reduction by 2030, making this decade critical. The evidence is clear: addressing climate change protects our economy, health, and future generations.",
        "The economic benefits of climate action far outweigh the costs. Research shows climate policies generate a return of $3-8 per dollar invested through healthcare savings, job creation, and avoided damages. Renewable energy already employs more Americans than fossil fuels and grows three times faster than other sectors. Meanwhile, climate inaction costs the US economy approximately $240 billion annually in disaster recovery, healthcare costs, and agricultural losses. These figures will rise exponentially without intervention. Forward-thinking businesses recognize this reality, with over 300 major corporations committing to 100% renewable energy, demonstrating that sustainability drives profit and innovation."
    ],
    "artificial intelligence": [
        "Artificial intelligence offers unprecedented opportunities to solve humanity's most pressing challenges. AI systems already outperform human experts in disease diagnosis, reducing medical errors by up to 85% in some specialties. In climate science, AI models predict extreme weather events with 89% accuracy, saving countless lives. Educational AI tutors have demonstrated the ability to improve student outcomes by 30% while addressing teacher shortages. Furthermore, AI-powered resource optimization in agriculture, energy, and manufacturing could reduce global carbon emissions by 4% by 2030 while increasing productivity. Embracing AI development with appropriate safeguards represents our best path toward a more prosperous, sustainable future.",
        "AI development creates more jobs than it displaces when properly implemented. Historical data shows technological revolutions consistently generate net employment gains - the computer revolution created 15.8 million more jobs than it eliminated. Current AI deployment follows this pattern, with companies implementing AI reporting 34% average productivity increases alongside workforce growth. New positions like AI ethics officers, data curators, and human-AI collaboration specialists are emerging rapidly. Additionally, AI augmentation allows humans to focus on inherently human skills like creativity, empathy, and complex decision-making - areas where AI still significantly lags. The evidence shows AI complements rather than replaces human potential."
    ],
    "social media": [
        "Social media has revolutionized civic engagement and democratized information access. Research shows platforms like Twitter have amplified marginalized voices, with 62% of racial justice movements crediting social media for their growth and policy impacts. During crises, these platforms facilitate rapid information sharing and community organization, with disaster response agencies reporting 40% faster coordination through social channels. For small businesses, social media provides affordable, targeted marketing, helping 67% of new ventures achieve profitability. Educational content thrives on these platforms, with 71% of users reporting learning new skills or concepts. When regulated thoughtfully, social media strengthens democracy, economic opportunity, and community resilience.",
        "Social media's positive impact on global connectivity creates unprecedented opportunities for collaboration. Cross-border friendships formed online have increased cultural understanding, with 68% of users reporting more positive attitudes toward different cultures. Professional networking platforms have democratized opportunity, with 35% of new jobs filled through these connections, particularly benefiting underrepresented groups. During the pandemic, social platforms reduced isolation, with mental health professionals noting their critical role in maintaining social bonds. Additionally, crowdfunding through social media has democratized philanthropy, raising billions for causes that traditional channels overlooked. These platforms, when designed responsibly, strengthen our collective ability to solve shared challenges."
    ],
    "renewable energy": [
        "Renewable energy represents both an environmental imperative and economic opportunity. Wind and solar power have become the cheapest forms of electricity generation in most global markets, with prices falling over 70% in the last decade. The sector now employs over 11 million people worldwide, growing 4-5 times faster than fossil fuel industries. Grid reliability concerns have been addressed through advances in storage technology, with battery costs declining 88% since 2010. Furthermore, distributed renewable systems enhance energy security and grid resilience against both natural disasters and cyber threats. The transition to renewables is no longer just environmentally necessary but economically inevitable.",
        "Renewable energy development addresses environmental justice concerns that have plagued traditional energy production. Fossil fuel infrastructure has historically concentrated pollution in low-income communities, with residents experiencing 63% higher rates of respiratory illness and reduced lifespans. In contrast, distributed solar and community wind projects return economic benefits directly to communities while eliminating local pollution. Indigenous communities have demonstrated particular success with renewable projects, achieving energy sovereignty while preserving cultural values. Rural areas benefit especially, with renewable installations generating 7 times more permanent jobs per unit of energy than fossil equivalents while providing stable income through land lease agreements."
    ],
    "genetic engineering": [
        "Genetic engineering presents revolutionary solutions to global challenges. Agricultural applications have already increased crop yields by up to 22% while reducing pesticide use by 37%, addressing food security for a growing population. Medical breakthroughs include gene therapies curing previously untreatable conditions like sickle cell disease and certain forms of blindness. CRISPR technology has democratized research, accelerating discovery while reducing costs by over 99% compared to earlier methods. Strict regulatory frameworks ensure safety while allowing innovation - after 25+ years of commercial use, genetically modified foods have shown no adverse health effects across thousands of studies. The responsible advancement of genetic engineering offers our best hope for addressing diseases, food security, and environmental challenges.",
        "Genetic engineering's precision makes it inherently safer than traditional breeding methods. Conventional breeding introduces thousands of uncharacterized genetic changes, while genetic engineering typically modifies 1-3 specific genes with extensive pre-market testing. This has practical benefits: drought-resistant crops developed through genetic engineering reduce water usage by up to 30% compared to conventional varieties. Medical applications have progressed from treating rare disorders to addressing common conditions - gene therapy approaches for heart disease, diabetes, and Alzheimer's show promising early results. With appropriate oversight, genetic technologies represent a natural extension of humanity's long history of innovation, offering targeted solutions to our most intractable problems."
    ]
}

# Con arguments database (simulating research)
con_arguments = {
    "climate change": [
        "Climate change policies often impose disproportionate economic burdens without guaranteed environmental benefits. Proposed carbon taxes would increase average household energy costs by 30% while disproportionately affecting lower-income families who spend three times more of their income on energy. Developing nations rightfully prioritize economic growth, with China and India building three new coal plants weekly despite climate agreements. Even if Western nations achieved net-zero emissions tomorrow, global emissions would continue rising. Meanwhile, climate models regularly overestimate warming - 95% of models from 2000-2010 predicted higher temperatures than actually occurred. We need pragmatic, economically sustainable approaches rather than policies that sacrifice prosperity for uncertain gains.",
        "Climate solutions must balance environmental goals with economic realities. Current renewable energy technologies cannot reliably meet baseload power demands, with Germany's energiewende demonstrating this challenge - despite $580 billion invested, emissions decreased just 12% while electricity prices doubled. Natural solutions like reforestation cost 75% less per ton of carbon sequestered than technical approaches. Additionally, climate adaptation strategies deliver immediate benefits regardless of emissions trajectories - infrastructure hardening, agricultural innovation, and water management systems protect communities today while remaining valuable in any climate scenario. A balanced approach acknowledges both the reality of climate change and the economic constraints facing ordinary citizens."
    ],
    "artificial intelligence": [
        "Artificial intelligence poses unprecedented risks that demand cautious development. AI systems increasingly make consequential decisions without transparency or accountability, with algorithmic biases already demonstrated in lending, hiring, and criminal justice. These systems amplify existing social inequalities - facial recognition software shows error rates 34% higher for darker-skinned women than light-skinned men. Job displacement threatens economic stability, with 47% of US jobs at high risk of automation within two decades according to Oxford economists. Most concerning, advanced AI development outpaces our ability to ensure alignment with human values, with leading AI researchers themselves warning of existential risks. Without dramatically stronger safeguards and international oversight, AI development prioritizes corporate profits over human wellbeing.",
        "AI development concentrates power in ways that undermine democracy and autonomy. Just five companies control the most advanced AI systems, creating unprecedented market dominance - these firms already capture 35% of all US corporate profits. AI-powered surveillance enables both corporate and government monitoring at scales previously impossible, with facial recognition deployed in public spaces without consent. Social media algorithms optimized by AI demonstrably increase polarization, with engagement-maximizing systems promoting divisive content that receives 6-8 times more interaction. Furthermore, language models trained on internet data perpetuate harmful stereotypes while presenting information with unwarranted authority. Without public oversight and democratically determined boundaries, AI systems primarily serve their creators rather than humanity broadly."
    ],
    "social media": [
        "Social media platforms systematically undermine mental health and democratic discourse. Engagement-based algorithms promote divisive, emotionally triggering content, with internal research at major platforms confirming increased anxiety, depression, and body image issues particularly among younger users. Adolescents using social media 3+ hours daily show 35% higher rates of suicidal ideation. Information integrity suffers as false news spreads six times faster than accurate information according to MIT research, while echo chambers reduce exposure to diverse viewpoints by up to 45%. Privacy violations are intrinsic to the business model, with platforms collecting over 52,000 data points per user to enable manipulation for advertising purposes. The evidence is clear: current social media design optimizes for profit at the expense of individual and societal wellbeing.",
        "Social media's attention economy creates fundamentally misaligned incentives with human flourishing. These platforms expertly exploit psychological vulnerabilities, with the average user checking their phone 96 times daily - interruptions that research shows reduce cognitive capacity equivalent to losing a full night's sleep. Content moderation remains ineffective, with harmful material reaching millions before removal and traumatizing both users and underpaid moderators. Local communities suffer as social interaction increasingly shifts online, with each hour of social media use associated with 8% reduced face-to-face social activity. Democratic governance faces unprecedented challenges when public discourse occurs on private platforms optimized for engagement rather than understanding. Without fundamental redesign prioritizing human wellbeing over shareholder value, social media will continue undermining social fabric."
    ],
    "renewable energy": [
        "Renewable energy transitions face practical limitations that proponents often minimize. Wind and solar's intermittency creates substantial grid management challenges, requiring either massive overbuilding (increasing costs by 40-300%) or continued fossil fuel backup. Material requirements present serious environmental and geopolitical concerns - a single wind turbine requires 900 tons of steel, 2,500 tons of concrete, and rare earth minerals often mined with significant environmental damage in politically unstable regions. The energy storage challenge remains unsolved at grid scale, with current battery technology requiring lithium mining that consumes 500,000 gallons of water per ton extracted. Additionally, the environmental footprint of renewables includes significant land use impacts - solar farms require 450 times more land than natural gas plants per megawatt. A realistic energy policy acknowledges these constraints.",
        "Current renewable energy policies often create inequitable outcomes while insufficiently addressing emissions. Residential solar incentives disproportionately benefit wealthy homeowners while raising electricity rates for everyone else, with California studies showing low-income residents paying an additional $65-$80 monthly to subsidize net metering. Wind development frequently faces opposition from rural communities concerned about noise, wildlife impacts, and property devaluation, yet urban policymakers often dismiss these concerns. Meanwhile, the fastest emissions reductions have come not from renewables but from natural gas replacing coal - a transition that has cut US power sector emissions 32% since 2005. Rather than ideological commitment to specific technologies, we need pragmatic approaches that consider all low-carbon options including nuclear power and natural gas with carbon capture."
    ],
    "genetic engineering": [
        "Genetic engineering raises profound ethical and safety concerns that warrant extreme caution. The technology's irreversibility distinguishes it from other innovations - once modified organisms enter ecosystems, they cannot be recalled. Agricultural applications threaten biodiversity through genetic contamination, with studies documenting transgene spread to wild relatives and non-target organisms. Corporate control of the technology raises serious justice concerns, with just three companies controlling 60% of the global seed market, threatening food sovereignty. Most concerning, emerging gene editing techniques have unpredictable off-target effects - recent studies found CRISPR caused unintended mutations at rates 50-500 times higher than initially reported. Given these risks, the precautionary principle demands we proceed with far greater restraint and democratic oversight.",
        "Genetic engineering's promised benefits remain largely theoretical while concrete risks accumulate. Despite decades of research, genetically modified crops have failed to deliver significant yield increases in real-world conditions, with a major USDA study finding no statistically significant yield advantage. Meanwhile, herbicide-resistant weeds have developed on over 120 million acres due to GM crop systems, creating 'superweeds' requiring more toxic herbicides. Medical applications face similar challenges - gene therapy has caused leukemia in multiple clinical trials, while CRISPR therapies show concerning immune reactions in up to 79% of humans. These technologies confront fundamental biological complexity that doesn't yield to reductionist engineering approaches. Nature's interconnected systems demand humility rather than hubris from our interventions."
    ]
}

# Custom CSS
st.markdown("""
<style>
    .main-header {text-align: center; color: #1E3A8A; margin-bottom: 30px;}
    .round-header {color: #1E3A8A; margin-top: 30px; margin-bottom: 10px;}
    .card {
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .pro-card {border-left: 5px solid #10B981;}
    .con-card {border-left: 5px solid #EF4444;}
    .score-box {
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        padding: 10px;
        border-radius: 5px;
        margin: 10px;
    }
    .pro-score {background-color: #ECFDF5; color: #10B981;}
    .con-score {background-color: #FEF2F2; color: #EF4444;}
    .winner-announcement {
        padding: 20px;
        background-color: #EFF6FF;
        border-radius: 8px;
        text-align: center;
        margin-top: 30px;
        border: 2px solid #3B82F6;
    }
    .sub-header {
        font-size: 1.2em;
        font-weight: bold;
        margin-top: 15px;
        margin-bottom: 5px;
    }
    .button-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Title and introduction
st.markdown("<h1 class='main-header'>AI Debate Simulator</h1>", unsafe_allow_html=True)

if not st.session_state.game_active:
    st.markdown("""
    Welcome to the AI Debate Simulator! This application simulates a debate between two virtual debaters:
    - **Pro Agent**: Argues in favor of the topic
    - **Con Agent**: Argues against the topic
    
    Each debate consists of 5 rounds with 2 arguments per round. After each argument, you'll vote for the most compelling case.
    """)
    
    # Topic selection
    st.markdown("### Select a Debate Topic")
    
    # Option to choose from predefined topics or enter custom topic
    topic_option = st.radio(
        "Choose from predefined topics or enter a custom topic:",
        ("Predefined Topic", "Custom Topic")
    )
    
    if topic_option == "Predefined Topic":
        predefined_topics = list(pro_arguments.keys())
        selected_topic = st.selectbox("Select a topic:", predefined_topics)
    else:
        selected_topic = st.text_input("Enter a custom topic:")
        
    if st.button("Start Debate"):
        if selected_topic:
            st.session_state.current_topic = selected_topic
            st.session_state.game_active = True
            st.session_state.pro_score = 0
            st.session_state.con_score = 0
            st.session_state.current_round = 1
            st.session_state.sub_round = 1
            st.session_state.debate_history = []
            st.session_state.winner_declared = False
            st.rerun()
        else:
            st.error("Please select or enter a topic to start the debate.")

else:
    # Display current scores
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<div class='score-box pro-score'>Pro Score: {st.session_state.pro_score}</div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='score-box con-score'>Con Score: {st.session_state.con_score}</div>", unsafe_allow_html=True)
    
    # Display current topic
    st.markdown(f"### Current Topic: {st.session_state.current_topic.capitalize()}")
    
    # Simulate research by showing a loading message
    if (st.session_state.current_round <= 5 and not st.session_state.winner_declared and 
        len(st.session_state.debate_history) < (st.session_state.current_round * 2) - (2 - st.session_state.sub_round)):
        
        with st.spinner("Debaters are researching and preparing their arguments..."):
            # Simulate processing time
            time.sleep(2)
            
            # Get arguments based on whether it's a predefined or custom topic
            if st.session_state.current_topic.lower() in pro_arguments:
                if st.session_state.sub_round == 1:
                    current_pro = pro_arguments[st.session_state.current_topic.lower()][0]
                    current_con = con_arguments[st.session_state.current_topic.lower()][0]
                else:
                    current_pro = pro_arguments[st.session_state.current_topic.lower()][1]
                    current_con = con_arguments[st.session_state.current_topic.lower()][1]
            else:
                # For custom topics, generate placeholder arguments based on the topic
                # This simulates AI "generating" relevant content
                if st.session_state.sub_round == 1:
                    custom_pro = f"The implementation of {st.session_state.current_topic} would benefit society in numerous ways. " \
                                f"Research shows that early adoption leads to improved outcomes across multiple sectors. " \
                                f"Evidence from similar initiatives demonstrates 40% higher efficiency and 25% cost reduction over time. " \
                                f"Additionally, surveys indicate 68% of stakeholders support this approach when properly implemented. " \
                                f"Economic analyses project sustainable growth with minimal disruption to existing systems. " \
                                f"The scientific consensus strongly supports moving forward with {st.session_state.current_topic} " \
                                f"as it addresses critical needs while creating new opportunities for innovation and progress."
                    
                    custom_con = f"Despite claimed benefits, {st.session_state.current_topic} presents significant concerns that cannot be overlooked. " \
                                f"Implementation costs are routinely underestimated by 45-60% according to independent economic analyses. " \
                                f"Unintended consequences have emerged in 73% of similar initiatives, creating new problems while solving old ones. " \
                                f"Ethical considerations remain inadequately addressed, with 58% of experts expressing serious reservations. " \
                                f"Alternative approaches offer comparable benefits with fewer risks and lower costs. " \
                                f"We must prioritize evidence-based policies rather than rushing into {st.session_state.current_topic} " \
                                f"before understanding the full implications for all stakeholders."
                    
                    current_pro = custom_pro
                    current_con = custom_con
                else:
                    custom_pro = f"Further research reinforces the case for {st.session_state.current_topic}. " \
                                f"Economic modeling shows 3-5% annual growth in affected sectors, with job creation exceeding losses by 2:1. " \
                                f"Pilot programs have demonstrated 35% improvement in target metrics while maintaining high user satisfaction. " \
                                f"International comparisons reveal successful implementation in 12 comparable cases with consistent positive outcomes. " \
                                f"Regulatory frameworks already exist to address major concerns, requiring only minor adaptations. " \
                                f"The cost of inaction far exceeds implementation costs, with delayed adoption estimated to increase expenses by 7% annually."
                    
                    custom_con = f"Closer examination of {st.session_state.current_topic} reveals fundamental flaws in the proposed approach. " \
                                f"Similar initiatives have failed to achieve 65% of projected benefits in real-world applications. " \
                                f"Vulnerable populations bear disproportionate transition costs, with limited access to offsetting benefits. " \
                                f"Security and privacy concerns remain inadequately addressed, creating significant liability issues. " \
                                f"The rush to implement lacks necessary testing in diverse contexts, risking substantial unintended consequences. " \
                                f"A phased, more cautious approach would better serve public interests while still capturing core benefits of {st.session_state.current_topic}."
                    
                    current_pro = custom_pro
                    current_con = custom_con
            
            # Add arguments to debate history
            debate_round = {
                "round": st.session_state.current_round,
                "sub_round": st.session_state.sub_round,
                "pro_argument": current_pro,
                "con_argument": current_con,
                "winner": None
            }
            st.session_state.debate_history.append(debate_round)
            st.rerun()
    
    # Display debate history and collect votes
    for i, round_data in enumerate(st.session_state.debate_history):
        round_num = round_data["round"]
        sub_round = round_data["sub_round"]
        
        st.markdown(f"<h3 class='round-header'>Round {round_num}.{sub_round}</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='card pro-card'>", unsafe_allow_html=True)
            st.markdown("<div class='sub-header'>Pro Argument:</div>", unsafe_allow_html=True)
            st.write(round_data["pro_argument"])
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col2:
            st.markdown("<div class='card con-card'>", unsafe_allow_html=True)
            st.markdown("<div class='sub-header'>Con Argument:</div>", unsafe_allow_html=True)
            st.write(round_data["con_argument"])
            st.markdown("</div>", unsafe_allow_html=True)
        
        # If this round hasn't been voted on yet and we're not at game end
        if round_data["winner"] is None and not st.session_state.winner_declared:
            st.markdown("<div class='button-container'>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"Vote for Pro Argument", key=f"pro_{round_num}_{sub_round}"):
                    st.session_state.debate_history[i]["winner"] = "pro"
                    st.session_state.pro_score += 1
                    
                    # Move to next sub-round or round
                    if st.session_state.sub_round == 1:
                        st.session_state.sub_round = 2
                    else:
                        st.session_state.current_round += 1
                        st.session_state.sub_round = 1
                    
                    # Check if game is over
                    if st.session_state.current_round > 5:
                        st.session_state.winner_declared = True
                    
                    st.rerun()
            
            with col2:
                if st.button(f"Vote for Con Argument", key=f"con_{round_num}_{sub_round}"):
                    st.session_state.debate_history[i]["winner"] = "con"
                    st.session_state.con_score += 1
                    
                    # Move to next sub-round or round
                    if st.session_state.sub_round == 1:
                        st.session_state.sub_round = 2
                    else:
                        st.session_state.current_round += 1
                        st.session_state.sub_round = 1
                    
                    # Check if game is over
                    if st.session_state.current_round > 5:
                        st.session_state.winner_declared = True
                    
                    st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            # Show who won this argument
            winner = round_data["winner"]
            if winner == "pro":
                st.success("You voted for the Pro argument in this round.")
            else:
                st.error("You voted for the Con argument in this round.")
    
    # Display final results if game is over
    if st.session_state.winner_declared:
        st.markdown("<div class='winner-announcement'>", unsafe_allow_html=True)
        
        if st.session_state.pro_score > st.session_state.con_score:
            st.markdown(f"### Debate Concluded: Pro Wins! 🏆")
            st.markdown(f"Final Score: Pro {st.session_state.pro_score} - Con {st.session_state.con_score}")
        elif st.session_state.con_score > st.session_state.pro_score:
            st.markdown(f"### Debate Concluded: Con Wins! 🏆")
            st.markdown(f"Final Score: Pro {st.session_state.pro_score} - Con {st.session_state.con_score}")
        else:
            st.markdown(f"### Debate Concluded: It's a Tie! 🤝")
            st.markdown(f"Final Score: Pro {st.session_state.pro_score} - Con {st.session_state.con_score}")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("Start New Debate"):
            st.session_state.game_active = False
            st.session_state.current_topic = ""
            st.session_state.pro_score = 0
            st.session_state.con_score = 0
            st.session_state.current_round = 1
            st.session_state.sub_round = 1
            st.session_state.debate_history = []
            st.session_state.winner_declared = False
            st.rerun()
