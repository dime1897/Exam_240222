from sys import argv
from google.cloud import pubsub_v1

PROJECT_ID = 'exam-240222'

cap=None

def callback(message):
    message.ack()
    msg = message.data.decode('utf-8')
    if cap is None: print(msg)
    else: 
        if str(cap) in msg: print(msg)

if __name__=='__main__':
    if len(argv)>1:
        try:
            cap = int(argv[1])
            if cap < 0 or cap > 99999:
                print("Argument error. Usage is:\n./"+argv[0]+" {int_value"+"}\nint_value must be in range(0,99999) (inclusive)")
        except:
            print("Argument error. Usage is:\n./"+argv[0]+" {int_value"+"}\nint_value must be in range(0,99999) (inclusive)")
            quit()
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(PROJECT_ID, "NUOVO-CANTIERE")
    pull = subscriber.subscribe(subscription_path, callback=callback)
    print("Sto aspettando che avviino qualche cantiere...")
    try:
        pull.result()
    except Exception as e:
        print(e)
        pull.cancel()