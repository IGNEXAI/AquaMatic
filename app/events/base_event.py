import inngest
import pydantic
import typing

TEvent = typing.TypeVar("TEvent", bound="BaseEvent")


class BaseEvent(pydantic.BaseModel):
    data: pydantic.BaseModel
    id: str = ""
    name: typing.ClassVar[str]
    ts: int = 0

    @classmethod
    def from_event(cls: type[TEvent], event: inngest.Event) -> TEvent:
        return cls.model_validate(event.model_dump(mode="json"))

    def to_event(self) -> inngest.Event:
        return inngest.Event(
            name=self.name,
            data=self.data.model_dump(mode="json"),
            id=self.id,
            ts=self.ts,
        )


class InvoicePaidEventData(pydantic.BaseModel):
    customerId: str
    invoiceId: str
    amount: int
    metadata: dict


class InvoicePaidEvent(BaseEvent):
    data: InvoicePaidEventData
    name: typing.ClassVar[str] = "billing/invoice.paid"
