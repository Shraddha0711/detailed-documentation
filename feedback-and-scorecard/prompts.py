def empathy_score_prompt(transcript):
    return f"""Given the following sales call transcript, evaluate the level of empathy shown by the speaker. Consider the following scale:
9-10: The speaker actively listens and demonstrates strong empathy for the audience. They acknowledge the feelings, concerns, or emotions expressed, and respond in a manner that shows they care and understand. Empathy is conveyed through phrasing like “I understand how you feel” or “I can relate to your concern,” and personalized responses to the situation.
7-8: The speaker shows some empathy, but it is less consistent or nuanced. They may acknowledge the audience’s concerns or feelings but fail to fully demonstrate understanding or engagement in their responses.
5-6: The speaker acknowledges emotions, but their responses feel more formulaic or inconsistent. Their empathy might be superficial, and they don’t fully engage with the audience on a deeper emotional level.
3-4: The speaker may barely acknowledge the emotions or needs of the audience. They may appear detached or overly focused on the message without considering how the audience feels.
1-2: No empathy shown at all. The speaker may sound dismissive, cold, or uninterested in the audience’s concerns.
Transcript: {transcript}
Score the empathy on a scale from 1 to 10. Only provide the score as a single number without any additional explanation.
Format your response as:
[number]
"""

def clarity_and_conciseness_prompt(transcript):
    return f"""Given the following sales call transcript, evaluate the level of empathy shown by the speaker. Consider the following scale:
9-10: The speaker is exceptionally clear in their message, with no ambiguity. They avoid jargon and use simple, straightforward language. Their speech is organized and direct, with each point being made succinctly without over-explanation or unnecessary tangents.
7-8: The speaker is mostly clear, but there may be some minor unnecessary elaboration or minor lapses in clarity. The message is generally easy to follow but may occasionally feel a bit too wordy.
5-6: The speaker’s speech is generally clear, but there are sections where it may be a bit convoluted, or they use more words than needed. Some points may require the audience to follow along more carefully or need clarification.
3-4: The speaker is not very clear in conveying their message. They may use uncertain language or frequently go off-topic, requiring the audience to deduce their main point. The message feels over-complicated.
1-2: Very unclear speech. The speaker frequently struggles to articulate points, making it difficult for the audience to understand what is being said causing frequent misunderstandings.
Transcript: {transcript}
Score the empathy on a scale from 1 to 10. Only provide the score as a single number without any additional explanation.
Format your response as:
[number]
"""

def grammar_and_language_prompt(transcript):
    return f"""Given the following sales call transcript, evaluate the level of empathy shown by the speaker. Consider the following scale:
9-10: Flawless grammar and pronunciation throughout the speech. The speaker uses clear, correct, and appropriate language. There is no confusion, and their diction is precise, enhancing the clarity of their message.
7-8: Minor grammatical mistakes that don’t impede comprehension. There might be occasional awkward phrasing or a slight misstep in word choice.
5-6: The speaker makes moderate grammatical errors or has slightly awkward phrasing at times, which may cause some disruption to the flow of their message.
3-4: Frequent grammatical mistakes that disrupt the flow of the speech. Some parts may be difficult to understand or cause confusion in meaning.
1-2: Poor grammar throughout, making it very difficult to follow the speech. Many errors distract from the speaker's credibility.
Transcript: {transcript}
Score the empathy on a scale from 1 to 10. Only provide the score as a single number without any additional explanation.
Format your response as:
[number]
"""

def listening_score_prompt(transcript):
    return f"""Given the following sales call transcript, evaluate the level of empathy shown by the speaker. Consider the following scale:
    9-10: The speaker actively listens to feedback, signs of engagement, or questions from the audience. They address concerns directly and demonstrate that they are fully tuned in to the audience’s needs or cues.
7-8: The speaker listens but may miss minor cues or slight nuances in audience reactions. They generally address questions but might require slight clarification.
5-6: The speaker listens but struggles to pick up on key cues or may ignore audience feedback. They attempt to respond but may need more follow-up or clarification.
3-4: The speaker appears distracted or not fully attentive to the audience’s reactions or feedback. They may miss key points or fail to engage with the audience’s signals effectively.
1-2: The speaker does not listen to the audience at all, continuing with their speech regardless of feedback or engagement cues.
Transcript: {transcript}
Score the empathy on a scale from 1 to 10. Only provide the score as a single number without any additional explanation.
Format your response as:
[number]
"""

