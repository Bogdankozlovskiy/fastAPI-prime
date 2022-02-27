from fastapi import APIRouter, Query
from pydantic import HttpUrl
from typing import Dict
from requests import post
from modules.callbacs.schemas import Invoice, InvoiceEvent, InvoiceEventRecived


router = APIRouter(tags=['callbacks'])
call_backs_router = APIRouter()


@call_backs_router.post("/{$callback_url}/invoices/{$request.body.id}", response_model=InvoiceEventRecived)
def call_back(body: InvoiceEvent):
    """
    actually this function will never bee calling
    this function need only for discribing how does will work call back
    """
    pass


@router.post("/invoices/", callbacks=call_backs_router.routes, response_model=Dict[str, str])
def create_invoice(invoice: Invoice, callback_url: HttpUrl = Query(...)):
    """
    Create an invoice.

    This will (let's imagine) let the API user (some external developer) create an
    invoice.

    And this path operation will:

    * Send the invoice to the client.
    * Collect the money from the client.
    * Send a notification back to the API user (the external developer), as a callback.
        * At this point is that the API will somehow send a POST request to the
            external API with the notification of the invoice event
            (e.g. "payment successful").
    """
    # Send the invoice, collect the money, send the notification (the callback)
    invoice_event = InvoiceEvent(description="invoice description", paid=True)
    response = post(f"{callback_url}/invoices/{invoice.id}", json=invoice_event.dict())
    msg = "Invoice received" if response.ok else "Invoice reject"
    return {"msg": msg}
