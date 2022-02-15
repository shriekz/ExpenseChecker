import re
import logging

filename = 'XMLSource/sms.xml'
acct_dict = {
    'XX1023': 'processAccount1023',
    'XX657': 'processAccount657'
}
reject_list = ['declined']

category_mapping_list = {
    'apollo': 'Healthcare',
    'isabel': 'Healthcare',
    'kavery medi': 'Healthcare',
    'pharma': 'Healthcare',
    'swiggy': 'Food',
    'sangeetha veg': 'Food',
    'foods': 'Groceries',
    'pazhamu': 'Groceries',
    'agoda': 'Travel',
    'hpcl': 'Fuel',
    'bpcl': 'Fuel',
    'iocl': 'Fuel',
    'jayam enter': 'Groceries',
    'spencers': 'Groceries',
    'sri krishna': 'Food',
    'ice crea': 'Food',
    'ach*indian': 'Investment',
    'bd-mf': 'Investment',
    'school': 'Education',
    'cinema': 'Entertainment',
    'hathway': 'Utilities',
    'tangedco': 'Utilities',
    'tneb': 'Utilities',
    'bil*onl*00032': 'Utilities',
    'bigbasket': 'Groceries',
    'hicare': 'Utilities',
    'jayaraj': 'Fitness',
    'pizza': 'Food',
    'ramanathan': 'Kids Activities',
    'shanmugam': 'Kids Activities',
    'zerodha': 'Investment',
    'amrutha sri': 'Groceries',
    'aarthi scans': 'Heathcare',
    'netmeds': 'Healthcare',
    'petrol': 'Fuel',
    'ayurved': 'Healthcare',
    'mcrenet': 'Food'
}


def logger():
    logging.basicConfig(level='INFO')
    print('I log this')


def processAccount1023(text, address):
    bank = 'icici'
    category = 'Unknown'
    if bank not in address.lower():
        return False, False, 0.0, 'Uncategorized'

    text = text.replace(',', '')
    regex = '(?:INR )(\\d+\\.\\d+)(?: is debited)'
    r1 = '(?:Info: )(.*?)(?:\\.)'
    matches = re.search(regex, text)
    if matches:
        Amt = float(matches.group(1))
        m = re.search(r1, text)
        if m:
            merchant = m.group(1).strip().lower()
            for key in category_mapping_list:
                if key in merchant:
                    category = category_mapping_list[key]
                    break

        return True, True, Amt, category
    else:
        return False, False, 0.0, 'Uncategorized'


def processAccount657(text, address):

    bank = 'icici'
    category = 'Unknown'
    if bank not in address.lower():
        return False, False, 0.0, 'Uncategorized'

    # remove all "," chars in string as don't know to process it.
    text = text.replace(',', '')
    regex = '((Acc(oun)?t) (?:XX|XXX)657.*)(debited.*)(INR *|Rs )(\\d+(\\.\\d+)?)( on)'
    r1 = '(?:Info: )(.*?)(?:\\.)'
    r2 = '(?:debited.*(?:;|&))(.*)(credited\\.)'
    category = 'Unknown'
    matches = re.search(regex, text)
    if matches:
        Amt = float(matches.group(6))
        m = re.search(r1, text)
        if m is None:
            m = re.search(r2, text)
        if m:
            merchant = m.group(1).strip().lower().lstrip('&')
            for key in category_mapping_list:
                if key in merchant:
                    category = category_mapping_list[key]
                    break

        return True, True, Amt, category
    else:
        return False, False, 0.0, category