def problem_resolution_effectiveness_prompt(transcript):
    return f"""Given the following sales call transcript, evaluate the level of empathy shown by the speaker. Consider the following scale:
9-10: The speaker identifies potential problems or objections in the presentation and immediately offers clear, effective solutions or responses. They demonstrate adaptability to overcome challenges.
7-8: The speaker resolves most issues or concerns raised but may lack some depth or nuances in their responses.
5-6: The speaker addresses some problems, but their solutions may be generic or not fully effective in satisfying audience concerns.
3-4: The speaker’s problem-solving is incomplete or ineffective. Issues raised by the audience are not resolved properly.
1-2: The speaker fails to address problems or concerns raised by the audience.
Transcript: {transcript}
Score the empathy on a scale from 1 to 10. Only provide the score as a single number without any additional explanation.
Format your response as:
[number]
"""

def personalisation_index_prompt(transcript):
    return f"""Given the following sales call transcript, evaluate the level of empathy shown by the speaker. Consider the following scale:
9-10: The speaker consistently provides a highly tailored experience to the audience, incorporating their name, specific details, preferences, and concerns into the conversation. Their responses feel unique and relevant to the individual, demonstrating thorough preparation.
7-8: Responses are mostly personalized, but there may be occasional generic elements or missed opportunities to incorporate unique audience details.
5-6: Some personalization is evident, but much of the interaction feels generic or templated. References to the audience’s specifics are minimal or inconsistent.
3-4: Minimal effort is made to personalize the conversation. The responses are predominantly generic and could apply to anyone.
1-2: No personalization is attempted. The interaction feels completely impersonal and robotic, failing to acknowledge the audience’s individuality.
Transcript: {transcript}
Score the empathy on a scale from 1 to 10. Only provide the score as a single number without any additional explanation.
Format your response as:
[number]
"""
def conflict_management_prompt(transcript):
    return f"""Given the following sales call transcript, evaluate the level of empathy shown by the speaker. Consider the following scale:
9-10: The speaker demonstrates exceptional conflict resolution skills, maintaining a calm, composed demeanor. They de-escalate tense situations effectively, acknowledging all parties’ concerns and finding a mutually acceptable resolution.
7-8: The speaker manages conflict well but may show slight hesitation in fully de-escalating the situation or miss some nuance in addressing all concerns. Resolution is achieved, but not optimally.
5-6: The speaker attempts to address conflict but does so incompletely or inconsistently. Their approach may unintentionally escalate tensions slightly, though they ultimately resolve the issue.
3-4: The speaker struggles with conflict resolution. Their tone, approach, or lack of listening causes further tension or fails to adequately address the root cause of the conflict.
1-2: The speaker handles conflict poorly, appearing defensive, dismissive, or aggressive. The conflict is unresolved or escalates further.
Transcript: {transcript}
Score the empathy on a scale from 1 to 10. Only provide the score as a single number without any additional explanation.
Format your response as:
[number]
"""

def response_time_prompt(transcript):
    return f"""Given the following sales call transcript, evaluate the level of empathy shown by the speaker. Consider the following scale:
9-10: Responses are delivered immediately or within an optimal timeframe, showing a strong sense of urgency and attentiveness. There are no delays, and the response time matches or exceeds expectations for the context.
7-8: Responses are mostly timely, but there may be slight delays (e.g., a few seconds of hesitation) that don’t significantly impact the flow of the conversation.
5-6: Response time is moderate, with noticeable delays that could affect the listener’s perception of attentiveness or engagement.
3-4: Responses are consistently slow or delayed, leaving the audience feeling ignored or unimportant.
1-2: Responses are excessively delayed, with large gaps of silence or extended pauses, creating frustration or disengagement.
Transcript: {transcript}
Score the empathy on a scale from 1 to 10. Only provide the score as a single number without any additional explanation.
Format your response as:
[number]
"""

