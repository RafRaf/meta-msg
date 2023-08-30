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
