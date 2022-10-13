def dotask(df):
    col = ['Sr No:', 'Product', 'SMS', 'Rating', 'Remarks','Type of lead','Mode','Cleaned_Remarks', 'Categories', 'Sub Categories',
           'NPS CAT', 'Total Nps Score']
    import pandas as pd
    import numpy as np
    import re
    import string
    #     global df_final
    #     df_final = pd.DataFrame(columns=col)

    def clean_text(text):
        delete_dict = {sp_character: '' for sp_character in string.punctuation}
        delete_dict[' '] = ' '
        table = str.maketrans(delete_dict)
        text1 = text.translate(table)
        # print('cleaned:'+text1)
        textArr = text1.split()
        text2 = ' '.join([w for w in textArr if (not w.isdigit() and (not w.isdigit() and len(w) > 2))])

        return text2.lower()

    df['Remarks'] = df['Remarks'].astype(str)
    df['Cleaned_Remarks'] = ''
    df['Cleaned_Remarks'] = df['Remarks'].apply(clean_text)

    df['Categories'] = ''
    df['Sub Categories'] = ''

    Chetan = {
        "Price_Related": ['sell', 'inr', 'price', 'prize', 'value', 'valuation', 'rate', 'refund', 'pricing', 'money',
                          'sold', 'payment'],
        "Not_Satisfied": ['pathetic', 'bad', 'not good', 'worst', 'poor', 'disappointed', 'not satisfied',
                          'recommended', \
                          'Unsatisfactory', 'time', ' corrupt', 'bed', 'multiple', 'nonsense', 'professionalism',
                          'not great', 'not happy', 'improved', 'disappointing', 'sucks', 'sucker', 'fake'],
        "Inspection_Related": ['inspection', 'inspected', 'inspect', ' verification', 'review', 'validated',
                               'quotation'],
        "CC_Related": ['customer care', 'call', 'politely', 'discussions', 'discussed'],
        "Unprofessional_Staff": ['leazy', 'fraudsters', 'lier', ' behavior', 'behaviour', 'inexperienced', 'rude',
                                 'staff',
                                 'Unprofessional', 'scam', 'lied '],
        "Offer_Related": ['offers', 'offered', 'offering', 'cashback', 'deal', 'offer'],
        "Process_Related": ['slow process', 'process', 'rubbish'],
        "Positive_Comments": ['good', 'fantastic', 'very professional', 'nice', 'excellent', 'satisfied'],
        "Follow_Up": ['follow up'],
        "Comparing": ['comparing', 'car 24', 'olx'],
        "Professional_Staff": ['courteous', 'Professional']
        }

    for i in range(0, len(df.Cleaned_Remarks)):

        if any(word in df.Cleaned_Remarks[i] for word in Chetan["Price_Related"]):
            df['Categories'][i] = 'Price Related'

        elif any(word in df.Cleaned_Remarks[i] for word in Chetan["Not_Satisfied"]):
            df['Categories'][i] = 'Not Satisfied'

        elif any(word in df.Cleaned_Remarks[i] for word in Chetan["Inspection_Related"]):
            df['Categories'][i] = 'Inspection Related'

        elif any(word in df.Cleaned_Remarks[i] for word in Chetan["CC_Related"]):
            df['Categories'][i] = 'CC Related'

        elif any(word in df.Cleaned_Remarks[i] for word in Chetan["Unprofessional_Staff"]):
            df['Categories'][i] = 'Unprofessional Staff'

        elif any(word in df.Cleaned_Remarks[i] for word in Chetan["Offer_Related"]):
            df['Categories'][i] = 'Offer Related'

        elif any(word in df.Cleaned_Remarks[i] for word in Chetan["Process_Related"]):
            df['Categories'][i] = 'Process Related'


        elif any(word in df.Cleaned_Remarks[i] for word in Chetan["Positive_Comments"]):
            df['Categories'][i] = 'Positive Comments'

        elif any(word in df.Cleaned_Remarks[i] for word in Chetan["Follow_Up"]):
            df['Categories'][i] = 'Follow Up'

        elif any(word in df.Cleaned_Remarks[i] for word in Chetan["Comparing"]):
            df['Categories'][i] = 'Comparing'

        elif any(word in df.Cleaned_Remarks[i] for word in Chetan["Professional_Staff"]):
            df['Categories'][i] = 'Professional Staff'

    df['Categories'] = df['Categories'].replace('', np.nan, regex=True)
    df['Categories'] = df['Categories'].replace(np.nan, 'Unproductive Comment')
    df['NPS CAT'] = ""
    df['Rating'] = df['Rating'].astype(int)
    detractor = df[df['Rating'] < 7]
    detractor['NPS CAT'] = "Detractor"
    promoter = df[df['Rating'] > 8]
    promoter['NPS CAT'] = "Promoter"
    passive = df[(df['Rating'] < 9) & (df['Rating'] > 6)]
    passive['NPS CAT'] = "Passive"
    df_1 = pd.concat([detractor, promoter, passive])
    Promoter_count = len(df_1[df_1['NPS CAT'] == 'Promoter'])
    Passive_count = len(df_1[df_1['NPS CAT'] == 'Passive'])
    Detractor_count = len(df_1[df_1['NPS CAT'] == 'Detractor'])
    df_1['Total Nps Score'] = ''
    df_1['Total Nps Score'] = (Promoter_count - Detractor_count) / (
            Promoter_count + Passive_count + Detractor_count) * 100
    col = ['Sr No:', 'Product', 'SMS', 'Rating', 'Remarks', 'Type of lead', 'Mode', 'Cleaned_Remarks', 'Categories',
           'Sub Categories','NPS CAT', 'Total Nps Score']
    global df_2
    df_2 = pd.DataFrame(columns=col)

    for i in df_1['Categories'].unique():
        j = i
        j = df_1[df_1['Categories'] == i]
        detractor = j[j['Rating'] < 7]
        detractor['NPS CAT'] = "Detractor"
        promoter = j[j['Rating'] > 8]
        promoter['NPS CAT'] = "Promoter"
        passive = j[(j['Rating'] < 9) & (j['Rating'] > 6)]
        passive['NPS CAT'] = "Passive"

        frames = [detractor, promoter, passive]
        a = pd.concat(frames)
        Promoter_count = len(a[a['NPS CAT'] == 'Promoter'])
        Passive_count = len(a[a['NPS CAT'] == 'Passive'])
        Detractor_count = len(a[a['NPS CAT'] == 'Detractor'])

        a['Total Nps Score Cat Wise'] = ''
        a['Total Nps Score Cat Wise'] = (Promoter_count - Detractor_count) / (Promoter_count + Passive_count
                                                                              + Detractor_count) * 100
        frames = [df_2, a]
        df_2 = pd.concat(frames)



    return df_2