def customer_satisfiction_score_prompt(transcript):
    return f"""Given the following sales call transcript, evaluate the level of empathy shown by the speaker. Consider the following scale:
9-10: The speaker leaves the audience feeling extremely satisfied, addressing all concerns and exceeding expectations with proactive, thoughtful service. The tone and resolution instill high confidence and trust.
7-8: The audience is mostly satisfied, with minor areas where the speaker could improve. The speaker resolves the issue effectively but may not go beyond basic expectations.
5-6: The audience is moderately satisfied, with noticeable gaps in how their concerns were addressed. While the issue may be resolved, there is room for improvement in effort, tone, or engagement.
3-4: The audience is dissatisfied, feeling that their concerns were not fully addressed or that the resolution was inadequate. The interaction may have lacked warmth or thoroughness.
1-2: The audience is highly dissatisfied, perceiving the speaker as unhelpful, dismissive, or ineffective in resolving concerns.
Transcript: {transcript}
Score the empathy on a scale from 1 to 10. Only provide the score as a single number without any additional explanation.
Format your response as:
[number]
"""

def positive_sentiment_score_prompt(transcript):
    return f"""Given the following sales call transcript, evaluate the level of empathy shown by the speaker. Consider the following scale:
9-10: The speaker consistently uses positive and uplifting language, framing their responses in a way that is optimistic and encouraging. Their tone and word choice create a warm and inviting atmosphere throughout the conversation.
7-8: The speaker maintains a mostly positive tone, but there may be occasional lapses where their language or tone could feel slightly neutral or flat.
5-6: The speaker’s sentiment is neutral, with limited positivity. Their language may feel routine, transactional, or lacking enthusiasm.
3-4: The speaker’s language conveys little to no positivity, feeling overly formal, indifferent, or mildly negative. The interaction lacks energy or warmth.
1-2: The speaker consistently uses negative, dismissive, or cold language. Their tone creates a sense of detachment or discomfort, negatively impacting the interaction.
Transcript: {transcript}
Score the empathy on a scale from 1 to 10. Only provide the score as a single number without any additional explanation.
Format your response as:
[number]
"""

def structure_and_flow_prompt(transcript):
    return f""" Given the following sales call transcript, evaluate the level of empathy shown by the speaker. Consider the following scale:
9-10: The presentation is exceptionally well-structured, with a clear introduction, coherent body, and concise conclusion. Transitions between points are smooth and logical, with clear organization.
7-8: The structure is generally good, but there may be occasional rough transitions or minor lapses in organization.
5-6: The presentation has a basic structure, but it may feel disjointed or difficult to follow at times due to weak transitions.
3-4: The structure is poor or confusing, with ideas jumping around and lacking clear connections between them.
1-2: The presentation has no clear structure or logical flow; the audience struggles to follow the argument.
Transcript: {transcript}
Score the empathy on a scale from 1 to 10. Only provide the score as a single number without any additional explanation.
Format your response as:
[number]
"""

def stuttering_words_prompt(transcript):
    return f"""Given the following sales call transcript, evaluate the level of empathy shown by the speaker. Consider the following scale:
9-10: The speaker speaks fluent and confidently without hesitation, stuttering, or using unnecessary filler words like "um," "uh," "like," or "you know."
7-8: Minimal stuttering or filler words that do not detract from the presentation’s effectiveness.
5-6: Noticeable use of filler words or slight stuttering that makes the speech feel less polished.
3-4: Frequent stuttering or repeated filler words, which causes the presentation to lose flow.
1-2: The speaker stutters consistently or uses excessive filler words.
Transcript: {transcript}
Score the empathy on a scale from 1 to 10. Only provide the score as a single number without any additional explanation.
Format your response as:
[number]
"""

