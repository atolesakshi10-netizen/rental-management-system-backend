import hashlib


def generate_agreement_hash(
    property_id,
    tenant_id,
    monthly_rent,
    start_date,
    end_date
):

    data = f"{property_id}{tenant_id}{monthly_rent}{start_date}{end_date}"

    return hashlib.sha256(
        data.encode()
    ).hexdigest()

def generate_payment_hash(
    agreement_id,
    amount,
    payment_date,
    payment_status
):

    data = f"{agreement_id}{amount}{payment_date}{payment_status}"

    return hashlib.sha256(
        data.encode()
    ).hexdigest()