
currencies2 = {
            'USD' :{
                        'HUF':'BOE/XUDLBK35'
                    },
            'GBP' :{
                        'HUF':'BOE/XUDLBK33',
                        'PLN' : 'BOE/XUDLBK47',
                        'BGN' : 'BOE/EURBGN'
                    },
            'EUR' :{
                        'BOE/XUDLBK34'
                    }

    }

print(currencies2['GBP']['HUF'])

from datetime import datetime
from datetime import timedelta
string = '2017-02-22'
datetime_object = datetime.strptime(string, '%Y-%m-%d')

list = []
for i in range (100):
    datetime_object = datetime_object + timedelta(days=1)
    if ((datetime_object.weekday() != 5) & (datetime_object.weekday() != 6)):
        date = str(datetime_object)
        date = date[:10]
        list.append(date)
print(list)


