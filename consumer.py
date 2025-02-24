# join a consumer group for dynamic partition assignment and offset commits
from kafka import KafkaConsumer
consumer = KafkaConsumer('wikimedia.recentchange', group_id='my_favorite_group', auto_offset_reset='earliest')
# or as a static member with a fixed group member name
# consumer = KafkaConsumer('my_favorite_topic', group_id='my_favorite_group',
#                          group_instance_id='consumer-1', leave_group_on_close=False)
i = 0

for msg in consumer:
    print (msg)
    i+=1
    if i == 1:
        break

    