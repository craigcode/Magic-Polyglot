def status_text(status):
    if status == 3:
        return 'done'
    else:
        return '3 days left'

def num2int(value):
    return str(int(value))

def user_created_str(data):
    ts = data[1][0:16]
    return f'Added by {data[0]} at {ts}'