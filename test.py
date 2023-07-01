import uuid
import base64

namespace = uuid.NAMESPACE_DNS
name = "example.com"

uuid_value = uuid.uuid4()
encoded_uuid = base64.urlsafe_b64encode(uuid_value.bytes).rstrip(b"=").decode("ascii")
print(uuid_value)
print(encoded_uuid)
