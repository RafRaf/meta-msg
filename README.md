# Meta-msg (Meta message)

`Meta-msg` it's an additional layer for your binary exchange systems. It lets you add status/error codes to your messages and raise/handle errors between microservices in traditional (pythonic) way.

I was badly inspired by gRPC libraries where you can raise an exception to handle error codes separetly from regular logic.

PS: HTTP & gRPC codes provided additionally for your convinience ([👉 Status codes](meta_msg/status_codes/)), but feel free to use custom/arbitary codes (The only restriction: they shouldn't be more than 4 bytes long integers)

## Installation

> pip install meta-msg

## Use case

If you use NATS, RabbitMQ or any other message brokers you probably know that they don't have error handling mechanisms. Just messages. If you want to raise an error you should build something on your own. `Meta-msg` fills this gap by adding a wrapper to messages and transfer status/error codes in them.

The example below shows how you can use protobuf in NATS and have error codes as we usually had in traditional gRPC approaches.

## Example

#### [example/producer.py](example/producer.py)
```python
import asyncio

import nats

from meta_msg import MetaMsg, GrpcStatus, ServerError
from example.proto import message_pb2


async def produce():
    nc = await nats.connect("tls://demo.nats.io:4443", connect_timeout=10)

    visitors = (
        ("Sarah", "woman", 32),
        ("Melony", "woman", 21),
        ("Tom", "man", 18)
    )

    for name, sex, age in visitors:
        visitor = message_pb2.Visitor(name=name, sex=sex, age=age)

        # Construct a message
        req_msg = MetaMsg.dump_message(visitor.SerializeToString())

        # Make a request to remote server
        resp_msg = await nc.request("toilet", req_msg, timeout=2)

        # Deserialize the answer
        try:
            raw_answer = MetaMsg.load_message(resp_msg.data)
        except ServerError as err:
            # If an error occurs, you get a status_code and the error message itself
            print(f"Oops: {GrpcStatus(err.status_code).name}, {err.message}")
        else:
            # Deserialize (protobuf)
            ticket = message_pb2.Ticket()
            ticket.ParseFromString(raw_answer)

            print(f"Hooray: {ticket}")

    await nc.close()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(produce())
```

#### [example/consumer.py](example/consumer.py)
```python
import asyncio

import nats

from meta_msg import MetaMsg, GrpcStatus
from example.proto import message_pb2


async def consume():
    nc = await nats.connect("tls://demo.nats.io:4443", connect_timeout=10)
    queue_number = 1

    async def handler(msg):
        nonlocal queue_number

        req_msg = MetaMsg.load_message(msg.data)

        # Deserialize (protobuf)
        visitor = message_pb2.Visitor()
        visitor.ParseFromString(req_msg)

        print(f"Knock-knock, \"{visitor.name}\" is here")

        # Now you can work with protobuf messages
        if visitor.sex != "woman":

            # Send an error message
            resp_msg = MetaMsg.err_message(
                f"Sorry {visitor.name}, this is a women's toilet".encode(),
                status_code=GrpcStatus.CANCELLED
            )
        else:

            # Send a protobuf message
            ticket = message_pb2.Ticket(
                queue_number=queue_number,
                welcome_text=f"Hey {visitor.name}, nice to see you here. Come in"
            )
            resp_msg = MetaMsg.dump_message(ticket.SerializeToString())

            queue_number += 1

        await nc.publish(msg.reply, resp_msg)

    await nc.subscribe("toilet", cb=handler)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(consume())
    loop.run_forever()
    loop.close()
```

## Conclusion

So having `Meta-msg` you can build flexible exchange systems on the top of any transport. NATS or RabbitMQ. Anything.