def product_knowledge_score_prompt(transcript):
    return f"""Given the following sales call transcript, evaluate the level of empathy shown by the speaker. Consider the following scale:
9-10: The speaker demonstrates comprehensive knowledge of the product or service. They confidently address all aspects, including features, benefits, use cases, and potential limitations, without hesitation. Responses are accurate, detailed, and tailored to the audience’s needs.
7-8: The speaker shows strong product knowledge, covering most aspects effectively, but may lack depth in addressing more complex questions or finer details.
5-6: The speaker demonstrates basic product knowledge, addressing general features and benefits but struggling with more nuanced questions or showing limited preparation.
3-4: The speaker’s product knowledge is inadequate, with vague or incomplete answers that lack clarity or specificity. They may rely on generic or incorrect information.
1-2: The speaker demonstrates very poor or no product knowledge, failing to provide accurate or relevant information about the product.
Transcript: {transcript}
Score the empathy on a scale from 1 to 10. Only provide the score as a single number without any additional explanation.
Format your response as:
[number]
"""

def persuasion_and_negotiation_skills_prompt(transcript):
    return f"""Given the following sales call transcript, evaluate the level of empathy shown by the speaker. Consider the following scale:
9-10: The speaker uses highly persuasive language, tailoring their approach to the audience’s needs. They effectively communicate value, address objections, and negotiate outcomes that benefit both parties. Their tone is assertive but respectful, with a focus on mutual agreement.
7-8: The speaker is largely persuasive, using logical arguments and negotiation techniques but may lack finesse in closing or balancing assertiveness and flexibility.
5-6: The speaker demonstrates moderate persuasion skills, with basic arguments that lack depth or a structured negotiation strategy. They may struggle to fully engage the audience in agreement.
3-4: The speaker’s persuasion and negotiation skills are limited, coming across as either too passive, overly aggressive, or unable to effectively address audience concerns.
1-2: The speaker shows no persuasion or negotiation ability, failing to influence the audience or facilitate productive dialogue.
Transcript: {transcript}
Score the empathy on a scale from 1 to 10. Only provide the score as a single number without any additional explanation.
Format your response as:
 [number]
"""

def objection_handling_prompt(transcript):
    return f"""Given the following sales call transcript, evaluate the level of empathy shown by the speaker. Consider the following scale:
    9-10: The speaker handles objections with confidence and tact, addressing concerns effectively without becoming defensive. They provide clear, logical solutions and pivot objections into opportunities to reinforce the product’s value.
7-8: The speaker handles most objections well but may miss minor nuances or provide slightly generic responses. Their approach is effective but lacks depth in certain areas.
5-6: The speaker acknowledges objections but struggles to address them fully or persuasively. Responses may feel repetitive or insufficient.
3-4: The speaker handles objections poorly, either ignoring them, becoming defensive, or failing to resolve the audience’s concerns adequately.
1-2: The speaker demonstrates no ability to handle objections, dismissing or completely ignoring audience concerns.
Transcript: {transcript}
Score the empathy on a scale from 1 to 10. Only provide the score as a single number without any additional explanation.
Format your response as:
[number]
"""

def confidence_score_prompt(transcript):
    return f"""Given the following sales call transcript, evaluate the level of empathy shown by the speaker. Consider the following scale:
9-10: The speaker exudes exceptional confidence, maintaining steady tone, posture, and energy throughout. Their delivery is assured and inspires trust in their knowledge and recommendations.
7-8: The speaker appears mostly confident, with occasional lapses (e.g., slight hesitation or nervous energy) that do not significantly impact their credibility.
5-6: The speaker’s confidence is moderate, with noticeable hesitation, a less assertive tone, or inconsistent delivery that affects the overall impression.
3-4: The speaker lacks confidence, coming across as unsure or overly nervous, which undermines the message and audience trust.
1-2: The speaker is extremely hesitant or uncertain, creating a lack of trust and engagement.
Transcript: {transcript}
Score the empathy on a scale from 1 to 10. Only provide the score as a single number without any additional explanation.
Format your response as:
[number]
"""

