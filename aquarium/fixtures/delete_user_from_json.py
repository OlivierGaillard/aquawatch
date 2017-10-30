import json

filenames = ['Deg', 'Ph', 'Redox']
if __name__=='__main__':
    for filename in filenames:
        print('handling file', filename)
        data = json.load(open(filename + '.json'))
        n = 0
        for m in data:
            n += 1
            fields = m['fields']
            del fields['user']
            m['fields'] = fields
        print('Updated ', str(n), 'entries.')
        new_filename = filename + 'New.json'
        with open(new_filename, mode='w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print('wrote to ', new_filename)
