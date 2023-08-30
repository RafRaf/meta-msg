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