def value_proposition_prompt(transcript):
    return f"""Given the following sales call transcript, evaluate the level of empathy shown by the speaker. Consider the following scale:
9-10: The speaker communicates a compelling and tailored value proposition, clearly explaining how the product meets the audience’s needs, solves problems, and delivers unique benefits. They focus on results and outcomes.
7-8: The speaker conveys a strong value proposition, but it may lack some customization or fail to highlight certain unique features effectively.
5-6: The speaker provides a basic value proposition, but it may feel generic or overly focused on features rather than benefits or audience needs.
3-4: The value proposition is weak or unclear, failing to connect the product’s features to audience needs or emphasizing irrelevant aspects.
1-2: The speaker presents no clear value proposition, leaving the audience uncertain about the product’s relevance or benefits.
Transcript: {transcript}
Score the empathy on a scale from 1 to 10. Only provide the score as a single number without any additional explanation.
Format your response as:
[number]
"""

def pitch_quality_prompt(transcript):
    return f"""Given the following sales call transcript, evaluate the level of empathy shown by the speaker. Consider the following scale:
9-10: The pitch is highly polished, with a clear, engaging, and persuasive delivery. The speaker uses effective storytelling, facts, and emotion to captivate the audience.
7-8: The pitch is strong, but may lack minor elements of polish or engagement (e.g., slightly rushed delivery or missed opportunities to connect emotionally).
5-6: The pitch is average, with basic delivery and content. While it gets the message across, it lacks strong engagement or creativity.
3-4: The pitch is poorly structured or unengaging, making it difficult for the audience to stay interested or understand the value.
1-2: The pitch is very weak or disorganized, failing to convey a compelling message or hold the audience’s attention.
Transcript: {transcript}
Score the empathy on a scale from 1 to 10. Only provide the score as a single number without any additional explanation.
Format your response as:
[number]
"""

def call_to_action_effectiveness_prompt(transcript):
    return f"""Given the following sales call transcript, evaluate the level of empathy shown by the speaker. Consider the following scale:
9-10: The speaker delivers a clear, specific, and compelling call to action that motivates the audience to act immediately. The action is easy to understand and aligned with the audience’s goals.
7-8: The call to action is effective, but it may lack minor elements of clarity, specificity, or urgency.
5-6: The call to action is adequate, but it may feel generic, vague, or not particularly motivating.
3-4: The call to action is unclear or weak, leaving the audience uncertain about next steps or unmotivated to act.
1-2: There is no call to action, or it is completely ineffective.
Transcript: {transcript}
Score the empathy on a scale from 1 to 10. Only provide the score as a single number without any additional explanation.
Format your response as:
[number]
"""

def questioning_technique_prompt(transcript):
    return f"""Given the following sales call transcript, evaluate the level of empathy shown by the speaker. Consider the following scale:
9-10: The speaker uses open-ended, insightful questions that uncover audience needs and encourage thoughtful dialogue. Their questions feel natural and relevant, leading to deeper engagement.
7-8: The speaker asks good questions, but they may occasionally miss opportunities for deeper exploration or customization.
5-6: The speaker asks basic or routine questions, with limited depth or relevance to the specific audience.
3-4: The speaker’s questions are unfocused or poorly phrased, leading to confusion or irrelevant answers.
1-2: The speaker asks no meaningful questions or fails to use questioning effectively.
Transcript: {transcript}
Score the empathy on a scale from 1 to 10. Only provide the score as a single number without any additional explanation.
Format your response as:
[number]
"""

