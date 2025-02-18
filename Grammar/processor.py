from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import openai, os

openai.api_key = os.getenv("OPENAI_KEY")

prompt_rules = '''I am building an arabic text to arabic sign language generator. For that I have videos of sign language animation of certain arabic words. But my first step to to convert the input arabic text into sign language grammar before mapping it to videos. I have some set of rules to follow for that:

If the input text is a simple sentence, we change its structure according to the below rules. 
R01. If  S = V + S + O Then  T = S + V + O
i.e. If the structure of S is a V (verb) + S (subject) + O (object), we re-order it to SVO. 
example قرأ ادم الكتاب (read Adam The book)  is changed to ادم قرأ ادالكتاب (Adam Read The book)

R02. If  S = w0…. wn where wn = “?” Then   T = wn + w1…. wn-1 + w0  
i.e. If S is an interrogative sentence, we make sign of the tool of interrogation (?) at the beginning, and the  interrogative particle ( ْﻦَﻣ (who),  َﻦْﯾَأ (where),  َﻒْﯿَﻛ (how) …) at the end of the sentence.
example أین تعیش ؟ (Where do you live?) is converted to ؟ تعیش أین (? Do you live where)

R03. If wi = fj where fj belongs to FP = {fj=0,…,fj=n} = {(which) ھي ,..., التي (she)} THEN ti = mj + (female) أنثى where mj belongs to MP = {mj=0,…,mj=n} = {(which) ھو ,..., التي (he)} is the corresponding masculine pronoun.  i.e.  If  the word  wi is  a feminine  pronoun FP  (subject,  demonstrative  or  relative),  we replace  it  by the corresponding masculine pronoun mj + the word (female) أنثى .  FP: is a set of feminine pronouns.  MP: is a set of masculine pronouns. 
example ھذه ھي التي أرید (this is which I want) is changed to ھذا أنثى ھو أنثى الذي أنثى أرید(this female is female which female I want)

R04. If  wi = أيّ(which) and Gender (wi+1) = masculine THEN  ti = ھذا أم ھذا (this or this for man)  If  wi = أيّ (which) and Gender (wi+1) = feminine THEN  ti = ھذه أم ھذه (this or this for woman) i.e. If the word is the interrogative pronoun أيّ (which), replace it by ھذا أم ھذا  (this or this for man)or ھذه أم ھذه (this or this for woman) depending to the object’s gender. 
Example ؟ قصة أعجبتك أيّ (which story you like ?)  is changed to ؟ قصة أعجبتك ھذه أم ھذه(? Story like this or this )
Another example ؟ الرجلین أقوى أيّ(which men is strong?) is changed to ؟ الرجلین أقوى ھذا أم ھذا (? Men strong this or this ) 

R05.  If wn = “?” and wi wi+1 wi+2 = ما ھو سبب (what is the reason) THEN ti ti+1 ti+2 = سبب (reason).   i.e. If the word is the interrogative pronoun  ما ھو سبب (what is the reason), replace it by سبب (reason). 
example ؟ سفرك إلى فرنسا ما ھو  سبب (? What is the reason you travel to France for)  is changed to سفرك إلى فرنسا سبب؟ (? travel to France for reason) 

R06. If wi belongs to IP = {(to) في ,... إلى(in)} THEN we remove wi   i.e. If the word wi is a particle exists in IP, we delete it.
example ذهبت إلى المسجد (I went to the mosque) is changed to ذهبت المسجد(I went the mosque) 

R07. If Prefix (wi) = “ال(the)” THEN we remove this prefix
example: ذهبت إلى المسجد (I went to the mosque) is changed to ذهبت مسجد(I went the mosque) 

R08. If Type (wi) = noun/verb and suffix (wi) = sj where sj belongs to S = {sj=0,…,sj=n} = {(your) ـي ,..., ك (my)} THEN ti = a0…. a|sj|-1 + ps where wi = a0….an and ps belongs to PS = {(you) أنا ,..., أنت (me)} i.e. If the word is a noun or a verb with suffix, we insert the corresponding subject pronoun of this suffix after/before the word.
example: ذهبت مسجد(I went the mosque) is changed to أنا ذھب مسجد(me go mosque) 
another example: ﺎﻨﻨطو اﺬھ (this is our home)   is changed to ﻦﺤﻧ ﻦطو اﺬھ (this is home our)

R09. If Gender (wi) = feminine THEN ti = wi + (female)أنثى   i.e. If the word’s gender is feminine, we add the word أنثى(female) after the current word wi.
example: ھذه معلمة(this is a teacher(woman)) is changed to ھذه معلم أنثى(this is a teacher(man)

R10. If Number (wi) = dual THEN ti = root(wi) + 2   i.e. If the word number is dual, we insert number 2 after the root of the word
example: ھذان ولدان(there are two boys) is changed to ھذان ولد 2(there are 2 boys) 

R11. If Number (wi) = plural THEN ti = root(wi) + “كثیر” (a lot)   i.e. If the word number is plural, we insert add the word “كثیر” (a lot) after the root of the word
example:  أقلام(pens) is changed to قلم كثیر(pen a lot)'''

def fix_grammar(arabic_input):
    prompt_input = f'''Now use these rule and convert the following input to the output arabic text with explanation:
    {arabic_input}. Only return the final arabic output. Only the final output. No explanation is needed.'''

    prompt = prompt_rules+prompt_input

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.3,
        messages=[
            {"role": "system", "content": "You are a system to convert input arabic text to arabic sign language grammar. You will be given an arabic sentence and will be expected to output the sign language sentence on the basis of some rules. These words generated by you will be then mapped to arabic sign language video and will be displayed in a web app."},
            {"role": "user", "content": prompt},
        ]
    )
    stage_1 = response['choices'][0]['message']['content']
    return stage_1.strip(" ").strip(".")