def rapport_building_prompt(transcript):
    return f"""Given the following sales call transcript, evaluate the level of empathy shown by the speaker. Consider the following scale:
9-10: The speaker builds strong, genuine rapport, using empathy, shared experiences, and relatable language to establish trust and connection.
7-8: The speaker builds good rapport, but there may be occasional missed opportunities to deepen the connection or fully engage.
5-6: The speaker makes some effort to build rapport, but the interaction feels more transactional than personal.
3-4: Rapport building is minimal or ineffective, with the speaker seeming distant or uninterested.
1-2: The speaker fails to build rapport, leaving the interaction cold and impersonal.
Transcript: {transcript}
Score the empathy on a scale from 1 to 10. Only provide the score as a single number without any additional explanation.
Format your response as:
[number]
"""

def active_listening_skills_prompt(transcript):
    return f"""Given the following sales call transcript, evaluate the level of empathy shown by the speaker. Consider the following scale:
    9-10: The speaker listens attentively and responds thoughtfully, incorporating audience feedback and cues into their responses. They avoid interrupting and show they are fully engaged.
7-8: The speaker listens well but may occasionally miss minor cues or show slight lapses in attentiveness.
5-6: The speaker’s listening is moderate, with some missed opportunities to acknowledge or address feedback.
3-4: The speaker demonstrates poor listening, interrupting or failing to incorporate audience input effectively.
1-2: The speaker does not listen at all, ignoring feedback and repeating irrelevant points.
Transcript: {transcript}
Score the empathy on a scale from 1 to 10. Only provide the score as a single number without any additional explanation.
Format your response as:
[number]
"""

def upselling_success_rate_prompt(transcript):
    return f"""Given the following sales call transcript, evaluate the level of empathy shown by the speaker. Consider the following scale:
9-10: The speaker consistently identifies and capitalizes on opportunities to upsell or cross-sell, seamlessly integrating additional products/services into the conversation. Their suggestions are relevant and valuable.
7-8: The speaker incorporates some upselling, but opportunities may be partially missed or less impactful. Suggestions are still generally relevant.
5-6: The speaker makes limited attempts to upsell, and their suggestions feel generic or forced.
3-4: The speaker rarely or ineffectively incorporates upselling, missing clear opportunities.
1-2: No upselling is attempted, or it is irrelevant and poorly executed.
Transcript: {transcript}
Score the empathy on a scale from 1 to 10. Only provide the score as a single number without any additional explanation.
Format your response as:
[number]
"""

def engagement_prompt(transcript):
    return f"""Given the following sales call transcript, evaluate the level of empathy shown by the speaker. Consider the following scale:
9-10: The speaker maintains high audience engagement throughout, using a dynamic delivery style, interactive elements, and strong eye contact.
7-8: The speaker is mostly engaging, with minor lapses in energy or interaction.
5-6: The speaker’s engagement is average, with limited interaction or audience-focused content.
3-4: The speaker struggles to maintain engagement, leading to audience disinterest or distraction.
1-2: The speaker is entirely disengaging, with a monotonous delivery or irrelevant content.
Transcript: {transcript}
Score the empathy on a scale from 1 to 10. Only provide the score as a single number without any additional explanation.
Format your response as:
[number]
"""

def feedback_prompt(transcript):
    return f"""
You are a professional call quality analyst reviewing a customer service interaction transcription. Your task is to provide a comprehensive, structured feedback report in the specified JSON format.

Transcription: {transcript}

Analysis Guidelines:
1. Conduct a thorough, multi-dimensional analysis of the customer service interaction
2. Identify at least 4 key points of feedback
3. For each point, provide:
   - A concise short feedback (1-2 sentence overview)
   - A detailed long feedback paragraph that comprehensively addresses:
     a. What the agent did well
     b. What the agent did incorrectly or could improve
     c. The underlying concept or best practice
     d. Specific recommendations for implementation

Output Format:
[
  "[[
    "short_feedback": "Concise overview of the first key observation",
    "long_feedback": "A comprehensive paragraph that provides in-depth analysis, highlighting strengths, areas for improvement, underlying concepts, and specific implementation advice in a continuous, narrative format."
  ],
  // ... additional feedback points follow the same structure
  ]"
]

"""
